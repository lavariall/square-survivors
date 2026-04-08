import pygame
from typing import Optional
from ..states import GameState
from .input_system import InputSystem
from ..constants import WINDOW_WIDTH, WINDOW_HEIGHT, FPS, BG_COLOR

class Engine:
    """The core wrapper that polls events and manages ticks."""
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
        pygame.display.set_caption("Square Survivor")
        self.clock = pygame.time.Clock()
        self.running = True
        self.input = InputSystem()
        self.current_state: Optional[GameState] = None

    def change_state(self, new_state: GameState):
        self.current_state = new_state

    def run(self):
        while self.running:
            dt = self.clock.tick(FPS) / 1000.0  # seconds
            if dt > 0.1: 
                dt = 0.1 # Cap dt for huge lag spikes
                
            events = pygame.event.get()
            self.input.update(events)
            
            for event in events:
                if event.type == pygame.QUIT:
                    self.running = False
                elif self.current_state:
                    self.current_state.handle_event(event)

            if self.current_state:
                self.current_state.update(dt)

            self.screen.fill(BG_COLOR)
            if self.current_state:
                self.current_state.draw(self.screen)
            
            pygame.display.flip()
        
        pygame.quit()


if __name__ == "__main__":
    # Test Engine Instantiation
    print("Testing Engine startup...")
    engine = Engine()
    
    # Run a dummy state that auto-quits after 1 second
    class DummyState(GameState):
        def __init__(self, eng):
            super().__init__(eng)
            self.timer = 0
        def handle_event(self, e): pass
        def update(self, dt):
            self.timer += dt
            if self.timer > 1.0:
                self.engine.running = False
        def draw(self, screen): pass
        
    engine.change_state(DummyState(engine))
    engine.run()
    print("Engine closed properly.")
