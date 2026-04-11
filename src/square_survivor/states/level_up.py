import pygame
import math
from .base import GameState
from ..core.input_system import InputAction
from ..systems.upgrade_system import UpgradeManager
from ..ui.components import Button
from ..core.config_manager import ConfigManager

class LevelUpState(GameState):
    def __init__(self, engine, play_state):
        super().__init__(engine)
        self.play_state = play_state
        self.config = ConfigManager.get_instance()
        self.font = pygame.font.SysFont("Arial", 48, bold=True)  # todo: use config e.g. (self.config.ui.font, self.config.ui.font_size_large, self.config.ui.font_large_bold)
        self.btn_font = pygame.font.SysFont("Arial", 18, bold=True)  # todo: use config e.g. (self.config.ui.font, self.config.ui.font_size_normal, self.config.ui.font_normal_bold)
        self.desc_font = pygame.font.SysFont("Arial", 14)  # todo: use config e.g. (self.config.ui.font, self.config.ui.font_size_small, self.config.ui.font_small_bold)
        
        self.choices = UpgradeManager.get_random_choices(self.play_state.player, self.play_state.player.upgrade_choices)
        self.buttons = []
        self.selected_index = 0
        
        # Centered Grid layout
        btn_w, btn_h = 200, 80
        spacing_x, spacing_y = 20, 70
        max_cols = 4
        
        num_choices = len(self.choices)
        if num_choices == 0:
            return

        num_rows = math.ceil(num_choices / max_cols)
        total_grid_h = num_rows * btn_h + (num_rows - 1) * spacing_y
        win_w, win_h = self.config.display.window_width, self.config.display.window_height
        grid_start_y = (win_h - total_grid_h) // 2 + 50
        
        for i, upgrade in enumerate(self.choices):
            row = i // max_cols
            col = i % max_cols
            
            items_in_row = min(max_cols, num_choices - row * max_cols)
            row_w = items_in_row * btn_w + (items_in_row - 1) * spacing_x
            row_start_x = (win_w - row_w) // 2
            
            bx = row_start_x + col * (btn_w + spacing_x)
            by = grid_start_y + row * (btn_h + spacing_y)
            
            def make_callback(upg=upgrade):
                return lambda: self.select_upgrade(upg)
                
            self.buttons.append(Button(bx, by, btn_w, btn_h, upgrade.name, self.btn_font, make_callback()))

    def select_upgrade(self, upgrade):
        upgrade.apply(self.play_state.player)
        self.play_state.player.level_ups_pending -= 1
        self.engine.change_state(self.play_state)

    def handle_event(self, event: pygame.event.Event):
        for i, btn in enumerate(self.buttons):
            btn.handle_event(event)
            if btn.hovered and event.type == pygame.MOUSEMOTION:
                self.selected_index = i

    def update(self, dt: float):
        if self.engine.input.was_just_pressed(InputAction.UP):
            if self.selected_index >= 4:
                self.selected_index -= 4
        elif self.engine.input.was_just_pressed(InputAction.DOWN):
            if self.selected_index + 4 < len(self.buttons):
                self.selected_index += 4
        elif self.engine.input.was_just_pressed(InputAction.LEFT):
            if self.selected_index > 0:
                self.selected_index -= 1
        elif self.engine.input.was_just_pressed(InputAction.RIGHT):
            if self.selected_index < len(self.buttons) - 1:
                self.selected_index += 1
        elif self.engine.input.was_just_pressed(InputAction.CONFIRM):
            if 0 <= self.selected_index < len(self.choices):
                self.select_upgrade(self.choices[self.selected_index])

    def draw(self, screen: pygame.Surface):
        # Draw background game state behind
        self.play_state.draw(screen) 
        
        win_w, win_h = self.config.display.window_width, self.config.display.window_height
        player_color = self.config.player.color
        text_light = self.config.ui.text_light

        # Transparent overlay
        overlay = pygame.Surface((win_w, win_h))
        overlay.set_alpha(200)
        overlay.fill((0, 0, 0))
        screen.blit(overlay, (0, 0))
        
        title = self.font.render("LEVEL UP!", True, player_color)
        screen.blit(title, title.get_rect(center=(win_w//2, win_h//3)))
        
        for i, btn in enumerate(self.buttons):
            btn.hovered = (i == self.selected_index)
            btn.draw(screen)
            desc_surf = self.desc_font.render(self.choices[i].description, True, text_light)
            screen.blit(desc_surf, desc_surf.get_rect(center=(btn.rect.centerx, btn.rect.bottom + 20)))
 
        # Confirmation hint
        hint = self.btn_font.render("Press [SPACE] to Confirm Choice", True, player_color)
        screen.blit(hint, hint.get_rect(center=(win_w//2, win_h - 40)))
