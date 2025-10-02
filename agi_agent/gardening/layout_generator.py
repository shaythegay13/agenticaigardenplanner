"""
Visual garden layout generator.
Creates optimized 2D layouts with companion planting and space efficiency.

v4.0 Phase 1 Feature: Visual layout generation
"""

from typing import List, Dict, Tuple, Optional
from dataclasses import dataclass, field
from enum import Enum
import math

from .companion_planting import get_companion_info


class SpacingMethod(str, Enum):
    """Garden spacing methods"""
    SQUARE_FOOT = "Square Foot"  # 1 sq ft grid
    INTENSIVE = "Intensive"  # Tight spacing
    TRADITIONAL = "Traditional"  # Row spacing
    WIDE = "Wide"  # Extra space


class PlantSize(str, Enum):
    """Relative plant sizes for layout"""
    SMALL = "Small"  # Lettuce, radishes (4-6" spacing)
    MEDIUM = "Medium"  # Peppers, cabbage (12-18" spacing)
    LARGE = "Large"  # Tomatoes, squash (24-36" spacing)
    VINE = "Vine"  # Cucumbers, melons (requires trellis or sprawl)


@dataclass
class CropPlacement:
    """A crop placed in the layout"""
    crop: str
    variety: Optional[str] = None
    quantity: int = 1
    size: PlantSize = PlantSize.MEDIUM
    position: Optional[Tuple[int, int]] = None  # (row, col) in grid
    companion_to: Optional[str] = None  # Which crop is this companioning
    notes: List[str] = field(default_factory=list)


@dataclass
class GardenBed:
    """A garden bed or growing space"""
    name: str
    width: int  # feet
    length: int  # feet
    sunlight: str  # Full/Partial/Shade
    placements: List[CropPlacement] = field(default_factory=list)


@dataclass
class GardenLayout:
    """Complete garden layout"""
    beds: List[GardenBed]
    spacing_method: SpacingMethod
    notes: List[str] = field(default_factory=list)


# Crop size database (can be expanded)
CROP_SIZES = {
    # Small crops (4-9 per sq ft)
    "lettuce": PlantSize.SMALL,
    "radishes": PlantSize.SMALL,
    "spinach": PlantSize.SMALL,
    "arugula": PlantSize.SMALL,
    "green onions": PlantSize.SMALL,
    "herbs": PlantSize.SMALL,
    "basil": PlantSize.SMALL,
    "cilantro": PlantSize.SMALL,
    "parsley": PlantSize.SMALL,
    
    # Medium crops (1-4 per sq ft)
    "peppers": PlantSize.MEDIUM,
    "eggplant": PlantSize.MEDIUM,
    "broccoli": PlantSize.MEDIUM,
    "cauliflower": PlantSize.MEDIUM,
    "cabbage": PlantSize.MEDIUM,
    "kale": PlantSize.MEDIUM,
    "chard": PlantSize.MEDIUM,
    "beets": PlantSize.MEDIUM,
    "carrots": PlantSize.MEDIUM,
    "onions": PlantSize.MEDIUM,
    "beans": PlantSize.MEDIUM,
    "peas": PlantSize.MEDIUM,
    
    # Large crops (1 per 2-4 sq ft)
    "tomatoes": PlantSize.LARGE,
    "corn": PlantSize.LARGE,
    "potatoes": PlantSize.LARGE,
    
    # Vining crops (special handling)
    "cucumbers": PlantSize.VINE,
    "squash": PlantSize.VINE,
    "zucchini": PlantSize.VINE,
    "melons": PlantSize.VINE,
    "pumpkins": PlantSize.VINE,
}


def get_crop_size(crop: str) -> PlantSize:
    """Get the size category for a crop"""
    crop_lower = crop.lower()
    
    # Direct match
    if crop_lower in CROP_SIZES:
        return CROP_SIZES[crop_lower]
    
    # Check for partial matches
    for key, size in CROP_SIZES.items():
        if key in crop_lower or crop_lower in key:
            return size
    
    # Default to medium if unknown
    return PlantSize.MEDIUM


