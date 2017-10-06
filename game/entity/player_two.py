from player import Player

from game.ai1 import ai2


class PlayerTwo(Player):

    name = "Tim"

    def __init__(self, pos, field):
        super(PlayerTwo, self).__init__(pos, field)

    def go(self):
        direction = ai2.calculate(self.pos, self.field, self.enemy.pos)
        return direction
