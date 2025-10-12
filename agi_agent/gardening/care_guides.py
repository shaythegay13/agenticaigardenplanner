"""
Crop-Specific Care Instructions Module
Detailed care calendars, fertilization schedules, and maintenance guides
"""

from typing import List, Dict, Optional
from .crop_families import CropFamily, CROP_FAMILIES


# Comprehensive care database for major crops
CARE_DATABASE = {
    # TOMATOES
    "tomato": {
        "family": CropFamily.SOLANACEAE,
        "care_calendar": {
            "week_1-2": "Transplant seedlings after last frost. Water deeply. Stake or cage plants.",
            "week_3-4": "Mulch around plants. Begin weekly fertilization with balanced fertilizer.",
            "week_5-6": "Prune suckers on indeterminate varieties. Monitor for pests.",
            "week_7-8": "Continue fertilization. Water consistently (1-2 inches per week).",
            "week_9-10": "First fruits forming. Switch to low-nitrogen, high-potassium fertilizer.",
            "week_11-12": "Begin harvesting ripe fruits. Remove diseased leaves promptly.",
            "week_13+": "Continue harvesting. Reduce watering as season ends.",
        },
        "fertilization": "Feed weekly with balanced 10-10-10 until flowering, then switch to 5-10-10. Side-dress with compost mid-season.",
        "watering": "1-2 inches per week. Water at base, avoid wetting leaves. Consistent moisture prevents blossom end rot.",
        "pruning": "Remove suckers on indeterminate varieties. Remove lower leaves for air circulation.",
        "support": "Stake or cage at planting. Tie stems loosely as they grow.",
        "common_tasks": [
            "Check daily for hornworms and remove by hand",
            "Remove yellowing lower leaves",
            "Harvest ripe fruits promptly to encourage more production",
            "Monitor for early blight and treat with copper fungicide if needed"
        ]
    },
    
    # PEPPERS
    "pepper": {
        "family": CropFamily.SOLANACEAE,
        "care_calendar": {
            "week_1-2": "Transplant after soil warms to 65°F. Space 18-24 inches apart.",
            "week_3-4": "Mulch to retain moisture. Begin fertilization every 2 weeks.",
            "week_5-6": "Stake tall varieties. Monitor for aphids.",
            "week_7-8": "First flowers appearing. Maintain consistent watering.",
            "week_9-10": "Small peppers forming. Continue fertilization.",
            "week_11-12": "Begin harvesting when peppers reach full size.",
            "week_13+": "Continue harvesting. Peppers sweeten as they ripen to final color.",
        },
        "fertilization": "Feed every 2 weeks with 5-10-10 fertilizer. Avoid high nitrogen which delays fruiting.",
        "watering": "1 inch per week. Deep, infrequent watering better than frequent shallow watering.",
        "pruning": "Pinch first flowers to encourage stronger plant. Remove damaged leaves.",
        "support": "Stake or cage heavy-fruiting varieties to prevent branch breakage.",
        "common_tasks": [
            "Check for aphids on new growth",
            "Harvest regularly to encourage more production",
            "Allow some peppers to fully ripen for sweetest flavor",
            "Protect from early fall frost with row covers"
        ]
    },
    
    # LETTUCE
    "lettuce": {
        "family": CropFamily.ASTERACEAE,
        "care_calendar": {
            "week_1-2": "Direct sow or transplant. Keep soil moist for germination.",
            "week_3-4": "Thin seedlings to 6-8 inches apart. Begin light fertilization.",
            "week_5-6": "Harvest outer leaves or wait for full heads.",
            "week_7-8": "Continue harvesting. Watch for bolting in warm weather.",
        },
        "fertilization": "Light feeding with nitrogen-rich fertilizer (fish emulsion) every 2 weeks.",
        "watering": "Keep soil consistently moist. Water in morning to prevent disease.",
        "pruning": "Harvest outer leaves regularly to encourage continued growth.",
        "support": "None needed.",
        "common_tasks": [
            "Harvest in morning for crispest leaves",
            "Succession plant every 2 weeks for continuous harvest",
            "Provide shade cloth in hot weather to prevent bolting",
            "Watch for slugs and use beer traps or diatomaceous earth"
        ]
    },
    
    # TOMATOES (additional detail)
    "basil": {
        "family": CropFamily.LAMIACEAE,
        "care_calendar": {
            "week_1-2": "Plant after last frost. Pinch growing tips to encourage bushiness.",
            "week_3-4": "Begin harvesting leaves. Fertilize lightly.",
            "week_5-6": "Pinch flower buds to keep plant producing leaves.",
            "week_7-8": "Continue harvesting. Plant may slow in extreme heat.",
            "week_9+": "Harvest heavily before first frost. Make pesto to preserve.",
        },
        "fertilization": "Light feeding monthly with balanced fertilizer. Avoid over-fertilizing.",
        "watering": "Keep soil moist but not waterlogged. Water at base of plant.",
        "pruning": "Pinch growing tips regularly. Remove flower buds immediately.",
        "support": "None needed.",
        "common_tasks": [
            "Harvest leaves in morning for best flavor",
            "Pinch flowers as soon as they appear",
            "Harvest regularly to encourage bushy growth",
            "Watch for Japanese beetles and remove by hand"
        ]
    },
    
    # CARROTS
    "carrot": {
        "family": CropFamily.APIACEAE,
        "care_calendar": {
            "week_1-2": "Direct sow. Keep soil moist for germination (10-14 days).",
            "week_3-4": "Thin seedlings to 2-3 inches apart. Mulch lightly.",
            "week_5-8": "Keep soil consistently moist. Weed carefully.",
            "week_9-10": "Carrots sizing up. Reduce watering slightly.",
            "week_11-12": "Begin harvesting when shoulders are 3/4 inch diameter.",
        },
        "fertilization": "Minimal fertilizer needed. Too much nitrogen causes hairy roots.",
        "watering": "1 inch per week. Consistent moisture prevents cracking.",
        "pruning": "None needed.",
        "support": "None needed.",
        "common_tasks": [
            "Thin seedlings carefully to avoid disturbing neighbors",
            "Mulch to prevent green shoulders",
            "Harvest before ground freezes",
            "Store in sand or sawdust for winter keeping"
        ]
    },
    
    # CUCUMBERS
    "cucumber": {
        "family": CropFamily.CUCURBITACEAE,
        "care_calendar": {
            "week_1-2": "Plant after soil warms. Provide trellis for vining types.",
            "week_3-4": "Mulch heavily. Begin weekly fertilization.",
            "week_5-6": "Flowers appearing. Ensure good pollination.",
            "week_7-8": "First cucumbers forming. Harvest when 6-8 inches long.",
            "week_9+": "Harvest daily to encourage continued production.",
        },
        "fertilization": "Feed weekly with balanced fertilizer. Switch to low-nitrogen when fruiting.",
        "watering": "1-2 inches per week. Consistent moisture prevents bitter cucumbers.",
        "pruning": "Remove dead leaves. Train vines onto trellis.",
        "support": "Trellis or cage for vining varieties. Saves space and improves air circulation.",
        "common_tasks": [
            "Harvest daily - overripe cucumbers stop production",
            "Check for cucumber beetles and hand-pick",
            "Ensure good pollination - plant flowers nearby",
            "Remove any diseased leaves immediately"
        ]
    },
    
    # BEANS
    "beans": {
        "family": CropFamily.FABACEAE,
        "care_calendar": {
            "week_1-2": "Direct sow after last frost. Provide support for pole beans.",
            "week_3-4": "Thin to 4-6 inches apart. Mulch lightly.",
            "week_5-6": "Flowers appearing. Avoid disturbing plants.",
            "week_7-8": "Begin harvesting snap beans when pods are firm.",
            "week_9+": "Harvest every 2-3 days to encourage production.",
        },
        "fertilization": "Minimal - beans fix their own nitrogen. Light compost tea if needed.",
        "watering": "1 inch per week. Water at base to prevent disease.",
        "pruning": "None needed.",
        "support": "Pole beans need 6-8 foot trellis or poles.",
        "common_tasks": [
            "Harvest in morning when pods are crisp",
            "Pick regularly to encourage more pods",
            "Avoid working in wet plants (spreads disease)",
            "Leave roots in soil after harvest to release nitrogen"
        ]
    },
    
    # SQUASH
    "squash": {
        "family": CropFamily.CUCURBITACEAE,
        "care_calendar": {
            "week_1-2": "Plant after last frost. Space 3-4 feet apart.",
            "week_3-4": "Mulch heavily. Begin weekly fertilization.",
            "week_5-6": "Large leaves developing. Monitor for squash bugs.",
            "week_7-8": "Flowers appearing. Hand-pollinate if needed.",
            "week_9-10": "Summer squash ready when 6-8 inches. Winter squash needs longer.",
            "week_11+": "Continue harvesting summer squash. Let winter squash mature on vine.",
        },
        "fertilization": "Feed weekly with balanced fertilizer until flowering, then reduce.",
        "watering": "1-2 inches per week. Water at base, avoid wetting leaves.",
        "pruning": "Remove dead leaves. Can prune excess vines if needed.",
        "support": "None for bush types. Trellis possible for vining types.",
        "common_tasks": [
            "Check daily for squash bugs and eggs - remove immediately",
            "Hand-pollinate flowers in morning if few bees",
            "Harvest summer squash when small and tender",
            "Cure winter squash in sun for 10-14 days before storage"
        ]
    },
    
    # KALE
    "kale": {
        "family": CropFamily.BRASSICACEAE,
        "care_calendar": {
            "week_1-2": "Plant in early spring or late summer. Space 12-18 inches.",
            "week_3-4": "Thin seedlings. Begin light fertilization.",
            "week_5-6": "Begin harvesting outer leaves when 8-10 inches.",
            "week_7+": "Continue harvesting. Flavor improves after light frost.",
        },
        "fertilization": "Feed every 3 weeks with nitrogen-rich fertilizer.",
        "watering": "1 inch per week. Consistent moisture for tender leaves.",
        "pruning": "Harvest outer leaves, leave center to continue growing.",
        "support": "None needed.",
        "common_tasks": [
            "Harvest outer leaves regularly",
            "Check for cabbage worms and remove by hand",
            "Mulch to retain moisture",
            "Flavor sweetens after frost - harvest through winter"
        ]
    },
    
    # ONIONS
    "onion": {
        "family": CropFamily.ALLIACEAE,
        "care_calendar": {
            "week_1-4": "Plant sets or transplants in early spring. Space 4-6 inches.",
            "week_5-8": "Keep weeded. Fertilize every 2-3 weeks.",
            "week_9-12": "Bulbs sizing up. Reduce watering as tops yellow.",
            "week_13-16": "When tops fall over, stop watering. Harvest when tops are brown.",
        },
        "fertilization": "Feed every 2-3 weeks with nitrogen-rich fertilizer until bulbing.",
        "watering": "1 inch per week until tops begin to yellow, then stop.",
        "pruning": "None needed.",
        "support": "None needed.",
        "common_tasks": [
            "Keep weed-free - onions don't compete well",
            "Don't bend tops over - let them fall naturally",
            "Cure in warm, dry place for 2-3 weeks before storage",
            "Harvest green onions anytime for fresh use"
        ]
    },
}


