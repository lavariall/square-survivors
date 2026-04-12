import pygame
from .base_weapon import Weapon

class HealingMagic(Weapon):
    """
    An 'invisible' weapon that heals the owner after a dash.
    It doesn't deal damage or have a physical presence in the world.
    """
    def __init__(self, owner):
        # Position doesn't matter, size 0
        super().__init__(owner.x, owner.y, 0, 0, 0)
        self.owner = owner
        self.active = True

    def on_after_dash(self, dt: float):
        """Heal the owner."""
        heal_amount = getattr(self.owner, "dash_heal_amount", 0.0)
        if heal_amount > 0:
            self.owner.hp = min(self.owner.max_hp, self.owner.hp + heal_amount)

    def update(self, dt: float):
        # Keep position synced with owner (though not strictly necessary for no-op)
        self.x, self.y = self.owner.x, self.owner.y

    def draw(self, screen: pygame.Surface, camera_offset: tuple[float, float]):
        # Invisible
        pass
