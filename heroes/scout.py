"""Scout: fragile and fast. Shows a movement special."""
import pygame

from core.hero import Hero


class Scout(Hero):
    NAME = "Scout"
    AUTHOR = "Starter kit"
    MAX_HP = 70
    SPEED = 220
    RADIUS = 13
    COLOUR = (114, 61, 138)
    SPECIAL_NAME = "Dash"
    SPECIAL_COOLDOWN = 4.0

    DASH_DISTANCE = 150
    DASH_DAMAGE = 15

    def special(self, world):
        # Leap forward, hurting anything along the way.
        start = pygame.math.Vector2(self.pos)
        self.pos += self.facing * self.DASH_DISTANCE
        world.keep_inside(self)
        middle = (start + self.pos) / 2
        for enemy in world.enemies_within(middle, self.DASH_DISTANCE / 2):
            enemy.take_damage(self.DASH_DAMAGE, world, source=self)
        world.ring(start, self.COLOUR, 30)
        world.ring(self.pos, self.COLOUR, 30)
