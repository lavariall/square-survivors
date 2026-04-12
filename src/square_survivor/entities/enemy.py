import pygame
from math import hypot
from .base_entity import Entity
from ..core.config_manager import ConfigManager

class Enemy(Entity):
    def __init__(self, x: float, y: float, hp: float, speed: float, damage: float, armor: float = 0.0, is_elite: bool = False, type_name: str = "basic"):
        self.type_name = type_name
        self.config = ConfigManager.get_instance().enemies.enemy_types.get(type_name, 
                      ConfigManager.get_instance().enemies.enemy_types["basic"])
                      
        size = self.config.size_elite if is_elite else self.config.size_normal
        super().__init__(x, y, size)
        
        self.max_hp = hp
        self.hp = hp
        self.speed = speed
        self.damage = damage
        self.armor = armor
        self.is_elite = is_elite
        self.xp_value = self.config.xp_value

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
        
        color = self.config.color_elite if self.is_elite else self.config.color_normal
        pygame.draw.rect(screen, color, (render_x, render_y, self.size, self.size))
        
        if self.is_elite:
            # Draw white border for elites
            pygame.draw.rect(screen, (255, 255, 255), (render_x, render_y, self.size, self.size), 2)

if __name__ == "__main__":
    e = Enemy(0, 0, 10, 50, 5)
    e.update(0.1, 10, 0)
    print("Enemy moved to:", e.x, e.y)
