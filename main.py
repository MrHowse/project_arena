"""Run the game:  python3 main.py

Add --strict to stop on the first content error and see the full traceback.
"""
import sys

from core.game import Game

if __name__ == "__main__":
    Game(strict="--strict" in sys.argv).run()
