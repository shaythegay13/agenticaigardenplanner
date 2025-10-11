from typing import List, Dict, Any, Optional
from .models import Sunlight, GardeningMethod, SpaceSize, Experience, CropInterest, Preference
from .crop_families import CROP_FAMILIES, CropFamily


class Plant:
    def __init__(self, name: str, categories: List[CropInterest],
                 light: List[Sunlight], methods: List[GardeningMethod],
                 sizes: List[SpaceSize], experience: List[Experience],
                 notes: str = "",
                 native_us_regions: Optional[List[str]] = None,
                 native_states: Optional[List[str]] = None,
                 regions_supported: Optional[List[str]] = None):
        self.name = name
        self.categories = categories
        self.light = light
        self.methods = methods
        self.sizes = sizes
        self.experience = experience
        self.notes = notes
        self.native_us_regions = set(native_us_regions or [])
        self.native_states = set(native_states or [])
        # regions_supported can be broader cultivation suitability beyond nativity
        self.regions_supported = set(regions_supported or [])


PLANTS: List[Plant] = [
    Plant(
        name="Lettuce",
        categories=[CropInterest.LEAFY_GREENS],
        light=[Sunlight.PARTIAL_SUN, Sunlight.PARTIAL_SHADE, Sunlight.FULL_SUN],
        methods=[GardeningMethod.CONTAINERS, GardeningMethod.RAISED_BEDS, GardeningMethod.IN_GROUND, GardeningMethod.INDOOR],
        sizes=[SpaceSize.SMALL, SpaceSize.MEDIUM, SpaceSize.LARGE, SpaceSize.VERY_LARGE],
        experience=[Experience.BEGINNER, Experience.NOVICE, Experience.INTERMEDIATE, Experience.ADVANCED],
        notes="Cool-season; quick harvest; frequent sowings.",
        regions_supported=["Northeast","Midwest","South","West"]
    ),
    Plant(
        name="Spinach",
        categories=[CropInterest.LEAFY_GREENS],
        light=[Sunlight.PARTIAL_SUN, Sunlight.PARTIAL_SHADE],
        methods=[GardeningMethod.CONTAINERS, GardeningMethod.RAISED_BEDS, GardeningMethod.IN_GROUND, GardeningMethod.INDOOR],
        sizes=[SpaceSize.SMALL, SpaceSize.MEDIUM, SpaceSize.LARGE, SpaceSize.VERY_LARGE],
        experience=[Experience.BEGINNER, Experience.NOVICE, Experience.INTERMEDIATE, Experience.ADVANCED],
        notes="Cool-season; bolts in heat.",
        regions_supported=["Northeast","Midwest","West"]
    ),
    Plant(
        name="Basil",
        categories=[CropInterest.HERBS],
        light=[Sunlight.FULL_SUN, Sunlight.PARTIAL_SUN],
        methods=[GardeningMethod.CONTAINERS, GardeningMethod.RAISED_BEDS, GardeningMethod.INDOOR],
        sizes=[SpaceSize.SMALL, SpaceSize.MEDIUM, SpaceSize.LARGE],
        experience=[Experience.BEGINNER, Experience.NOVICE, Experience.INTERMEDIATE, Experience.ADVANCED],
        notes="Warm-season; great for containers and windowsills.",
        regions_supported=["Northeast","Midwest","South","West"]
    ),
    Plant(
        name="Tomatoes",
        categories=[CropInterest.TOMATOES],
        light=[Sunlight.FULL_SUN],
        methods=[GardeningMethod.CONTAINERS, GardeningMethod.RAISED_BEDS, GardeningMethod.IN_GROUND, GardeningMethod.ROOFTOP],
        sizes=[SpaceSize.MEDIUM, SpaceSize.LARGE, SpaceSize.VERY_LARGE],
        experience=[Experience.NOVICE, Experience.INTERMEDIATE, Experience.ADVANCED],
        notes="Warm-season; needs staking and regular feeding.",
        regions_supported=["Northeast","Midwest","South","West"]
    ),
    Plant(
        name="Peppers",
        categories=[CropInterest.PEPPERS],
        light=[Sunlight.FULL_SUN],
        methods=[GardeningMethod.CONTAINERS, GardeningMethod.RAISED_BEDS, GardeningMethod.IN_GROUND, GardeningMethod.ROOFTOP],
        sizes=[SpaceSize.MEDIUM, SpaceSize.LARGE, SpaceSize.VERY_LARGE],
        experience=[Experience.NOVICE, Experience.INTERMEDIATE, Experience.ADVANCED],
        notes="Warm-season; compact varieties suit containers.",
        regions_supported=["Northeast","Midwest","South","West"]
    ),
    Plant(
        name="Radishes",
        categories=[CropInterest.ROOT_VEGETABLES],
        light=[Sunlight.FULL_SUN, Sunlight.PARTIAL_SUN],
        methods=[GardeningMethod.CONTAINERS, GardeningMethod.RAISED_BEDS, GardeningMethod.IN_GROUND],
        sizes=[SpaceSize.SMALL, SpaceSize.MEDIUM, SpaceSize.LARGE, SpaceSize.VERY_LARGE],
        experience=[Experience.BEGINNER, Experience.NOVICE, Experience.INTERMEDIATE, Experience.ADVANCED],
        notes="Very fast-growing cool-season root.",
        regions_supported=["Northeast","Midwest","West"]
    ),
    Plant(
        name="Cucumbers",
        categories=[CropInterest.SQUASH_CUCUMBERS],
        light=[Sunlight.FULL_SUN],
        methods=[GardeningMethod.RAISED_BEDS, GardeningMethod.IN_GROUND, GardeningMethod.VERTICAL, GardeningMethod.ROOFTOP],
        sizes=[SpaceSize.MEDIUM, SpaceSize.LARGE, SpaceSize.VERY_LARGE],
        experience=[Experience.NOVICE, Experience.INTERMEDIATE, Experience.ADVANCED],
        notes="Warm-season; trellis for space efficiency.",
        regions_supported=["Northeast","Midwest","South","West"]
    ),
    Plant(
        name="Pole Beans",
        categories=[CropInterest.BEANS_PEAS],
        light=[Sunlight.FULL_SUN, Sunlight.PARTIAL_SUN],
        methods=[GardeningMethod.RAISED_BEDS, GardeningMethod.IN_GROUND, GardeningMethod.VERTICAL],
        sizes=[SpaceSize.MEDIUM, SpaceSize.LARGE, SpaceSize.VERY_LARGE],
        experience=[Experience.BEGINNER, Experience.NOVICE, Experience.INTERMEDIATE, Experience.ADVANCED],
        notes="Warm-season; vertical support needed.",
        regions_supported=["Northeast","Midwest","South","West"]
    ),
    Plant(
        name="Mint",
        categories=[CropInterest.HERBS],
        light=[Sunlight.PARTIAL_SUN, Sunlight.PARTIAL_SHADE],
        methods=[GardeningMethod.CONTAINERS, GardeningMethod.INDOOR],
        sizes=[SpaceSize.SMALL, SpaceSize.MEDIUM],
        experience=[Experience.BEGINNER, Experience.NOVICE, Experience.INTERMEDIATE, Experience.ADVANCED],
        notes="Vigorous; best kept in containers.",
        regions_supported=["Northeast","Midwest","South","West"]
    ),
    Plant(
        name="Microgreens",
        categories=[CropInterest.MICROGREENS],
        light=[Sunlight.ARTIFICIAL_ONLY, Sunlight.PARTIAL_SHADE, Sunlight.PARTIAL_SUN],
        methods=[GardeningMethod.INDOOR, GardeningMethod.CONTAINERS],
        sizes=[SpaceSize.SMALL, SpaceSize.MEDIUM],
        experience=[Experience.BEGINNER, Experience.NOVICE, Experience.INTERMEDIATE, Experience.ADVANCED],
        notes="Very fast; great for artificial lights.",
        regions_supported=["Northeast","Midwest","South","West"]
    ),
    # Native plants examples for regions
    Plant(
        name="Bee Balm (Monarda didyma)",
        categories=[CropInterest.HERBS],
        light=[Sunlight.FULL_SUN, Sunlight.PARTIAL_SUN],
        methods=[GardeningMethod.RAISED_BEDS, GardeningMethod.IN_GROUND, GardeningMethod.CONTAINERS],
        sizes=[SpaceSize.MEDIUM, SpaceSize.LARGE, SpaceSize.VERY_LARGE],
        experience=[Experience.BEGINNER, Experience.NOVICE, Experience.INTERMEDIATE, Experience.ADVANCED],
        notes="Native perennial; pollinator magnet; aromatic foliage.",
        native_us_regions=["Northeast","Midwest"],
        native_states=["New York","Pennsylvania","Ohio","Michigan","Vermont","Massachusetts"],
        regions_supported=["Northeast","Midwest"]
    ),
    Plant(
        name="Purple Coneflower (Echinacea purpurea)",
        categories=[CropInterest.HERBS],
        light=[Sunlight.FULL_SUN, Sunlight.PARTIAL_SUN],
        methods=[GardeningMethod.RAISED_BEDS, GardeningMethod.IN_GROUND, GardeningMethod.CONTAINERS],
        sizes=[SpaceSize.MEDIUM, SpaceSize.LARGE, SpaceSize.VERY_LARGE],
        experience=[Experience.BEGINNER, Experience.NOVICE, Experience.INTERMEDIATE, Experience.ADVANCED],
        notes="Native perennial; drought tolerant once established.",
        native_us_regions=["Midwest","South","Northeast"],
        regions_supported=["Midwest","South","Northeast","West"]
    ),
    Plant(
        name="Blue Grama (Bouteloua gracilis)",
        categories=[CropInterest.HERBS],
        light=[Sunlight.FULL_SUN],
        methods=[GardeningMethod.IN_GROUND, GardeningMethod.RAISED_BEDS],
        sizes=[SpaceSize.LARGE, SpaceSize.VERY_LARGE],
        experience=[Experience.INTERMEDIATE, Experience.ADVANCED],
        notes="Native warm-season grass; very drought tolerant.",
        native_us_regions=["West"],
        regions_supported=["West"]
    ),
]


