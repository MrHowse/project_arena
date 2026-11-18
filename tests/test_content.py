"""The contract test: every enemy, hero, weapon and pickup must pass this.

Run it before every push:

    python3 -m unittest

It checks three things about each class:
    1. it is labelled   (a NAME and an AUTHOR)
    2. it is fair       (stats inside the limits and the budget)
    3. it works         (ten seconds of play with no errors)
"""
import inspect
import pathlib
import re
import unittest

import pygame

import settings
from core import controls
from core.enemy import Enemy
from core.registry import FOLDERS, ROOT, Registry
from core.world import World

SECONDS = 10
DT = 1 / settings.FPS


def label(cls):
    file = pathlib.Path(inspect.getfile(cls))
    return f"{file.parent.name}/{file.name}: {cls.NAME} (made by {cls.AUTHOR})"


class Sparring(Enemy):
    """A plain opponent, so a hero or weapon is never failed by someone else's enemy."""
    NAME, AUTHOR = "Sparring partner", "Tests"
    MAX_HP, SPEED, DAMAGE = 40, 70, 4

    def think(self, world, dt):
        self.move_towards(world.hero, dt, world)


def is_colour(value):
    return (isinstance(value, (tuple, list)) and len(value) == 3
            and all(isinstance(part, int) and 0 <= part <= 255 for part in value))


class ContentTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        pygame.init()
        cls.screen = pygame.display.set_mode((settings.WIDTH, settings.HEIGHT))
        cls.registry = Registry().load()

    def everything(self):
        r = self.registry
        return r.enemies + r.heroes + r.weapons + r.pickups

    def new_world(self, hero=None, weapon=None):
        r = self.registry
        return World(r, hero or r.heroes[0], weapon or r.weapons[0], strict=True, seed=7)

    def play(self, world, seconds=SECONDS, fight=True):
        """Run the world for a while, drawing every frame as the real game does.

        fight=True: the bot moves, aims, attacks and uses its special.
        fight=False: the hero stands still and is kept alive, so enemies get
        the chance to walk right up and do everything they do at close range.
        """
        for _ in range(int(seconds * settings.FPS)):
            if fight:
                world.update(DT, controls.read_bot(world))
            else:
                world.hero.hp = world.hero.MAX_HP
                world.update(DT, controls.Controls())
            world.draw(self.screen)
            if not world.hero.alive:
                break

    # ---- 0. the folders themselves ----------------------------------------
    def test_every_file_loads(self):
        problems = [f"{file}: {problem}" for file, problem in self.registry.errors]
        self.assertEqual(problems, [], "\nThese files could not be loaded:\n  " + "\n  ".join(problems))

    def test_file_names(self):
        for folder in FOLDERS:
            for path in (ROOT / folder).glob("*.py"):
                if path.name.startswith("_"):
                    continue
                with self.subTest(file=f"{folder}/{path.name}"):
                    self.assertRegex(path.name, r"^[a-z][a-z0-9_]*\.py$",
                                     "File names use lowercase letters, numbers and underscores only.")

    def test_the_game_has_enough_to_run(self):
        r = self.registry
        self.assertTrue(r.heroes, "heroes/ needs at least one hero")
        self.assertTrue(r.weapons, "weapons/ needs at least one weapon")
        self.assertTrue([e for e in r.enemies if e.THREAT == 1], "enemies/ needs at least one THREAT 1 enemy")

    # ---- 1. labelled --------------------------------------------------------
    def test_names_and_authors(self):
        for cls in self.everything():
            with self.subTest(label(cls)):
                self.assertNotIn(cls.NAME, ("", "Unnamed"), "Give your class a NAME.")
                self.assertNotIn(cls.AUTHOR, ("", "Unknown"), "Put your name in AUTHOR.")
                self.assertLessEqual(len(cls.NAME), 18, "NAME must fit on the screen: 18 characters or fewer.")
                self.assertTrue(is_colour(cls.COLOUR), "COLOUR is three whole numbers from 0 to 255.")

    def test_names_are_unique(self):
        for folder in FOLDERS:
            names = [cls.NAME.lower() for cls in getattr(self.registry, folder)]
            repeats = sorted({name for name in names if names.count(name) > 1})
            self.assertEqual(repeats, [], f"Two classes in {folder}/ share a NAME: {repeats}")

    # ---- 2. fair ------------------------------------------------------------
    def test_enemy_stats(self):
        for cls in self.registry.enemies:
            with self.subTest(label(cls)):
                self.assertIn(cls.THREAT, settings.ENEMY_BUDGET, "THREAT must be 1, 2, 3 or 4.")
                self.assertGreaterEqual(cls.MAX_HP, 1, "MAX_HP must be at least 1.")
                self.assertTrue(0 <= cls.SPEED <= 260, "SPEED must be from 0 to 260.")
                self.assertTrue(0 <= cls.DAMAGE <= 40, "DAMAGE must be from 0 to 40.")
                biggest = 60 if cls.THREAT == 4 else 40
                self.assertTrue(8 <= cls.RADIUS <= biggest, f"RADIUS must be from 8 to {biggest}.")
                self.assertLessEqual(
                    cls.cost(), cls.budget(),
                    f"Costs {cls.cost():.1f} points but THREAT {cls.THREAT} allows {cls.budget()}. "
                    "Lower a stat, or raise THREAT.")

    def test_hero_stats(self):
        for cls in self.registry.heroes:
            with self.subTest(label(cls)):
                self.assertTrue(40 <= cls.MAX_HP <= 200, "MAX_HP must be from 40 to 200.")
                self.assertTrue(100 <= cls.SPEED <= 260, "SPEED must be from 100 to 260.")
                self.assertGreaterEqual(cls.SPECIAL_COOLDOWN, 1.5, "SPECIAL_COOLDOWN must be at least 1.5.")
                self.assertTrue(10 <= cls.RADIUS <= 24, "RADIUS must be from 10 to 24.")
                self.assertLessEqual(
                    cls.cost(), settings.HERO_BUDGET,
                    f"Costs {cls.cost():.1f} points but heroes get {settings.HERO_BUDGET}. Lower a stat.")

    def test_weapon_stats(self):
        for cls in self.registry.weapons:
            with self.subTest(label(cls)):
                self.assertGreaterEqual(cls.COOLDOWN, 0.1, "COOLDOWN must be at least 0.1 seconds.")
                self.assertGreaterEqual(cls.HITS, 1, "HITS must be at least 1.")
                self.assertLessEqual(
                    cls.dps(), settings.WEAPON_MAX_DPS,
                    f"Deals {cls.dps():.0f} damage per second but the limit is {settings.WEAPON_MAX_DPS}. "
                    "Lower DAMAGE or raise COOLDOWN.")

    # ---- 3. works -----------------------------------------------------------
    def test_enemies_work(self):
        for cls in self.registry.enemies:
            with self.subTest(label(cls)):
                world = self.new_world()
                hero = world.hero
                world.spawn_enemy(cls)                          # from the edge
                world.spawn_enemy(cls, hero.pos + (120, 0))     # close
                world.spawn_enemy(cls, hero.pos)                # right on top
                self.play(world, seconds=6, fight=False)
                self.play(world, seconds=6, fight=True)
                victim = world.spawn_enemy(cls)         # being defeated must work too
                victim.take_damage(victim.MAX_HP * 10, world, source=world.hero)
                world.update(DT, controls.read_bot(world))
                self.assertFalse(victim.alive, "An enemy with no health left must be defeated.")

    def test_heroes_work(self):
        for cls in self.registry.heroes:
            with self.subTest(label(cls)):
                world = self.new_world(hero=cls)
                for _ in range(3):
                    world.spawn_enemy(Sparring)
                world.spawn_enemy(Sparring, world.hero.pos)
                world.hero.special(world)               # with enemies in the arena
                self.play(world)
                empty = self.new_world(hero=cls)        # and with none at all
                empty.hero.special(empty)
                self.play(empty, seconds=2)

    def test_weapons_work(self):
        for cls in self.registry.weapons:
            with self.subTest(label(cls)):
                world = self.new_world(weapon=cls)
                for _ in range(3):
                    world.spawn_enemy(Sparring)
                world.spawn_enemy(Sparring, world.hero.pos)
                self.play(world)

    def test_pickups_work(self):
        for cls in self.registry.pickups:
            with self.subTest(label(cls)):
                world = self.new_world()
                world.hero.hp = 1
                pickup = world.spawn_pickup(cls, world.hero.pos)
                world.spawn_enemy(Sparring)
                self.play(world, seconds=3)
                self.assertFalse(pickup.alive, "A pickup the hero touches must be used up.")


if __name__ == "__main__":
    unittest.main()
