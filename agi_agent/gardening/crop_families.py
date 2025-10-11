"""
Crop family classifications for disease and companion planting recommendations.
Maps crops to their botanical families for intelligent recommendations.
"""

from enum import Enum
from typing import List, Dict, Set

class CropFamily(str, Enum):
    """Botanical families for crop classification"""
    SOLANACEAE = "Nightshades"  # Tomatoes, peppers, eggplant, potatoes
    BRASSICACEAE = "Brassicas"  # Cabbage, broccoli, kale, radish
    CUCURBITACEAE = "Cucurbits"  # Cucumbers, squash, melons, pumpkins
    FABACEAE = "Legumes"  # Beans, peas, lentils, peanuts
    APIACEAE = "Umbellifers"  # Carrots, celery, parsley, fennel
    ALLIACEAE = "Alliums"  # Onions, garlic, leeks, chives
    ASTERACEAE = "Composites"  # Lettuce, sunflowers, artichokes
    CHENOPODIACEAE = "Chenopods"  # Beets, chard, spinach, quinoa
    POACEAE = "Grasses"  # Corn, wheat, rice, oats, barley
    ROSACEAE = "Rose Family"  # Apples, pears, strawberries, almonds
    RUTACEAE = "Citrus"  # Oranges, lemons, limes, grapefruit
    VITACEAE = "Grape Family"  # Grapes
    MUSACEAE = "Banana Family"  # Bananas, plantains
    LAURACEAE = "Laurel Family"  # Avocado
    ANACARDIACEAE = "Cashew Family"  # Mango, cashew, pistachio
    JUGLANDACEAE = "Walnut Family"  # Walnuts, pecans, hickory
    PROTEACEAE = "Protea Family"  # Macadamia
    LAMIACEAE = "Mint Family"  # Basil, mint, oregano, thyme
    TROPICAL_FRUIT = "Tropical Fruits"  # Papaya, pineapple, dragon fruit
    BERRIES = "Berry Fruits"  # Blueberries, raspberries, blackberries