def recommend_plants(
    interests: List[CropInterest],
    sunlight: Sunlight,
    method: GardeningMethod,
    size: SpaceSize,
    experience: Experience,
    preferences: List[Preference],
    us_region: Optional[str] = None,
    state: Optional[str] = None,
) -> List[Plant]:
    """Filter plants by constraints and interests. If interests include SUGGEST, use all categories."""
    if CropInterest.SUGGEST in interests:
        categories = set([c for p in PLANTS for c in p.categories])
    else:
        categories = set(interests)

    results: List[Plant] = []
    for p in PLANTS:
        if not (set(p.categories) & categories):
            continue
        if sunlight not in p.light:
            continue
        if method not in p.methods:
            continue
        if size not in p.sizes:
            continue
        if experience not in p.experience:
            continue
        # Region suitability: if regions_supported present, prefer matches
        if p.regions_supported and us_region and us_region not in p.regions_supported:
            # still include but lower score later
            results.append(p)
        else:
            results.append(p)

    # Preference-based simple prioritization: FAST_GROWING, LOW_MAINTENANCE, etc. handled via sorting by heuristics
    def score(plant: Plant) -> int:
        s = 0
        if Preference.FAST_GROWING in preferences and ("fast" in plant.notes.lower() or "quick" in plant.notes.lower()):
            s += 2
        if Preference.LOW_MAINTENANCE in preferences or Preference.EASY_CARE in preferences:
            if "easy" in plant.notes.lower() or "vigorous" in plant.notes.lower():
                s += 2
        if Preference.YEAR_ROUND in preferences and (CropInterest.MICROGREENS in plant.categories or GardeningMethod.INDOOR in plant.methods):
            s += 1
        # Native preferences
        if Preference.NATIVE in preferences and us_region and (us_region in plant.native_us_regions):
            s += 3
        if Preference.NATIVE_NYC in preferences and (state == "New York" or (us_region == "Northeast" and "New York" in plant.native_states)):
            s += 4
        # Region suitability bonus
        if us_region and (not plant.regions_supported or us_region in plant.regions_supported):
            s += 1
        return -s  # negative for ascending sort

    results.sort(key=score)
    
    # If we have very few results, add crops from extended database
    if len(results) < 10:
        extended_crops = generate_extended_crop_recommendations(
            sunlight, method, size, experience, crop_interests, preferences
        )
        # Add extended crops that aren't already in results
        existing_names = {p.name.lower() for p in results}
        for crop in extended_crops:
            if crop.name.lower() not in existing_names:
                results.append(crop)
                if len(results) >= 15:  # Cap at 15 total recommendations
                    break
    
    return results


