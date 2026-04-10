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

    def knockback_logic(self, enemy: Enemy):
        """Apply knockback to an enemy based on weapon position."""
        dist = math.hypot(enemy.x - self.x, enemy.y - self.y)
        if dist > 0:
            kx = (enemy.x - self.x) / dist
            ky = (enemy.y - self.y) / dist
            enemy.x += kx * self.knockback
            enemy.y += ky * self.knockback

    def update(self, dt: float):
        """Update logic for the weapon."""
        pass

    def draw(self, screen: pygame.Surface, camera_offset: tuple[float, float]):
        """Default draw logic."""
        pass
