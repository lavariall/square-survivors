import pygame
from .base_entity import Entity
from ..constants import XP_COLOR, XP_ORB_LIFESPAN

class XPOrb(Entity):
    def __init__(self, x: float, y: float, value: float):
        super().__init__(x, y, 8)
        self.value = value
        self.timer = XP_ORB_LIFESPAN

    def update(self, dt: float):
        if not self.active: return
        self.timer -= dt
        if self.timer <= 0:
            self.active = False

    def draw(self, screen: pygame.Surface, camera_offset: tuple[float, float]):
        if not self.active: return
        render_x = int(self.x - camera_offset[0])
        render_y = int(self.y - camera_offset[1])
        pygame.draw.circle(screen, XP_COLOR, (render_x, render_y), self.size // 2)

if __name__ == "__main__":
    orb = XPOrb(100, 100, 5)
    print("XPOrb instantiated safely with value:", orb.value)
