"""Entity: the abstract base class for anything that lives in the arena."""
from abc import ABC, abstractmethod

import pygame

Vec = pygame.math.Vector2


def as_point(target):
    """Accept either an Entity or a position and return the position."""
    return target.pos if hasattr(target, "pos") else Vec(target)


class Entity(ABC):
    """Shared data and behaviour for heroes and enemies.

    ABC stands for Abstract Base Class. You can never create a plain Entity.
    It exists so every child class is guaranteed to have the same basics.
    """

    NAME = "Unnamed"
    AUTHOR = "Unknown"
    MAX_HP = 10
    SPEED = 60              # pixels per second
    RADIUS = 14             # size of the body, and of the hit circle
    COLOUR = (200, 200, 200)

    def __init__(self, x, y):
        self.pos = Vec(x, y)
        self.hp = self.MAX_HP
        self.alive = True
        self.age = 0.0              # seconds since this entity was created
        self.flash = 0.0            # counts down while the body flashes white
        self.knock = Vec(0, 0)      # leftover push from a knockback
        self.slow_time = 0.0
        self.slow_factor = 1.0
        self.last_hit_by = None

    # ---- the contract: every child class must provide these -------------
    @abstractmethod
    def update(self, world, dt):
        """Advance this entity by dt seconds."""

    @abstractmethod
    def draw(self, surface):
        """Draw this entity on the screen."""

    # ---- helpers every child class may use -------------------------------
    @property
    def speed(self):
        """Current speed, allowing for any slow effect."""
        return self.SPEED * (self.slow_factor if self.slow_time > 0 else 1.0)

    def distance_to(self, target):
        return self.pos.distance_to(as_point(target))

    def direction_to(self, target):
        """A vector of length 1 pointing at the target (or zero if on top of it)."""
        gap = as_point(target) - self.pos
        return gap.normalize() if gap.length() > 0.001 else Vec(0, 0)

    def move(self, direction, dt, world):
        """Move in a direction at this entity's speed, staying inside the arena."""
        direction = Vec(direction)
        if direction.length() > 0.001:
            self.pos += direction.normalize() * self.speed * dt
        world.keep_inside(self)

    def move_towards(self, target, dt, world):
        self.move(self.direction_to(target), dt, world)

    def move_away_from(self, target, dt, world):
        self.move(-self.direction_to(target), dt, world)

    def push(self, direction, strength=260):
        """Shove this entity. The push fades out over about a third of a second."""
        direction = Vec(direction)
        if direction.length() > 0.001:
            self.knock += direction.normalize() * strength

    def slow(self, seconds, factor=0.5):
        """Reduce speed for a while. factor 0.5 means half speed."""
        self.slow_time = max(self.slow_time, seconds)
        self.slow_factor = factor

    def hasten(self, seconds, factor=1.5):
        """Raise speed for a while. factor 1.5 means half as fast again."""
        self.slow_time = max(self.slow_time, seconds)
        self.slow_factor = factor

    def heal(self, amount):
        self.hp = min(self.MAX_HP, self.hp + amount)

    def take_damage(self, amount, world, source=None):
        """Lose hit points. Returns True if this hit was the fatal one."""
        if not self.alive or amount <= 0:
            return False
        self.hp -= amount
        self.flash = 0.12
        self.last_hit_by = source
        world.floating_text(str(int(amount)), self.pos, self.COLOUR)
        if self.hp <= 0:
            self.hp = 0
            self.alive = False
            self.on_death(world)
            return True
        return False

    def on_death(self, world):
        """Runs once when hit points reach zero. Override it for a last trick."""

    def tick(self, dt, world):
        """Housekeeping shared by every entity. Called from update()."""
        self.age += dt
        self.flash = max(0.0, self.flash - dt)
        self.slow_time = max(0.0, self.slow_time - dt)
        if self.knock.length() > 1:
            self.pos += self.knock * dt
            self.knock *= max(0.0, 1 - 6 * dt)
            world.keep_inside(self)

    def draw_body(self, surface):
        """A plain circle with an outline. Good enough until you draw your own."""
        colour = (255, 255, 255) if self.flash > 0 else self.COLOUR
        centre = (int(self.pos.x), int(self.pos.y))
        pygame.draw.circle(surface, colour, centre, self.RADIUS)
        pygame.draw.circle(surface, (35, 31, 32), centre, self.RADIUS, 2)

    def draw_health_bar(self, surface):
        if self.hp >= self.MAX_HP:
            return
        width = self.RADIUS * 2
        left = int(self.pos.x - self.RADIUS)
        top = int(self.pos.y - self.RADIUS - 8)
        pygame.draw.rect(surface, (35, 31, 32), (left, top, width, 4))
        fill = int(width * self.hp / self.MAX_HP)
        pygame.draw.rect(surface, (227, 27, 34), (left, top, fill, 4))
