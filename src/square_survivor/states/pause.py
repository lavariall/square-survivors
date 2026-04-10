import pygame
from .base import GameState
from ..core.input_system import InputAction
from ..constants import WINDOW_WIDTH, WINDOW_HEIGHT, PLAYER_COLOR, TEXT_LIGHT

class PauseState(GameState):
    def __init__(self, engine, play_state):
        super().__init__(engine)
        self.play_state = play_state
        self.title_font = pygame.font.SysFont("Arial", 48, bold=True)
        self.hint_font = pygame.font.SysFont("Arial", 24, bold=True)

    def handle_event(self, event: pygame.event.Event):
        # We handle discrete inputs in update() for consistency with other menus
        pass

    def update(self, dt: float):
        if self.engine.input.was_just_pressed(InputAction.PAUSE) or \
           self.engine.input.was_just_pressed(InputAction.CONFIRM):
            self.engine.change_state(self.play_state)

    def draw(self, screen: pygame.Surface):
        # Draw background game state behind
        self.play_state.draw(screen) 
        
        # Transparent overlay
        overlay = pygame.Surface((WINDOW_WIDTH, WINDOW_HEIGHT))
        overlay.set_alpha(180) # Slightly lighter than level up
        overlay.fill((0, 0, 0))
        screen.blit(overlay, (0, 0))
        
        # Title
        title_surf = self.title_font.render("Pause", True, PLAYER_COLOR)
        title_rect = title_surf.get_rect(center=(WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2 - 50))
        screen.blit(title_surf, title_rect)
        
        # Hint
        hint_surf = self.hint_font.render("Press [ESC] or [SPACE] to continue", True, TEXT_LIGHT)
        hint_rect = hint_surf.get_rect(center=(WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2 + 50))
        screen.blit(hint_surf, hint_rect)
