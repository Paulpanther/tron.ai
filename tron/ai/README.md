# AI-Directory
Drop your AI here to add them to the Game

## Structure
Your code has to be inside one folder with an arbitrary name.
The name should be similar to the name of your ai and has to be a valid python-package-name.
Inside the folder has to be an empty `__init__.py` file and a file called `ai.py`.
`ai.py` has to look like this:
```
from entity.player import Player


class AI(Player):

    def __init__(self, pos, field, name="Your AIs Name"):
        super(AI, self).__init__(pos, field, name)

    def go(self):
        # Your code goes here
        return # 0 or 1 or 2 or 3
```

## Rules
You are allowed to define new functions and classes, import other packages or files you made in your AIs directory.
You are not allowed to write any code that does things which are not part of the game.
Your code must not harm the host computer in any way or do anything which may not be in the interest of the
owner of the computer.
You are not allowed to gain advantage in the game by using game-data except the field, your position and position
of the other players.
**Play fair! This game is not about competition but about learning to use AI**