"""TEMPLATE: copy this file, rename the copy (no leading underscore), make it yours.

Check your numbers with:  python3 sandbox.py weapons/your_file.py
"""
from core.weapon import Weapon


class MyWeapon(Weapon):
    NAME = "Unnamed"
    AUTHOR = "Unknown"
    DAMAGE = 10
    COOLDOWN = 0.5              # seconds between attacks
    HITS = 1                    # raise this if one attack fires several shots
    COLOUR = (35, 31, 32)

    def attack(self, world, owner, direction):
        # direction is a vector of length 1 pointing where the hero is aiming.
        self.fire(world, owner, direction)
