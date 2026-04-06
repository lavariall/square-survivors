import pygame
from math import hypot
from .base_entity import Entity
from ..constants import DANGER

class Enemy(Entity):
    def __init__(self, x: float, y: float, hp: float, speed: float, damage: float):
        super().__init__(x, y, 20)
        self.max_hp = hp
        self.hp = hp
        self.speed = speed
        self.damage = damage

    def update(self, dt: float, target_x: float, target_y: float):
        if not self.active: return
        
        dx = target_x - self.x
        dy = target_y - self.y
        dist = hypot(dx, dy)
        
        if dist > 0:
            self.x += (dx / dist) * self.speed * dt
            self.y += (dy / dist) * self.speed * dt

    def draw(self, screen: pygame.Surface, camera_offset: tuple[float, float]):
        if not self.active: return
        render_x = int(self.x - camera_offset[0] - self.size/2)
        render_y = int(self.y - camera_offset[1] - self.size/2)
        pygame.draw.rect(screen, DANGER, (render_x, render_y, self.size, self.size))

if __name__ == "__main__":
    e = Enemy(0, 0, 10, 50, 5)
    e.update(0.1, 10, 0)
    print("Enemy moved to:", e.x, e.y)