def get_plants_per_sqft(size: PlantSize, method: SpacingMethod) -> float:
    """Get number of plants per square foot based on size and method"""
    if method == SpacingMethod.SQUARE_FOOT:
        if size == PlantSize.SMALL:
            return 4.0  # 4-16 depending on crop
        elif size == PlantSize.MEDIUM:
            return 1.0
        elif size == PlantSize.LARGE:
            return 0.25  # 1 per 4 sq ft
        else:  # VINE
            return 0.25  # With trellis
    
    elif method == SpacingMethod.INTENSIVE:
        # Tighter spacing
        if size == PlantSize.SMALL:
            return 9.0
        elif size == PlantSize.MEDIUM:
            return 2.0
        elif size == PlantSize.LARGE:
            return 0.5
        else:  # VINE
            return 0.25
    
    elif method == SpacingMethod.TRADITIONAL:
        # Row spacing - less efficient
        if size == PlantSize.SMALL:
            return 2.0
        elif size == PlantSize.MEDIUM:
            return 0.5
        elif size == PlantSize.LARGE:
            return 0.25
        else:  # VINE
            return 0.125  # Sprawling
    
    else:  # WIDE
        # Extra space for ease
        if size == PlantSize.SMALL:
            return 2.0
        elif size == PlantSize.MEDIUM:
            return 0.5
        elif size == PlantSize.LARGE:
            return 0.125
        else:  # VINE
            return 0.0625  # 1 per 16 sq ft


def calculate_bed_capacity(bed: GardenBed, method: SpacingMethod) -> Dict[PlantSize, int]:
    """Calculate how many plants of each size can fit in a bed"""
    total_sqft = bed.width * bed.length
    
    capacity = {}
    for size in PlantSize:
        plants_per_sqft = get_plants_per_sqft(size, method)
        capacity[size] = int(total_sqft * plants_per_sqft)
    
    return capacity


def generate_layout(
    crops: List[str],
    bed_width: int = 4,
    bed_length: int = 8,
    spacing_method: SpacingMethod = SpacingMethod.SQUARE_FOOT,
    sunlight: str = "Full Sun"
) -> GardenLayout:
    """
    Generate an optimized garden layout.
    
    Args:
        crops: List of crops to plant
        bed_width: Width of bed in feet
        bed_length: Length of bed in feet
        spacing_method: Spacing method to use
        sunlight: Sunlight level (Full Sun/Partial Sun/Shade)
    
    Returns:
        Complete garden layout with placements
    """
    bed = GardenBed(
        name=f"{bed_width}'x{bed_length}' Bed",
        width=bed_width,
        length=bed_length,
        sunlight=sunlight
    )
    
    # Get companion info for all crops
    companion_data = {}
    for crop in crops:
        info = get_companion_info(crop)
        if info:
            companion_data[crop] = info
    
    # Sort crops by size (large first for better placement)
    crops_with_size = [(crop, get_crop_size(crop)) for crop in crops]
    crops_with_size.sort(key=lambda x: (
        0 if x[1] == PlantSize.LARGE else
        1 if x[1] == PlantSize.VINE else
        2 if x[1] == PlantSize.MEDIUM else 3
    ))
    
    # Calculate how many of each crop can fit
    total_sqft = bed_width * bed_length
    placements = []
    
    for crop, size in crops_with_size:
        # Determine quantity based on size
        plants_per_sqft = get_plants_per_sqft(size, spacing_method)
        
        # Reserve space proportionally
        if size == PlantSize.LARGE or size == PlantSize.VINE:
            quantity = max(1, int(total_sqft * plants_per_sqft / len(crops)))
        elif size == PlantSize.MEDIUM:
            quantity = max(2, int(total_sqft * plants_per_sqft / len(crops)))
        else:  # SMALL
            quantity = max(4, int(total_sqft * plants_per_sqft / len(crops)))
        
        # Check for companion planting opportunities
        companion_to = None
        notes = []
        
        if crop in companion_data:
            for other_crop, _ in crops_with_size:
                if other_crop != crop and other_crop in companion_data[crop].good_companions:
                    companion_to = other_crop
                    notes.append(f"Companion to {other_crop}")
                    break
        
        placement = CropPlacement(
            crop=crop,
            quantity=quantity,
            size=size,
            companion_to=companion_to,
            notes=notes
        )
        placements.append(placement)
    
    bed.placements = placements
    
    # Add layout notes
    layout_notes = []
    layout_notes.append(f"Total space: {total_sqft} sq ft")
    layout_notes.append(f"Spacing method: {spacing_method.value}")
    
    # Add companion planting notes
    companions_found = sum(1 for p in placements if p.companion_to)
    if companions_found > 0:
        layout_notes.append(f"Companion plantings: {companions_found}")
    
    return GardenLayout(
        beds=[bed],
        spacing_method=spacing_method,
        notes=layout_notes
    )