# Crop to family mapping
CROP_FAMILIES: Dict[str, CropFamily] = {
    # Nightshades
    "tomatoes": CropFamily.SOLANACEAE,
    "peppers": CropFamily.SOLANACEAE,
    "eggplant": CropFamily.SOLANACEAE,
    "potatoes": CropFamily.SOLANACEAE,
    "tomatillo": CropFamily.SOLANACEAE,
    
    # Brassicas
    "broccoli": CropFamily.BRASSICACEAE,
    "cabbage": CropFamily.BRASSICACEAE,
    "cauliflower": CropFamily.BRASSICACEAE,
    "kale": CropFamily.BRASSICACEAE,
    "brussels_sprouts": CropFamily.BRASSICACEAE,
    "radishes": CropFamily.BRASSICACEAE,
    "turnips": CropFamily.BRASSICACEAE,
    "arugula": CropFamily.BRASSICACEAE,
    "bok_choy": CropFamily.BRASSICACEAE,
    "kohlrabi": CropFamily.BRASSICACEAE,
    "collard_greens": CropFamily.BRASSICACEAE,
    
    # Cucurbits
    "cucumbers": CropFamily.CUCURBITACEAE,
    "zucchini": CropFamily.CUCURBITACEAE,
    "squash": CropFamily.CUCURBITACEAE,
    "pumpkin": CropFamily.CUCURBITACEAE,
    "melons": CropFamily.CUCURBITACEAE,
    "watermelon": CropFamily.CUCURBITACEAE,
    "cantaloupe": CropFamily.CUCURBITACEAE,
    "honeydew": CropFamily.CUCURBITACEAE,
    
    # Legumes
    "beans": CropFamily.FABACEAE,
    "peas": CropFamily.FABACEAE,
    "lentils": CropFamily.FABACEAE,
    "chickpeas": CropFamily.FABACEAE,
    "soybeans": CropFamily.FABACEAE,
    "peanuts": CropFamily.FABACEAE,
    "kidney_beans": CropFamily.FABACEAE,
    "black_beans": CropFamily.FABACEAE,
    "lima_beans": CropFamily.FABACEAE,
    "mung_beans": CropFamily.FABACEAE,
    
    # Umbellifers
    "carrots": CropFamily.APIACEAE,
    "celery": CropFamily.APIACEAE,
    "parsley": CropFamily.APIACEAE,
    "cilantro": CropFamily.APIACEAE,
    "fennel": CropFamily.APIACEAE,
    "parsnip": CropFamily.APIACEAE,
    
    # Alliums
    "onions": CropFamily.ALLIACEAE,
    "garlic": CropFamily.ALLIACEAE,
    "leeks": CropFamily.ALLIACEAE,
    "chives": CropFamily.ALLIACEAE,
    "shallots": CropFamily.ALLIACEAE,
    
    # Composites
    "lettuce": CropFamily.ASTERACEAE,
    "sunflowers": CropFamily.ASTERACEAE,
    "artichokes": CropFamily.ASTERACEAE,
    "endive": CropFamily.ASTERACEAE,
    "radicchio": CropFamily.ASTERACEAE,
    
    # Chenopods
    "beets": CropFamily.CHENOPODIACEAE,
    "swiss_chard": CropFamily.CHENOPODIACEAE,
    "spinach": CropFamily.CHENOPODIACEAE,
    "quinoa": CropFamily.CHENOPODIACEAE,
    
    # Grasses/Grains
    "corn": CropFamily.POACEAE,
    "wheat": CropFamily.POACEAE,
    "rice": CropFamily.POACEAE,
    "oats": CropFamily.POACEAE,
    "barley": CropFamily.POACEAE,
    "rye": CropFamily.POACEAE,
    "millet": CropFamily.POACEAE,
    "sorghum": CropFamily.POACEAE,
    
    # Herbs (Mint family)
    "basil": CropFamily.LAMIACEAE,
    "mint": CropFamily.LAMIACEAE,
    "oregano": CropFamily.LAMIACEAE,
    "thyme": CropFamily.LAMIACEAE,
    "sage": CropFamily.LAMIACEAE,
    "rosemary": CropFamily.LAMIACEAE,
    
    # Fruits
    "strawberries": CropFamily.ROSACEAE,
    "apples": CropFamily.ROSACEAE,
    "pears": CropFamily.ROSACEAE,
    "peaches": CropFamily.ROSACEAE,
    "plums": CropFamily.ROSACEAE,
    "cherries": CropFamily.ROSACEAE,
    "almonds": CropFamily.ROSACEAE,
    "raspberries": CropFamily.BERRIES,
    "blackberries": CropFamily.BERRIES,
    "blueberries": CropFamily.BERRIES,
    "cranberries": CropFamily.BERRIES,
    "grapes": CropFamily.VITACEAE,
    "oranges": CropFamily.RUTACEAE,
    "lemons": CropFamily.RUTACEAE,
    "limes": CropFamily.RUTACEAE,
    "grapefruit": CropFamily.RUTACEAE,
    "bananas": CropFamily.MUSACEAE,
    "avocado": CropFamily.LAURACEAE,
    "mango": CropFamily.ANACARDIACEAE,
    "cashews": CropFamily.ANACARDIACEAE,
    "pistachios": CropFamily.ANACARDIACEAE,
    "walnuts": CropFamily.JUGLANDACEAE,
    "pecans": CropFamily.JUGLANDACEAE,
    "macadamia": CropFamily.PROTEACEAE,
    "papaya": CropFamily.TROPICAL_FRUIT,
    "pineapple": CropFamily.TROPICAL_FRUIT,
    "dragon_fruit": CropFamily.TROPICAL_FRUIT,
    
    # Extended Fruits
    "kiwi": CropFamily.TROPICAL_FRUIT,
    "fig": CropFamily.TROPICAL_FRUIT,
    "pomegranate": CropFamily.TROPICAL_FRUIT,
    "persimmon": CropFamily.TROPICAL_FRUIT,
    "nectarine": CropFamily.ROSACEAE,
    "apricot": CropFamily.ROSACEAE,
    "quince": CropFamily.ROSACEAE,
    "gooseberry": CropFamily.BERRIES,
    "currant": CropFamily.BERRIES,
    "elderberry": CropFamily.BERRIES,
    "mulberry": CropFamily.BERRIES,
    "goji_berry": CropFamily.SOLANACEAE,  # Actually nightshade family!
    "kumquat": CropFamily.RUTACEAE,
    "tangerine": CropFamily.RUTACEAE,
    "clementine": CropFamily.RUTACEAE,
    
    # Extended Vegetables
    "asparagus": CropFamily.ASTERACEAE,
    "artichoke": CropFamily.ASTERACEAE,
    "celery": CropFamily.APIACEAE,
    "parsnip": CropFamily.APIACEAE,
    "sweet_potato": CropFamily.SOLANACEAE,
    "potato": CropFamily.SOLANACEAE,
    "yam": CropFamily.TROPICAL_FRUIT,
    "okra": CropFamily.TROPICAL_FRUIT,
    "rhubarb": CropFamily.CHENOPODIACEAE,
    "rutabaga": CropFamily.BRASSICACEAE,
    "daikon": CropFamily.BRASSICACEAE,
    "collard_greens": CropFamily.BRASSICACEAE,
    "mustard_greens": CropFamily.BRASSICACEAE,
    "watercress": CropFamily.BRASSICACEAE,
    "endive": CropFamily.ASTERACEAE,
    "chicory": CropFamily.ASTERACEAE,
    "escarole": CropFamily.ASTERACEAE,
    
    # Extended Legumes
    "lentils": CropFamily.FABACEAE,
    "chickpeas": CropFamily.FABACEAE,
    "black_beans": CropFamily.FABACEAE,
    "kidney_beans": CropFamily.FABACEAE,
    "pinto_beans": CropFamily.FABACEAE,
    "navy_beans": CropFamily.FABACEAE,
    "lima_beans": CropFamily.FABACEAE,
    "fava_beans": CropFamily.FABACEAE,
    "adzuki_beans": CropFamily.FABACEAE,
    "mung_beans": CropFamily.FABACEAE,
    "black_eyed_peas": CropFamily.FABACEAE,
    "soybeans": CropFamily.FABACEAE,
    
    # Grains
    "wheat": CropFamily.POACEAE,
    "amaranth": CropFamily.CHENOPODIACEAE,  # Pseudo-grain
    "buckwheat": CropFamily.CHENOPODIACEAE,  # Pseudo-grain
    "teff": CropFamily.POACEAE,
    "farro": CropFamily.POACEAE,
    "spelt": CropFamily.POACEAE,
    "kamut": CropFamily.POACEAE,
    
    # Herbs (extended)
    "dill": CropFamily.APIACEAE,
    "tarragon": CropFamily.ASTERACEAE,
    "chervil": CropFamily.APIACEAE,
    "marjoram": CropFamily.LAMIACEAE,
    "lavender": CropFamily.LAMIACEAE,
    "lemon_balm": CropFamily.LAMIACEAE,
    "catnip": CropFamily.LAMIACEAE,
    
    # Nuts (extended)
    "hazelnuts": CropFamily.JUGLANDACEAE,
    "chestnuts": CropFamily.ROSACEAE,
    "brazil_nuts": CropFamily.TROPICAL_FRUIT,
    "pine_nuts": CropFamily.TROPICAL_FRUIT,
}

