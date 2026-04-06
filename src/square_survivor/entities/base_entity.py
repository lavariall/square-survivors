import abc
import pygame

class Entity(abc.ABC):
    """Abstract base class for all in-game objects."""
    
    def __init__(self, x: float, y: float, size: float):
        self.x = x
        self.y = y
        self.size = size
        self.rect = pygame.Rect(self.x - getattr(self, "size", 0)/2, self.y - getattr(self, "size", 0)/2, self.size, self.size)
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
        self.rect.width = self.size
        self.rect.height = self.size
        self.rect.centerx = int(self.x)
        self.rect.centery = int(self.y)
        return self.rect


if __name__ == "__main__":
    class DummyEntity(Entity):
        def update(self, dt): pass
        def draw(self, screen, offset): pass
        
    e = DummyEntity(10, 20, 5)
    print("Entity compiled and instantiated:", e.get_rect())
