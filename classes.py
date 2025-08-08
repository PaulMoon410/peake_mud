"""
Class definitions for PyPeake MUD
Defines available character classes and their characteristics

Copyright (c) 2025 PyPeake MUD
Licensed under the MIT License - see LICENSE file for details
"""

CLASSES = {
    "Warrior": {
        "description": "Master of melee combat, high health and armor, devastating physical attacks.",
        "primary_stat": "Strength",
        "starting_skills": ["Sword Mastery", "Shield Block", "Battle Cry"],
        "stat_bonuses": {
            "strength": 3,
            "constitution": 2,
            "dexterity": 1,
            "intelligence": -1
        },
        "special_abilities": ["Heavy Armor Mastery", "Weapon Expertise"],
        "mana_multiplier": 0.5,
        "health_multiplier": 1.5
    },
    
    "Mage": {
        "description": "Master of arcane magic, powerful spells, but fragile in combat.",
        "primary_stat": "Intelligence",
        "starting_skills": ["Fireball", "Magic Missile", "Mana Shield"],
        "stat_bonuses": {
            "intelligence": 4,
            "wisdom": 2,
            "constitution": -2,
            "strength": -1
        },
        "special_abilities": ["Spell Mastery", "Mana Efficiency"],
        "mana_multiplier": 2.0,
        "health_multiplier": 0.8
    },
    
    "Rogue": {
        "description": "Stealthy assassin, high damage from behind, lockpicking and trap detection.",
        "primary_stat": "Dexterity",
        "starting_skills": ["Backstab", "Stealth", "Lockpicking"],
        "stat_bonuses": {
            "dexterity": 4,
            "intelligence": 1,
            "charisma": 1,
            "strength": -1,
            "constitution": -1
        },
        "special_abilities": ["Sneak Attack", "Trap Detection"],
        "mana_multiplier": 0.8,
        "health_multiplier": 1.0
    },
    
    "Cleric": {
        "description": "Divine spellcaster, healing magic, undead turning, moderate combat ability.",
        "primary_stat": "Wisdom",
        "starting_skills": ["Heal", "Bless", "Turn Undead"],
        "stat_bonuses": {
            "wisdom": 3,
            "charisma": 2,
            "constitution": 1,
            "dexterity": -1
        },
        "special_abilities": ["Divine Magic", "Healing Mastery"],
        "mana_multiplier": 1.5,
        "health_multiplier": 1.2
    },
    
    "Ranger": {
        "description": "Nature's guardian, archery expertise, animal companions, tracking abilities.",
        "primary_stat": "Dexterity",
        "starting_skills": ["Archery", "Track", "Animal Friend"],
        "stat_bonuses": {
            "dexterity": 3,
            "wisdom": 2,
            "constitution": 1,
            "charisma": -1
        },
        "special_abilities": ["Archery Mastery", "Nature Lore"],
        "mana_multiplier": 1.0,
        "health_multiplier": 1.1
    },
    
    "Paladin": {
        "description": "Holy warrior, divine magic, healing, protection of the innocent.",
        "primary_stat": "Charisma",
        "starting_skills": ["Holy Strike", "Heal", "Divine Protection"],
        "stat_bonuses": {
            "charisma": 3,
            "strength": 2,
            "wisdom": 1,
            "intelligence": -1
        },
        "special_abilities": ["Divine Grace", "Undead Bane"],
        "mana_multiplier": 1.2,
        "health_multiplier": 1.3
    },
    
    "Barbarian": {
        "description": "Primal warrior, berserker rage, incredible strength and endurance.",
        "primary_stat": "Constitution",
        "starting_skills": ["Rage", "Intimidate", "Survival"],
        "stat_bonuses": {
            "strength": 3,
            "constitution": 3,
            "wisdom": -1,
            "intelligence": -2
        },
        "special_abilities": ["Berserker Rage", "Damage Resistance"],
        "mana_multiplier": 0.3,
        "health_multiplier": 1.6
    },
    
    "Bard": {
        "description": "Jack of all trades, inspiring songs, moderate magic and combat ability.",
        "primary_stat": "Charisma",
        "starting_skills": ["Inspire", "Sleep Song", "Charm"],
        "stat_bonuses": {
            "charisma": 3,
            "dexterity": 2,
            "intelligence": 1,
            "constitution": -1
        },
        "special_abilities": ["Song Magic", "Jack of All Trades"],
        "mana_multiplier": 1.3,
        "health_multiplier": 1.0
    }
}

def get_class_description(class_name):
    """Get detailed description of a class"""
    if class_name in CLASSES:
        char_class = CLASSES[class_name]
        description = f"{char_class['description']}\n\n"
        description += f"Primary Stat: {char_class['primary_stat']}\n\n"
        description += "Starting Skills:\n"
        for skill in char_class['starting_skills']:
            description += f"- {skill}\n"
        description += "\nStat Modifiers:\n"
        for stat, modifier in char_class['stat_bonuses'].items():
            sign = "+" if modifier >= 0 else ""
            description += f"- {stat.title()}: {sign}{modifier}\n"
        description += f"\nHealth Multiplier: {char_class['health_multiplier']}x\n"
        description += f"Mana Multiplier: {char_class['mana_multiplier']}x\n"
        return description
    return "Unknown class"

def get_available_classes():
    """Get list of all available classes"""
    return list(CLASSES.keys())

def get_class_stat_bonus(class_name, stat):
    """Get the stat bonus for a specific class and stat"""
    if class_name in CLASSES and stat in CLASSES[class_name]['stat_bonuses']:
        return CLASSES[class_name]['stat_bonuses'][stat]
    return 0
