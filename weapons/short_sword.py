"""Ninja Blade: A complex weapon with lifesteal, scaling reach, and an overheat mechanic."""
from core.weapon import Weapon

class ShortSword(Weapon):
    NAME = "Ninja Blade"
    AUTHOR = "Leo"
    DAMAGE = 20
    COOLDOWN = 0.15
    COLOUR = (220, 20, 60) 

    def attack(self, world, owner, direction):
        # 1. Set up a rage meter for the player
        if not hasattr(owner, 'rage_meter'):
            owner.rage_meter = 0
            
        owner.rage_meter += 1

        # 2. Mechanical Change: Increasing Attack
        # The weapon's physical attack distance grows based on your rage meter
        bonus_reach = owner.rage_meter * 3
        self.slash(world, owner, direction, reach=60 + bonus_reach, arc=120)

        # 3. Mechanical Change: Vampire Healing
        # Heal 1 HP every time you swing, but use min() to never go past your max health
        if hasattr(owner, 'health') and hasattr(owner, 'max_health'):
            owner.health = min(owner.health + 1, owner.max_health)

        # 4. Mechanical Change: Overheat / Penalty
        # If the player spams the weapon too much (50 swings), it detonates
        # It resets their rage to 0 and hurts the player
        if owner.rage_meter >= 50:
            owner.rage_meter = 0
            if hasattr(owner, 'health'):
                owner.health -= 20
                print("Overheat! The Ninja Blade burned you!")