def generate_extended_crop_recommendations(
    sunlight, method, size, experience, crop_interests, preferences
) -> List[Plant]:
    """Generate recommendations from the extended 270+ crop database"""
    recommendations = []
    
    # Map crop interests to families
    interest_to_family = {
        CropInterest.TOMATOES: [CropFamily.SOLANACEAE],
        CropInterest.PEPPERS: [CropFamily.SOLANACEAE],
        CropInterest.LEAFY_GREENS: [CropFamily.ASTERACEAE, CropFamily.BRASSICACEAE, CropFamily.CHENOPODIACEAE],
        CropInterest.HERBS: [CropFamily.LAMIACEAE, CropFamily.APIACEAE],
        CropInterest.ROOT_VEGETABLES: [CropFamily.APIACEAE, CropFamily.BRASSICACEAE],
        CropInterest.SQUASH_CUCUMBERS: [CropFamily.CUCURBITACEAE],
        CropInterest.BEANS_PEAS: [CropFamily.FABACEAE],
        CropInterest.BERRIES: [CropFamily.BERRIES, CropFamily.ROSACEAE],
        CropInterest.FRUIT_TREES: [CropFamily.ROSACEAE, CropFamily.RUTACEAE],
    }
    
    # Get relevant families based on user interests
    target_families = []
    
    # Check if user selected "I don't know - suggest crops for me"
    if CropInterest.SUGGEST in crop_interests:
        # Provide diverse beginner-friendly recommendations
        if experience == Experience.BEGINNER:
            # Prioritize easy, fast-growing crops for beginners
            target_families = [
                CropFamily.LAMIACEAE,  # Herbs (basil, mint)
                CropFamily.ASTERACEAE,  # Lettuce, greens
                CropFamily.BRASSICACEAE,  # Radishes, kale
                CropFamily.FABACEAE,  # Beans, peas
            ]
        else:
            # Include all families for variety
            target_families = list(CropFamily)
    else:
        # Use specific interests
        for interest in crop_interests:
            target_families.extend(interest_to_family.get(interest, []))
    
    # If still no specific interests, include beginner-friendly families
    if not target_families:
        target_families = [
            CropFamily.LAMIACEAE,
            CropFamily.ASTERACEAE,
            CropFamily.BRASSICACEAE,
            CropFamily.FABACEAE,
        ]
    
    # Generate Plant objects for crops in target families
    for crop_key, family in CROP_FAMILIES.items():
        if family in target_families:
            crop_name = crop_key.replace("_", " ").title()
            # Skip if already in main PLANTS list
            if any(p.name.lower() == crop_name.lower() for p in PLANTS):
                continue
            
            # Determine categories based on family
            categories = []
            if family == CropFamily.SOLANACEAE:
                categories = [CropInterest.TOMATOES, CropInterest.PEPPERS]
            elif family in [CropFamily.ASTERACEAE, CropFamily.BRASSICACEAE, CropFamily.CHENOPODIACEAE]:
                categories = [CropInterest.LEAFY_GREENS]
            elif family in [CropFamily.LAMIACEAE, CropFamily.APIACEAE]:
                categories = [CropInterest.HERBS]
            elif family == CropFamily.APIACEAE:
                categories = [CropInterest.ROOT_VEGETABLES]
            elif family == CropFamily.CUCURBITACEAE:
                categories = [CropInterest.SQUASH_CUCUMBERS]
            elif family == CropFamily.FABACEAE:
                categories = [CropInterest.BEANS_PEAS]
            elif family in [CropFamily.BERRIES, CropFamily.ROSACEAE]:
                categories = [CropInterest.BERRIES]
            elif family in [CropFamily.RUTACEAE, CropFamily.TROPICAL_FRUIT]:
                categories = [CropInterest.FRUIT_TREES]
            else:
                categories = [CropInterest.LEAFY_GREENS]  # Default
            
            # Determine suitable methods based on crop type
            suitable_methods = [GardeningMethod.RAISED_BEDS, GardeningMethod.IN_GROUND]
            
            # Herbs and small crops work well in containers and indoors
            if family in [CropFamily.LAMIACEAE, CropFamily.ASTERACEAE]:
                suitable_methods.extend([GardeningMethod.CONTAINERS, GardeningMethod.INDOOR, GardeningMethod.VERTICAL])
            
            # Skip large trees/shrubs for small spaces or indoor growing
            if family in [CropFamily.ROSACEAE, CropFamily.RUTACEAE, CropFamily.JUGLANDACEAE]:
                if size == SpaceSize.SMALL or method == GardeningMethod.INDOOR:
                    continue  # Skip trees for small/indoor spaces
                suitable_methods = [GardeningMethod.IN_GROUND]
            
            # Check if this crop is suitable for the user's method
            if method not in suitable_methods:
                continue
            
            # Create Plant object with sensible defaults
            plant = Plant(
                name=crop_name,
                categories=categories,
                light=[Sunlight.FULL_SUN, Sunlight.PARTIAL_SUN],  # Most crops
                methods=suitable_methods,
                sizes=[SpaceSize.SMALL, SpaceSize.MEDIUM, SpaceSize.LARGE, SpaceSize.VERY_LARGE],
                experience=[Experience.BEGINNER, Experience.NOVICE, Experience.INTERMEDIATE, Experience.ADVANCED],
                notes=f"{family.value} family crop - easy to grow",
                regions_supported=["Northeast", "Midwest", "South", "West"]
            )
            recommendations.append(plant)
    
    return recommendations[:20]  # Return top 20
