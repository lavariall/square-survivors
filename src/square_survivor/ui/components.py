import pygame
from typing import Callable, Tuple
from ..core.config_manager import ConfigManager

class Button:
    def __init__(self, x: int, y: int, w: int, h: int, text: str, font: pygame.font.Font, on_click: Callable):
        self.rect = pygame.Rect(x, y, w, h)
        self.text = text
        self.font = font
        self.on_click = on_click
        self.hovered = False

    def handle_event(self, event: pygame.event.Event):
        if event.type == pygame.MOUSEMOTION:
            self.hovered = self.rect.collidepoint(event.pos)
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1 and self.hovered:
                self.on_click()

    def draw(self, screen: pygame.Surface):
        config = ConfigManager.get_instance()
        player_color = config.player.color
        
        if self.hovered:
            # Glow effect
            glow_surf = pygame.Surface((self.rect.w + 20, self.rect.h + 20), pygame.SRCALPHA)
            pygame.draw.rect(glow_surf, (player_color[0], player_color[1], player_color[2], 100), glow_surf.get_rect(), border_radius=12)
            screen.blit(glow_surf, (self.rect.x - 10, self.rect.y - 10))
            
            pygame.draw.rect(screen, player_color, self.rect, border_radius=8)
            text_surf = self.font.render(self.text, True, (0, 0, 0))
        else:
            # Alpha background
            btn_surf = pygame.Surface((self.rect.w, self.rect.h), pygame.SRCALPHA)
            pygame.draw.rect(btn_surf, (player_color[0], player_color[1], player_color[2], 76), btn_surf.get_rect(), border_radius=8)
            screen.blit(btn_surf, self.rect.topleft)
            
            pygame.draw.rect(screen, player_color, self.rect, 2, border_radius=8)
            text_surf = self.font.render(self.text, True, player_color)
            
        tr = text_surf.get_rect(center=self.rect.center)
        screen.blit(text_surf, tr)

class ProgressBar:
    def __init__(self, x: int, y: int, w: int, h: int, color: Tuple[int, int, int]):
        self.rect = pygame.Rect(x, y, w, h)
        self.color = color
        self.progress = 1.0

    def set_progress(self, current: float, maximum: float):
        if maximum > 0:
            self.progress = max(0.0, min(1.0, current / maximum))
        else:
            self.progress = 0.0

    def draw(self, screen: pygame.Surface):
        config = ConfigManager.get_instance().ui
        # Background
        pygame.draw.rect(screen, (0, 0, 0, 128), self.rect, border_radius=10)
        # Border
        pygame.draw.rect(screen, config.panel_border_color, self.rect, 2, border_radius=10)
        
        if self.progress > 0:
            fill_rect = pygame.Rect(self.rect.x, self.rect.y, int(self.rect.width * self.progress), self.rect.height)
            pygame.draw.rect(screen, self.color, fill_rect, border_radius=10)

class InputBox:
    def __init__(self, x, y, w, h, font):
        self.rect = pygame.Rect(x, y, w, h)
        self.font = font
        self.text = ""
        self.active = False

    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            if self.rect.collidepoint(event.pos):
                self.active = not self.active
            else:
                self.active = False
        if event.type == pygame.KEYDOWN:
            if self.active:
                if event.key == pygame.K_RETURN:
                    # Could handle submission
                    pass
                elif event.key == pygame.K_BACKSPACE:
                    self.text = self.text[:-1]
                else:
                    if len(self.text) < 15: # max 15 chars
                        self.text += event.unicode

    def draw(self, screen):
        config = ConfigManager.get_instance()
        player_color = config.player.color
        player_color_dim = config.ui.player_color_dim
        text_light = config.ui.text_light

        color = player_color if self.active else player_color_dim
        # Draw background and border
        pygame.draw.rect(screen, (10, 10, 15), self.rect, border_radius=4)
        pygame.draw.rect(screen, color, self.rect, 2, border_radius=4)
        
        txt_surf = self.font.render(self.text, True, text_light)
        screen.blit(txt_surf, (self.rect.x + 5, self.rect.y + self.rect.height // 2 - txt_surf.get_height() // 2))

if __name__ == "__main__":
    pygame.init()
    screen = pygame.display.set_mode((200, 200))
    font = pygame.font.SysFont("Arial", 20)
    btn = Button(50, 50, 100, 50, "Test", font, lambda: print("Clicked!"))
    bar = ProgressBar(50, 120, 100, 20, (255, 0, 0))
    bar.set_progress(50, 100)
    print("UI Components logic loaded.")
