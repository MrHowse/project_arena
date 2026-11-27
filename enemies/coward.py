from core.enemy import Enemy


class Coward(Enemy):
    NAME = "Coward"
    AUTHOR = "Ben"
    THREAT = 2
    MAX_HP = 15
    SPEED = 75
    DAMAGE = 5
    RADIUS = 12
    COLOUR = (255, 140, 200)

    def think(self, world, dt):
   
        if self.hp < self.MAX_HP / 2:
            self.move_towards(world.hero, -dt, world)
        else:
            self.move_towards(world.hero, dt, world)
