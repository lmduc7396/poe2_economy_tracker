"""
POE2 Economy Tracker - Configuration
Farming method mappings and settings
"""

# Farming methods and their corresponding poe2scout API categories
FARMING_METHODS = {
    "Breach": {
        "icon": "https://web.poecdn.com/gen/image/WzI1LDE0LHsiZiI6IjJESXRlbXMvQ3VycmVuY3kvQnJlYWNoL0JyZWFjaHN0b25lU3BsaW50ZXIiLCJ3IjoxLCJoIjoxLCJzY2FsZSI6MSwicmVhbG0iOiJwb2UyIn1d/00c84e43a8/BreachstoneSplinter.png",
        "categories": ["breach"],
        "color": "#9b59b6",  # Purple
        "description": "Breach Catalysts, Splinters, Breachstones"
    },
    "Abyssal": {
        "icon": "https://web.poecdn.com//gen/image/WzI1LDE0LHsiZiI6IjJESXRlbXMvQ3VycmVuY3kvQWJ5c3MvUHJlc2VydmVkSmF3Ym9uZSIsInNjYWxlIjoxLCJyZWFsbSI6InBvZTIifV0/2bb7939b21/PreservedJawbone.png",
        "categories": ["abyss", "lineagesupportgems"],
        "color": "#2ecc71",  # Green
        "description": "Abyssal Bones, some Lineage Gems"
    },
    "Ritual": {
        "icon": "https://web.poecdn.com/gen/image/WzI1LDE0LHsiZiI6IjJESXRlbXMvQ3VycmVuY3kvT21lbnMvVm9vZG9vT21lbnMxUmVkIiwidyI6MSwiaCI6MSwic2NhbGUiOjEsInJlYWxtIjoicG9lMiJ9XQ/1c90d2eb1f/VoodooOmens1Red.png",
        "categories": ["ritual"],
        "color": "#e74c3c",  # Red
        "description": "Omens, Audience with the King"
    },
    "Expedition": {
        "icon": "https://web.poecdn.com/gen/image/WzI1LDE0LHsiZiI6IjJESXRlbXMvQ3VycmVuY3kvRXhwZWRpdGlvbi9CYXJ0ZXJSZWZyZXNoQ3VycmVuY3kiLCJ3IjoxLCJoIjoxLCJzY2FsZSI6MSwicmVhbG0iOiJwb2UyIn1d/b0f42eaf8d/BarterRefreshCurrency.png",
        "categories": ["expedition"],
        "color": "#f39c12",  # Orange
        "description": "Coinage, Artifacts, Logbooks"
    },
    "Delirium": {
        "icon": "https://web.poecdn.com/gen/image/WzI1LDE0LHsiZiI6IjJESXRlbXMvQ3VycmVuY3kvRGlzdGlsbGVkRW1vdGlvbnMvRGlzdGlsbGVkRGVzcGFpciIsInciOjEsImgiOjEsInNjYWxlIjoxLCJyZWFsbSI6InBvZTIifV0/794fb40302/DistilledDespair.png",
        "categories": ["delirium"],
        "color": "#bdc3c7",  # Silver/Gray
        "description": "Distilled Emotions, Simulacrum"
    },
    "Vaal Temple": {
        "icon": "https://web.poecdn.com/gen/image/WzI1LDE0LHsiZiI6IjJESXRlbXMvQ3VycmVuY3kvSW5jdXJzaW9uQ3JhZnRpbmdPcmJzL0luY3Vyc2lvbkdyZWF0ZXJWYWFsT3JiIiwic2NhbGUiOjEsInJlYWxtIjoicG9lMiJ9XQ/7ba6f79f63/IncursionGreaterVaalOrb.png",
        "categories": ["incursion"],
        "color": "#e91e63",  # Pink/Magenta
        "description": "Vaal Orbs, Incursion crafting"
    },
    "Trial of Chaos": {
        "icon": "https://web.poecdn.com/gen/image/WzI1LDE0LHsiZiI6IjJESXRlbXMvQ3VycmVuY3kvU291bENvcmVzL0dyZWF0ZXJTb3VsQ29yZUNyaXQiLCJ3IjoxLCJoIjoxLCJzY2FsZSI6MSwicmVhbG0iOiJwb2UyIn1d/6d3a52eb08/GreaterSoulCoreCrit.png",
        "categories": ["ultimatum"],
        "color": "#ff5722",  # Deep Orange
        "description": "Soul Cores, Inscribed Ultimatums"
    },
    "Sekhema": {
        "icon": "https://web.poecdn.com/gen/image/WzI1LDE0LHsiZiI6IjJESXRlbXMvSmV3ZWxzL0JyZWFjaEpld2VsIiwidyI6MSwiaCI6MSwic2NhbGUiOjEsInJlYWxtIjoicG9lMiJ9XQ/9c17747ff2/BreachJewel.png",
        "categories": ["jewel"],  # Jewels from unique category
        "color": "#00bcd4",  # Cyan
        "description": "Time-Lost Jewels, Grand Spectrum"
    },
}

