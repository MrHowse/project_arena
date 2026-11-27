"""Bull: stalks, winds up, then charges. Shows a state machine.

A state machine means the enemy is always in exactly one state, and each
state has its own rule for what to do and when to switch to another state.

    stalk  --close enough-->  wind_up  --0.6 s-->  charge  --0.7 s-->  rest
      ^                                                                  |
      +--------------------------- 1.0 s -------------------------------+
"""
import pygame
from core.enemy import Enemy


class Bull(Enemy):
    NAME = "Bull"
    AUTHOR = "Starter kit"
    THREAT = 2
    MAX_HP = 60
    SPEED = 70
    DAMAGE = 14
    RADIUS = 17
    COLOUR = (109, 45, 0)
    SCORE = 25

    CHARGE_RANGE = 220
    CHARGE_SPEED = 5            # times normal speed

    def __init__(self, x, y):
        super().__init__(x, y)  # always call this first in your own __init__
        self.state = "stalk"
        self.state_time = 0.0
        self.charge_direction = None

        # Load the sprite image and scale it to match the enemy's diameter (RADIUS * 2)
        raw_image = pygame.image.load("assets_e/angrydriver.png").convert_alpha()
        size = self.RADIUS * 2
        self.image = pygame.transform.smoothscale(raw_image, (size, size))

    def change_state(self, new_state):
        self.state = new_state
        self.state_time = 0.0

    def think(self, world, dt):
        self.state_time += dt
        hero = world.hero

        if self.state == "stalk":
            self.move_towards(hero, dt, world)
            if self.distance_to(hero) < self.CHARGE_RANGE:
                self.change_state("wind_up")

        elif self.state == "wind_up":
            # Stand still and lock in a direction. This is the player's warning.
            self.charge_direction = self.direction_to(hero)
            if self.state_time > 0.6:
                self.change_state("charge")

        elif self.state == "charge":
            self.pos += self.charge_direction * self.speed * self.CHARGE_SPEED * dt
            world.keep_inside(self)
            if self.state_time > 0.7:
                self.change_state("rest")

        elif self.state == "rest":
            if self.state_time > 1.0:
                self.change_state("stalk")

    def draw(self, surface):
        # Optional: draw a gold warning circle underneath while winding up
        if self.state == "wind_up":
            pygame.draw.circle(surface, (252, 175, 23), (int(self.pos.x), int(self.pos.y)), self.RADIUS + 4)

        # Center the image on self.pos and draw it
        rect = self.image.get_rect(center=(int(self.pos.x), int(self.pos.y)))
        surface.blit(self.image, rect)
