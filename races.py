"""
Race definitions for PyPeake MUD
Defines available races and their characteristics
"""

RACES = {
    "Human": {
        "description": "Versatile and adaptable, humans are well-balanced in all aspects.",
        "bonuses": ["Balanced stats", "Quick learner", "Diplomatic"],
        "stat_bonuses": {
            "strength": 1,
            "dexterity": 1,
            "constitution": 1,
            "intelligence": 1,
            "wisdom": 1,
            "charisma": 1
        },
        "special_abilities": ["Extra experience gain"],
        "restrictions": []
    },
    
    "Elf": {
        "description": "Graceful and wise, elves have a natural affinity for magic and archery.",
        "bonuses": ["High dexterity", "Magical affinity", "Keen senses"],
        "stat_bonuses": {
            "dexterity": 3,
            "intelligence": 2,
            "wisdom": 2,
            "constitution": -1
        },
        "special_abilities": ["Enhanced mana regeneration", "Archery expertise"],
        "restrictions": []
    },
    
    "Dwarf": {
        "description": "Hardy mountain folk known for their strength, endurance, and craftsmanship.",
        "bonuses": ["High constitution", "Poison resistance", "Master craftsman"],
        "stat_bonuses": {
            "strength": 2,
            "constitution": 3,
            "wisdom": 1,
            "dexterity": -1,
            "charisma": -1
        },
        "special_abilities": ["Poison resistance", "Enhanced smithing"],
        "restrictions": []
    },
    
    "Halfling": {
        "description": "Small but nimble folk with incredible luck and stealth abilities.",
        "bonuses": ["High dexterity", "Lucky", "Stealthy"],
        "stat_bonuses": {
            "dexterity": 3,
            "charisma": 2,
            "wisdom": 1,
            "strength": -2
        },
        "special_abilities": ["Lucky escapes", "Enhanced stealth"],
        "restrictions": []
    },
    
    "Orc": {
        "description": "Powerful and fierce warriors with natural combat prowess.",
        "bonuses": ["High strength", "Battle fury", "Intimidating presence"],
        "stat_bonuses": {
            "strength": 4,
            "constitution": 2,
            "intelligence": -2,
            "charisma": -1
        },
        "special_abilities": ["Berserker rage", "Intimidation"],
        "restrictions": []
    },
    
    "Gnome": {
        "description": "Small, intelligent beings with a natural aptitude for magic and tinkering.",
        "bonuses": ["High intelligence", "Magical aptitude", "Inventive"],
        "stat_bonuses": {
            "intelligence": 3,
            "wisdom": 2,
            "dexterity": 1,
            "strength": -2,
            "constitution": -1
        },
        "special_abilities": ["Enhanced spell power", "Tinkering expertise"],
        "restrictions": []
    }
}

def get_race_description(race_name):
    """Get detailed description of a race"""
    if race_name in RACES:
        race = RACES[race_name]
        description = f"{race['description']}\n\n"
        description += "Racial Bonuses:\n"
        for bonus in race['bonuses']:
            description += f"- {bonus}\n"
        description += "\nStat Modifiers:\n"
        for stat, modifier in race['stat_bonuses'].items():
            sign = "+" if modifier >= 0 else ""
            description += f"- {stat.title()}: {sign}{modifier}\n"
        return description
    return "Unknown race"

def get_available_races():
    """Get list of all available races"""
    return list(RACES.keys())
