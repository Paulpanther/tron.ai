from entity.player import Player


class AI(Player):

    def __init__(self, pos, field, name="Dummy AI"):
        super(AI, self).__init__(pos, field, name)

    def go(self):
        return 1
