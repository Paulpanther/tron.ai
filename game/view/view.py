import pygame

from game import config


class View(object):
    def __init__(self, game, title="Tron", bg_color=(255, 255, 255)):
        self.game = game
        self.gamestate = None

        width = config.width * config.TILE_SIZE[0]
        height = config.height * config.TILE_SIZE[1]
        self.res = width, height

        self.title = title
        self.bg_color = bg_color

        self.screen = pygame.display.set_mode(self.res)
        pygame.display.set_caption(self.title)

        self.background = pygame.Surface(self.screen.get_size())
        self.background.fill(self.bg_color)
        self.background.convert()

        self.screen.blit(self.background, (0,0))
        self.clock = pygame.time.Clock()
        self.FPS = 60
        self.playtime = 0.0

        self.running = False

    def start(self):
        first_render = True

        self.running = True
        while self.running:
            milliseconds = self.clock.tick(self.FPS)
            seconds = milliseconds / 1000.0

            for e in pygame.event.get():
                if e.type == pygame.QUIT:
                    self.running = False
                if e.type == pygame.KEYUP:
                    if e.key == pygame.K_ESCAPE:
                        pygame.event.post(pygame.event.Event(pygame.QUIT))

            # Update
            if not first_render:
                self.gamestate = self.game.update()
                if self.gamestate is not False:
                    self.running = False

            # Render
            # self.screen.blit(self.background, (0, 0))
            for c in self.game.changes:
                f, t = c  # f = from, t = to
                rect = pygame.Rect((t[0] * config.TILE_SIZE[0], t[1] * config.TILE_SIZE[1]), config.TILE_SIZE)
                value = self.game.field[t[0]][t[1]]
                pygame.draw.rect(self.screen, config.colors[value], rect, 0)

                pygame.draw.line(self.screen,
                                 (255, 255, 255),
                                 ((f[0] + 0.5) * config.TILE_SIZE[0], (f[1] + 0.5) * config.TILE_SIZE[1]),
                                 ((t[0] + 0.5) * config.TILE_SIZE[0], (t[1] + 0.5) * config.TILE_SIZE[1]))



            pygame.display.flip()
            first_render = False

        self.end(self.gamestate)

    def end(self, winner):
        self.running = False
        if winner == 0:
            pass
        elif winner == 1:
            print self.game.player1.name, "won the game"
        elif winner == 2:
            print self.game.player2.name, "won the game"
        elif winner == 3:
            print "You both lost, idiots"
        raw_input("Press Enter to end game")
