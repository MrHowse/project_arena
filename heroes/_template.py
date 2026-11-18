"""TEMPLATE: copy this file, rename the copy (no leading underscore), make it yours.

Check your stats with:  python3 sandbox.py heroes/your_file.py
"""
from core.hero import Hero


class MyHero(Hero):
    NAME = "Unnamed"
    AUTHOR = "Unknown"
    MAX_HP = 90
    SPEED = 170
    COLOUR = (144, 182, 212)
    SPECIAL_NAME = "Special"
    SPECIAL_COOLDOWN = 5.0      # seconds between uses

    def special(self, world):
        # Runs when the player presses SPACE. Make it worth pressing.
        self.heal(10)
