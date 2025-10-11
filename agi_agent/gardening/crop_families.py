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
    
    # ALL REMAINING FRUITS (from your list)
    "acai": CropFamily.TROPICAL_FRUIT,
    "acerola_cherry": CropFamily.TROPICAL_FRUIT,
    "bael": CropFamily.TROPICAL_FRUIT,
    "bilberry": CropFamily.BERRIES,
    "breadfruit": CropFamily.TROPICAL_FRUIT,
    "buddhas_hand": CropFamily.RUTACEAE,
    "cape_gooseberry": CropFamily.SOLANACEAE,
    "cherimoya": CropFamily.TROPICAL_FRUIT,
    "coconut": CropFamily.TROPICAL_FRUIT,
    "crab_apple": CropFamily.ROSACEAE,
    "date": CropFamily.TROPICAL_FRUIT,
    "durian": CropFamily.TROPICAL_FRUIT,
    "feijoa": CropFamily.TROPICAL_FRUIT,
    "guava": CropFamily.TROPICAL_FRUIT,
    "jackfruit": CropFamily.TROPICAL_FRUIT,
    "longan": CropFamily.TROPICAL_FRUIT,
    "lychee": CropFamily.TROPICAL_FRUIT,
    "mangosteen": CropFamily.TROPICAL_FRUIT,
    "marionberry": CropFamily.BERRIES,
    "passionfruit": CropFamily.TROPICAL_FRUIT,
    "rambutan": CropFamily.TROPICAL_FRUIT,
    "starfruit": CropFamily.TROPICAL_FRUIT,
    "tamarind": CropFamily.FABACEAE,
    
    # ALL REMAINING VEGETABLES
    "brussels_sprouts": CropFamily.BRASSICACEAE,
    "cress": CropFamily.BRASSICACEAE,
    "green_beans": CropFamily.FABACEAE,
    "mushroom": CropFamily.TROPICAL_FRUIT,  # Not a plant but included
    "tomatillo": CropFamily.SOLANACEAE,
    
    # ALL REMAINING NUTS
    "andean_walnut": CropFamily.JUGLANDACEAE,
    "argan_nut": CropFamily.TROPICAL_FRUIT,
    "beech_nut": CropFamily.TROPICAL_FRUIT,
    "betel_nut": CropFamily.TROPICAL_FRUIT,
    "black_walnut": CropFamily.JUGLANDACEAE,
    "breadnut": CropFamily.TROPICAL_FRUIT,
    "bunya_nut": CropFamily.TROPICAL_FRUIT,
    "butternut": CropFamily.JUGLANDACEAE,
    "candle_nut": CropFamily.TROPICAL_FRUIT,
    "chilean_hazelnut": CropFamily.JUGLANDACEAE,
    "chinese_chestnut": CropFamily.ROSACEAE,
    "dika_nut": CropFamily.TROPICAL_FRUIT,
    "english_walnut": CropFamily.JUGLANDACEAE,
    "filbert": CropFamily.JUGLANDACEAE,
    "ginkgo_nut": CropFamily.TROPICAL_FRUIT,
    "hickory_nut": CropFamily.JUGLANDACEAE,
    "jack_nut": CropFamily.TROPICAL_FRUIT,
    "kola_nut": CropFamily.TROPICAL_FRUIT,
    "kurrajong_nut": CropFamily.TROPICAL_FRUIT,
    "lotus_nut": CropFamily.TROPICAL_FRUIT,
    "malabar_chestnut": CropFamily.TROPICAL_FRUIT,
    "marcona_almond": CropFamily.ROSACEAE,
    "mongongo_nut": CropFamily.TROPICAL_FRUIT,
    "monkey_puzzle_nut": CropFamily.TROPICAL_FRUIT,
    "palm_nut": CropFamily.TROPICAL_FRUIT,
    "paradise_nut": CropFamily.TROPICAL_FRUIT,
    "pignoli": CropFamily.TROPICAL_FRUIT,
    "pili_nut": CropFamily.TROPICAL_FRUIT,
    "saba_nut": CropFamily.TROPICAL_FRUIT,
    "tiger_nut": CropFamily.CHENOPODIACEAE,
    "water_caltrop": CropFamily.TROPICAL_FRUIT,
    
    # ALL REMAINING GRAINS
    "bulgur": CropFamily.POACEAE,
    "einkorn": CropFamily.POACEAE,
    "fonio": CropFamily.POACEAE,
    "freekeh": CropFamily.POACEAE,
    "semolina": CropFamily.POACEAE,
    "triticale": CropFamily.POACEAE,
    "wild_rice": CropFamily.POACEAE,
    
    # ALL REMAINING LEGUMES
    "haricot": CropFamily.FABACEAE,
    "black_turtle_bean": CropFamily.FABACEAE,
    "scarlet_runner_bean": CropFamily.FABACEAE,
    "rice_bean": CropFamily.FABACEAE,
    "moth_bean": CropFamily.FABACEAE,
    "tepary_bean": CropFamily.FABACEAE,
    "broad_bean": CropFamily.FABACEAE,
    "horse_bean": CropFamily.FABACEAE,
    "field_bean": CropFamily.FABACEAE,
    "garden_pea": CropFamily.FABACEAE,
    "protein_pea": CropFamily.FABACEAE,
    "garbanzo": CropFamily.FABACEAE,
    "pigeon_pea": CropFamily.FABACEAE,
    "bambara_groundnut": CropFamily.FABACEAE,
    "vetch": CropFamily.FABACEAE,
    "lupin": CropFamily.FABACEAE,
    "lablab_bean": CropFamily.FABACEAE,
    "jack_bean": CropFamily.FABACEAE,
    "sword_bean": CropFamily.FABACEAE,
    "winged_bean": CropFamily.FABACEAE,
    "velvet_bean": CropFamily.FABACEAE,
    "yam_bean": CropFamily.FABACEAE,
    "lentil_dal": CropFamily.FABACEAE,
    "cannellini_bean": CropFamily.FABACEAE,
    "mesquite_bean": CropFamily.FABACEAE,
    
    # RICE VARIETIES (35+)
    "aizon_rice": CropFamily.POACEAE,
    "ambemohar_rice": CropFamily.POACEAE,
    "annapoornna_rice": CropFamily.POACEAE,
    "atop_rice": CropFamily.POACEAE,
    "basmati_rice": CropFamily.POACEAE,
    "barma_black_rice": CropFamily.POACEAE,
    "bhut_muri_rice": CropFamily.POACEAE,
    "bora_rice": CropFamily.POACEAE,
    "champa_rice": CropFamily.POACEAE,
    "chokuwa_rice": CropFamily.POACEAE,
    "clearfield_rice": CropFamily.POACEAE,
    "dubraj_rice": CropFamily.POACEAE,
    "gandhasala_rice": CropFamily.POACEAE,
    "gobindobhog_rice": CropFamily.POACEAE,
    "hansraj_rice": CropFamily.POACEAE,
    "hasan_serai_rice": CropFamily.POACEAE,
    "hmt_rice": CropFamily.POACEAE,
    "idly_rice": CropFamily.POACEAE,
    "jay_shrirama_rice": CropFamily.POACEAE,
    "joha_rice": CropFamily.POACEAE,
    "jyothi_rice": CropFamily.POACEAE,
    "kamini_rice": CropFamily.POACEAE,
    "kasalath_rice": CropFamily.POACEAE,
    "katta_sambar_rice": CropFamily.POACEAE,
    "laxmi_bhog_rice": CropFamily.POACEAE,
    "minicate_rice": CropFamily.POACEAE,
    "molakolukulu_rice": CropFamily.POACEAE,
    "navara_rice": CropFamily.POACEAE,
    "patna_rice": CropFamily.POACEAE,
    "ponni_rice": CropFamily.POACEAE,
    "pusa_basmati_1121_rice": CropFamily.POACEAE,
    "radhunipagal_rice": CropFamily.POACEAE,
    "raja_hansa_rice": CropFamily.POACEAE,
    "ranjit_rice": CropFamily.POACEAE,
    "rosematta_rice": CropFamily.POACEAE,
    "sona_masuri_rice": CropFamily.POACEAE,
    "surekha_rice": CropFamily.POACEAE,
    "tulaipanji_rice": CropFamily.POACEAE,
    
    # SEEDS (edible/plantable)
    "sunflower_seed": CropFamily.ASTERACEAE,
    "pumpkin_seed": CropFamily.CUCURBITACEAE,
    "flax_seed": CropFamily.TROPICAL_FRUIT,
    "chia_seed": CropFamily.LAMIACEAE,
    "sesame_seed": CropFamily.TROPICAL_FRUIT,
    "hemp_seed": CropFamily.TROPICAL_FRUIT,
    "poppy_seed": CropFamily.TROPICAL_FRUIT,
    "caraway_seed": CropFamily.APIACEAE,
    "nigella_seed": CropFamily.TROPICAL_FRUIT,
    "mustard_seed": CropFamily.BRASSICACEAE,
    "coriander_seed": CropFamily.APIACEAE,
    "cumin_seed": CropFamily.APIACEAE,
    "fennel_seed": CropFamily.APIACEAE,
    "fenugreek_seed": CropFamily.FABACEAE,
    "basil_seed": CropFamily.LAMIACEAE,
    "watermelon_seed": CropFamily.CUCURBITACEAE,
    "grape_seed": CropFamily.VITACEAE,
    "cottonseed": CropFamily.TROPICAL_FRUIT,
    "safflower_seed": CropFamily.ASTERACEAE,
    "cardamom_seed": CropFamily.TROPICAL_FRUIT,
    "celery_seed": CropFamily.APIACEAE,
    "moringa_seed": CropFamily.TROPICAL_FRUIT,
    "lotus_seed": CropFamily.TROPICAL_FRUIT,
    "jackfruit_seed": CropFamily.TROPICAL_FRUIT,
    "sacha_inchi_seed": CropFamily.TROPICAL_FRUIT,
    "canola_seed": CropFamily.BRASSICACEAE,
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
    CropFamily.ROSACEAE: [
        "Fire Blight", "Apple Scab", "Powdery Mildew",
        "Brown Rot", "Cedar Apple Rust", "Black Knot",
        "Leaf Curl", "Bacterial Canker", "Crown Gall"
    ],
    CropFamily.BERRIES: [
        "Gray Mold (Botrytis)", "Anthracnose", "Powdery Mildew",
        "Verticillium Wilt", "Phytophthora Root Rot", "Leaf Spot",
        "Cane Blight", "Orange Rust", "Mummy Berry"
    ],
    CropFamily.RUTACEAE: [
        "Citrus Canker", "Citrus Greening (HLB)", "Citrus Black Spot",
        "Melanose", "Alternaria Brown Spot", "Phytophthora Root Rot",
        "Sooty Mold", "Citrus Scab"
    ],
    CropFamily.VITACEAE: [
        "Powdery Mildew", "Downy Mildew", "Black Rot",
        "Botrytis Bunch Rot", "Anthracnose", "Pierce's Disease",
        "Crown Gall", "Phomopsis Cane and Leaf Spot"
    ],
    CropFamily.TROPICAL_FRUIT: [
        "Anthracnose", "Fusarium Wilt", "Root Rot",
        "Leaf Spot", "Fruit Rot", "Bacterial Soft Rot",
        "Powdery Mildew", "Cercospora Leaf Spot"
    ],
    CropFamily.JUGLANDACEAE: [
        "Walnut Blight", "Anthracnose", "Crown Rot",
        "Thousand Cankers Disease", "Phytophthora Root Rot", "Leaf Blotch"
    ],
    CropFamily.ANACARDIACEAE: [
        "Anthracnose", "Powdery Mildew", "Bacterial Black Spot",
        "Verticillium Wilt", "Root Rot", "Sooty Mold"
    ],
    CropFamily.LAMIACEAE: [
        "Powdery Mildew", "Downy Mildew", "Root Rot",
        "Fusarium Wilt", "Botrytis Gray Mold", "Bacterial Leaf Spot"
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
