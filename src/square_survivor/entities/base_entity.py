import abc
import pygame

class Entity(pygame.sprite.Sprite):
    """Abstract base class for all in-game objects."""
    
    def __init__(self, x: float, y: float, size: float):
        super().__init__()
        self.x = x
        self.y = y
        self.size = size
        # Standard Sprite attributes
        self.image = pygame.Surface((size, size), pygame.SRCALPHA)
        self.rect = self.image.get_rect()
        self.active = True

    @abc.abstractmethod
    def update(self, dt: float):
        """Update entity logic."""
        pass

    @abc.abstractmethod
    def draw(self, screen: pygame.Surface, camera_offset: tuple[float, float]):
        """Render entity to screen."""
        pass

    def get_rect(self) -> pygame.Rect:
        """Returns the world-space bounding box for collision."""
        self.rect.width = int(self.size)
        self.rect.height = int(self.size)
        self.rect.centerx = int(self.x)
        self.rect.centery = int(self.y)
        return self.rect


if __name__ == "__main__":
    class DummyEntity(Entity):
        def update(self, dt): pass
        def draw(self, screen, offset): pass
        
    e = DummyEntity(10, 20, 5)
    print("Entity compiled and instantiated:", e.get_rect())
