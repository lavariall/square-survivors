import pygame
from .base_weapon import Weapon

class SprintMagic(Weapon):
    """
    An 'invisible' weapon that increases the owner's movement speed after a dash.
    """
    def __init__(self, owner):
        super().__init__(owner.x, owner.y, 0, 0, 0)
        self.owner = owner
        self.active = True
        self.boost_timer = 0.0

    def on_after_dash(self, dt: float):
        """Trigger the sprint boost."""
        self.boost_timer = getattr(self.owner, "dash_sprint_duration", 1.0)

    def update(self, dt: float):
        if self.boost_timer > 0:
            self.boost_timer -= dt
            self.owner.move_speed_modifier = getattr(self.owner, "dash_sprint_boost", 1.5)
        else:
            # Only reset if we were the one who set it (simple version)
            # In a more complex system, we'd use a stack or list of multipliers
            if self.owner.move_speed_modifier > 1.0:
                 self.owner.move_speed_modifier = 1.0
        
        self.x, self.y = self.owner.x, self.owner.y

    def draw(self, screen: pygame.Surface, camera_offset: tuple[float, float]):
        pass
