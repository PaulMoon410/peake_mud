"""
Database module for PyPeake MUD
Simple JSON-based player data storage

Copyright (c) 2025 PyPeake MUD
Licensed under the MIT License - see LICENSE file for details
"""

import json
import os
from datetime import datetime

class Database:
    def __init__(self, db_file="players.json"):
        self.db_file = db_file
        self.players = {}
        self.load_players()
    
    def load_players(self):
        """Load player data from JSON file"""
        if os.path.exists(self.db_file):
            try:
                with open(self.db_file, 'r') as f:
                    self.players = json.load(f)
                print(f"Loaded {len(self.players)} players from database")
            except (json.JSONDecodeError, IOError) as e:
                print(f"Error loading player database: {e}")
                self.players = {}
        else:
            print("No existing player database found, creating new one")
            self.players = {}
    
    def save_players(self):
        """Save all player data to JSON file"""
        try:
            # Create backup of existing file
            if os.path.exists(self.db_file):
                backup_file = f"{self.db_file}.backup"
                os.rename(self.db_file, backup_file)
            
            with open(self.db_file, 'w') as f:
                json.dump(self.players, f, indent=2)
            
            # Remove backup if save was successful
            backup_file = f"{self.db_file}.backup"
            if os.path.exists(backup_file):
                os.remove(backup_file)
                
        except IOError as e:
            print(f"Error saving player database: {e}")
            # Restore backup if save failed
            backup_file = f"{self.db_file}.backup"
            if os.path.exists(backup_file):
                os.rename(backup_file, self.db_file)
    
    def get_player(self, username):
        """Get player data by username"""
        return self.players.get(username.lower())
    
    def save_player(self, player_data):
        """Save or update a player's data"""
        username = player_data['name'].lower()
        player_data['last_saved'] = datetime.now().isoformat()
        self.players[username] = player_data
        self.save_players()
        print(f"Player {player_data['name']} saved to database")
    
    def delete_player(self, username):
        """Delete a player from the database"""
        username = username.lower()
        if username in self.players:
            del self.players[username]
            self.save_players()
            return True
        return False
    
    def player_exists(self, username):
        """Check if a player exists in the database"""
        return username.lower() in self.players
    
    def get_all_players(self):
        """Get all player data"""
        return self.players
    
    def get_player_count(self):
        """Get total number of players"""
        return len(self.players)
    
    def get_players_by_level(self, min_level=None, max_level=None):
        """Get players within a level range"""
        filtered_players = {}
        for username, player_data in self.players.items():
            level = player_data.get('level', 1)
            if min_level is not None and level < min_level:
                continue
            if max_level is not None and level > max_level:
                continue
            filtered_players[username] = player_data
        return filtered_players
    
    def get_top_players(self, limit=10, sort_by='level'):
        """Get top players sorted by specified criteria"""
        players_list = list(self.players.items())
        
        if sort_by == 'level':
            players_list.sort(key=lambda x: x[1].get('level', 1), reverse=True)
        elif sort_by == 'experience':
            players_list.sort(key=lambda x: x[1].get('experience', 0), reverse=True)
        elif sort_by == 'created_at':
            players_list.sort(key=lambda x: x[1].get('created_at', ''), reverse=True)
        
        return dict(players_list[:limit])
    
    def cleanup_old_players(self, days_inactive=30):
        """Remove players who haven't logged in for specified days"""
        from datetime import datetime, timedelta
        
        cutoff_date = datetime.now() - timedelta(days=days_inactive)
        players_to_remove = []
        
        for username, player_data in self.players.items():
            last_login = player_data.get('last_login', '')
            if last_login:
                try:
                    login_date = datetime.fromisoformat(last_login)
                    if login_date < cutoff_date:
                        players_to_remove.append(username)
                except ValueError:
                    # Invalid date format, consider for removal
                    players_to_remove.append(username)
        
        for username in players_to_remove:
            del self.players[username]
        
        if players_to_remove:
            self.save_players()
            print(f"Removed {len(players_to_remove)} inactive players")
        
        return len(players_to_remove)
    
    def export_player_stats(self):
        """Export basic statistics about players"""
        stats = {
            'total_players': len(self.players),
            'races': {},
            'classes': {},
            'level_distribution': {},
            'average_level': 0
        }
        
        total_level = 0
        for player_data in self.players.values():
            # Race stats
            race = player_data.get('race', 'Unknown')
            stats['races'][race] = stats['races'].get(race, 0) + 1
            
            # Class stats
            char_class = player_data.get('char_class', 'Unknown')
            stats['classes'][char_class] = stats['classes'].get(char_class, 0) + 1
            
            # Level stats
            level = player_data.get('level', 1)
            total_level += level
            level_range = f"{(level-1)//5*5+1}-{(level-1)//5*5+5}"
            stats['level_distribution'][level_range] = stats['level_distribution'].get(level_range, 0) + 1
        
        if len(self.players) > 0:
            stats['average_level'] = total_level / len(self.players)
        
        return stats
