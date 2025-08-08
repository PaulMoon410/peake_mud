#!/usr/bin/env python3
"""
Simple Telnet Client for PyPeake MUD
Connect to the MUD server using telnet
"""

import socket
import threading
import sys

class MUDClient:
    def __init__(self, host='localhost', port=4000):
        self.host = host
        self.port = port
        self.socket = None
        self.connected = False
    
    def connect(self):
        """Connect to the MUD server"""
        try:
            self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.socket.connect((self.host, self.port))
            self.connected = True
            print(f"Connected to PyPeake MUD at {self.host}:{self.port}")
            return True
        except Exception as e:
            print(f"Failed to connect: {e}")
            return False
    
    def disconnect(self):
        """Disconnect from the server"""
        self.connected = False
        if self.socket:
            self.socket.close()
        print("Disconnected from server")
    
    def send_message(self, message):
        """Send a message to the server"""
        try:
            self.socket.send((message + '\n').encode('utf-8'))
        except Exception as e:
            print(f"Error sending message: {e}")
            self.connected = False
    
    def receive_messages(self):
        """Receive messages from the server"""
        while self.connected:
            try:
                data = self.socket.recv(1024)
                if not data:
                    break
                message = data.decode('utf-8')
                print(message, end='')
            except Exception as e:
                if self.connected:
                    print(f"Error receiving message: {e}")
                break
        self.connected = False
    
    def start(self):
        """Start the client"""
        if not self.connect():
            return
        
        # Start receiving messages in a separate thread
        receive_thread = threading.Thread(target=self.receive_messages)
        receive_thread.daemon = True
        receive_thread.start()
        
        # Main input loop
        try:
            while self.connected:
                user_input = input()
                if not self.connected:
                    break
                self.send_message(user_input)
        except KeyboardInterrupt:
            print("\nDisconnecting...")
        except EOFError:
            print("\nConnection closed")
        finally:
            self.disconnect()

if __name__ == "__main__":
    # Allow command line arguments for host and port
    host = 'localhost'
    port = 4000
    
    if len(sys.argv) >= 2:
        host = sys.argv[1]
    if len(sys.argv) >= 3:
        try:
            port = int(sys.argv[2])
        except ValueError:
            print("Invalid port number")
            sys.exit(1)
    
    client = MUDClient(host, port)
    client.start()
