"""The heads-up display: health, wave, score and the message feed.

This file belongs to the HUD squad. It works, and it is plain on purpose.
"""
import pygame

import settings
from core.effects import font


def text(surface, words, pos, size=24, colour=settings.WHITE, anchor="topleft"):
    """Draw words on the screen. Returns the rectangle they filled."""
    image = font(size).render(str(words), True, colour)
    box = image.get_rect(**{anchor: pos})
    surface.blit(image, box)
    return box


def bar(surface, box, fraction, colour, back=settings.INK):
    """Draw a bar that is `fraction` full (0.0 to 1.0)."""
    box = pygame.Rect(box)
    pygame.draw.rect(surface, back, box)
    fill = box.copy()
    fill.width = int(box.width * max(0.0, min(1.0, fraction)))
    pygame.draw.rect(surface, colour, fill)
    pygame.draw.rect(surface, settings.WHITE, box, 2)


def draw_hud(surface, world):
    hero = world.hero
    pygame.draw.rect(surface, settings.NAVY, (0, 0, settings.WIDTH, 70))

    text(surface, hero.NAME, (40, 10), 22, settings.GOLD)
    bar(surface, (40, 32, 200, 16), hero.hp / hero.MAX_HP, settings.RED)
    text(surface, f"{int(hero.hp)} / {hero.MAX_HP}", (140, 40), 18, anchor="center")

    ready = 1 - hero.special_timer / hero.SPECIAL_COOLDOWN
    text(surface, f"{hero.SPECIAL_NAME} [SPACE]", (270, 10), 22, settings.GOLD)
    bar(surface, (270, 32, 150, 16), ready, settings.GOLD if ready >= 1 else settings.GREEN)

    weapon = hero.weapon.NAME if hero.weapon else "None"
    text(surface, "Weapon", (450, 10), 22, settings.GOLD)
    text(surface, weapon, (450, 32), 22)

    text(surface, f"Wave {world.wave}", (760, 10), 26, anchor="topright")
    text(surface, f"Score {world.score}", (760, 38), 22, settings.GOLD, anchor="topright")

    # The message feed sits in the strip below the arena. Newest line last.
    y = settings.HEIGHT - 26
    for words, seconds in world.messages[-1:]:
        text(surface, words, (40, y), 20, settings.WHITE)
    if world.crashes:
        text(surface, f"{len(world.crashes)} content error(s): see the terminal",
             (760, y), 20, settings.GOLD, anchor="topright")
