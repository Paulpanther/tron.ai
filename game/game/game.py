import time

import config
from entity.player_two import PlayerTwo

from game.entity.player_one import PlayerOne


class Game(object):

    def __init__(self):
        self.size = config.width, config.height
        self.field = [[0 for x in range(self.size[0])] for y in range(self.size[1])]

        pos1 = (0, 0)
        pos2 = self.size[0] - 1, self.size[1] - 1

        self.player1 = PlayerOne(pos1, self.field)
        self.player2 = PlayerTwo(pos2, self.field)
        self.player1.enemy = self.player2
        self.player2.enemy = self.player1

        self.field[pos1[0]][pos1[1]] = 1
        self.field[pos2[0]][pos2[1]] = 2

        self.changes = []

    def update(self):
        self.changes = []
        # Get Player Direction

        p1_time = time.time()
        p1g = self.player1.go()
        p1_time = time.time() - p1_time

        p2_time = time.time()
        p2g = self.player2.go()
        p2_time = time.time() - p2_time

        if p1_time < p2_time:
            print "P1 AI is faster"
        elif p2_time > p1_time:
            print "P2 AI is faster"
        else:
            print "Will never happen anyway, but: Your exactly the same speed: 42"
        # Future Fields
        f1 = self.getField(p1g, self.player1.pos)
        f2 = self.getField(p2g, self.player2.pos)
        # Availability of future fields
        a1 = self.isAvailable(f1)
        a2 = self.isAvailable(f2)

        # Game Overs
        if not a1 and not a2:
            # Both dead
            return 3
        if not a1:
            # P1 dead
            return 2
        if not a2:
            # P2 dead
            return 1

        # Block future fields
        self.field[f1[0]][f1[1]] = 1
        self.field[f2[0]][f2[1]] = 2

        self.changes.extend([(self.player1.pos, f1), (self.player2.pos, f2)])

        # Update the positions and the field
        self.player1.pos = f1
        self.player1.field = self.field

        self.player2.pos = f2
        self.player2.field = self.field

        return False

    def getField(self, goto, current):
        """
        Returns future postiion, could be invalid
        :param goto:
        :param current:
        :return:
        """
        # Goto is direction
        # Current is position

        if goto == 0:
            return (current[0]+1, current[1])
        if goto == 1:
            return (current[0], current[1]+1)
        if goto == 2:
            return (current[0]-1, current[1])
        if goto == 3:
            return (current[0], current[1]-1)
        print "How?!: ", goto, current

    def isAvailable(self, f):
        """
        Checks if tile is valid and empty
        :param f:
        :return:
        """
        if f[0] >= len(self.field[0]) or f[1] >= len(self.field[1]) or f[0] < 0 or f[1] < 0:
            return False

        return self.field[f[0]][f[1]] == 0
