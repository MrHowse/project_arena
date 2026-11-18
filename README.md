# Project Arena

A top-down gladiator arena built by thirteen people at once. Pick a hero and a
weapon, then survive as many waves as you can. Every enemy, hero, weapon and
pickup is one file written by one person.

"Project Arena" is a placeholder. Naming the game is the team's first decision.

## Play

    python3 -m pip install -r requirements.txt
    python3 main.py

Move with W A S D, aim with the mouse, attack with the left mouse button,
use your special with SPACE. ESC returns to the menu.

## Test one class by itself

    python3 sandbox.py enemies/grunt.py

## Run the tests

    python3 -m unittest

## Where things live

| Folder or file | What is in it | Who changes it |
|---|---|---|
| `enemies/` `heroes/` `weapons/` `pickups/` | One file per class | The person who wrote the file |
| `settings.py` | Every number the team might tune | Anyone, in a small pull request that says why |
| `core/` | The engine | Systems jobs, with a maintainer's review |
| `tests/` | The checks every class must pass | Maintainers |
| `sandbox.py` `main.py` | The two ways to run the game | Maintainers |
| `CREDITS.md` | Who built what | Everyone |

How to contribute is in [CONTRIBUTING.md](CONTRIBUTING.md).
What a class can ask the game to do is in [docs/API.md](docs/API.md).
