"""Grunt: the simplest enemy there is. Read this one first."""
from core.enemy import Enemy


class Grunt(Enemy):
    NAME = "Ass"
    AUTHOR = "James"
    THREAT = 1
    MAX_HP = 1
    SPEED = 260
    DAMAGE = 1
    RADIUS = 30
    COLOUR = (190, 20, 27)

    def think(self, world, dt):
        # Walk straight at the hero. Touch damage is handled for us.
        self.move_towards(world.hero, dt, world)
