"""Gladiator: a sturdy all-rounder. Read this one first."""
from core.hero import Hero
from weapons.short_sword import ShortSword

class Gladiator(Hero):
    NAME = "Gladiator"
    AUTHOR = "Starter kit"
    MAX_HP = 100
    SPEED = 180
    COLOUR = (0, 58, 112)
    SPECIAL_NAME = "Shield wall"
    SPECIAL_COOLDOWN = 5.0

    def __init__(self, *args, **kwargs):
        # Sets up the base character normally
        super().__init__(*args, **kwargs)
        # Forces the character to equip your custom Ninja Blade
        self.weapon = ShortSword()

    def special(self, world):
        # Take no damage for 1.5 seconds and shove nearby enemies away
        self.shield = 1.5
        world.ring(self.pos, (252, 175, 23), 90)
        for enemy in world.enemies_within(self.pos, 90):
            enemy.push(enemy.pos - self.pos, 420)