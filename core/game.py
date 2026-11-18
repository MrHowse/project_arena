"""Game: the window, the main loop and the scenes (menu, play, game over)."""
import pygame

import settings
from core import controls, sound
from core.hud import draw_hud, text
from core.registry import Registry
from core.waves import WaveDirector
from core.world import World


def draw_arena(surface, arena):
    surface.fill(settings.WALL)
    pygame.draw.rect(surface, settings.SAND, arena)
    for i in range(60):                      # a fixed scatter of darker sand
        x = arena.left + 12 + (i * 137) % (arena.width - 24)
        y = arena.top + 12 + (i * 251) % (arena.height - 24)
        pygame.draw.circle(surface, settings.SAND_DARK, (x, y), 3)
    pygame.draw.rect(surface, settings.INK, arena, 3)


class Scene:
    """A screen of the game. The Game swaps scenes by setting game.scene."""

    def __init__(self, game):
        self.game = game

    def handle(self, event):
        pass

    def update(self, dt):
        pass

    def draw(self, surface):
        pass


class MenuScene(Scene):
    def __init__(self, game):
        super().__init__(game)
        self.hero_index = 0
        self.weapon_index = 0

    def handle(self, event):
        if event.type != pygame.KEYDOWN:
            return
        registry = self.game.registry
        if not registry.heroes or not registry.weapons:
            return
        if event.key in (pygame.K_a, pygame.K_LEFT):
            self.hero_index = (self.hero_index - 1) % len(registry.heroes)
        elif event.key in (pygame.K_d, pygame.K_RIGHT):
            self.hero_index = (self.hero_index + 1) % len(registry.heroes)
        elif event.key in (pygame.K_w, pygame.K_UP):
            self.weapon_index = (self.weapon_index - 1) % len(registry.weapons)
        elif event.key in (pygame.K_s, pygame.K_DOWN):
            self.weapon_index = (self.weapon_index + 1) % len(registry.weapons)
        elif event.key in (pygame.K_RETURN, pygame.K_SPACE):
            hero = registry.heroes[self.hero_index]
            weapon = registry.weapons[self.weapon_index]
            self.game.scene = PlayScene(self.game, hero, weapon)

    def draw(self, surface):
        registry = self.game.registry
        surface.fill(settings.NAVY)
        text(surface, settings.TITLE, (400, 70), 72, settings.GOLD, anchor="center")
        counts = (f"{len(registry.heroes)} heroes   {len(registry.weapons)} weapons   "
                  f"{len(registry.enemies)} enemies   {len(registry.pickups)} pickups")
        text(surface, counts, (400, 125), 22, anchor="center")
        if not registry.heroes or not registry.weapons:
            text(surface, "The game needs at least one hero and one weapon.", (400, 250), 28, anchor="center")
        else:
            hero = registry.heroes[self.hero_index]
            weapon = registry.weapons[self.weapon_index]
            text(surface, "HERO   (A / D to change)", (400, 185), 20, settings.GOLD, anchor="center")
            text(surface, hero.NAME, (400, 220), 44, anchor="center")
            text(surface, f"made by {hero.AUTHOR}", (400, 252), 20, anchor="center")
            text(surface, f"Health {hero.MAX_HP}   Speed {hero.SPEED}   Special: {hero.SPECIAL_NAME}",
                 (400, 278), 20, anchor="center")
            text(surface, "WEAPON   (W / S to change)", (400, 335), 20, settings.GOLD, anchor="center")
            text(surface, weapon.NAME, (400, 370), 44, anchor="center")
            text(surface, f"made by {weapon.AUTHOR}", (400, 402), 20, anchor="center")
            text(surface, f"Damage {weapon.DAMAGE}   Cooldown {weapon.COOLDOWN} s", (400, 428), 20, anchor="center")
            text(surface, "Press ENTER to fight", (400, 490), 32, settings.GOLD, anchor="center")
            text(surface, "Move: W A S D    Aim: mouse    Attack: left click    Special: SPACE    Menu: ESC",
                 (400, 530), 18, anchor="center")
        y = 560
        for file, problem in registry.errors[:3]:
            text(surface, f"Could not load {file}: {problem}"[:110], (400, y), 18, settings.GOLD, anchor="center")
            y += 20


class PlayScene(Scene):
    def __init__(self, game, hero_class, weapon_class):
        super().__init__(game)
        self.world = World(game.registry, hero_class, weapon_class, strict=game.strict, seed=game.seed)
        self.director = WaveDirector(self.world)

    def handle(self, event):
        if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
            self.game.scene = MenuScene(self.game)

    def update(self, dt):
        world = self.world
        world.update(dt, self.game.read_controls(world))
        self.director.update(dt)
        if not world.hero.alive:
            sound.play("game_over")
            self.game.scene = GameOverScene(self.game, world)

    def draw(self, surface):
        draw_arena(surface, self.world.arena)
        self.world.draw(surface)
        draw_hud(surface, self.world)


class GameOverScene(Scene):
    def __init__(self, game, world):
        super().__init__(game)
        self.world = world

    def handle(self, event):
        if event.type == pygame.KEYDOWN and event.key in (pygame.K_RETURN, pygame.K_ESCAPE):
            self.game.scene = MenuScene(self.game)

    def draw(self, surface):
        world = self.world
        surface.fill(settings.NAVY)
        text(surface, "Defeated", (400, 130), 72, settings.RED, anchor="center")
        killer = world.hero.last_hit_by
        if killer is not None:
            text(surface, f"by {killer.NAME}, made by {killer.AUTHOR}", (400, 190), 26, anchor="center")
        text(surface, f"You reached wave {world.wave}", (400, 270), 34, anchor="center")
        text(surface, f"Score {world.score}   Enemies defeated {world.defeated}",
             (400, 310), 26, settings.GOLD, anchor="center")
        y = 380
        for line in world.crashes[:4]:
            text(surface, line[:105], (400, y), 18, settings.GOLD, anchor="center")
            y += 22
        text(surface, "Press ENTER for the menu", (400, 540), 26, anchor="center")


class Game:
    def __init__(self, strict=False, seed=None, bot=False):
        pygame.init()
        self.screen = pygame.display.set_mode((settings.WIDTH, settings.HEIGHT))
        pygame.display.set_caption(settings.TITLE)
        self.clock = pygame.time.Clock()
        self.strict = strict
        self.seed = seed
        self.bot = bot                  # True: the computer plays (used by the tests)
        self.registry = Registry().load()
        for file, problem in self.registry.errors:
            print(f"COULD NOT LOAD {file}: {problem}")
        self.scene = MenuScene(self)
        self.running = True

    def read_controls(self, world):
        return controls.read_bot(world) if self.bot else controls.read_player()

    def run(self, max_frames=None):
        frames = 0
        while self.running and (max_frames is None or frames < max_frames):
            dt = 1 / settings.FPS if self.bot else min(self.clock.tick(settings.FPS) / 1000, 0.05)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                else:
                    self.scene.handle(event)
            self.scene.update(dt)
            self.scene.draw(self.screen)
            pygame.display.flip()
            frames += 1
        return frames
