import abc
import pygame

class GameState(abc.ABC):
    """Abstract base class for all game states."""
    
    def __init__(self, engine):
        self.engine = engine

    @abc.abstractmethod
    def handle_event(self, event: pygame.event.Event):
        """Handle Pygame events like input."""
        pass

    @abc.abstractmethod
    def update(self, dt: float):
        """Update game logic based on delta time."""
        pass

    @abc.abstractmethod
    def draw(self, screen: pygame.Surface):
        """Draw the current state to the screen."""
        pass


if __name__ == "__main__":
    # Example usage / basic test
    class DummyState(GameState):
        def handle_event(self, event): pass
        def update(self, dt): pass
        def draw(self, screen): pass
    
    print("GameState ABC compiled correctly:", issubclass(DummyState, GameState))
