"""Small visual effects. They never change the game, they only show what happened."""
import math

import pygame

Vec = pygame.math.Vector2
_font_cache = {}


def font(size):
    if size not in _font_cache:
        _font_cache[size] = pygame.font.SysFont(None, size)
    return _font_cache[size]


class FloatingText:
    def __init__(self, text, pos, colour, size=20, life=0.7):
        self.text, self.pos, self.colour = text, Vec(pos), colour
        self.size, self.life, self.alive = size, life, True

    def update(self, dt):
        self.pos.y -= 40 * dt
        self.life -= dt
        self.alive = self.life > 0

    def draw(self, surface):
        image = font(self.size).render(self.text, True, self.colour)
        outline = font(self.size).render(self.text, True, (35, 31, 32))
        x, y = int(self.pos.x - image.get_width() / 2), int(self.pos.y - 24)
        surface.blit(outline, (x + 1, y + 1))
        surface.blit(image, (x, y))


class Ring:
    """A circle that grows and fades. Used for blasts and pickups."""

    def __init__(self, pos, colour, max_radius=60, life=0.3):
        self.pos, self.colour, self.max_radius = Vec(pos), colour, max_radius
        self.life = self.total = life
        self.alive = True

    def update(self, dt):
        self.life -= dt
        self.alive = self.life > 0

    def draw(self, surface):
        progress = 1 - self.life / self.total
        radius = max(2, int(self.max_radius * progress))
        pygame.draw.circle(surface, self.colour, (int(self.pos.x), int(self.pos.y)), radius, 3)


class Arc:
    """The sweep of a melee weapon."""

    def __init__(self, pos, direction, reach, arc_degrees, colour, life=0.12):
        self.pos, self.reach, self.colour = Vec(pos), reach, colour
        self.angle = math.atan2(-direction.y, direction.x)
        self.half = math.radians(arc_degrees) / 2
        self.life, self.alive = life, True

    def update(self, dt):
        self.life -= dt
        self.alive = self.life > 0

    def draw(self, surface):
        box = pygame.Rect(0, 0, self.reach * 2, self.reach * 2)
        box.center = (int(self.pos.x), int(self.pos.y))
        pygame.draw.arc(surface, self.colour, box, self.angle - self.half, self.angle + self.half, 5)
