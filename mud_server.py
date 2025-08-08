#!/usr/bin/env python3
"""
PyPeake MUD Server
A simple Python MUD with login, race, and class selection

Copyright (c) 2025 PyPeake MUD
Licensed under the MIT License - see LICENSE file for details
"""

import socket
import threading
import json
import hashlib
import os
from datetime import datetime
from player import Player
from races import RACES
from classes import CLASSES
from database import Database

class MUDServer:
    def __init__(self, host='localhost', port=4000):
        self.host = host
        self.port = port
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.players = {}  # Connected players
        self.db = Database()
        
    def start_server(self):
        """Start the MUD server"""
        self.socket.bind((self.host, self.port))
        self.socket.listen(5)
        print(f"PyPeake MUD Server started on {self.host}:{self.port}")
        print("Waiting for connections...")
        
        try:
            while True:
                client_socket, address = self.socket.accept()
                print(f"New connection from {address}")
                
                # Create a new thread for each client
                client_thread = threading.Thread(
                    target=self.handle_client,
                    args=(client_socket, address)
                )
                client_thread.daemon = True
                client_thread.start()
                
        except KeyboardInterrupt:
            print("\nShutting down server...")
            self.socket.close()
    
    def handle_client(self, client_socket, address):
        """Handle individual client connections"""
        try:
            self.send_welcome(client_socket)
            player = self.login_process(client_socket)
            
            if player:
                self.players[client_socket] = player
                self.send_message(client_socket, f"Welcome to PyPeake, {player.name}!")
                self.game_loop(client_socket, player)
            
        except Exception as e:
            print(f"Error handling client {address}: {e}")
        finally:
            if client_socket in self.players:
                player = self.players[client_socket]
                print(f"Player {player.name} disconnected")
                del self.players[client_socket]
            client_socket.close()
    
    def send_welcome(self, client_socket):
        """Send welcome message to new connections"""
        welcome_msg = """
╔══════════════════════════════════════╗
║           Welcome to PyPeake         ║
║        A Python Text Adventure       ║
╚══════════════════════════════════════╝

Choose an option:
1. Login
2. Create New Character
3. Quit

Enter your choice (1-3): """
        
        self.send_message(client_socket, welcome_msg)
    
    def login_process(self, client_socket):
        """Handle the login process"""
        while True:
            try:
                response = self.receive_message(client_socket).strip()
                
                if response == '1':
                    return self.login_existing_player(client_socket)
                elif response == '2':
                    return self.create_new_player(client_socket)
                elif response == '3':
                    self.send_message(client_socket, "Goodbye!")
                    return None
                else:
                    self.send_message(client_socket, "Invalid choice. Please enter 1, 2, or 3: ")
                    
            except:
                return None
    
    def login_existing_player(self, client_socket):
        """Handle existing player login"""
        self.send_message(client_socket, "Username: ")
        username = self.receive_message(client_socket).strip()
        
        self.send_message(client_socket, "Password: ")
        password = self.receive_message(client_socket).strip()
        
        player_data = self.db.get_player(username)
        if player_data and self.verify_password(password, player_data['password_hash']):
            player = Player.from_dict(player_data)
            self.send_message(client_socket, f"Login successful! Welcome back, {player.name}.")
            return player
        else:
            self.send_message(client_socket, "Invalid username or password. Returning to main menu...\n")
            self.send_welcome(client_socket)
            return None
    
    def create_new_player(self, client_socket):
        """Handle new player creation"""
        # Get username
        while True:
            self.send_message(client_socket, "Enter desired username: ")
            username = self.receive_message(client_socket).strip()
            
            if len(username) < 3:
                self.send_message(client_socket, "Username must be at least 3 characters long.\n")
                continue
            
            if self.db.get_player(username):
                self.send_message(client_socket, "Username already exists. Please choose another.\n")
                continue
            
            break
        
        # Get password
        while True:
            self.send_message(client_socket, "Enter password: ")
            password = self.receive_message(client_socket).strip()
            
            if len(password) < 4:
                self.send_message(client_socket, "Password must be at least 4 characters long.\n")
                continue
            
            self.send_message(client_socket, "Confirm password: ")
            confirm_password = self.receive_message(client_socket).strip()
            
            if password != confirm_password:
                self.send_message(client_socket, "Passwords don't match. Please try again.\n")
                continue
            
            break
        
        # Race selection
        race = self.select_race(client_socket)
        if not race:
            return None
        
        # Class selection
        char_class = self.select_class(client_socket)
        if not char_class:
            return None
        
        # Create the player
        password_hash = self.hash_password(password)
        player = Player(username, password_hash, race, char_class)
        
        # Save to database
        self.db.save_player(player.to_dict())
        
        self.send_message(client_socket, f"\nCharacter created successfully!")
        self.send_message(client_socket, f"Name: {player.name}")
        self.send_message(client_socket, f"Race: {player.race}")
        self.send_message(client_socket, f"Class: {player.char_class}")
        self.send_message(client_socket, f"Health: {player.health}/{player.max_health}")
        self.send_message(client_socket, f"Mana: {player.mana}/{player.max_mana}")
        
        return player
    
    def select_race(self, client_socket):
        """Handle race selection"""
        while True:
            race_list = "\n=== Choose Your Race ===\n"
            for i, (race_name, race_data) in enumerate(RACES.items(), 1):
                race_list += f"{i}. {race_name}\n"
                race_list += f"   Description: {race_data['description']}\n"
                race_list += f"   Bonuses: {', '.join(race_data['bonuses'])}\n\n"
            
            race_list += "Enter your choice (1-{}): ".format(len(RACES))
            self.send_message(client_socket, race_list)
            
            try:
                choice = int(self.receive_message(client_socket).strip())
                if 1 <= choice <= len(RACES):
                    race_name = list(RACES.keys())[choice - 1]
                    return race_name
                else:
                    self.send_message(client_socket, "Invalid choice. Please try again.\n")
            except ValueError:
                self.send_message(client_socket, "Please enter a valid number.\n")
            except:
                return None
    
    def select_class(self, client_socket):
        """Handle class selection"""
        while True:
            class_list = "\n=== Choose Your Class ===\n"
            for i, (class_name, class_data) in enumerate(CLASSES.items(), 1):
                class_list += f"{i}. {class_name}\n"
                class_list += f"   Description: {class_data['description']}\n"
                class_list += f"   Primary Stat: {class_data['primary_stat']}\n"
                class_list += f"   Starting Skills: {', '.join(class_data['starting_skills'])}\n\n"
            
            class_list += "Enter your choice (1-{}): ".format(len(CLASSES))
            self.send_message(client_socket, class_list)
            
            try:
                choice = int(self.receive_message(client_socket).strip())
                if 1 <= choice <= len(CLASSES):
                    class_name = list(CLASSES.keys())[choice - 1]
                    return class_name
                else:
                    self.send_message(client_socket, "Invalid choice. Please try again.\n")
            except ValueError:
                self.send_message(client_socket, "Please enter a valid number.\n")
            except:
                return None
    
    def game_loop(self, client_socket, player):
        """Main game loop for connected players"""
        self.send_message(client_socket, "\n=== Game Commands ===")
        self.send_message(client_socket, "- stats: View your character stats")
        self.send_message(client_socket, "- look: Look around your current location")
        self.send_message(client_socket, "- who: See who else is online")
        self.send_message(client_socket, "- say <message>: Say something to other players")
        self.send_message(client_socket, "- quit: Leave the game")
        self.send_message(client_socket, "\nYou are standing in the Town Square.")
        self.send_message(client_socket, "> ")
        
        while True:
            try:
                command = self.receive_message(client_socket).strip().lower()
                
                if not command:
                    continue
                
                if command == 'quit':
                    self.send_message(client_socket, "Goodbye!")
                    break
                elif command == 'stats':
                    self.show_stats(client_socket, player)
                elif command == 'look':
                    self.look_around(client_socket, player)
                elif command == 'who':
                    self.show_online_players(client_socket)
                elif command.startswith('say '):
                    message = command[4:]
                    self.broadcast_say(client_socket, player, message)
                else:
                    self.send_message(client_socket, "Unknown command. Type 'quit' to leave.")
                
                self.send_message(client_socket, "> ")
                
            except:
                break
    
    def show_stats(self, client_socket, player):
        """Display player stats"""
        stats = f"""
=== Character Stats ===
Name: {player.name}
Race: {player.race}
Class: {player.char_class}
Level: {player.level}

Health: {player.health}/{player.max_health}
Mana: {player.mana}/{player.max_mana}

Attributes:
- Strength: {player.strength}
- Dexterity: {player.dexterity}
- Constitution: {player.constitution}
- Intelligence: {player.intelligence}
- Wisdom: {player.wisdom}
- Charisma: {player.charisma}

Experience: {player.experience}
"""
        self.send_message(client_socket, stats)
    
    def look_around(self, client_socket, player):
        """Show current location description"""
        description = """
You are standing in the Town Square of PyPeake.
A bustling center of activity with merchants, adventurers, and townsfolk.
To the north lies the Great Forest, to the south the Rolling Hills.
The Adventurer's Guild stands prominently to the east.
"""
        self.send_message(client_socket, description)
    
    def show_online_players(self, client_socket):
        """Show list of online players"""
        if not self.players:
            self.send_message(client_socket, "No other players are currently online.")
            return
        
        player_list = "=== Online Players ===\n"
        for socket, player in self.players.items():
            if socket != client_socket:
                player_list += f"- {player.name} (Level {player.level} {player.race} {player.char_class})\n"
        
        if player_list == "=== Online Players ===\n":
            player_list += "No other players are currently online."
        
        self.send_message(client_socket, player_list)
    
    def broadcast_say(self, sender_socket, sender_player, message):
        """Broadcast a say message to all players in the area"""
        say_message = f"{sender_player.name} says: {message}"
        
        for socket, player in self.players.items():
            if socket != sender_socket:
                self.send_message(socket, say_message)
        
        self.send_message(sender_socket, f"You say: {message}")
    
    def send_message(self, client_socket, message):
        """Send a message to a client"""
        try:
            client_socket.send((message + '\n').encode('utf-8'))
        except:
            pass
    
    def receive_message(self, client_socket):
        """Receive a message from a client"""
        return client_socket.recv(1024).decode('utf-8').strip()
    
    def hash_password(self, password):
        """Hash a password for secure storage"""
        return hashlib.sha256(password.encode()).hexdigest()
    
    def verify_password(self, password, hash_value):
        """Verify a password against its hash"""
        return hashlib.sha256(password.encode()).hexdigest() == hash_value

if __name__ == "__main__":
    server = MUDServer()
    try:
        server.start_server()
    except KeyboardInterrupt:
        print("\nServer stopped by user")