# Common diseases by family
FAMILY_DISEASES: Dict[CropFamily, List[str]] = {
    CropFamily.SOLANACEAE: [
        "Early Blight", "Late Blight", "Septoria Leaf Spot",
        "Verticillium Wilt", "Fusarium Wilt", "Bacterial Spot",
        "Tomato Mosaic Virus", "Blossom End Rot"
    ],
    CropFamily.BRASSICACEAE: [
        "Clubroot", "Black Rot", "Downy Mildew",
        "Powdery Mildew", "Cabbage Worm", "Flea Beetles",
        "White Rust", "Alternaria Leaf Spot"
    ],
    CropFamily.CUCURBITACEAE: [
        "Powdery Mildew", "Downy Mildew", "Anthracnose",
        "Bacterial Wilt", "Cucumber Mosaic Virus", "Fusarium Wilt",
        "Gummy Stem Blight", "Angular Leaf Spot"
    ],
    CropFamily.FABACEAE: [
        "Bean Rust", "Anthracnose", "Bacterial Blight",
        "Powdery Mildew", "Root Rot", "Mosaic Virus",
        "White Mold", "Fusarium Wilt"
    ],
    CropFamily.APIACEAE: [
        "Carrot Rust Fly", "Leaf Blight", "Cercospora Leaf Spot",
        "Powdery Mildew", "Aster Yellows", "Bacterial Soft Rot"
    ],
    CropFamily.ALLIACEAE: [
        "Onion Smut", "Downy Mildew", "Purple Blotch",
        "Botrytis Leaf Blight", "White Rot", "Fusarium Basal Rot"
    ],
    CropFamily.ASTERACEAE: [
        "Downy Mildew", "Bottom Rot", "Tipburn",
        "Lettuce Mosaic Virus", "Septoria Leaf Spot", "Powdery Mildew"
    ],
    CropFamily.CHENOPODIACEAE: [
        "Cercospora Leaf Spot", "Downy Mildew", "Powdery Mildew",
        "Root Rot", "Damping Off", "Leaf Miners"
    ],
}

