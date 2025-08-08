#!/usr/bin/env python3
"""
Test script for PyPeake MUD components
"""

from player import Player
from races import RACES, get_race_description
from classes import CLASSES, get_class_description
from database import Database
import os

def test_races():
    """Test race system"""
    print("=== Testing Races ===")
    for race_name in RACES:
        print(f"Race: {race_name}")
        description = get_race_description(race_name)
        print(description[:100] + "...\n")

def test_classes():
    """Test class system"""
    print("=== Testing Classes ===")
    for class_name in CLASSES:
        print(f"Class: {class_name}")
        description = get_class_description(class_name)
        print(description[:100] + "...\n")

def test_player_creation():
    """Test player creation"""
    print("=== Testing Player Creation ===")
    
    # Create a test player
    player = Player("TestWarrior", "test_hash", "Human", "Warrior")
    print(f"Created: {player}")
    print(f"Health: {player.health}/{player.max_health}")
    print(f"Mana: {player.mana}/{player.max_mana}")
    print(f"Strength: {player.strength}")
    
    # Test level up
    player.gain_experience(1500)
    print(f"After gaining 1500 exp - Level: {player.level}")

def test_database():
    """Test database operations"""
    print("=== Testing Database ===")
    
    # Create test database file
    test_db = Database("test_players.json")
    
    # Create and save a test player
    player = Player("TestPlayer", "password_hash", "Elf", "Mage")
    test_db.save_player(player.to_dict())
    
    # Load the player back
    loaded_data = test_db.get_player("TestPlayer")
    if loaded_data:
        loaded_player = Player.from_dict(loaded_data)
        print(f"Successfully loaded: {loaded_player}")
    
    # Clean up
    if os.path.exists("test_players.json"):
        os.remove("test_players.json")
    print("Database test completed")

if __name__ == "__main__":
    print("PyPeake MUD Component Tests\n")
    
    test_races()
    test_classes()
    test_player_creation()
    test_database()
    
    print("All tests completed successfully!")
