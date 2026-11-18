"""Hero: the abstract base class for every playable character."""
from abc import abstractmethod

import pygame

from core.entity import Entity

Vec = pygame.math.Vector2


class Hero(Entity):
    """To make a hero: inherit from Hero, set the stats, write special().

    Moving, aiming, attacking with the chosen weapon and taking damage
    already work. Your job is the stats, the look and the special move.
    """

    MAX_HP = 100
    SPEED = 180
    RADIUS = 15
    COLOUR = (0, 58, 112)
    SPECIAL_NAME = "Special"
    SPECIAL_COOLDOWN = 5.0      # seconds between uses of the special move
    HURT_PAUSE = 0.5            # seconds of safety after being hit

    def __init__(self, x, y):
        super().__init__(x, y)
        self.weapon = None
        self.facing = Vec(1, 0)
        self.special_timer = 0.0
        self.safe_timer = 0.0
        self.shield = 0.0       # seconds of taking no damage at all

    # ---- the one method you MUST write -----------------------------------
    @abstractmethod
    def special(self, world):
        """Your hero's special move. Runs when the player presses SPACE."""

    # ---- already written for you -----------------------------------------
    def update(self, world, dt):
        self.tick(dt, world)
        self.special_timer = max(0.0, self.special_timer - dt)
        self.safe_timer = max(0.0, self.safe_timer - dt)
        self.shield = max(0.0, self.shield - dt)
        controls = world.controls
        self.move(controls.move, dt, world)
        aim = Vec(controls.aim) - self.pos
        if aim.length() > 1:
            self.facing = aim.normalize()
        if self.weapon:
            self.weapon.update(dt)
            if controls.attack:
                self.weapon.try_attack(world, self, self.facing)
        if controls.special and self.special_timer <= 0:
            self.special_timer = self.SPECIAL_COOLDOWN
            self.special(world)

    def take_damage(self, amount, world, source=None):
        if self.safe_timer > 0 or self.shield > 0:
            return False
        self.safe_timer = self.HURT_PAUSE
        return super().take_damage(amount, world, source)

    def draw(self, surface):
        self.draw_body(surface)
        tip = self.pos + self.facing * (self.RADIUS + 8)
        pygame.draw.line(surface, (35, 31, 32), self.pos, tip, 4)
        if self.shield > 0:
            pygame.draw.circle(surface, (252, 175, 23), (int(self.pos.x), int(self.pos.y)), self.RADIUS + 6, 3)

    @classmethod
    def cost(cls):
        """How much of the hero budget these stats use."""
        return cls.MAX_HP / 10 + cls.SPEED / 15 + 20 / cls.SPECIAL_COOLDOWN
