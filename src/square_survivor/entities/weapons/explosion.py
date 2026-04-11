import pygame
from .base_weapon import Weapon
from ...core.config_manager import ConfigManager

class Explosion(Weapon):
    def __init__(self, x: float, y: float, max_radius: float, damage: float, knockback: float, duration: float = 0.3):
        super().__init__(x, y, max_radius * 2, damage, knockback)
        self.max_radius = max_radius
        self.duration = duration
        self.timer = 0.0
        
        # Sprite setup
        self.image = pygame.Surface((max_radius * 2, max_radius * 2), pygame.SRCALPHA)
        self.rect = self.image.get_rect()
        self.rect.center = (int(x), int(y))

    def update(self, dt: float):
        self.timer += dt
        if self.timer >= self.duration:
            self.kill()
            self.active = False
            
        # Update current size for collision (rect grows)
        progress = self.timer / self.duration
        current_size = self.max_radius * 2 * progress
        self.rect.width = int(current_size)
        self.rect.height = int(current_size)
        self.rect.center = (int(self.x), int(self.y))

    def draw(self, screen: pygame.Surface, camera_offset: tuple[float, float]):
        progress = self.timer / self.duration
        current_size = self.max_radius * 2 * progress
        
        render_x = int(self.x - camera_offset[0] - current_size / 2)
        render_y = int(self.y - camera_offset[1] - current_size / 2)
        
        # Transparent explosion square
        alpha = int(255 * (1.0 - progress))
        base_color = ConfigManager.get_instance().ui.explosion_color
        color = (base_color[0], base_color[1], base_color[2], alpha)
        
        temp_surface = pygame.Surface((current_size, current_size), pygame.SRCALPHA)
        pygame.draw.rect(temp_surface, color, (0, 0, current_size, current_size), 2)
        screen.blit(temp_surface, (render_x, render_y))