def get_care_guide(crop_name: str) -> Optional[Dict]:
    """Get care guide for a specific crop"""
    crop_key = crop_name.lower().replace(" ", "_")
    return CARE_DATABASE.get(crop_key)


def generate_care_calendar(crop_name: str) -> str:
    """
    Generate a week-by-week care calendar for a crop.
    
    Args:
        crop_name: Name of the crop
    
    Returns:
        Formatted care calendar
    """
    care_guide = get_care_guide(crop_name)
    
    if not care_guide:
        return f"\n**{crop_name} Care Calendar:**\nDetailed care calendar not available. Follow general care guidelines.\n"
    
    calendar = f"\n**{crop_name} Care Calendar:**\n\n"
    
    # Week-by-week schedule
    for week, tasks in care_guide["care_calendar"].items():
        calendar += f"• {week.replace('_', ' ').title()}: {tasks}\n"
    
    calendar += "\n"
    
    return calendar


def generate_detailed_care_guide(crops: List[str]) -> str:
    """
    Generate detailed care guides for selected crops.
    
    Args:
        crops: List of crop names
    
    Returns:
        Formatted care guide
    """
    guide = "\n\n" + "="*70 + "\n"
    guide += "DETAILED CARE INSTRUCTIONS\n"
    guide += "="*70 + "\n\n"
    
    # Get care guides for crops that have them
    crops_with_guides = []
    for crop in crops[:5]:  # Show detailed guides for top 5 crops
        care_guide = get_care_guide(crop)
        if care_guide:
            crops_with_guides.append((crop, care_guide))
    
    if not crops_with_guides:
        guide += "General care guidelines apply to your selected crops.\n"
        guide += "Water consistently, fertilize as needed, and monitor for pests.\n\n"
        return guide
    
    for crop, care_guide in crops_with_guides:
        guide += f"**{crop.upper()}**\n"
        guide += f"Family: {care_guide['family'].value}\n\n"
        
        # Fertilization
        guide += f"**Fertilization:** {care_guide['fertilization']}\n\n"
        
        # Watering
        guide += f"**Watering:** {care_guide['watering']}\n\n"
        
        # Pruning
        guide += f"**Pruning:** {care_guide['pruning']}\n\n"
        
        # Support
        guide += f"**Support:** {care_guide['support']}\n\n"
        
        # Common tasks
        guide += "**Weekly Tasks:**\n"
        for task in care_guide['common_tasks']:
            guide += f"  • {task}\n"
        
        guide += "\n" + "-"*70 + "\n\n"
    
    return guide


