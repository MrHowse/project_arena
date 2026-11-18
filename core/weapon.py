"""Weapon: the abstract base class for everything a hero can attack with."""
import math
from abc import ABC, abstractmethod

import pygame

from core.effects import Arc
from core.projectile import Projectile

Vec = pygame.math.Vector2


class Weapon(ABC):
    """To make a weapon: inherit from Weapon, set the stats, write attack()."""

    NAME = "Unnamed"
    AUTHOR = "Unknown"
    DAMAGE = 10
    COOLDOWN = 0.4          # seconds between attacks
    HITS = 1                # how many times one attack can hit the same enemy
    COLOUR = (35, 31, 32)

    def __init__(self):
        self.timer = 0.0

    # ---- the one method you MUST write -----------------------------------
    @abstractmethod
    def attack(self, world, owner, direction):
        """Make the attack happen. direction is a vector of length 1."""

    # ---- already written for you -----------------------------------------
    def update(self, dt):
        self.timer = max(0.0, self.timer - dt)

    def try_attack(self, world, owner, direction):
        if self.timer <= 0:
            self.timer = self.COOLDOWN
            self.attack(world, owner, Vec(direction))

    def fire(self, world, owner, direction, speed=420, damage=None, radius=5,
             lifetime=1.2, pierce=False, colour=None):
        """Launch a projectile. Returns it, in case you want to change it."""
        direction = Vec(direction)
        if direction.length() == 0:
            direction = Vec(1, 0)
        direction = direction.normalize()
        shot = Projectile(owner.pos + direction * owner.RADIUS, direction * speed,
                          self.DAMAGE if damage is None else damage, "hero", owner=owner,
                          radius=radius, colour=colour or self.COLOUR, lifetime=lifetime, pierce=pierce)
        world.projectiles.append(shot)
        return shot

    def slash(self, world, owner, direction, reach=60, arc=90, damage=None, knockback=200):
        """Hit every enemy inside a wedge in front of the owner. Returns those hit."""
        direction = Vec(direction)
        hit = []
        for enemy in world.enemies:
            gap = enemy.pos - owner.pos
            if not enemy.alive or gap.length() > reach + enemy.RADIUS:
                continue
            angle = 0 if gap.length() < 1 else abs(direction.angle_to(gap))
            angle = min(angle, 360 - angle)
            if angle <= arc / 2:
                enemy.take_damage(self.DAMAGE if damage is None else damage, world, source=owner)
                enemy.push(gap, knockback)
                hit.append(enemy)
        world.effects.append(Arc(owner.pos, direction, reach, arc, self.COLOUR))
        return hit

    @classmethod
    def dps(cls):
        """Damage per second if every attack lands. Used for the fairness check."""
        return cls.DAMAGE * cls.HITS / cls.COOLDOWN


def rotate(direction, degrees):
    """Return direction turned by a number of degrees. Handy for spread shots."""
    radians = math.radians(degrees)
    x, y = direction.x, direction.y
    return Vec(x * math.cos(radians) - y * math.sin(radians),
               x * math.sin(radians) + y * math.cos(radians))
