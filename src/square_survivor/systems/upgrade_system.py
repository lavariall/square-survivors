import abc
import random
from typing import List, Type
from ..entities.player import Player

class Upgrade(abc.ABC):
    """Abstract base class for all upgrades."""
    
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
    def get_random_choices(cls, count: int = 3) -> List[Upgrade]:
        if not cls._registry:
            return []
        choices = random.sample(cls._registry, min(count, len(cls._registry)))
        return [c() for c in choices]


# --- Definitions of actual Upgrades ---
@UpgradeManager.register
class BlastCore(Upgrade):
    name = "Blast Core"
    description = "Explosion Damage +20%"
    def apply(self, player: Player):
        player.explosion_damage *= 1.2

@UpgradeManager.register
class WideArea(Upgrade):
    name = "Wide Area"
    description = "Explosion Radius +20%"
    def apply(self, player: Player):
        player.explosion_radius *= 1.2

@UpgradeManager.register
class Forceful(Upgrade):
    name = "Forceful"
    description = "Explosion Knockback +50%"
    def apply(self, player: Player):
        player.explosion_knockback *= 1.5

@UpgradeManager.register
class Agility(Upgrade):
    name = "Agility"
    description = "Dash Cooldown -15%"
    def apply(self, player: Player):
        player.dash_cooldown_max *= 0.85

@UpgradeManager.register
class Endurance(Upgrade):
    name = "Endurance"
    description = "Max HP +20"
    def apply(self, player: Player):
        player.max_hp += 20
        player.hp += 20

@UpgradeManager.register
class Overcharge(Upgrade):
    name = "Overcharge"
    description = "Attack Delay -15%"
    def apply(self, player: Player):
        player.explosion_cooldown_max *= 0.85

@UpgradeManager.register
class Swiftness(Upgrade):
    name = "Swiftness"
    description = "Move Speed +10%"
    def apply(self, player: Player):
        player.base_speed *= 1.1

@UpgradeManager.register
class Magnetism(Upgrade):
    name = "Magnetism"
    description = "Pickup Radius +50%"
    def apply(self, player: Player):
        player.pickup_radius *= 1.5

if __name__ == "__main__":
    player = Player()
    choices = UpgradeManager.get_random_choices(2)
    print("Sample generated upgrades:")
    for c in choices:
        print(f" - {c.name}: {c.description}")
        c.apply(player)
    print("Modified Player HP:", player.max_hp)
