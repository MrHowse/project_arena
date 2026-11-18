"""Health potion: gives back some health. Read this one first."""
from core.pickup import Pickup


class HealthPotion(Pickup):
    NAME = "Health potion"
    AUTHOR = "Starter kit"
    COLOUR = (227, 27, 34)

    HEAL = 30

    def apply(self, hero, world):
        hero.heal(self.HEAL)
