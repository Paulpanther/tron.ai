class Player(object):

    def __init__(self, pos, field, name="Unnamed"):
        self.pos = pos
        self.field = field
        self.enemies = []
        self.name = name

    def go(self):
        return 0
