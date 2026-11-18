"""Controls: what the player (or a test bot) wants the hero to do this frame."""
import math

import pygame

Vec = pygame.math.Vector2


class Controls:
    def __init__(self):
        self.move = Vec(0, 0)       # direction to walk in
        self.aim = (0, 0)           # the point the hero faces
        self.attack = False
        self.special = False


def read_player():
    """Turn the keyboard and mouse into a Controls object."""
    controls = Controls()
    keys = pygame.key.get_pressed()
    controls.move = Vec(
        (keys[pygame.K_d] or keys[pygame.K_RIGHT]) - (keys[pygame.K_a] or keys[pygame.K_LEFT]),
        (keys[pygame.K_s] or keys[pygame.K_DOWN]) - (keys[pygame.K_w] or keys[pygame.K_UP]))
    controls.aim = pygame.mouse.get_pos()
    controls.attack = pygame.mouse.get_pressed()[0] or keys[pygame.K_j]
    controls.special = keys[pygame.K_SPACE]
    return controls


def read_bot(world):
    """A simple automatic player. The tests use it to play with no window."""
    controls = Controls()
    hero = world.hero
    target = world.nearest_enemy(hero.pos)
    angle = hero.age * 1.3
    controls.move = Vec(math.cos(angle), math.sin(angle))
    controls.aim = tuple(target.pos) if target else tuple(world.arena.center)
    controls.attack = True
    controls.special = True
    return controls
