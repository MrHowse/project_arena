"""TEMPLATE: copy this file, rename the copy, then make it yours.

    1. Copy this file. Name the copy after your enemy, in lowercase with
       underscores and NO leading underscore, for example  sand_wraith.py
    2. Rename the class, and fill in NAME and AUTHOR.
    3. Choose your stats. Check them with:  python3 sandbox.py enemies/sand_wraith.py
    4. Write think().

Files that start with an underscore are ignored by the game.
"""
from core.enemy import Enemy


class MyEnemy(Enemy):
    NAME = "Unnamed"            # shown in the game
    AUTHOR = "Unknown"          # your name: you get the credit, and the bug reports
    THREAT = 1                  # 1, 2 or 3. Sets how many stat points you may spend
    MAX_HP = 20
    SPEED = 60
    DAMAGE = 5
    RADIUS = 13
    COLOUR = (144, 182, 212)    # (red, green, blue)

    def think(self, world, dt):
        # Called 60 times a second. world.hero is the player.
        self.move_towards(world.hero, dt, world)