def generate_ascii_layout(layout: GardenLayout) -> str:
    """
    Generate ASCII art representation of the layout.
    
    Args:
        layout: Garden layout to visualize
    
    Returns:
        ASCII art string
    """
    output = []
    output.append("=" * 70)
    output.append("GARDEN LAYOUT VISUALIZATION")
    output.append("=" * 70)
    output.append("")
    
    for bed in layout.beds:
        # Bed header
        output.append(f"┌{'─' * (bed.width * 8 + 2)}┐")
        output.append(f"│ {bed.name} ({bed.sunlight}){' ' * (bed.width * 8 - len(bed.name) - len(bed.sunlight) - 2)}│")
        output.append(f"├{'─' * (bed.width * 8 + 2)}┤")
        
        # Group placements by size for layout
        large_plants = [p for p in bed.placements if p.size in (PlantSize.LARGE, PlantSize.VINE)]
        medium_plants = [p for p in bed.placements if p.size == PlantSize.MEDIUM]
        small_plants = [p for p in bed.placements if p.size == PlantSize.SMALL]
        
        # Layout large plants first (north end to avoid shading)
        if large_plants:
            for plant in large_plants:
                crop_display = f"[{plant.crop.upper()}]"
                if plant.quantity > 1:
                    crop_display += f" x{plant.quantity}"
                output.append(f"│ {crop_display:<{bed.width * 8}} │")
        
        # Medium plants
        if medium_plants:
            output.append(f"│ {'':<{bed.width * 8}} │")
            for plant in medium_plants:
                crop_display = f"[{plant.crop.title()}]"
                if plant.quantity > 1:
                    crop_display += f" x{plant.quantity}"
                if plant.companion_to:
                    crop_display += f" (with {plant.companion_to})"
                output.append(f"│ {crop_display:<{bed.width * 8}} │")
        
        # Small plants (can fill gaps)
        if small_plants:
            output.append(f"│ {'':<{bed.width * 8}} │")
            small_line = " ".join([f"[{p.crop[:4]}]x{p.quantity}" for p in small_plants])
            output.append(f"│ {small_line:<{bed.width * 8}} │")
        
        output.append(f"└{'─' * (bed.width * 8 + 2)}┘")
        output.append("")
        
        # Planting notes
        output.append("Planting Notes:")
        for i, plant in enumerate(bed.placements, 1):
            size_desc = {
                PlantSize.LARGE: "24-36\" spacing",
                PlantSize.MEDIUM: "12-18\" spacing",
                PlantSize.SMALL: "4-6\" spacing",
                PlantSize.VINE: "Needs trellis or 36\" spacing"
            }.get(plant.size, "")
            
            output.append(f"  {i}. {plant.crop.title()}: {plant.quantity} plants ({size_desc})")
            for note in plant.notes:
                output.append(f"     • {note}")
        
        output.append("")
    
    # Overall layout notes
    if layout.notes:
        output.append("Layout Notes:")
        for note in layout.notes:
            output.append(f"  • {note}")
    
    return "\n".join(output)


def generate_layout_guide(crops: List[str], user_space: str = "4x8 bed") -> str:
    """
    Generate a complete layout guide for given crops.
    
    Args:
        crops: List of crops to layout
        user_space: User's space description
    
    Returns:
        Complete layout guide as string
    """
    # Parse space (simplified - assume 4x8 if unclear)
    try:
        parts = user_space.lower().split('x')
        width = int(''.join(filter(str.isdigit, parts[0]))) if parts else 4
        length = int(''.join(filter(str.isdigit, parts[1]))) if len(parts) > 1 else 8
    except:
        width, length = 4, 8
    
    # Generate layout
    layout = generate_layout(crops, width, length)
    
    # Generate ASCII visualization
    ascii_viz = generate_ascii_layout(layout)
    
    return ascii_viz
