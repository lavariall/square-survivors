import abc
import random
from typing import List, Type
from ..entities.player import Player

class Upgrade(abc.ABC):
    """Abstract base class for all upgrades."""
    
    _available = True
    likelihood = 100 # Default weight for random selection

    @classmethod
    def enable(cls):
        cls._available = True

    @classmethod
    def disable(cls):
        cls._available = False

    @classmethod
    def is_available(cls, player: Player) -> bool:
        return cls._available

    @property
    @abc.abstractmethod
    def name(self) -> str:
        pass

    @property
    @abc.abstractmethod
    def description(self) -> str:
        pass

    @abc.abstractmethod
    def apply(self, player: Player):
        """Applies the upgrade logic to the player."""
        pass


class UpgradeManager:
    """Registry pattern to keep track of all available upgrades seamlessly."""
    
    _registry: List[Type[Upgrade]] = []

    @classmethod
    def register(cls, upgrade_cls: Type[Upgrade]):
        cls._registry.append(upgrade_cls)
        return upgrade_cls

    @classmethod
    def get_random_choices(cls, player: Player, count: int = 3) -> List[Upgrade]:
        if not cls._registry:
            return []
        
        available = [u for u in cls._registry if u.is_available(player)]
        if not available:
            return []

        # Weighted sampling without replacement
        num_to_pick = min(count, len(available))
        chosen_types = []
        pool = list(available)
        
        for _ in range(num_to_pick):
            weights = [u.likelihood for u in pool]
            # Use random.choices to pick one weighted element
            # pool might contain elements with 0 likelihood, handle gracefully
            if sum(weights) <= 0:
                # Fallback to uniform if all weights are zero
                selected = random.choice(pool)
            else:
                selected = random.choices(pool, weights=weights, k=1)[0]
                
            chosen_types.append(selected)
            pool.remove(selected)
            
        return [c() for c in chosen_types]


# --- Definitions of actual Upgrades ---
@UpgradeManager.register
class BlastCore(Upgrade):
    name = "Blast Core"
    description = "Explosion Damage +20%"
    likelihood = 50
    def apply(self, player: Player):
        player.explosion_damage *= 1.2

@UpgradeManager.register
class WideArea(Upgrade):
    name = "Wide Area"
    description = "Explosion Radius +20%"
    likelihood = 500
    def apply(self, player: Player):
        player.explosion_radius *= 1.2

@UpgradeManager.register
class Forceful(Upgrade):
    name = "Forceful"
    description = "Explosion Knockback +50%"
    likelihood = 50
    def apply(self, player: Player):
        player.explosion_knockback *= 1.5

@UpgradeManager.register
class Agility(Upgrade):
    name = "Agility"
    description = "Dash Cooldown -40%"
    likelihood = 50
    def apply(self, player: Player):
        player.dash_cooldown_max *= 0.60

@UpgradeManager.register
class Endurance(Upgrade):
    name = "Endurance"
    description = "Max HP +25"
    likelihood = 50
    def apply(self, player: Player):
        player.max_hp += 25
        player.hp += 25

@UpgradeManager.register
class HealthRegen(Upgrade):
    name = "Health Regen"
    description = "Health Regen +3/sec"
    likelihood = 500
    def apply(self, player: Player):
        player.health_regen += 3

@UpgradeManager.register
class Overcharge(Upgrade):
    name = "Overcharge"
    description = "Attack Delay -20%"
    likelihood = 500
    def apply(self, player: Player):
        player.explosion_cooldown_max *= 0.80

@UpgradeManager.register
class Swiftness(Upgrade):
    name = "Swiftness"
    description = "Move Speed +10%"
    likelihood = 200
    def apply(self, player: Player):
        player.base_speed *= 1.1

@UpgradeManager.register
class Magnetism(Upgrade):
    name = "Magnetism"
    description = "Pickup Radius +50%"
    likelihood = 500
    def apply(self, player: Player):
        player.pickup_radius *= 1.5

@UpgradeManager.register
class DashMaster(Upgrade):
    name = "Dash Master"
    description = "Dash Distance +20%"
    likelihood = 50
    def apply(self, player: Player):
        player.dash_distance *= 1.2

@UpgradeManager.register
class IncreaseUpgradeChoices(Upgrade):
    name = "Increase Upgrade Choices"
    description = "Increase Upgrade Choices +1"
    likelihood = 50
    def apply(self, player: Player):
        player.upgrade_choices += 1
        if player.upgrade_choices >= 7:
            self.disable()

if __name__ == "__main__":
    player = Player()
    # Test weighted selection by making one upgrade super likely
    WideArea.likelihood = 10000 
    print("Testing weighted selection (WideArea likelihood set to 10000):")
    choices = UpgradeManager.get_random_choices(player, 3)
    for c in choices:
        print(f" - {c.name}")
    
    # Reset for next tests
    Swiftness.likelihood = 100
    print("\nModified Player Upgrade Choices:", player.upgrade_choices)
