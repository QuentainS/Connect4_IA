# Connect4 for AI

## Goal of this project

The idea is to provide a simple game with a client/server structure possibility. Anyone can develop an AI and try defeat the others. You can also easily run the game locally (e.g. to train a learning model). Each game is saved into a pickle file, in order to provide an easy and simple way to generate datasets.

## How to play

To start playing the game and create your own AI, you only have to modify the bot.py file. This file contains the "compute_move()" function, used to send order to the game.

Once your best algorithm implemented, you can run the client by running the client.py file. This file is by default setup to work on localhost. To setup a specific server ip, TODO

### Example

As an example, if you want to run the script locally, you only have to run the server :

```bash
python3 server.py
```

and then, your run the two clients by doing this twice :

```bash
python3 bot.py
```

### Game data structure

To start, the only big information to understand is the game data structure. In fact, your client will receive the current state of the game at each turn. All of theses states are sent to your AI implementation as the "history" variables.

Here is an exemple :
