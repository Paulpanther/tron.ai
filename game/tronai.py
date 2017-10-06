from view.view import View

from game.game import Game


def main():
    g = Game()
    v = View(g)

    v.start()

if __name__ == "__main__":
    main()
