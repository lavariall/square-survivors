import pygame
import random
from typing import List
from ..constants import MAP_SIZE, TILE_SIZE, OBSTACLE_COLOR, OBSTACLE_BORDER

class MapGenerator:
    """Procedural Map Generation System."""
    
    def __init__(self, density: float = 0.05):
        self.obstacles: List[pygame.Rect] = []
        self.density = density

    def generate(self, safe_zone_center: tuple[float, float], safe_radius: float = 200.0):
        tiles_line = MAP_SIZE // TILE_SIZE
        self.obstacles.clear()

        for i in range(tiles_line):
            for j in range(tiles_line):
                tx = i * TILE_SIZE + TILE_SIZE/2
                ty = j * TILE_SIZE + TILE_SIZE/2
                
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
                # White 60% opacity (153/255)
                pygame.draw.rect(alpha_surf, (255, 255, 255, 153), r)
                pygame.draw.rect(alpha_surf, (255, 255, 255, 200), r, 2)
        screen.blit(alpha_surf, (0, 0))

if __name__ == "__main__":
    mg = MapGenerator(density=1.0)
    mg.generate((MAP_SIZE/2, MAP_SIZE/2))
    print(f"Generated {len(mg.obstacles)} obstacles with 100% density outside safe zone.")
