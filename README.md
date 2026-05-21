# CS2 Custom Sounds
I found a [repository](https://github.com/zzhabib/CS-Jukebox) for Counter-Strike 2 which allows users to play custom sounds upon certain in game events.  This project only seems to work for Windows, so I made my own cross platform version in Python.  The program uses Valve's [game state integration](https://developer.valvesoftware.com/wiki/Counter-Strike:_Global_Offensive_Game_State_Integration) which lets CS2 send requests tracking in game events.  Therefore, the program is VAC safe.

Demo video showing custom killsound, mvp sound, and round start sound:

https://github.com/user-attachments/assets/b7b9b280-c522-4c0c-a0ab-a1457323c3b7

## Features

Currently, sounds can be added for the following events:
* Player kills
* Player deaths
* Round win
* Round win (mvp)
* Round loss
* Freeze time
* Round start
* Bomb planted
* Round 10 second warning (via round start)
* Bomb 10 second warning (via bomb planted)

The round start and bomb planted sounds play at the beginning of the round and when the bomb is planted respectively.  Knowing the round time and bomb time allows for playing a sound when the time is almost up.  For example, to achieve a 10 seconds left sound on the bomb, create a sound file with 30 seconds of blank space at the beginning.

## Setup

### Requirements

Python, pygame

```
pip install pygame
```

### Game State Integration

Copy the file named `gamestate_integration_consolesample.cfg` to this location:

```
Steam/steamapps/common/Counter-Strike Global Offensive/game/csgo/cfg/gamestate_integration_consolesample.cfg
```

### Port Configuration

Inside `config.py` modify `PORT` to the port number you wish to use for the GSI server.  Make sure the `.cfg` file has the same port number.  The default port is 4000.

### Sound Configuration

Inside `config.py` modify the sound variables with the path of the file you wish to play upon certain in game events.  Since `pygame` is used, `.wav` and `.ogg` files are allowed.  Volume can be configured in the config.

## Usage

Run the program:

```
python3 main.py
```

Then start CS2.  The program can also be restarted while the game is running.  Note that sounds might not play on the first round.
