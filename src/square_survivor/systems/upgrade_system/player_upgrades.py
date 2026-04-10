from .base_upgrade import Upgrade, UpgradeManager
from ...entities.player import Player

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
class ExperienceBooster(Upgrade):
    name = "Experience Booster"
    description = "Experience Booster +25%"
    likelihood = 200
    def apply(self, player: Player):
        player.experience_booster *= 1.25
