import pygame
from .base_weapon import Weapon
from ...constants import PLAYER_COLOR

class SaturnSquare(Weapon):
    def __init__(self, owner, index: int, size: float, damage: float, hp: float, knockback: float, radius: float = 100):
        # Initialize at a temporary position, will be updated immediately
        super().__init__(owner.x, owner.y, size, damage, knockback)
        self.owner = owner
        self.index = index
        self.radius = radius
        self.hp = hp
        self.max_hp = hp
        self.life_timer = 10.0 # Default 10 seconds
        self.active = True
        
        # Sprite setup with transparent surface as requested
        self._rebuild_sprite()

    def _rebuild_sprite(self):
        """Rebuilds the image and rect based on current size."""
        self.image = pygame.Surface((self.size, self.size), pygame.SRCALPHA)
        pygame.draw.rect(self.image, PLAYER_COLOR, (0, 0, self.size, self.size), 2) # Semantic color
        self.rect = self.image.get_rect()

    def update(self, dt: float):
        # Update rotation speed from owner if needed (or use default)
        rotation_speed = getattr(self.owner, "saturn_squares_rotation_speed", 180.0)
        
        # Sync size if it changed (e.g. from upgrade)
        new_size = getattr(self.owner, "saturn_squares_size", self.size)
        if new_size != self.size:
            self.size = new_size
            self._rebuild_sprite()
            
        # Sync other stats from owner
        self.damage = getattr(self.owner, "saturn_squares_damage", self.damage)
        self.knockback = getattr(self.owner, "saturn_squares_knockback", self.knockback)

        # Handle lifespan
        if getattr(self.owner, "saturn_squares_lifespan_active", True):
            self.life_timer -= dt
            if self.life_timer <= 0:
                self.active = False
                self.kill()

        # Calculate current angle based on master angle from owner and our index
        total_count = getattr(self.owner, "saturn_squares_count", 1)
        master_angle = getattr(self.owner, "saturn_squares_angle", 0.0)
        
        # Stabilize polar coordinates: Spread evenly over 360 degrees
        angle = (master_angle + (self.index * 360.0 / total_count)) % 360
        
        # Calculate new world position using rotating offset
        offset = pygame.Vector2(self.radius, 0).rotate(angle)
        self.x = self.owner.x + offset.x
        self.y = self.owner.y + offset.y
        
        # Update rect for collision
        self.rect.center = (int(self.x), int(self.y))
        
        # Handle lifespan/health check elsewhere or here
        if self.hp <= 0:
            self.kill()

    def draw(self, screen: pygame.Surface, camera_offset: tuple[float, float]):
        render_x = int(self.x - camera_offset[0] - self.size / 2)
        render_y = int(self.y - camera_offset[1] - self.size / 2)
        
        # Draw the transparent surface with border
        screen.blit(self.image, (render_x, render_y))
