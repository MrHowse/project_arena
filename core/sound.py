"""Sound hooks. Silent for now: this file belongs to the Audio squad.

The engine already calls play() at the right moments ("hit", "defeat",
"pickup", "wave", "special", "hurt", "game_over"). Make those names produce
sound and the whole game gains audio without anyone else changing a line.

Rule: sound must never be able to crash the game. A Mac with no audio device
should still run it, so keep everything inside try/except.
"""

ENABLED = False


def play(name):
    """Play the sound with this name. Unknown names are ignored."""
    if not ENABLED:
        return
