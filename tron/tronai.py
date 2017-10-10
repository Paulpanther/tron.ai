import importlib
import os
import sys

from game.game import Game
from view.view import View


def main():

    dirs = os.listdir('ai')
    aifolder = []

    fullpath = os.path.dirname(sys.modules['__main__'].__file__)

    for aidir in dirs:
        if os.path.isdir(os.path.join(fullpath, 'ai/'+aidir)):
            aifolder.append(aidir)

    ai = [importlib.import_module("ai."+aidir+".ai") for aidir in aifolder]

    g = Game(ai)
    v = View(g)

    v.start()


if __name__ == "__main__":
    main()
