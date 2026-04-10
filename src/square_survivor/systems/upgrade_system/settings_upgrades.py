from .base_upgrade import Upgrade, UpgradeManager
from ...entities.player import Player

@UpgradeManager.register
class IncreaseUpgradeChoices(Upgrade):
    name = "Increase Upgrade Choices"
    description = "Increase Upgrade Choices +1 (Max 7)"
    likelihood = 50
    def apply(self, player: Player):
        player.upgrade_choices += 1
        if player.upgrade_choices >= 7:
            self.disable()
