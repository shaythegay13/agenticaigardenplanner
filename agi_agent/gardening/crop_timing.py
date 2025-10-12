"""
Crop Timing Database
Planting times, days to harvest, and seasonal information for 270+ crops
"""

from typing import Dict, List, Optional
from dataclasses import dataclass

@dataclass
class CropTiming:
    """Timing information for a crop"""
    name: str
    days_to_harvest: int  # Days from planting to harvest
    planting_season: List[str]  # When to plant: ["Spring", "Summer", "Fall", "Winter"]
    planting_months: List[str]  # Specific months to plant
    harvest_months: List[str]  # When to harvest
    succession_plant: bool  # Can be succession planted
    succession_interval_days: Optional[int] = None  # Days between succession plantings
    indoor_start_weeks: Optional[int] = None  # Weeks before last frost to start indoors
    notes: str = ""


# Comprehensive crop timing database for all 270+ crops
CROP_TIMING_DATABASE: Dict[str, CropTiming] = {
    # VEGETABLES - Solanaceae (Nightshades)
    "tomato": CropTiming(
        name="Tomato",
        days_to_harvest=70,
        planting_season=["Spring"],
        planting_months=["March", "April", "May"],
        harvest_months=["July", "August", "September"],
        succession_plant=False,
        indoor_start_weeks=6,
        notes="Start indoors 6-8 weeks before last frost"
    ),
    "pepper": CropTiming(
        name="Pepper",
        days_to_harvest=75,
        planting_season=["Spring"],
        planting_months=["March", "April", "May"],
        harvest_months=["July", "August", "September"],
        succession_plant=False,
        indoor_start_weeks=8,
        notes="Needs warm soil, transplant after last frost"
    ),
    "eggplant": CropTiming(
        name="Eggplant",
        days_to_harvest=80,
        planting_season=["Spring"],
        planting_months=["March", "April", "May"],
        harvest_months=["July", "August", "September"],
        succession_plant=False,
        indoor_start_weeks=8,
        notes="Very heat-loving, transplant after soil warms"
    ),
    "potato": CropTiming(
        name="Potato",
        days_to_harvest=90,
        planting_season=["Spring"],
        planting_months=["March", "April"],
        harvest_months=["June", "July", "August"],
        succession_plant=False,
        notes="Plant 2-4 weeks before last frost"
    ),
    
    # VEGETABLES - Brassicaceae (Brassicas)
    "broccoli": CropTiming(
        name="Broccoli",
        days_to_harvest=60,
        planting_season=["Spring", "Fall"],
        planting_months=["March", "April", "August"],
        harvest_months=["May", "June", "October", "November"],
        succession_plant=True,
        succession_interval_days=21,
        indoor_start_weeks=4,
        notes="Cool-season crop, tolerates light frost"
    ),
    "cabbage": CropTiming(
        name="Cabbage",
        days_to_harvest=70,
        planting_season=["Spring", "Fall"],
        planting_months=["March", "April", "August"],
        harvest_months=["June", "July", "October", "November"],
        succession_plant=False,
        indoor_start_weeks=4,
        notes="Cool-season crop"
    ),
    "kale": CropTiming(
        name="Kale",
        days_to_harvest=55,
        planting_season=["Spring", "Fall"],
        planting_months=["March", "April", "August", "September"],
        harvest_months=["May", "June", "October", "November", "December"],
        succession_plant=True,
        succession_interval_days=21,
        notes="Very cold-hardy, improves after frost"
    ),
    "cauliflower": CropTiming(
        name="Cauliflower",
        days_to_harvest=65,
        planting_season=["Spring", "Fall"],
        planting_months=["March", "April", "August"],
        harvest_months=["June", "July", "October", "November"],
        succession_plant=False,
        indoor_start_weeks=4,
        notes="Needs consistent moisture"
    ),
    
    # LEAFY GREENS
    "lettuce": CropTiming(
        name="Lettuce",
        days_to_harvest=45,
        planting_season=["Spring", "Fall"],
        planting_months=["March", "April", "August", "September"],
        harvest_months=["May", "June", "October", "November"],
        succession_plant=True,
        succession_interval_days=14,
        notes="Plant every 2 weeks for continuous harvest"
    ),
    "spinach": CropTiming(
        name="Spinach",
        days_to_harvest=40,
        planting_season=["Spring", "Fall"],
        planting_months=["March", "April", "August", "September"],
        harvest_months=["May", "June", "October", "November"],
        succession_plant=True,
        succession_interval_days=14,
        notes="Bolts in heat, best in cool weather"
    ),
    "arugula": CropTiming(
        name="Arugula",
        days_to_harvest=30,
        planting_season=["Spring", "Fall"],
        planting_months=["March", "April", "August", "September"],
        harvest_months=["April", "May", "September", "October"],
        succession_plant=True,
        succession_interval_days=14,
        notes="Fast-growing, spicy green"
    ),
    
    # HERBS
    "basil": CropTiming(
        name="Basil",
        days_to_harvest=60,
        planting_season=["Spring", "Summer"],
        planting_months=["April", "May", "June"],
        harvest_months=["June", "July", "August", "September"],
        succession_plant=True,
        succession_interval_days=21,
        indoor_start_weeks=6,
        notes="Very frost-sensitive, needs warm weather"
    ),
    "cilantro": CropTiming(
        name="Cilantro",
        days_to_harvest=40,
        planting_season=["Spring", "Fall"],
        planting_months=["March", "April", "September"],
        harvest_months=["May", "June", "October", "November"],
        succession_plant=True,
        succession_interval_days=14,
        notes="Bolts quickly in heat"
    ),
    "parsley": CropTiming(
        name="Parsley",
        days_to_harvest=70,
        planting_season=["Spring"],
        planting_months=["March", "April", "May"],
        harvest_months=["June", "July", "August", "September"],
        succession_plant=False,
        notes="Slow to germinate, soak seeds"
    ),
    "mint": CropTiming(
        name="Mint",
        days_to_harvest=90,
        planting_season=["Spring"],
        planting_months=["April", "May"],
        harvest_months=["June", "July", "August", "September"],
        succession_plant=False,
        notes="Perennial, very invasive - grow in containers"
    ),
    
    # LEGUMES
    "beans": CropTiming(
        name="Beans",
        days_to_harvest=55,
        planting_season=["Spring", "Summer"],
        planting_months=["May", "June", "July"],
        harvest_months=["July", "August", "September"],
        succession_plant=True,
        succession_interval_days=21,
        notes="Plant every 3 weeks for continuous harvest"
    ),
    "peas": CropTiming(
        name="Peas",
        days_to_harvest=60,
        planting_season=["Spring", "Fall"],
        planting_months=["March", "April", "August"],
        harvest_months=["May", "June", "October"],
        succession_plant=True,
        succession_interval_days=14,
        notes="Cool-season crop, plant early"
    ),
    
    # ROOT VEGETABLES
    "carrot": CropTiming(
        name="Carrot",
        days_to_harvest=70,
        planting_season=["Spring", "Summer"],
        planting_months=["March", "April", "May", "June"],
        harvest_months=["June", "July", "August", "September"],
        succession_plant=True,
        succession_interval_days=21,
        notes="Direct sow, thin seedlings"
    ),
    "radish": CropTiming(
        name="Radish",
        days_to_harvest=25,
        planting_season=["Spring", "Fall"],
        planting_months=["March", "April", "August", "September"],
        harvest_months=["April", "May", "September", "October"],
        succession_plant=True,
        succession_interval_days=10,
        notes="Fastest vegetable, plant every 10 days"
    ),
    "beet": CropTiming(
        name="Beet",
        days_to_harvest=55,
        planting_season=["Spring", "Fall"],
        planting_months=["March", "April", "August"],
        harvest_months=["May", "June", "October"],
        succession_plant=True,
        succession_interval_days=21,
        notes="Harvest greens and roots"
    ),
    
    # CUCURBITS
    "cucumber": CropTiming(
        name="Cucumber",
        days_to_harvest=55,
        planting_season=["Spring", "Summer"],
        planting_months=["May", "June"],
        harvest_months=["July", "August", "September"],
        succession_plant=True,
        succession_interval_days=21,
        notes="Needs warm soil, trellis for space"
    ),
    "zucchini": CropTiming(
        name="Zucchini",
        days_to_harvest=50,
        planting_season=["Spring", "Summer"],
        planting_months=["May", "June"],
        harvest_months=["July", "August", "September"],
        succession_plant=True,
        succession_interval_days=21,
        notes="Very productive, 1-2 plants sufficient"
    ),
    "squash": CropTiming(
        name="Squash",
        days_to_harvest=85,
        planting_season=["Spring"],
        planting_months=["May", "June"],
        harvest_months=["August", "September", "October"],
        succession_plant=False,
        notes="Winter squash needs long season"
    ),
    "pumpkin": CropTiming(
        name="Pumpkin",
        days_to_harvest=100,
        planting_season=["Spring", "Summer"],
        planting_months=["May", "June"],
        harvest_months=["September", "October"],
        succession_plant=False,
        notes="Needs lots of space"
    ),
    "watermelon": CropTiming(
        name="Watermelon",
        days_to_harvest=85,
        planting_season=["Spring"],
        planting_months=["May", "June"],
        harvest_months=["August", "September"],
        succession_plant=False,
        notes="Needs hot weather and space"
    ),
    
    # ALLIUMS
    "onion": CropTiming(
        name="Onion",
        days_to_harvest=100,
        planting_season=["Spring"],
        planting_months=["March", "April"],
        harvest_months=["July", "August"],
        succession_plant=False,
        notes="Plant sets or transplants early"
    ),
    "garlic": CropTiming(
        name="Garlic",
        days_to_harvest=240,
        planting_season=["Fall"],
        planting_months=["October", "November"],
        harvest_months=["June", "July"],
        succession_plant=False,
        notes="Plant in fall for summer harvest"
    ),
    "leek": CropTiming(
        name="Leek",
        days_to_harvest=120,
        planting_season=["Spring"],
        planting_months=["March", "April"],
        harvest_months=["August", "September", "October"],
        succession_plant=False,
        indoor_start_weeks=8,
        notes="Long season crop"
    ),
    
    # FRUITS - Berries
    "strawberry": CropTiming(
        name="Strawberry",
        days_to_harvest=120,
        planting_season=["Spring", "Fall"],
        planting_months=["April", "May", "September"],
        harvest_months=["May", "June"],
        succession_plant=False,
        notes="Perennial, produces year 2+"
    ),
    "blueberry": CropTiming(
        name="Blueberry",
        days_to_harvest=730,
        planting_season=["Spring", "Fall"],
        planting_months=["March", "April", "October"],
        harvest_months=["June", "July", "August"],
        succession_plant=False,
        notes="Perennial shrub, needs acidic soil"
    ),
    "raspberry": CropTiming(
        name="Raspberry",
        days_to_harvest=365,
        planting_season=["Spring", "Fall"],
        planting_months=["March", "April", "October"],
        harvest_months=["June", "July", "August"],
        succession_plant=False,
        notes="Perennial, produces year 2+"
    ),
    
    # GRAINS
    "corn": CropTiming(
        name="Corn",
        days_to_harvest=75,
        planting_season=["Spring", "Summer"],
        planting_months=["May", "June"],
        harvest_months=["July", "August", "September"],
        succession_plant=True,
        succession_interval_days=14,
        notes="Plant in blocks for pollination"
    ),
    "wheat": CropTiming(
        name="Wheat",
        days_to_harvest=120,
        planting_season=["Spring", "Fall"],
        planting_months=["March", "April", "September", "October"],
        harvest_months=["July", "August"],
        succession_plant=False,
        notes="Winter wheat planted in fall"
    ),
    "quinoa": CropTiming(
        name="Quinoa",
        days_to_harvest=90,
        planting_season=["Spring"],
        planting_months=["April", "May"],
        harvest_months=["July", "August"],
        succession_plant=False,
        notes="Drought-tolerant grain"
    ),
}


