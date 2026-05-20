# CS2 Custom Sounds
I found a [repository](https://github.com/zzhabib/CS-Jukebox) for Counter-Strike 2 which allows users to play custom sounds upon certain in game events.  This project only seems to work for Windows, so I made my own cross platform version in Python.  The program uses Valve's [game state integration](https://developer.valvesoftware.com/wiki/Counter-Strike:_Global_Offensive_Game_State_Integration) which lets CS2 send requests tracking in game events.  Therefore, the program is VAC safe.

Demo video showing custom killsound and mvp sound:

https://github.com/user-attachments/assets/7b41de0a-fe96-443f-ae05-4d7cf08ad91c

## Features

Currently, sounds can be added for the following events:
* Player kills
* Player deaths
* Round win
* Round win (mvp)
* Round loss

## Setup

### Requirements

Python, playsound3

```
pip install playsound3
```

### Game State Integration

Copy the file named `gamestate_integration_consolesample.cfg` to this location:

```
Steam/steamapps/common/Counter-Strike Global Offensive/game/csgo/cfg/
```

### Port Configuration

Inside `config.py` modify `PORT` to the port number you wish to use for the GSI server.  Make sure the `.cfg` file has the same port number.  The default port is 4000.

### Sound Configuration

Inside `config.py` modify the sound variables with the path of the file you wish to play upon certain in game events.  Since `playsound3` is used, `.wav` and `.mp3` files are allowed.  Also since `playsound3` is used, this program cannot adjust volume and you must adjust the volume inside the file directly.

## Usage

Run the program:

```
python3 main.py
```

Then start CS2.
