"""TEMPLATE: copy this file, rename the copy (no leading underscore), make it yours.

Test it with:  python3 sandbox.py pickups/your_file.py
"""
from core.pickup import Pickup


class MyPickup(Pickup):
    NAME = "Unnamed"
    AUTHOR = "Unknown"
    COLOUR = (84, 137, 48)
    LIFETIME = 12.0             # seconds before it disappears

    def apply(self, hero, world):
        # Runs once, when the hero walks over the pickup.
        hero.heal(5)
