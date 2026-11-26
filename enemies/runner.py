"""
interesting stuff here
"""
from core.enemy import Enemy
import random
import pygame


class Runner(Enemy):
    NAME = "Runner"            # shown in the game
    AUTHOR = "Lincoln"          # your name: you get the credit, and the bug reports
    THREAT = 1                  # 1, 2 or 3. Sets how many stat points you may spend
    MAX_HP = 5
    SPEED = 190
    DAMAGE = 8
    RADIUS = 13
    CHARGED = False

    def __init__(self, x, y):
        super().__init__(x, y)
        self.facing = pygame.math.Vector2(1,0)
        self.timers = {}
        self.touch_timer = 0.0
        self.EXPLODES = random.choice([True,False])
        self.COLOUR = (212, 107, 80) if self.EXPLODES else (146, 191, 78)    # (red, green, blue)

    def update(self, world, dt):
        #the runner needs a larger push or the hero can never break away for a shot after contact
        self.tick(dt, world)
        for name in self.timers:
            self.timers[name] = max(0.0, self.timers[name] - dt)
        self.touch_timer = max(0.0, self.touch_timer - dt)
        self.think(world, dt)
        hero = world.hero
        if hero.alive and self.touch_timer <= 0 and self.distance_to(hero) <= self.RADIUS + hero.RADIUS:
            hero.take_damage(self.DAMAGE, world, source=self)
            hero.push(self.direction_to(hero), 500)
            self.touch_timer = self.TOUCH_COOLDOWN

    def think(self, world, dt):
        self.facing = self.direction_to(world.hero)
        self.move(self.facing, dt, world)
        if self.distance_to(world.hero) < 200 and not self.CHARGED:
            self.hasten(4,1.2)
            self.CHARGED = True
    
    def on_death(self, world):
        if self.EXPLODES:
            world.blast(self.pos, 40, 12, source=self, hurts="hero")

    def draw(self, surface):
        #a wonky octagon thing
        vertices = [self.pos + self.facing * 14]
        for i in range(7):
            offset = 360/8 * (i+1)
            vertices.append(self.pos + self.facing.rotate(offset) * 11)
        colour = (255, 255, 255) if self.flash > 0 else self.COLOUR
        pygame.draw.polygon(surface, colour, vertices)
        pygame.draw.polygon(surface, (35, 31, 32), vertices, 2)