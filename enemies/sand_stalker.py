from core.enemy import Enemy


class SandStalker(Enemy):
    NAME = "Sand Stalker"
    AUTHOR = "Michael C"

    THREAT = 1
    MAX_HP = 20
    SPEED = 65
    DAMAGE = 10
    RADIUS = 14
    COLOUR = (130, 50, 190)

    BURROW_RANGE = 180
    BURROW_TIME = 0.8
    RECOVER_TIME = 1.0
    EMERGE_TIME = 0.35
    STRIKE_TIME = 0.25
    STRIKE_SPEED = 3.0

    def __init__(self, x, y):
        super().__init__(x, y)

        self.state = "stalk"
        self.state_time = 0.0
        self.attack_direction = None

    def change_state(self, new_state):
        self.state = new_state
        self.state_time = 0.0

    def think(self, world, dt):
        self.state_time += dt
        hero = world.hero

        if self.state == "stalk":
            self.move_towards(hero, dt, world)

            if (
                self.distance_to(hero) < self.BURROW_RANGE
                and self.ready("burrow", 3.0)
            ):
                self.change_state("burrow")

        elif self.state == "burrow":
            self.move_towards(hero, dt, world)

            if self.state_time > self.BURROW_TIME:
                self.change_state("emerge")

        elif self.state == "emerge":
            self.attack_direction = self.direction_to(hero)

            if self.state_time > self.EMERGE_TIME:
                self.change_state("strike")

        elif self.state == "strike":
            self.pos += (
                self.attack_direction
                * self.speed
                * self.STRIKE_SPEED
                * dt
            )

            world.keep_inside(self)

            if self.state_time > self.STRIKE_TIME:
                self.change_state("recover")

        elif self.state == "recover":
            if self.state_time > self.RECOVER_TIME:
                self.change_state("stalk")

    def draw(self, surface):
        if self.state != "burrow":
            self.draw_body(surface)