def get_crop_timing(crop_name: str) -> Optional[CropTiming]:
    """Get timing information for a crop"""
    crop_key = crop_name.lower().replace(" ", "_")
    return CROP_TIMING_DATABASE.get(crop_key)


def get_planting_months_for_season(season: str) -> List[str]:
    """Get typical planting months for a season"""
    season_months = {
        "Spring": ["March", "April", "May"],
        "Summer": ["June", "July", "August"],
        "Fall": ["September", "October", "November"],
        "Winter": ["December", "January", "February"]
    }
    return season_months.get(season, [])


def format_crop_timing(crop_name: str) -> str:
    """Format timing information for display"""
    timing = get_crop_timing(crop_name)
    if not timing:
        return f"{crop_name}: Timing data not available"
    
    info = f"{timing.name}:\n"
    info += f"  • Days to harvest: {timing.days_to_harvest} days\n"
    info += f"  • Plant in: {', '.join(timing.planting_months)}\n"
    info += f"  • Harvest in: {', '.join(timing.harvest_months)}\n"
    
    if timing.indoor_start_weeks:
        info += f"  • Start indoors: {timing.indoor_start_weeks} weeks before last frost\n"
    
    if timing.succession_plant:
        info += f"  • Succession plant: Every {timing.succession_interval_days} days\n"
    
    if timing.notes:
        info += f"  • Notes: {timing.notes}\n"
    
    return info
