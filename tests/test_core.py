"""Tests for the engine itself. The maintainers keep these passing."""
import contextlib
import io
import unittest

import pygame

import settings
from core import controls
from core.enemy import Enemy
from core.game import Game
from core.registry import Registry
from core.waves import WaveDirector
from core.world import World


class Dummy(Enemy):
    NAME, AUTHOR = "Dummy", "Tests"
    MAX_HP, SPEED, DAMAGE = 20, 0, 0

    def think(self, world, dt):
        pass


class Broken(Enemy):
    NAME, AUTHOR = "Broken", "Tests"

    def think(self, world, dt):
        return 1 / 0


class CoreTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        pygame.init()
        pygame.display.set_mode((settings.WIDTH, settings.HEIGHT))
        cls.registry = Registry().load()

    def world(self, strict=True):
        r = self.registry
        return World(r, r.heroes[0], r.weapons[0], strict=strict, seed=3)

    def test_registry_finds_the_starter_kit(self):
        names = {cls.NAME for cls in self.registry.enemies}
        self.assertTrue({"Grunt", "Archer", "Bull"} <= names)
        self.assertFalse(any(cls.NAME == "Unnamed" for cls in self.registry.enemies),
                         "Template files must not be loaded as content.")

    def test_abstract_classes_cannot_be_created(self):
        with self.assertRaises(TypeError):
            Enemy(0, 0)

    def test_damage_and_defeat(self):
        world = self.world()
        enemy = world.spawn_enemy(Dummy, world.arena.topleft)
        self.assertFalse(enemy.take_damage(5, world))
        self.assertEqual(enemy.hp, 15)
        self.assertTrue(enemy.take_damage(50, world))
        world.update(1 / 60, controls.Controls())
        self.assertEqual(world.enemies, [])
        self.assertEqual(world.score, Dummy.SCORE)

    def test_entities_stay_inside_the_arena(self):
        world = self.world()
        enemy = world.spawn_enemy(Dummy, (-500, 9000))
        self.assertTrue(world.arena.collidepoint(enemy.pos))

    def test_hero_is_safe_just_after_a_hit(self):
        world = self.world()
        hero = world.hero
        hero.take_damage(10, world)
        hero.take_damage(10, world)
        self.assertEqual(hero.hp, hero.MAX_HP - 10)

    def test_a_broken_class_is_removed_not_fatal(self):
        world = self.world(strict=False)
        world.spawn_enemy(Broken, world.arena.topleft)
        with contextlib.redirect_stdout(io.StringIO()):     # hide the expected error report
            world.update(1 / 60, controls.Controls())
        self.assertEqual(world.enemies, [])
        self.assertEqual(world.score, 0, "A crashed enemy gives no points.")
        self.assertIn("Broken (made by Tests) crashed", world.crashes[0])

    def test_strict_mode_raises(self):
        world = self.world(strict=True)
        world.spawn_enemy(Broken, world.arena.topleft)
        with self.assertRaises(ZeroDivisionError):
            world.update(1 / 60, controls.Controls())

    def test_waves_grow_and_respect_threat_gates(self):
        world = self.world()
        director = WaveDirector(world)
        first, later = director.build_wave(1), director.build_wave(8)
        self.assertTrue(all(cls.THREAT == 1 for cls in first))
        self.assertLessEqual(sum(cls.THREAT for cls in first), settings.WAVE_BASE_POINTS)
        self.assertGreater(sum(cls.THREAT for cls in later), sum(cls.THREAT for cls in first))

    def test_a_whole_game_plays_without_errors(self):
        game = Game(strict=False, seed=5, bot=True)
        pygame.event.post(pygame.event.Event(pygame.KEYDOWN, key=pygame.K_RETURN))
        game.run(max_frames=60 * 45)
        self.assertNotEqual(type(game.scene).__name__, "MenuScene")
        crashes = game.scene.world.crashes
        self.assertEqual(crashes, [], "\nContent crashed during a full game:\n  " + "\n  ".join(crashes))


if __name__ == "__main__":
    unittest.main()
