"""Finds every enemy, hero, weapon and pickup by looking in the content folders.

This is why nobody has to edit a shared list to add their class: save a file
in the right folder and the game discovers it the next time it starts.
"""
import importlib
import inspect
import pathlib

from core.enemy import Enemy
from core.hero import Hero
from core.pickup import Pickup
from core.weapon import Weapon

ROOT = pathlib.Path(__file__).resolve().parent.parent
FOLDERS = {"enemies": Enemy, "heroes": Hero, "weapons": Weapon, "pickups": Pickup}


class Registry:
    def __init__(self):
        self.enemies, self.heroes, self.weapons, self.pickups = [], [], [], []
        self.errors = []        # (file, message) for anything that failed to load

    def problem(self, label, message):
        if (label, message) not in self.errors:
            self.errors.append((label, message))

    def load(self):
        for folder, base in FOLDERS.items():
            found = []
            for path in sorted((ROOT / folder).glob("*.py")):
                if path.name.startswith("_"):
                    continue    # files starting with _ are templates, not content
                found.extend(self.load_file(folder, path, base))
            setattr(self, folder, sorted(found, key=lambda cls: cls.NAME.lower()))
        return self

    def load_file(self, folder, path, base):
        label = f"{folder}/{path.name}"
        try:
            module = importlib.import_module(f"{folder}.{path.stem}")
        except Exception as error:      # a broken file must not stop the game
            self.problem(label, f"{type(error).__name__}: {error}")
            return []
        found = []
        for _, cls in inspect.getmembers(module, inspect.isclass):
            if cls.__module__ != module.__name__ or not issubclass(cls, base):
                continue
            if inspect.isabstract(cls):
                missing = ", ".join(sorted(cls.__abstractmethods__))
                self.problem(label, f"{cls.__name__} is missing: {missing}()")
                continue
            found.append(cls)
        if not found and not any(file == label for file, _ in self.errors):
            self.problem(label, f"no {base.__name__} class found in this file")
        return found

    def classes_in(self, path):
        """Load one file by path. Used by the sandbox."""
        path = pathlib.Path(path).resolve()
        folder = path.parent.name
        if folder not in FOLDERS:
            raise SystemExit(f"{path.name} must be inside one of: {', '.join(FOLDERS)}")
        return folder, self.load_file(folder, path, FOLDERS[folder])
