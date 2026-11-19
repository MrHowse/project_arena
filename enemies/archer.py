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

    IMAGE = None

    @classmethod
    def get_image(cls):
        if cls.IMAGE is None:
            raw = pygame.image.load("assets_e/archer_eye.png").convert_alpha()
            size = cls.RADIUS * 2
            cls.IMAGE = pygame.transform.smoothscale(raw, (50, 50))
        return cls.IMAGE


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
        image = self.get_image()
        rect = image.get_rect(center=(self.pos.x, self.pos.y))
        surface.blit(image, rect)
