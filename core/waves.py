"""WaveDirector: decides which enemies arrive, and when.

This file belongs to the Waves squad. The version here is deliberately plain:
each wave has a number of threat points to spend, and it spends them on
random enemies. Making waves feel designed is the squad's job.
"""
import settings
from core import sound


class WaveDirector:
    def __init__(self, world):
        self.world = world
        self.queue = []                     # enemy classes still to arrive
        self.spawn_timer = 0.0
        self.break_timer = 1.5              # a short pause before wave 1

    def update(self, dt):
        world = self.world
        if self.queue:
            self.spawn_timer -= dt
            if self.spawn_timer <= 0:
                world.spawn_enemy(self.queue.pop(0))
                self.spawn_timer = settings.SPAWN_GAP
        elif not world.enemies:
            self.break_timer -= dt
            if self.break_timer <= 0:
                self.start_next_wave()

    def start_next_wave(self):
        world = self.world
        world.wave += 1
        self.queue = self.build_wave(world.wave)
        self.spawn_timer = 0.0
        self.break_timer = settings.WAVE_BREAK
        sound.play("wave")
        world.say(f"Wave {world.wave}: {len(self.queue)} enemies")

    def allowed(self, wave):
        """The ordinary enemy classes that may appear in this wave."""
        top = 1
        if wave >= settings.THREAT_2_FROM_WAVE:
            top = 2
        if wave >= settings.THREAT_3_FROM_WAVE:
            top = 3
        return [cls for cls in self.world.registry.enemies if cls.THREAT <= top]

    def build_wave(self, wave):
        """Return the list of enemy classes for a wave, in arrival order."""
        world = self.world
        points = settings.WAVE_BASE_POINTS + settings.WAVE_GROWTH * (wave - 1)
        choices = self.allowed(wave)
        queue = []
        while choices and points > 0:
            affordable = [cls for cls in choices if cls.THREAT <= points]
            if not affordable:
                break
            pick = world.random.choice(affordable)
            queue.append(pick)
            points -= pick.THREAT
        bosses = [cls for cls in world.registry.enemies if cls.THREAT == 4]
        if bosses and wave % settings.BOSS_EVERY == 0:
            queue.append(world.random.choice(bosses))
        return queue
