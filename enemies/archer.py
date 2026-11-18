"""Archer: keeps its distance and shoots. Shows timers and ranged attacks."""
import pygame

from core.enemy import Enemy


class Archer(Enemy):
    NAME = "Archer"
    AUTHOR = "Starter kit"
    THREAT = 1
    MAX_HP = 20
    SPEED = 60
    DAMAGE = 6
    RANGED = True               # costs 4 budget points, because range is powerful
    RADIUS = 12
    COLOUR = (84, 137, 48)

    TOO_CLOSE = 170             # back away inside this distance
    TOO_FAR = 260               # move closer beyond this distance

    def think(self, world, dt):
        hero = world.hero
        distance = self.distance_to(hero)
        if distance < self.TOO_CLOSE:
            self.move_away_from(hero, dt, world)
        elif distance > self.TOO_FAR:
            self.move_towards(hero, dt, world)
        # ready() is True at most once every 1.6 seconds.
        if self.ready("shoot", 1.6):
            self.shoot(world, hero, speed=230)

    def draw(self, surface):
        # Optional: draw something more interesting than a circle.
        self.draw_body(surface)
        pygame.draw.line(surface, (35, 31, 32),
                         (self.pos.x - 8, self.pos.y - 8), (self.pos.x + 8, self.pos.y + 8), 3)
