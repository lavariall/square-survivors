import pygame
from math import hypot
from .base_entity import Entity
from ..constants import ENEMY_COLOR

class Enemy(Entity):
    def __init__(self, x: float, y: float, hp: float, speed: float, damage: float, is_elite: bool = False):
        super().__init__(x, y, 30 if is_elite else 20)
        self.max_hp = hp
        self.hp = hp
        self.speed = speed
        self.damage = damage
        self.is_elite = is_elite

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
        from ..constants import ELITE_COLOR
        
        render_x = int(self.x - camera_offset[0] - self.size/2)
        render_y = int(self.y - camera_offset[1] - self.size/2)
        
        color = ELITE_COLOR if self.is_elite else ENEMY_COLOR
        pygame.draw.rect(screen, color, (render_x, render_y, self.size, self.size))
        
        if self.is_elite:
            # Draw white border for elites
            pygame.draw.rect(screen, (255, 255, 255), (render_x, render_y, self.size, self.size), 2)

if __name__ == "__main__":
    e = Enemy(0, 0, 10, 50, 5)
    e.update(0.1, 10, 0)
    print("Enemy moved to:", e.x, e.y)
