import pygame

from core.enemy import Enemy


class Netter(Enemy):
    NAME = "Netter"
    AUTHOR = "Starter kit"
    THREAT = 1
    MAX_HP = 25
    SPEED = 75
    DAMAGE = 2
    RADIUS = 13
    COLOUR = (40, 160, 140)

    def __init__(self, x, y):
        super().__init__(x, y)
        self.last_hero_pos = None

    def draw(self, surface):
        # Draw a faint, steady net circle on the ground (no explosion!)
        pygame.draw.circle(surface, self.COLOUR, (int(self.pos.x), int(self.pos.y)), 90, 2)
        super().draw(surface)

    def think(self, world, dt):
        hero = world.hero
        self.move_towards(hero, dt, world)

        # Cut the hero's movement speed by 50% while inside the 90px net circle
        if self.last_hero_pos is not None and self.distance_to(hero) <= 90:
            moved = hero.pos - self.last_hero_pos
            hero.pos -= moved * 0.6

        self.last_hero_pos = pygame.math.Vector2(hero.pos)