# Categories that are general drops (not tied to specific farming)
GENERAL_CATEGORIES = [
    "currency",
    "fragments",
    "runes",
    "essences",
    "talismans",
    "uncutgems",
    "vaultkeys",
]

# API Configuration
API_BASE_URL = "https://poe2scout.com/api"
CACHE_TTL_SECONDS = 1800  # 30 minutes

# Default league
DEFAULT_LEAGUE = "Fate of the Vaal"

# Profit score weights
VOLUME_WEIGHT = 1.0
PRICE_CHANGE_WEIGHT = 1.0
MIN_VOLUME_THRESHOLD = 5  # Minimum volume to be considered
MIN_CHAOS_VALUE = 1  # Minimum chaos value to display

# Item name overrides - items that don't match their API category
# These 8 Omens are in the "ritual" API category but actually drop from Abyss
ITEM_FARMING_OVERRIDES = {
    "Omen of the Sovereign": "Abyssal",
    "Omen of the Blackblooded": "Abyssal",
    "Omen of the Liege": "Abyssal",
    "Omen of Abyssal Echoes": "Abyssal",
    "Omen of Dextral Necromancy": "Abyssal",
    "Omen of Sinistral Necromancy": "Abyssal",
    "Omen of Light": "Abyssal",
    "Omen of Putrefaction": "Abyssal",
    # Diamond jewels - each from different content
    "Against the Darkness Time-Lost Diamond": "Sekhema",  # Zarokh
    "Controlled Metamorphosis Diamond": "Breach",  # Xesht
    "Flesh Crucible Diamond": "Vaal Temple",  # Atziri
    "From Nothing Diamond": "Ritual",  # King in the Mists
    "Megalomaniac Diamond": "Delirium",  # Simulacrum
    "The Adorned Diamond": "Trial of Chaos",  # Trialmaster

    # Lineage Support Gems - override default "Abyssal" category mapping
    # Expedition (Olroth, Origin of the Fall)
    "Uhtred's Augury": "Expedition",
    "Uhtred's Omen": "Expedition",
    "Uhtred's Exodus": "Expedition",

    # Breach (Xesht, We That Are One)
    "Xoph's Pyre": "Breach",
    "Esh's Radiance": "Breach",
    "Tul's Stillness": "Breach",
    "Uul-Netol's Embrace": "Breach",

    # Vaal Temple (Atziri, the Red Queen)
    "Atziri's Impatience": "Vaal Temple",
    "Zerphi's Infamy": "Vaal Temple",

    # Trial of Chaos (The Trialmaster)
    "Ixchel's Torment": "Trial of Chaos",

    # Sekhema (Zarokh, the Temporal)
    "Zarokh's Refrain": "Sekhema",
    "Zarokh's Revolt": "Sekhema",

    # Abyssal (Large Abyssal Troves) - keep as Abyssal
    "Kurgal's Leash": "Abyssal",
    "Amanamu's Tithe": "Abyssal",
    "Tecrod's Revenge": "Abyssal",

    # General drops / Anomaly bosses / Pinnacle bosses (not tied to league mechanics)
    # Set to None so they don't appear under any farming method
    "Dialla's Desire": None,  # Can drop anywhere
    "Garukhan's Resolve": None,  # Anomaly boss Zahmir
    "Rakiata's Flow": None,  # Anomaly boss Manoki
    "Rigwald's Ferocity": None,  # Anomaly bosses in Derelict Mansion
    "Atalui's Bloodletting": None,  # Anomaly bosses in Sealed Vault
    "Khatal's Rejuvenation": None,  # Anomaly boss Zahmir
    "Atziri's Allure": None,  # Anomaly bosses in Sealed Vault
    "Arbiter's Ignition": None,  # Pinnacle boss The Arbiter of Ash
    # Additional lineage gems - general drops (can drop anywhere)
    "Tawhoa's Tending": None,
    "Doedre's Undoing": None,
    "Hayoxi's Fulmination": None,
    "Sione's Temper": None,
    "Kulemak's Dominion": None,
    "Arjun's Medal": None,
    "Dominus' Grasp": None,
    "Ratha's Assault": None,
    "Kaom's Madness": None,
    "Brutus' Brain": None,
    "Ahn's Citadel": None,
    "Einhar's Beastrite": None,
    "Ailith's Chimes": None,
    "Kalisa's Crescendo": None,
    "Daresso's Passion": None,
    "Vilenta's Propulsion": None,
    "Bhatair's Vengeance": None,
    "Oisín's Oath": None,
    "Arakaali's Lust": None,
    "Uruk's Smelting": None,
    "Morgana's Tempest": None,
    "Tasalio's Rhythm": None,
    "Xibaqua's Rending": None,
    "Romira's Requital": None,
    "Paquate's Pact": None,
    "Tacati's Ire": None,
    "Cirel's Cultivation": None,
    "Varashta's Blessing": None,
    "Guatelitzi's Ablation": None,
}