def generate_maintenance_schedule(crops: List[str]) -> str:
    """
    Generate a general maintenance schedule for all crops.
    
    Args:
        crops: List of crop names
    
    Returns:
        Formatted maintenance schedule
    """
    schedule = "\n\n**WEEKLY MAINTENANCE CHECKLIST:**\n\n"
    
    schedule += "**Daily Tasks:**\n"
    schedule += "• Check soil moisture - water if top inch is dry\n"
    schedule += "• Harvest ripe produce to encourage more production\n"
    schedule += "• Scout for pests and remove by hand\n"
    schedule += "• Remove any diseased or damaged leaves\n\n"
    
    schedule += "**Weekly Tasks:**\n"
    schedule += "• Deep watering (1-2 inches) if no rain\n"
    schedule += "• Weed around plants\n"
    schedule += "• Check stakes and supports, adjust as needed\n"
    schedule += "• Apply mulch if it's thin\n"
    schedule += "• Fertilize crops that need weekly feeding\n\n"
    
    schedule += "**Bi-Weekly Tasks:**\n"
    schedule += "• Fertilize most crops\n"
    schedule += "• Prune and train vining plants\n"
    schedule += "• Check for signs of disease\n"
    schedule += "• Succession plant quick crops (lettuce, radishes)\n\n"
    
    schedule += "**Monthly Tasks:**\n"
    schedule += "• Refresh mulch layer\n"
    schedule += "• Side-dress heavy feeders with compost\n"
    schedule += "• Review and adjust watering schedule\n"
    schedule += "• Plan next season's plantings\n\n"
    
    return schedule


