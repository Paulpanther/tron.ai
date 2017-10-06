from player import Player

from game.ai1 import ai1


class PlayerOne(Player):

    def __init__(self, pos, field):
        super(PlayerOne, self).__init__(pos, field)

    def go(self):
        direction = ai1.calculate(self.pos, self.field, self.enemy.pos)
        return direction
