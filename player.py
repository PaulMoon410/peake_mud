"""
Player class for PyPeake MUD
Represents a player character with all their attributes and methods

Copyright (c) 2025 PyPeake MUD
Licensed under the MIT License - see LICENSE file for details
"""

from datetime import datetime
from races import RACES
from classes import CLASSES

class Player:
    def __init__(self, name, password_hash, race, char_class):
        self.name = name
        self.password_hash = password_hash
        self.race = race
        self.char_class = char_class
        self.level = 1
        self.experience = 0
        
        # Base attributes (will be modified by race/class bonuses)
        self.strength = 10
        self.dexterity = 10
        self.constitution = 10
        self.intelligence = 10
        self.wisdom = 10
        self.charisma = 10
        
        # Apply race bonuses
        self.apply_race_bonuses()
        
        # Apply class bonuses
        self.apply_class_bonuses()
        
        # Calculate derived stats
        self.max_health = self.constitution * 10 + 50
        self.health = self.max_health
        self.max_mana = self.intelligence * 5 + self.wisdom * 5 + 25
        self.mana = self.max_mana
        
        # Location and state
        self.location = "town_square"
        self.created_at = datetime.now().isoformat()
        self.last_login = datetime.now().isoformat()
    
    def apply_race_bonuses(self):
        """Apply racial attribute bonuses"""
        if self.race in RACES:
            race_data = RACES[self.race]
            for bonus in race_data.get('stat_bonuses', {}):
                if hasattr(self, bonus):
                    setattr(self, bonus, getattr(self, bonus) + race_data['stat_bonuses'][bonus])
    
    def apply_class_bonuses(self):
        """Apply class attribute bonuses"""
        if self.char_class in CLASSES:
            class_data = CLASSES[self.char_class]
            for bonus in class_data.get('stat_bonuses', {}):
                if hasattr(self, bonus):
                    setattr(self, bonus, getattr(self, bonus) + class_data['stat_bonuses'][bonus])
    
    def gain_experience(self, amount):
        """Add experience points and check for level up"""
        self.experience += amount
        
        # Simple level calculation (every 1000 exp = 1 level)
        new_level = (self.experience // 1000) + 1
        if new_level > self.level:
            self.level_up(new_level)
    
    def level_up(self, new_level):
        """Handle level up"""
        old_level = self.level
        self.level = new_level
        
        # Increase stats on level up
        health_increase = self.constitution * 2
        mana_increase = (self.intelligence + self.wisdom)
        
        self.max_health += health_increase
        self.max_mana += mana_increase
        self.health = self.max_health  # Full heal on level up
        self.mana = self.max_mana      # Full mana restore on level up
        
        return f"Congratulations! You've reached level {new_level}!"
    
    def take_damage(self, amount):
        """Apply damage to the player"""
        self.health = max(0, self.health - amount)
        return self.health <= 0  # Returns True if player dies
    
    def heal(self, amount):
        """Restore health points"""
        self.health = min(self.max_health, self.health + amount)
    
    def use_mana(self, amount):
        """Use mana points"""
        if self.mana >= amount:
            self.mana -= amount
            return True
        return False
    
    def restore_mana(self, amount):
        """Restore mana points"""
        self.mana = min(self.max_mana, self.mana + amount)
    
    def get_race_info(self):
        """Get information about the player's race"""
        return RACES.get(self.race, {})
    
    def get_class_info(self):
        """Get information about the player's class"""
        return CLASSES.get(self.char_class, {})
    
    def to_dict(self):
        """Convert player to dictionary for database storage"""
        return {
            'name': self.name,
            'password_hash': self.password_hash,
            'race': self.race,
            'char_class': self.char_class,
            'level': self.level,
            'experience': self.experience,
            'strength': self.strength,
            'dexterity': self.dexterity,
            'constitution': self.constitution,
            'intelligence': self.intelligence,
            'wisdom': self.wisdom,
            'charisma': self.charisma,
            'max_health': self.max_health,
            'health': self.health,
            'max_mana': self.max_mana,
            'mana': self.mana,
            'location': self.location,
            'created_at': self.created_at,
            'last_login': self.last_login
        }
    
    @classmethod
    def from_dict(cls, data):
        """Create player from dictionary (loaded from database)"""
        # Create player with basic info
        player = cls(data['name'], data['password_hash'], data['race'], data['char_class'])
        
        # Override with saved values
        player.level = data.get('level', 1)
        player.experience = data.get('experience', 0)
        player.strength = data.get('strength', 10)
        player.dexterity = data.get('dexterity', 10)
        player.constitution = data.get('constitution', 10)
        player.intelligence = data.get('intelligence', 10)
        player.wisdom = data.get('wisdom', 10)
        player.charisma = data.get('charisma', 10)
        player.max_health = data.get('max_health', 100)
        player.health = data.get('health', player.max_health)
        player.max_mana = data.get('max_mana', 50)
        player.mana = data.get('mana', player.max_mana)
        player.location = data.get('location', 'town_square')
        player.created_at = data.get('created_at', datetime.now().isoformat())
        player.last_login = datetime.now().isoformat()
        
        return player
    
    def __str__(self):
        return f"{self.name} (Level {self.level} {self.race} {self.char_class})"