# Companion planting by family
FAMILY_COMPANIONS: Dict[CropFamily, Dict[str, List[CropFamily]]] = {
    CropFamily.SOLANACEAE: {
        "good": [CropFamily.ALLIACEAE, CropFamily.LAMIACEAE, CropFamily.APIACEAE],
        "avoid": [CropFamily.BRASSICACEAE, CropFamily.FABACEAE]
    },
    CropFamily.BRASSICACEAE: {
        "good": [CropFamily.ALLIACEAE, CropFamily.ASTERACEAE, CropFamily.APIACEAE],
        "avoid": [CropFamily.SOLANACEAE, CropFamily.CUCURBITACEAE]
    },
    CropFamily.CUCURBITACEAE: {
        "good": [CropFamily.FABACEAE, CropFamily.POACEAE, CropFamily.ALLIACEAE],
        "avoid": [CropFamily.SOLANACEAE]
    },
    CropFamily.FABACEAE: {
        "good": [CropFamily.CUCURBITACEAE, CropFamily.POACEAE, CropFamily.APIACEAE],
        "avoid": [CropFamily.ALLIACEAE]
    },
    CropFamily.APIACEAE: {
        "good": [CropFamily.SOLANACEAE, CropFamily.FABACEAE, CropFamily.ALLIACEAE],
        "avoid": []
    },
    CropFamily.ALLIACEAE: {
        "good": [CropFamily.SOLANACEAE, CropFamily.BRASSICACEAE, CropFamily.ASTERACEAE],
        "avoid": [CropFamily.FABACEAE]
    },
}

def get_crop_family(crop_name: str) -> CropFamily:
    """Get the botanical family for a crop"""
    return CROP_FAMILIES.get(crop_name.lower().replace(" ", "_"), None)

def get_family_diseases(family: CropFamily) -> List[str]:
    """Get common diseases for a crop family"""
    return FAMILY_DISEASES.get(family, [])

def get_companion_recommendations(family: CropFamily) -> Dict[str, List[CropFamily]]:
    """Get companion planting recommendations for a family"""
    return FAMILY_COMPANIONS.get(family, {"good": [], "avoid": []})
