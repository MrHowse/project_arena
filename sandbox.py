"""Test ONE class by itself, without waiting for it to turn up in a wave.

    python3 sandbox.py enemies/grunt.py
    python3 sandbox.py heroes/gladiator.py
    python3 sandbox.py weapons/short_sword.py
    python3 sandbox.py pickups/health_potion.py

Keys:  N = spawn another    R = reset    ESC = quit
The sandbox is strict: if your code has an error it stops and shows you where.
"""
import sys

import pygame

import settings
from core import controls
from core.game import Game, Scene, draw_arena
from core.hud import draw_hud, text
from core.world import World


def describe(folder, cls):
    """Print the stats and the fairness check for one class."""
    print(f"\n{cls.NAME}  (made by {cls.AUTHOR})  from {folder}/")
    if folder == "enemies":
        cost, budget = cls.cost(), cls.budget()
        verdict = "OK" if cost <= budget else "OVER BUDGET"
        print(f"  THREAT {cls.THREAT}   health {cls.MAX_HP}   speed {cls.SPEED}   damage {cls.DAMAGE}")
        print(f"  cost {cost:.1f} of {budget} points: {verdict}")
    elif folder == "heroes":
        cost = cls.cost()
        verdict = "OK" if cost <= settings.HERO_BUDGET else "OVER BUDGET"
        print(f"  health {cls.MAX_HP}   speed {cls.SPEED}   special every {cls.SPECIAL_COOLDOWN} s")
        print(f"  cost {cost:.1f} of {settings.HERO_BUDGET} points: {verdict}")
    elif folder == "weapons":
        verdict = "OK" if cls.dps() <= settings.WEAPON_MAX_DPS else "TOO STRONG"
        print(f"  damage {cls.DAMAGE}   cooldown {cls.COOLDOWN} s")
        print(f"  {cls.dps():.0f} damage per second of {settings.WEAPON_MAX_DPS} allowed: {verdict}")


class SandboxScene(Scene):
    def __init__(self, game, folder, cls):
        super().__init__(game)
        self.folder, self.cls = folder, cls
        self.reset()

    def pick(self, group, wanted):
        """Use the class being tested if it belongs to this group, else the first one."""
        if self.folder == wanted:
            return self.cls
        if not group:
            raise SystemExit(f"The sandbox needs at least one class in {wanted}/")
        return group[0]

    def reset(self):
        registry = self.game.registry
        hero = self.pick(registry.heroes, "heroes")
        weapon = self.pick(registry.weapons, "weapons")
        self.world = World(registry, hero, weapon, strict=True, seed=self.game.seed)
        self.spawn()

    def spawn(self):
        world, registry = self.world, self.game.registry
        if self.folder == "enemies":
            world.spawn_enemy(self.cls)
        elif self.folder == "pickups":
            world.hero.hp = max(1, world.hero.MAX_HP // 2)
            world.spawn_pickup(self.cls, world.hero.pos + (120, 0))
        else:
            for _ in range(3):
                world.spawn_enemy(self.pick(registry.enemies, "enemies"))

    def handle(self, event):
        if event.type != pygame.KEYDOWN:
            return
        if event.key == pygame.K_ESCAPE:
            self.game.running = False
        elif event.key == pygame.K_n:
            self.spawn()
        elif event.key == pygame.K_r:
            self.reset()

    def update(self, dt):
        self.world.update(dt, self.game.read_controls(self.world))
        if not self.world.hero.alive:
            self.reset()

    def draw(self, surface):
        draw_arena(surface, self.world.arena)
        self.world.draw(surface)
        draw_hud(surface, self.world)
        text(surface, f"SANDBOX: {self.cls.NAME}    N = spawn another    R = reset    ESC = quit",
             (400, settings.HEIGHT - 26), 20, settings.GOLD, anchor="midtop")


def run(path, max_frames=None, bot=False, seed=None):
    game = Game(strict=True, seed=seed, bot=bot)
    folder, classes = game.registry.classes_in(path)
    problems = [p for file, p in game.registry.errors if file.endswith(path.replace("\\", "/").split("/")[-1])]
    if not classes:
        for problem in problems:
            print("PROBLEM:", problem)
        raise SystemExit(f"No working class found in {path}. Fix the problem above and try again.")
    for cls in classes:
        describe(folder, cls)
    game.scene = SandboxScene(game, folder, classes[0])
    return game.run(max_frames)


if __name__ == "__main__":
    if len(sys.argv) < 2:
        raise SystemExit(__doc__)
    run(sys.argv[1])
