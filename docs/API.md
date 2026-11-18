# What your class can use

Everything here already exists. `self` is your enemy or hero, `world` is the arena.

## Every enemy and hero (from `Entity`)

| You write | What you get |
|---|---|
| `self.pos` | Position, a vector. `self.pos.x` and `self.pos.y` are pixels |
| `self.hp`, `self.MAX_HP` | Health now, and at the start |
| `self.age` | Seconds since this one was created |
| `self.speed` | Speed right now, in pixels per second |
| `self.distance_to(target)` | Pixels to an entity or a position |
| `self.direction_to(target)` | A vector of length 1 pointing at it |
| `self.move_towards(target, dt, world)` | Walk at it |
| `self.move_away_from(target, dt, world)` | Walk away from it |
| `self.move(direction, dt, world)` | Walk in any direction |
| `self.take_damage(amount, world, source=self)` | Lose health. True if that was fatal |
| `self.heal(amount)` | Gain health, never above `MAX_HP` |
| `self.push(direction, strength)` | Get shoved |
| `self.slow(seconds, factor)` | Slow down, for example `slow(2, 0.5)` |
| `self.hasten(seconds, factor)` | Speed up, for example `hasten(3, 1.5)` |
| `self.draw_body(surface)` | Draw the standard circle |
| `def on_death(self, world):` | Write this method to act once when defeated |

## Enemies only

| You write | What you get |
|---|---|
| `self.ready("name", seconds)` | True at most once every `seconds` |
| `self.shoot(world, target, speed=220)` | Fire a projectile. Set `RANGED = True` |

## Heroes only

| You write | What you get |
|---|---|
| `self.facing` | A vector of length 1 pointing at the mouse |
| `self.shield = 1.5` | Take no damage for that many seconds |
| `self.weapon` | The weapon the player chose |

## Weapons

| You write | What you get |
|---|---|
| `self.fire(world, owner, direction, speed=420, pierce=False)` | Launch a projectile |
| `self.slash(world, owner, direction, reach=60, arc=90)` | Hit every enemy in a wedge. Returns a list |
| `rotate(direction, degrees)` | A turned copy of a direction. `from core.weapon import rotate` |

## The world

| You write | What you get |
|---|---|
| `world.hero` | The player |
| `world.enemies` | The list of living enemies |
| `world.arena` | The sand, a `pygame.Rect` |
| `world.nearest_enemy(pos, max_range=None)` | The closest enemy, or `None` |
| `world.enemies_within(pos, radius)` | A list of enemies in a circle |
| `world.blast(pos, radius, damage, source=self)` | Damage every enemy in a circle |
| `world.blast(pos, radius, damage, source=self, hurts="hero")` | The same, against the hero |
| `world.spawn_enemy(SomeEnemy, pos)` | Add an enemy |
| `world.random_point()` | A random position on the sand |
| `world.say("text")` | Put a line in the message feed |
| `world.ring(pos, colour, radius)` | A ring effect |
| `world.random` | Use `world.random.random()` instead of `random.random()` |

## The budgets

    enemy cost  = MAX_HP / 10 + SPEED / 20 + DAMAGE / 2   (+ 4 if RANGED)
    limit       = 14 for THREAT 1, 22 for THREAT 2, 32 for THREAT 3, 70 for a boss (THREAT 4)

    hero cost   = MAX_HP / 10 + SPEED / 15 + 20 / SPECIAL_COOLDOWN
    limit       = 28

    weapon      = DAMAGE x HITS / COOLDOWN must be 60 or less
