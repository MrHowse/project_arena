"""Projectile: anything that flies in a straight line and hurts what it touches."""
import pygame

Vec = pygame.math.Vector2


class Projectile:
    def __init__(self, pos, velocity, damage, team, owner=None,
                 radius=5, colour=(35, 31, 32), lifetime=1.5, pierce=False):
        self.pos = Vec(pos)
        self.velocity = Vec(velocity)
        self.damage = damage
        self.team = team              # "hero" hurts enemies, "enemy" hurts the hero
        self.owner = owner
        self.radius = radius
        self.colour = colour
        self.lifetime = lifetime
        self.pierce = pierce          # True: keeps flying after a hit
        self.alive = True
        self.already_hit = []

    def update(self, world, dt):
        self.pos += self.velocity * dt
        self.lifetime -= dt
        if self.lifetime <= 0 or not world.arena.collidepoint(self.pos.x, self.pos.y):
            self.alive = False
            return
        targets = world.enemies if self.team == "hero" else [world.hero]
        for target in targets:
            if not target.alive or target in self.already_hit:
                continue
            if self.pos.distance_to(target.pos) <= self.radius + target.RADIUS:
                target.take_damage(self.damage, world, source=self.owner)
                self.already_hit.append(target)
                if not self.pierce:
                    self.alive = False
                    return

    def draw(self, surface):
        centre = (int(self.pos.x), int(self.pos.y))
        pygame.draw.circle(surface, self.colour, centre, self.radius)
        pygame.draw.circle(surface, (35, 31, 32), centre, self.radius, 1)
