import pygame
import math
from ..base_entity import Entity
from ..enemy import Enemy

class Weapon(Entity):
    """Base class for all materialized weapons."""
    def __init__(self, x: float, y: float, size: float, damage: float, knockback: float = 0):
        super().__init__(x, y, size)
        self.damage = damage
        self.knockback = knockback

    def knockback_logic(self, enemy: Enemy, source: Entity = None):
        """Apply knockback to an enemy based on source position (defaults to self)."""
        ref = source if source else self
        dist = math.hypot(enemy.x - ref.x, enemy.y - ref.y)
        if dist > 0:
            kx = (enemy.x - ref.x) / dist
            ky = (enemy.y - ref.y) / dist
            enemy.x += kx * self.knockback
            enemy.y += ky * self.knockback

    def update(self, dt: float):
        """Update logic for the weapon."""
        pass
        
    def on_after_dash(self, dt: float):
        """Standardized hook called by the player after a dash."""
        pass

    def draw(self, screen: pygame.Surface, camera_offset: tuple[float, float]):
        """Default draw logic."""
        pass
