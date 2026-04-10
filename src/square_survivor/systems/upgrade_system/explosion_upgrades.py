from .base_upgrade import Upgrade, UpgradeManager
from ...entities.player import Player

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
class Overcharge(Upgrade):
    name = "Overcharge"
    description = "Attack Delay -20%"
    likelihood = 500
    def apply(self, player: Player):
        player.explosion_cooldown_max *= 0.80
