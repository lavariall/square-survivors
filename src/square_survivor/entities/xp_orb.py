from .base_entity import Entity
from ..core.config_manager import ConfigManager

class XPOrb(Entity):
    def __init__(self, x: float, y: float, value: float):
        import pygame # For the Entity base class requirements if needed, but it's already in base_entity
        self.config = ConfigManager.get_instance().xp_orbs
        super().__init__(x, y, self.config.size)
        self.value = value
        self.timer = self.config.lifespan

    def update(self, dt: float):
        if not self.active: return
        self.timer -= dt
        if self.timer <= 0:
            self.active = False

    def draw(self, screen: pygame.Surface, camera_offset: tuple[float, float]):
        import pygame
        if not self.active: return
        render_x = int(self.x - camera_offset[0])
        render_y = int(self.y - camera_offset[1])
        pygame.draw.circle(screen, self.config.color, (render_x, render_y), self.size // 2)

if __name__ == "__main__":
    orb = XPOrb(100, 100, 5)
    print("XPOrb instantiated safely with value:", orb.value)
