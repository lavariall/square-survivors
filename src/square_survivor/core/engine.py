import pygame
from typing import Optional
from ..states import GameState
from .input_system import InputSystem, InputAction
from .config_manager import ConfigManager
from ..systems.upgrade_system.base_upgrade import UpgradeManager

class Engine:
    """The core wrapper that polls events and manages ticks."""
    def __init__(self):
        pygame.init()
        # Initialize configuration
        self.config = ConfigManager.get_instance()
        
        # Initialize Upgrade System
        UpgradeManager.initialize_from_config(self.config.upgrades)
        
        # Virtual Resolution Setup
        self.virtual_width = self.config.display.window_width
        self.virtual_height = self.config.display.window_height
        self.virtual_screen = pygame.Surface((self.virtual_width, self.virtual_height))
        
        self.screen: Optional[pygame.Surface] = None
        self._reinit_display()
        
        pygame.display.set_caption(self.config.display.title)
        self.clock = pygame.time.Clock()
        self.running = True
        self.input = InputSystem()
        self.current_state: Optional[GameState] = None

    def _reinit_display(self):
        """Initializes or re-initializes the physical display surface."""
        flags = 0
        if self.config.display.fullscreen:
            flags |= pygame.FULLSCREEN
            # Fullscreen at native resolution
            target_res = (0, 0)
        else:
            target_res = (self.virtual_width, self.virtual_height)
        
        self.screen = pygame.display.set_mode(target_res, flags)

    def _handle_fullscreen_toggle(self):
        """Toggles fullscreen state and re-initializes display."""
        self.config.display.fullscreen = not self.config.display.fullscreen
        self._reinit_display()

    def change_state(self, new_state: GameState):
        self.current_state = new_state

    def run(self):
        while self.running:
            # Check for config updates (hot reloading)
            self.config.check_for_updates()
            
            dt = self.clock.tick(self.config.display.fps) / 1000.0  # seconds
            if dt > 0.1: 
                dt = 0.1 # Cap dt for huge lag spikes
                
            events = pygame.event.get()
            self.input.update(events)
            
            if self.input.was_just_pressed(InputAction.TOGGLE_FULLSCREEN):
                self._handle_fullscreen_toggle()
            
            for event in events:
                if event.type == pygame.QUIT:
                    self.running = False
                elif self.current_state:
                    self.current_state.handle_event(event)

            if self.current_state:
                self.current_state.update(dt)

            # 1. Draw to virtual screen
            self.virtual_screen.fill(self.config.world.bg_color)
            if self.current_state:
                self.current_state.draw(self.virtual_screen)
            
            # 2. Scale and center on physical screen
            self.screen.fill((0, 0, 0)) # Letterboxing bars
            
            sw, sh = self.screen.get_size()
            scale = min(sw / self.virtual_width, sh / self.virtual_height)
            
            new_w = int(self.virtual_width * scale)
            new_h = int(self.virtual_height * scale)
            
            scaled_surface = pygame.transform.scale(self.virtual_screen, (new_w, new_h))
            
            x_off = (sw - new_w) // 2
            y_off = (sh - new_h) // 2
            
            self.screen.blit(scaled_surface, (x_off, y_off))
            
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