def generate_fertilization_guide(crops: List[str]) -> str:
    """
    Generate crop-specific fertilization recommendations.
    
    Args:
        crops: List of crop names
    
    Returns:
        Formatted fertilization guide
    """
    guide = "\n\n**FERTILIZATION GUIDE:**\n\n"
    
    # Categorize crops
    heavy_feeders = []
    moderate_feeders = []
    light_feeders = []
    
    for crop in crops:
        family = CROP_FAMILIES.get(crop.lower().replace(" ", "_"))
        if family in [CropFamily.SOLANACEAE, CropFamily.CUCURBITACEAE]:
            heavy_feeders.append(crop)
        elif family == CropFamily.FABACEAE:
            light_feeders.append(crop)
        else:
            moderate_feeders.append(crop)
    
    if heavy_feeders:
        guide += "**Heavy Feeders** (weekly feeding):\n"
        guide += f"Crops: {', '.join(heavy_feeders)}\n"
        guide += "• Feed weekly with balanced 10-10-10 fertilizer\n"
        guide += "• Switch to 5-10-10 when flowering/fruiting\n"
        guide += "• Side-dress with compost mid-season\n"
        guide += "• Water well after fertilizing\n\n"
    
    if moderate_feeders:
        guide += "**Moderate Feeders** (bi-weekly feeding):\n"
        guide += f"Crops: {', '.join(moderate_feeders)}\n"
        guide += "• Feed every 2 weeks with balanced fertilizer\n"
        guide += "• Use compost tea or fish emulsion\n"
        guide += "• Reduce feeding as harvest approaches\n\n"
    
    if light_feeders:
        guide += "**Light Feeders** (minimal feeding):\n"
        guide += f"Crops: {', '.join(light_feeders)}\n"
        guide += "• Minimal fertilizer needed\n"
        guide += "• Compost at planting is usually sufficient\n"
        guide += "• Over-fertilizing can reduce production\n\n"
    
    guide += "**Fertilizer Types:**\n"
    guide += "• 10-10-10: Balanced for vegetative growth\n"
    guide += "• 5-10-10: Lower nitrogen for fruiting\n"
    guide += "• Fish emulsion: Gentle, organic nitrogen source\n"
    guide += "• Compost tea: All-purpose, adds beneficial microbes\n"
    guide += "• Bone meal: Phosphorus for root development\n"
    guide += "• Kelp meal: Potassium and trace minerals\n\n"
    
    return guide


def generate_pruning_guide(crops: List[str]) -> str:
    """
    Generate pruning and training recommendations.
    
    Args:
        crops: List of crop names
    
    Returns:
        Formatted pruning guide
    """
    guide = "\n\n**PRUNING & TRAINING GUIDE:**\n\n"
    
    # Check which crops need pruning
    needs_pruning = []
    for crop in crops:
        care_guide = get_care_guide(crop)
        if care_guide and "prune" in care_guide.get("pruning", "").lower():
            needs_pruning.append((crop, care_guide["pruning"]))
    
    if needs_pruning:
        for crop, pruning_info in needs_pruning:
            guide += f"**{crop.title()}:** {pruning_info}\n\n"
    else:
        guide += "Most of your selected crops require minimal pruning.\n"
        guide += "General tips:\n"
        guide += "• Remove dead, diseased, or damaged leaves promptly\n"
        guide += "• Thin overcrowded plants for better air circulation\n"
        guide += "• Harvest regularly to encourage continued production\n\n"
    
    return guide
