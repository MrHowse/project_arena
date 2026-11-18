"""Grunt: the simplest enemy there is. Read this one first."""
from core.enemy import Enemy


class Grunt(Enemy):
    NAME = "Grunt"
    AUTHOR = "Starter kit"
    THREAT = 1
    MAX_HP = 30
    SPEED = 80
    DAMAGE = 8
    RADIUS = 13
    COLOUR = (190, 20, 27)

    def think(self, world, dt):
        # Walk straight at the hero. Touch damage is handled for us.
        self.move_towards(world.hero, dt, world)
