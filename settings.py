"""Every number the whole team might want to tune lives here.

Change a value, run the game, see what happens. Because everyone shares this
file, change it in its own small pull request and say why in the description.
"""

TITLE = "Project Arena"          # Team decision 1: give the game a real name.

WIDTH, HEIGHT = 800, 640
FPS = 60

# The sand the fight happens on: (left, top, width, height) in pixels.
ARENA = (40, 80, 720, 520)

# Colours are (red, green, blue), each 0 to 255.
SAND = (214, 186, 132)
SAND_DARK = (196, 166, 112)
WALL = (92, 62, 44)
INK = (35, 31, 32)
WHITE = (255, 255, 255)
NAVY = (0, 24, 68)
GOLD = (252, 175, 23)
RED = (227, 27, 34)
GREEN = (84, 137, 48)

# ---- Fair play: the stat budget -------------------------------------------
# An enemy's cost is worked out from its stats (see Enemy.cost in core/enemy.py).
# A THREAT 1 enemy may cost up to 14 points, THREAT 2 up to 22, THREAT 3 up to 32.
# THREAT 4 is a boss: one arrives at the end of every BOSS_EVERY-th wave.
ENEMY_BUDGET = {1: 14, 2: 22, 3: 32, 4: 70}
HERO_BUDGET = 28                 # see Hero.cost in core/hero.py
WEAPON_MAX_DPS = 60              # damage per second, see Weapon.dps in core/weapon.py

# ---- Waves (owned by the Waves squad) -------------------------------------
WAVE_BASE_POINTS = 4             # threat points available in wave 1
WAVE_GROWTH = 3                  # extra threat points each wave after that
WAVE_BREAK = 3.0                 # seconds of calm between waves
SPAWN_GAP = 0.9                  # seconds between enemies arriving
THREAT_2_FROM_WAVE = 3           # tougher enemies are held back until these waves
THREAT_3_FROM_WAVE = 6
BOSS_EVERY = 5                   # a boss (THREAT 4) joins every 5th wave, if one exists
PICKUP_DROP_CHANCE = 0.18        # chance a defeated enemy drops a pickup
