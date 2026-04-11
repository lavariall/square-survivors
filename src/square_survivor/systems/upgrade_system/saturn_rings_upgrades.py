from .base_upgrade import Upgrade, UpgradeManager
from ...entities.player import Player

@UpgradeManager.register
class RingDensity(Upgrade):
    name = "Ring Density"
    description = "Increases Saturn Square count by 1 (Max 7)"
    likelihood = 500
    def apply(self, player: Player):
        player.saturn_squares_count += 1
        if player.saturn_squares_count >= 7:
            self.disable()

@UpgradeManager.register
class ReinforcedSquares(Upgrade):
    name = "Reinforced Squares"
    description = "Saturn Squares HP +50%"
    likelihood = 100
    def apply(self, player: Player):
        player.saturn_squares_hp *= 1.5

@UpgradeManager.register
class LethalSpin(Upgrade):
    name = "Lethal Spin"
    description = "Saturn Squares Damage +30%"
    likelihood = 100
    def apply(self, player: Player):
        player.saturn_squares_damage *= 1.3

@UpgradeManager.register
class EternalSpin(Upgrade):
    name = "Eternal Spin"
    description = "Saturn Squares lifespan decrease turned off"
    likelihood = 200
    def apply(self, player: Player):
        player.saturn_squares_lifespan_active = False
        self.disable()

@UpgradeManager.register
class GiantRings(Upgrade):
    name = "Giant Rings"
    description = "Saturn Squares size +50%"
    likelihood = 100
    def apply(self, player: Player):
        player.saturn_squares_size *= 1.5
        self.disable()
