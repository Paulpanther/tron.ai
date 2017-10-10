import copy
import time

import config


class Game(object):

    def __init__(self, ai):

        # Get Size of field
        self.size = config.width, config.height

        # Init field
        # self.field = [[[0] * self.size[0]] * self.size[1]] # Does not work because first list is passed by reference
        self.field = [[0 for y in range(self.size[0])] for x in range(self.size[1])]

        # Calc distance between players
        # Players all start at y = 0
        distance = self.size[0] / len(ai)

        # Set positions
        pos = [(distance*i, 0) for i in range(len(ai))]

        # Init field (Set player)
        for n, p in enumerate(pos):
            self.field[p[0]][p[1]] = n+1

        # Init players with position and field
        self.players = [pai.AI(pos[n], self.field) for n, pai in enumerate(ai)]

        # Set enemy-position
        for n, player in enumerate(self.players):
            enemies = copy.deepcopy(pos)
            enemies.pop(n)
            player.enemies = enemies

        # Average response time
        self.response_times = [False] * len(ai)

        # Current ticks
        self.ticks = 0

        # List of dead players [player, dead_tick]
        self.dead = {}

        # Changes made in Game#update()
        # Required for View
        self.changes = [((p[0], p[1]-1), p) for p in pos]

    def update(self):
        """ Updates the Game

        Lets the players calculate their new position.
        The positions get set if they are available.
        If a player returns a cell which is not available, the player dies

        :return: The dead players if all players are dead, else False
        """

        self.changes = []

        for n, player in enumerate(self.players):

            # Check if player is deadsac
            if self.is_dead(player):
                continue

            # Calc response time
            player_time = time.time()

            # Let player calculate direction to go
            player_dir = player.go()

            # Add time to average
            player_time = time.time() - player_time
            self.calc_average(player_time, n)

            # Get future cell
            player_cell = get_cell(player_dir, player.pos)

            # Check if cell is available
            if not is_available(player_cell, self.field):
                # Kill player
                self.kill_player(player)
            else:
                # Block next cell
                self.field[player_cell[0]][player_cell[1]] = n+1
                self.changes.append([player.pos, player_cell])

                # Update player position and field
                player.pos = player_cell
                player.field = self.field

        # Return dead players if all are dead
        if len(self.dead) == len(self.players):
            return self.dead

        self.ticks += 1
        return False

    def is_dead(self, player):
        """ Checks if player is in dead-list

        :param player: The player to check
        :return: True if Game#dead contains player else False
        """

        for tick, dead_player in self.dead.iteritems():
            if player in dead_player:
                return True
        return False

    def kill_player(self, player):
        """ Adds the player to the dead-list and notices the tick

        :param player: The player to kill
        :return: None
        """

        if self.ticks in self.dead:
            self.dead[self.ticks].append(player)
        else:
            self.dead[self.ticks] = [player]

    def calc_average(self, player_time, n):
        """ Calculates the average response time

        :param player_time: The time the player needed to response
        :param n: The player index
        :return: None
        """

        if not self.response_times[n]:
            self.response_times[n] = player_time
        else:
            self.response_times[n] = (self.response_times[n] + player_time) / 2.


def get_cell(direction, current):
    """ Returns future position, could be invalid

    Allowed directions are: 0 (East), 1 (South), 2 (West), 3 (North)

    :param direction: The direction in which the player wants to go
    :param current: The current position of the player
    :return: The next cell the player will go to
    """

    if direction == 0:
        return current[0]+1, current[1]
    if direction == 1:
        return current[0], current[1]+1
    if direction == 2:
        return current[0]-1, current[1]
    if direction == 3:
        return current[0], current[1]-1
    raise ValueError('Invalid direction: {}. Allowed directions are: 0, 1, 2, 3'.format(direction))


def is_available(cell, field):
    """ Checks if cell is valid and empty
    :param cell: The cell to check
    :param field: The field where to check
    :return: True if the cell is available else False
    """

    if cell[0] >= len(field[0]) or \
            cell[1] >= len(field) or \
            cell[0] < 0 or cell[1] < 0:
        return False

    return field[cell[0]][cell[1]] == 0
