"""Enemy: the abstract base class every enemy in the game inherits from."""
from abc import abstractmethod

import pygame

import settings
from core.entity import Entity, as_point
from core.projectile import Projectile

Vec = pygame.math.Vector2


class Enemy(Entity):
    """To make an enemy: inherit from Enemy, set the stats, write think().

    Everything else (moving, taking damage, hurting the hero on contact,
    being drawn as a circle) already works. Override more only if you want to.
    """

    THREAT = 1              # 1 = common, 2 = tough, 3 = elite. Sets your budget.
    DAMAGE = 5              # damage dealt each time this enemy touches the hero
    RANGED = False          # set True if your enemy ever calls self.shoot()
    SCORE = 10              # points for defeating it
    TOUCH_COOLDOWN = 0.8    # seconds between touch hits

    def __init__(self, x, y):
        super().__init__(x, y)
        self.timers = {}
        self.touch_timer = 0.0

    # ---- the one method you MUST write -----------------------------------
    @abstractmethod
    def think(self, world, dt):
        """Decide what to do this frame. Called 60 times a second."""

    # ---- already written for you -----------------------------------------
    def update(self, world, dt):
        self.tick(dt, world)
        for name in self.timers:
            self.timers[name] = max(0.0, self.timers[name] - dt)
        self.touch_timer = max(0.0, self.touch_timer - dt)
        self.think(world, dt)
        hero = world.hero
        if hero.alive and self.touch_timer <= 0 and self.distance_to(hero) <= self.RADIUS + hero.RADIUS:
            hero.take_damage(self.DAMAGE, world, source=self)
            hero.push(self.direction_to(hero), 180)
            self.touch_timer = self.TOUCH_COOLDOWN

    def draw(self, surface):
        self.draw_body(surface)

    def ready(self, name, seconds):
        """True at most once every `seconds`. Use it to pace attacks.

            if self.ready("shoot", 1.5):
                self.shoot(world, world.hero)
        """
        if self.timers.get(name, 0.0) <= 0:
            self.timers[name] = seconds
            return True
        return False

    def shoot(self, world, target, speed=220, damage=None, radius=5, colour=None):
        """Fire a projectile at a target (an entity or a position)."""
        direction = self.direction_to(as_point(target))
        if direction.length() == 0:
            direction = Vec(1, 0)
        shot = Projectile(self.pos + direction * self.RADIUS, direction * speed,
                          self.DAMAGE if damage is None else damage, "enemy", owner=self,
                          radius=radius, colour=colour or self.COLOUR, lifetime=4.0)
        world.projectiles.append(shot)
        return shot

    @classmethod
    def cost(cls):
        """How much of the stat budget this enemy uses. Lower is weaker."""
        points = cls.MAX_HP / 10 + cls.SPEED / 20 + cls.DAMAGE / 2
        return points + (4 if cls.RANGED else 0)

    @classmethod
    def budget(cls):
        return settings.ENEMY_BUDGET.get(cls.THREAT, 0)
