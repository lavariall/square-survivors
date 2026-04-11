import abc
import random
from typing import List, Type, Union
from ...entities.player import Player
from ...models.upgrade_models import UpgradeDefinition, UpgradeEffect

class Upgrade(abc.ABC):
    """Abstract base class for all upgrades."""
    
    def __init__(self):
        self._available = True
        self.likelihood = 100

    def enable(self):
        self._available = True

    def disable(self):
        self._available = False

    def is_available(self, player: Player) -> bool:
        return self._available

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


class DataDrivenUpgrade(Upgrade):
    """Generic upgrade implementation that follows the Type Object pattern."""
    
    def __init__(self, key: str, definition: UpgradeDefinition):
        super().__init__()
        self.key = key
        self.definition = definition
        self._available = definition.is_active
        self.likelihood = definition.likelihood

    @property
    def name(self) -> str:
        return self.definition.name

    @property
    def description(self) -> str:
        return self.definition.description

    def is_available(self, player: Player) -> bool:
        if not super().is_available(player):
            return False
            
        # Check limits if defined
        if self.definition.limit:
            current_val = getattr(player, self.definition.limit.stat, 0)
            if current_val >= self.definition.limit.value:
                return False
                
        return True

    def apply(self, player: Player):
        for effect in self.definition.effects:
            if not hasattr(player, effect.stat):
                print(f"[Upgrade] Warning: Player does not have attribute '{effect.stat}'")
                continue
                
            current_val = getattr(player, effect.stat)
            
            if effect.op == "add":
                setattr(player, effect.stat, current_val + effect.value)
            elif effect.op == "mul":
                setattr(player, effect.stat, current_val * effect.value)
            elif effect.op == "set":
                setattr(player, effect.stat, effect.value)
        
        # Post-application logic
        if self.definition.one_time:
            self.disable()
            
        if self.definition.limit:
            new_val = getattr(player, self.definition.limit.stat)
            if new_val >= self.definition.limit.value:
                self.disable()


class UpgradeManager:
    """Registry pattern to keep track of all available upgrades seamlessly."""
    
    _registry: List[Upgrade] = []

    @classmethod
    def register(cls, upgrade: Union[Type[Upgrade], Upgrade]):
        """Registers an upgrade class or instance."""
        if isinstance(upgrade, type):
            # Support for legacy class-based registration if needed
            cls._registry.append(upgrade())
        else:
            cls._registry.append(upgrade)
        return upgrade

    @classmethod
    def initialize_from_config(cls, upgrades_config):
        """Populates the registry from the loaded configuration categories."""
        cls._registry.clear()
        for category, upgrades in upgrades_config.categories.items():
            for key, definition in upgrades.items():
                if definition.is_active:
                    cls.register(DataDrivenUpgrade(key, definition))

    @classmethod
    def get_random_choices(cls, player: Player, count: int = 3) -> List[Upgrade]:
        if not cls._registry:
            return []
        
        available = [u for u in cls._registry if u.is_available(player)]
        if not available:
            return []

        # Weighted sampling without replacement
        num_to_pick = min(count, len(available))
        chosen = []
        pool = list(available)
        
        for _ in range(num_to_pick):
            weights = [u.likelihood for u in pool]
            if sum(weights) <= 0:
                selected = random.choice(pool)
            else:
                selected = random.choices(pool, weights=weights, k=1)[0]
                
            chosen.append(selected)
            pool.remove(selected)
            
        return chosen