# Boss-specific unique item drops (from poe2wiki)
# Maps unique item names to their farming method/boss source
UNIQUE_ITEM_DROP_SOURCES = {
    # Sekhema (Zarokh, the Temporal)
    "Sekhema's Resolve": "Sekhema",
    "Against the Darkness": "Sekhema",
    "Sandstorm Visage": "Sekhema",
    "Temporalis": "Sekhema",

    # Trial of Chaos (The Trialmaster)
    "The Adorned": "Trial of Chaos",
    "Mahuxotl's Machination": "Trial of Chaos",
    "Glimpse of Chaos": "Trial of Chaos",
    "Zerphi's Genesis": "Trial of Chaos",
    "Hateforge": "Trial of Chaos",

    # Expedition (Olroth, Origin of the Fall)
    "Olrovasara": "Expedition",
    "Keeper of the Arc": "Expedition",
    "Svalinn": "Expedition",
    "Heroic Tragedy": "Expedition",
    "Olroth's Resolve": "Expedition",

    # Breach (Xesht, We That Are One)
    "Beyond Reach": "Breach",
    "Xoph's Blood": "Breach",
    "The Pandemonius": "Breach",
    "Choir of the Storm": "Breach",
    "Hand of Wisdom and Action": "Breach",
    "Skin of the Loyal": "Breach",
    "Controlled Metamorphosis": "Breach",

    # Delirium (Simulacrum wave 15)
    "Assailum": "Delirium",
    "Perfidy": "Delirium",
    "Collapsing Horizon": "Delirium",
    "Melting Maelstrom": "Delirium",
    "Strugglescream": "Delirium",
    "Megalomaniac": "Delirium",

    # Ritual (The King in the Mists)
    "Beetlebite": "Ritual",
    "Ingenuity": "Ritual",
    "The Burden of Shadows": "Ritual",
    "Pragmatism": "Ritual",
    "From Nothing": "Ritual",

    # Vaal Temple (Atziri, the Red Queen)
    "Atziri's Step": "Vaal Temple",
    "Drillneck": "Vaal Temple",
    "Atziri's Splendour": "Vaal Temple",
    "Atziri's Rule": "Vaal Temple",
    "Atziri's Contempt": "Vaal Temple",
    "Flesh Crucible": "Vaal Temple",
}

# Unique item categories to fetch from poe2scout API
UNIQUE_CATEGORIES = ["accessory", "armour", "weapon", "flask"]

# Fragment item to farming method mapping
FRAGMENT_FARMING_SOURCES = {
    "Simulacrum Splinter": "Delirium",
    "Breach Splinter": "Breach",
    "Runic Splinter": "Expedition",
    "Primary Calamity Fragment": None,  # Universal
    "Secondary Calamity Fragment": None,
    "Tertiary Calamity Fragment": None,
    "Ancient Crisis Fragment": None,
    "Weathered Crisis Fragment": None,
    "Faded Crisis Fragment": None,
    "Cowardly Fate": "Trial of Chaos",
    "Deadly Fate": "Trial of Chaos",
    "Victorious Fate": "Trial of Chaos",
}

# Minimum value in divine orbs for unique items to be included
MIN_DIVINE_VALUE = 1
