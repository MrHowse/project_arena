"""World: everything in the arena, and the helpers content classes can call."""
import random
import traceback

import pygame

import settings
from core import sound
from core.effects import FloatingText, Ring

Vec = pygame.math.Vector2
CONTENT_FOLDERS = ("enemies", "heroes", "weapons", "pickups")


class World:
    def __init__(self, registry, hero_class, weapon_class, strict=False, seed=None):
        self.registry = registry
        self.strict = strict            # True: a content error stops the game (sandbox, tests)
        self.random = random.Random(seed)
        self.arena = pygame.Rect(settings.ARENA)
        self.hero = hero_class(*self.arena.center)
        self.hero.weapon = weapon_class()
        self.enemies = []
        self.projectiles = []
        self.pickups = []
        self.effects = []
        self.controls = None
        self.time = 0.0
        self.score = 0
        self.defeated = 0
        self.wave = 0
        self.messages = []              # [text, seconds left] for the feed
        self.crashes = []               # content errors caught during play

    # ---- helpers for content classes -------------------------------------
    def keep_inside(self, entity):
        r = entity.RADIUS
        entity.pos.x = min(max(entity.pos.x, self.arena.left + r), self.arena.right - r)
        entity.pos.y = min(max(entity.pos.y, self.arena.top + r), self.arena.bottom - r)

    def enemies_within(self, pos, radius):
        """Every living enemy within `radius` pixels of a position."""
        pos = Vec(pos)
        return [e for e in self.enemies if e.alive and e.pos.distance_to(pos) <= radius + e.RADIUS]

    def nearest_enemy(self, pos, max_range=None):
        """The closest living enemy, or None if there is not one in range."""
        pos = Vec(pos)
        living = [e for e in self.enemies if e.alive]
        if not living:
            return None
        nearest = min(living, key=lambda e: e.pos.distance_to(pos))
        if max_range is not None and nearest.pos.distance_to(pos) > max_range:
            return None
        return nearest

    def blast(self, pos, radius, damage, source=None, hurts="enemies"):
        """Damage everything in a circle. hurts is "enemies" or "hero"."""
        pos = Vec(pos)
        self.ring(pos, settings.GOLD if hurts == "enemies" else settings.RED, radius)
        if hurts == "enemies":
            for enemy in self.enemies_within(pos, radius):
                enemy.take_damage(damage, self, source=source)
                enemy.push(enemy.pos - pos, 220)
        elif self.hero.alive and self.hero.pos.distance_to(pos) <= radius + self.hero.RADIUS:
            self.hero.take_damage(damage, self, source=source)

    def spawn_enemy(self, enemy_class, pos=None):
        """Add an enemy. With no position it walks in from a random edge."""
        pos = self.edge_point() if pos is None else Vec(pos)
        enemy = enemy_class(pos.x, pos.y)
        self.keep_inside(enemy)
        self.enemies.append(enemy)
        return enemy

    def spawn_pickup(self, pickup_class, pos):
        pickup = pickup_class(*Vec(pos))
        self.pickups.append(pickup)
        return pickup

    def random_point(self, margin=30):
        a = self.arena
        return Vec(self.random.uniform(a.left + margin, a.right - margin),
                   self.random.uniform(a.top + margin, a.bottom - margin))

    def edge_point(self):
        a, side = self.arena, self.random.choice("NSEW")
        if side in "NS":
            return Vec(self.random.uniform(a.left, a.right), a.top if side == "N" else a.bottom)
        return Vec(a.left if side == "W" else a.right, self.random.uniform(a.top, a.bottom))

    def say(self, text, seconds=3.5):
        """Put a line in the message feed."""
        self.messages.append([text, seconds])
        del self.messages[:-4]

    def ring(self, pos, colour, radius=60):
        self.effects.append(Ring(pos, colour, radius))

    def floating_text(self, text, pos, colour=settings.WHITE):
        self.effects.append(FloatingText(text, pos, colour))

    # ---- the frame --------------------------------------------------------
    def update(self, dt, controls):
        self.controls = controls
        self.time += dt
        if self.hero.alive:
            self.safely(self.hero, self.hero.update, self, dt)
        for enemy in list(self.enemies):
            self.safely(enemy, enemy.update, self, dt)
        for shot in list(self.projectiles):
            self.safely(shot.owner or shot, shot.update, self, dt)
        for pickup in list(self.pickups):
            self.safely(pickup, pickup.update, self, dt)
        for effect in self.effects:
            effect.update(dt)
        for enemy in self.enemies:
            if not enemy.alive:
                self.enemy_defeated(enemy)
        self.enemies = [e for e in self.enemies if e.alive]
        self.projectiles = [p for p in self.projectiles if p.alive]
        self.pickups = [p for p in self.pickups if p.alive]
        self.effects = [e for e in self.effects if e.alive]
        for message in self.messages:
            message[1] -= dt
        self.messages = [m for m in self.messages if m[1] > 0]

    def enemy_defeated(self, enemy):
        if getattr(enemy, "crashed", False):
            return
        self.score += enemy.SCORE
        self.defeated += 1
        sound.play("defeat")
        self.say(f"{enemy.NAME} defeated (made by {enemy.AUTHOR})")
        if self.registry.pickups and self.random.random() < settings.PICKUP_DROP_CHANCE:
            self.spawn_pickup(self.random.choice(self.registry.pickups), enemy.pos)

    def draw(self, surface):
        for group in (self.pickups, self.enemies, self.projectiles):
            for thing in group:
                self.safely(getattr(thing, "owner", None) or thing, thing.draw, surface)
        for enemy in self.enemies:
            enemy.draw_health_bar(surface)
        if self.hero.alive:
            self.safely(self.hero, self.hero.draw, surface)
        for effect in self.effects:
            effect.draw(surface)

    # ---- keeping one person's bug from stopping everyone's game ----------
    def safely(self, thing, method, *args):
        """Run a content method. If it raises an error, report it and carry on."""
        try:
            method(*args)
        except Exception as error:
            if self.strict:
                raise
            self.report(thing, error)

    def report(self, thing, error):
        where = ""
        for frame in reversed(traceback.extract_tb(error.__traceback__)):
            parts = frame.filename.replace("\\", "/").split("/")
            if len(parts) >= 2 and parts[-2] in CONTENT_FOLDERS:
                where = f" at {parts[-2]}/{parts[-1]} line {frame.lineno}"
                break
        name = getattr(thing, "NAME", type(thing).__name__)
        author = getattr(thing, "AUTHOR", "Unknown")
        line = f"{name} (made by {author}) crashed: {type(error).__name__}: {error}{where}"
        if line not in self.crashes:
            self.crashes.append(line)
            print("CONTENT ERROR:", line)
        self.say(f"{name} by {author} crashed and was removed")
        thing.crashed = True
        thing.alive = False
