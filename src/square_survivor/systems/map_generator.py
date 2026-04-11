import pygame
import random
from typing import List
from ..core.config_manager import ConfigManager

class MapGenerator:
    """Procedural Map Generation System."""
    
    def __init__(self, density: float = 0.05):
        self.obstacles: List[pygame.Rect] = []
        self.density = density

    def generate(self, safe_zone_center: tuple[float, float], safe_radius: float = 200.0):
        config = ConfigManager.get_instance().world
        tiles_line = config.map_size // config.tile_size
        self.obstacles.clear()

        for i in range(tiles_line):
            for j in range(tiles_line):
                tx = i * config.tile_size + config.tile_size/2
                ty = j * config.tile_size + config.tile_size/2
                
                dist_to_center = ((tx - safe_zone_center[0])**2 + (ty - safe_zone_center[1])**2)**0.5
                if dist_to_center > safe_radius and random.random() < self.density:
                    w = 50 + random.random() * 100
                    h = 50 + random.random() * 100
                    rect = pygame.Rect(tx - w/2, ty - h/2, w, h)
                    self.obstacles.append(rect)

    def compute_collisions(self, entity):
        """Pushes entities out of static geometry."""
        ent_rect = entity.get_rect()
        for obs in self.obstacles:
            if ent_rect.colliderect(obs):
                # Basic push out
                diff_left = ent_rect.right - obs.left
                diff_right = obs.right - ent_rect.left
                diff_top = ent_rect.bottom - obs.top
                diff_bot = obs.bottom - ent_rect.top
                
                min_diff = min(diff_left, diff_right, diff_top, diff_bot)
                
                if min_diff == diff_left: entity.x -= diff_left
                elif min_diff == diff_right: entity.x += diff_right
                elif min_diff == diff_top: entity.y -= diff_top
                elif min_diff == diff_bot: entity.y += diff_bot
                
                # Update rect
                ent_rect.centerx = int(entity.x)
                ent_rect.centery = int(entity.y)

    def draw(self, screen: pygame.Surface, camera_offset: tuple[float, float], viewport: pygame.Rect):
        alpha_surf = pygame.Surface(screen.get_size(), pygame.SRCALPHA)
        for obs in self.obstacles:
            if obs.colliderect(viewport):
                r = obs.copy()
                r.x -= camera_offset[0]
                r.y -= camera_offset[1]
                # White 60% opacity fill and 200/255 border
                config = ConfigManager.get_instance().world
                pygame.draw.rect(alpha_surf, config.obstacle_color, r)
                pygame.draw.rect(alpha_surf, config.obstacle_border_color, r, 2)
        screen.blit(alpha_surf, (0, 0))

