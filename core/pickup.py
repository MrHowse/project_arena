"""Pickup: the abstract base class for things the hero can collect."""
from abc import ABC, abstractmethod

import pygame

Vec = pygame.math.Vector2


class Pickup(ABC):
    """To make a pickup: inherit from Pickup, set the look, write apply()."""

    NAME = "Unnamed"
    AUTHOR = "Unknown"
    RADIUS = 10
    COLOUR = (84, 137, 48)
    LIFETIME = 12.0         # seconds before it disappears

    def __init__(self, x, y):
        self.pos = Vec(x, y)
        self.age = 0.0
        self.alive = True

    # ---- the one method you MUST write -----------------------------------
    @abstractmethod
    def apply(self, hero, world):
        """What happens when the hero collects this."""

    # ---- already written for you -----------------------------------------
    def update(self, world, dt):
        self.age += dt
        if self.age >= self.LIFETIME:
            self.alive = False
            return
        hero = world.hero
        if hero.alive and self.pos.distance_to(hero.pos) <= self.RADIUS + hero.RADIUS:
            self.apply(hero, world)
            world.ring(self.pos, self.COLOUR, 40)
            world.say(f"Picked up {self.NAME}")
            self.alive = False

    def draw(self, surface):
        """A diamond that blinks when it is about to vanish."""
        if self.LIFETIME - self.age < 3 and int(self.age * 8) % 2 == 0:
            return
        x, y, r = int(self.pos.x), int(self.pos.y), self.RADIUS
        points = [(x, y - r), (x + r, y), (x, y + r), (x - r, y)]
        pygame.draw.polygon(surface, self.COLOUR, points)
        pygame.draw.polygon(surface, (35, 31, 32), points, 2)
