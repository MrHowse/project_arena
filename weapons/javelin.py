"""Javelin: slow to throw, but it passes through every enemy in its path."""
from core.weapon import Weapon


class Javelin(Weapon):
    NAME = "Javelin"
    AUTHOR = "Starter kit"
    DAMAGE = 22
    COOLDOWN = 0.7
    COLOUR = (252, 175, 23)

    def attack(self, world, owner, direction):
        # fire() launches a projectile. pierce=True lets it keep flying after a hit.
        self.fire(world, owner, direction, speed=520, radius=6, pierce=True)
