import pygame

import config


class View(object):
    def __init__(self, game, title="Tron", bg_color=config.colors[0]):
        self.game = game
        self.gamestate = None

        width = config.width * config.CELL_SIZE[0]
        height = config.height * config.CELL_SIZE[1]
        self.res = width, height

        self.title = title
        self.bg_color = bg_color

        self.screen = pygame.display.set_mode(self.res)
        pygame.display.set_caption(self.title)

        self.background = pygame.Surface(self.screen.get_size())
        self.background.fill(self.bg_color)
        self.background.convert()

        self.screen.blit(self.background, (0, 0))
        self.clock = pygame.time.Clock()
        self.FPS = 60
        self.playtime = 0.0

        self.running = False

    def start(self):
        first_render = True

        self.running = True

        while self.running:

            for e in pygame.event.get():
                if e.type == pygame.QUIT:
                    self.running = False
                if e.type == pygame.KEYUP:
                    if e.key == pygame.K_ESCAPE:
                        pygame.event.post(pygame.event.Event(pygame.QUIT))

            # Update
            if first_render:
                # Draw init cells first
                self.draw_cells()

            else:
                self.gamestate = self.game.update()
                if self.gamestate is not False:
                    self.running = False

            # Render
            self.draw_cells()

            pygame.display.flip()
            first_render = False

        self.end(self.gamestate)

    def draw_cells(self):
        for c in self.game.changes:
            f, t = c  # f = from, t = to
            rect = pygame.Rect((t[0] * config.CELL_SIZE[0], t[1] * config.CELL_SIZE[1]), config.CELL_SIZE)
            value = self.game.field[t[0]][t[1]]
            pygame.draw.rect(self.screen, config.colors[value%len(config.colors)], rect, 0)

            pygame.draw.line(self.screen,
                             config.colors[0],
                             ((f[0] + .5) * config.CELL_SIZE[0], (f[1] + .5) * config.CELL_SIZE[1]),
                             ((t[0] + .5) * config.CELL_SIZE[0], (t[1] + .5) * config.CELL_SIZE[1]))

    def end(self, dead):
        """ Terminates the View and prints the winners

        :param dead: All player with their dead time
        :return: None
        """

        # Terminate the View
        self.running = False

        # Print Winners
        print("Game ended\n\nThe Winners:")
        for n, tick in enumerate(sorted(dead.iterkeys())):
            players = dead[tick]

            # Prepare player names
            player_names = ''
            for player in players:
                player_names += player.name + ', '
            player_names = player_names[:-2]

            print('{}.: {} at tick {}'.format(n+1, player_names, str(tick)))
        print('')

        # TODO change view, so window does not close when game is finished
        raw_input("Press Enter to end tron.ai")
