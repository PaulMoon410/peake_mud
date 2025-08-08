# PyPeake MUD

A simple Python Multi-User Dungeon (MUD) with login functionality, race selection, and class selection.

## Features

- **User Authentication**: Secure login system with password hashing
- **Character Creation**: Choose from 6 races and 8 character classes
- **Real-time Multiplayer**: Multiple players can connect simultaneously
- **Character Stats**: Full attribute system with race/class bonuses
- **Basic Commands**: Stats viewing, looking around, player communication
- **Persistent Data**: Player data saved to JSON database

## Races

- **Human**: Balanced and versatile
- **Elf**: Graceful with magical affinity
- **Dwarf**: Hardy and strong craftsmen
- **Halfling**: Small but lucky and nimble
- **Orc**: Powerful warriors
- **Gnome**: Intelligent magical tinkerers

## Classes

- **Warrior**: Melee combat master
- **Mage**: Arcane spellcaster
- **Rogue**: Stealthy assassin
- **Cleric**: Divine healer
- **Ranger**: Nature's guardian
- **Paladin**: Holy warrior
- **Barbarian**: Primal berserker
- **Bard**: Jack of all trades

## Installation

1. Clone or download the project
2. Ensure Python 3.6+ is installed
3. No additional dependencies required (uses only standard library)

## Running the Server

```bash
python mud_server.py
```

The server will start on `localhost:4000` by default.

## Connecting to the Game

### Option 1: Use the included client
```bash
python client.py
```

### Option 2: Use telnet
```bash
telnet localhost 4000
```

### Option 3: Use any MUD client
Connect to `localhost` port `4000`

## Basic Commands

Once logged in, you can use these commands:

- `stats` - View your character statistics
- `look` - Look around your current location
- `who` - See who else is online
- `say <message>` - Say something to other players
- `quit` - Leave the game

## File Structure

- `mud_server.py` - Main server application
- `player.py` - Player character class
- `races.py` - Race definitions and bonuses
- `classes.py` - Character class definitions
- `database.py` - JSON-based player data storage
- `client.py` - Simple telnet client
- `players.json` - Player database (created automatically)

## Character Creation Process

1. Connect to the server
2. Choose "Create New Character"
3. Enter a unique username (3+ characters)
4. Enter a password (4+ characters)
5. Select your race from the available options
6. Select your character class
7. Your character is created with stats based on race/class bonuses

## Player Stats

Each character has six core attributes:
- **Strength**: Physical power and melee damage
- **Dexterity**: Agility, speed, and ranged accuracy
- **Constitution**: Health and endurance
- **Intelligence**: Magical power and mana
- **Wisdom**: Divine magic and perception
- **Charisma**: Social skills and leadership

Derived stats:
- **Health**: Based on Constitution
- **Mana**: Based on Intelligence and Wisdom
- **Level**: Increases with experience

## Customization

The game is designed to be easily extensible:

- Add new races in `races.py`
- Add new classes in `classes.py`
- Modify stat bonuses and descriptions
- Extend the command system in `mud_server.py`
- Add new locations and game mechanics

## Technical Details

- **Networking**: TCP sockets with threading for multiple clients
- **Security**: SHA-256 password hashing
- **Data Storage**: JSON files for simplicity and portability
- **Client Handling**: Each client runs in its own thread
- **Error Handling**: Graceful disconnect handling

## Development Notes

This is a basic MUD framework that can be extended with:
- Combat system
- Item and inventory management
- Multiple rooms and areas
- NPCs and monsters
- Quests and storylines
- Guilds and player groups
- Economic system

## License

This project is open source and available for educational and personal use.
