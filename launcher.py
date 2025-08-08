#!/usr/bin/env python3
"""
Game launcher and utility script for PyPeake MUD
Provides easy commands to start server, client, or manage database

Copyright (c) 2025 PyPeake MUD
Licensed under the MIT License - see LICENSE file for details
"""

import sys
import os
import subprocess
import argparse
from database import Database

def start_server(host='localhost', port=4000):
    """Start the MUD server"""
    print(f"Starting PyPeake MUD Server on {host}:{port}")
    os.system(f"python mud_server.py")

def start_client(host='localhost', port=4000):
    """Start the MUD client"""
    print(f"Connecting to PyPeake MUD at {host}:{port}")
    os.system(f"python client.py {host} {port}")

def show_stats():
    """Show database statistics"""
    db = Database()
    stats = db.export_player_stats()
    
    print("=== PyPeake MUD Statistics ===")
    print(f"Total Players: {stats['total_players']}")
    print(f"Average Level: {stats['average_level']:.1f}")
    
    print("\nRace Distribution:")
    for race, count in stats['races'].items():
        percentage = (count / stats['total_players']) * 100 if stats['total_players'] > 0 else 0
        print(f"  {race}: {count} ({percentage:.1f}%)")
    
    print("\nClass Distribution:")
    for char_class, count in stats['classes'].items():
        percentage = (count / stats['total_players']) * 100 if stats['total_players'] > 0 else 0
        print(f"  {char_class}: {count} ({percentage:.1f}%)")
    
    print("\nLevel Distribution:")
    for level_range, count in stats['level_distribution'].items():
        percentage = (count / stats['total_players']) * 100 if stats['total_players'] > 0 else 0
        print(f"  Level {level_range}: {count} ({percentage:.1f}%)")

def list_players():
    """List all players"""
    db = Database()
    players = db.get_all_players()
    
    if not players:
        print("No players found in database")
        return
    
    print("=== All Players ===")
    print(f"{'Name':<15} {'Race':<10} {'Class':<12} {'Level':<5} {'Created':<19}")
    print("-" * 70)
    
    for username, player_data in sorted(players.items()):
        name = player_data.get('name', username)
        race = player_data.get('race', 'Unknown')
        char_class = player_data.get('char_class', 'Unknown')
        level = player_data.get('level', 1)
        created = player_data.get('created_at', 'Unknown')[:19]  # Trim to date/time only
        
        print(f"{name:<15} {race:<10} {char_class:<12} {level:<5} {created:<19}")

def backup_database():
    """Create a backup of the player database"""
    import shutil
    from datetime import datetime
    
    if not os.path.exists('players.json'):
        print("No player database found to backup")
        return
    
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    backup_filename = f"players_backup_{timestamp}.json"
    
    shutil.copy2('players.json', backup_filename)
    print(f"Database backed up to: {backup_filename}")

def main():
    """Main launcher function"""
    parser = argparse.ArgumentParser(description='PyPeake MUD Launcher')
    parser.add_argument('command', choices=['server', 'client', 'stats', 'players', 'backup'], 
                       help='Command to execute')
    parser.add_argument('--host', default='localhost', help='Server host (default: localhost)')
    parser.add_argument('--port', type=int, default=4000, help='Server port (default: 4000)')
    
    args = parser.parse_args()
    
    if args.command == 'server':
        start_server(args.host, args.port)
    elif args.command == 'client':
        start_client(args.host, args.port)
    elif args.command == 'stats':
        show_stats()
    elif args.command == 'players':
        list_players()
    elif args.command == 'backup':
        backup_database()

if __name__ == "__main__":
    if len(sys.argv) == 1:
        print("PyPeake MUD Launcher")
        print("\nUsage:")
        print("  python launcher.py server    - Start the MUD server")
        print("  python launcher.py client    - Connect as a client")
        print("  python launcher.py stats     - Show database statistics")
        print("  python launcher.py players   - List all players")
        print("  python launcher.py backup    - Backup player database")
        print("\nOptions:")
        print("  --host HOST    Server hostname (default: localhost)")
        print("  --port PORT    Server port (default: 4000)")
        print("\nExamples:")
        print("  python launcher.py server")
        print("  python launcher.py client --host 192.168.1.100 --port 4000")
    else:
        main()
