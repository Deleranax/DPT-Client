import argparse

try:
    game
except NameError:
    game = None

parser = argparse.ArgumentParser(description='Start the game.')
parser.add_argument('--debug', help='enable debug logging', action="store_true")


def main():
    from dpt.game import Game
    global game
    args = parser.parse_args()
    game = Game(args.debug)
    game.play()

if __name__ == '__main__':
    main()
