"""Short sword: a quick swing that hits everything in front of you."""
from core.weapon import Weapon


class ShortSword(Weapon):
    NAME = "Short sword"
    AUTHOR = "Starter kit"
    DAMAGE = 12
    COOLDOWN = 0.35
    COLOUR = (255, 255, 255)

    def attack(self, world, owner, direction):
        # slash() hits every enemy inside a wedge: 60 pixels long, 100 degrees wide.
        self.slash(world, owner, direction, reach=60, arc=100)
