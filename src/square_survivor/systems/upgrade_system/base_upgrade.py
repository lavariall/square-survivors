import abc
import random
from typing import List, Type
from ...entities.player import Player

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
            if sum(weights) <= 0:
                selected = random.choice(pool)
            else:
                selected = random.choices(pool, weights=weights, k=1)[0]
                
            chosen_types.append(selected)
            pool.remove(selected)
            
        return [c() for c in chosen_types]
