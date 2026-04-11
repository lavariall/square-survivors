import pygame
import os
import json
from .base import GameState
from ..core.input_system import InputAction
from ..ui.components import Button
from ..core.config_manager import ConfigManager

class MenuState(GameState):
    def __init__(self, engine):
        super().__init__(engine)
        self.config = ConfigManager.get_instance()
        self.font = pygame.font.SysFont("Arial", 48, bold=True)
        self.btn_font = pygame.font.SysFont("Arial", 22, bold=True)
        self.hs_font = pygame.font.SysFont("Arial", 18)
        self.diff_buttons = []
        
        btn_w, btn_h = 160, 50
        spacing = 20
        win_w, win_h = self.config.display.window_width, self.config.display.window_height
        
        # Sorting Hierarchy: 1. Difficulty, 2. Level, 3. Victory
        priorities = self.config.difficulty.priorities
        sorted_diffs = sorted(priorities.keys(), key=lambda x: priorities[x])
        self.difficulties = sorted_diffs
        for i, diff in enumerate(self.difficulties):
            bx = win_w//2 - (btn_w * 2 + spacing * 1.5)//2 + (i % 2) * (btn_w + spacing)
            by = win_h//2 - 40 + (i // 2) * (btn_h + spacing)
            
            def make_start(d=diff):
                return lambda: self.start_game(d)
                
            self.diff_buttons.append(Button(
                bx, by, btn_w, btn_h,
                diff, self.btn_font, make_start()
            ))

        self.selected_index = 0
        self.load_highscores()
        
    def load_highscores(self):
        self.highscores = []
        if os.path.exists("highscores.json"):
            try:
                with open("highscores.json", "r") as f:
                    self.highscores = json.load(f)
            except:
                pass

    def start_game(self, difficulty="Normal"):
        from .play import PlayState
        self.engine.change_state(PlayState(self.engine, difficulty))

    def handle_event(self, event: pygame.event.Event):
        for i, btn in enumerate(self.diff_buttons):
            btn.handle_event(event)
            if btn.hovered and event.type == pygame.MOUSEMOTION:
                self.selected_index = i

    def update(self, dt: float):
        if self.engine.input.was_just_pressed(InputAction.UP):
            if self.selected_index >= 2: self.selected_index -= 2
        elif self.engine.input.was_just_pressed(InputAction.DOWN):
            if self.selected_index <= 1: self.selected_index += 2
        elif self.engine.input.was_just_pressed(InputAction.LEFT):
            if self.selected_index > 0: self.selected_index -= 1
        elif self.engine.input.was_just_pressed(InputAction.RIGHT):
            if self.selected_index < len(self.diff_buttons) - 1: self.selected_index += 1
        elif self.engine.input.was_just_pressed(InputAction.CONFIRM):
            self.start_game(self.difficulties[self.selected_index])

    def draw(self, screen: pygame.Surface):
        win_w, win_h = self.config.display.window_width, self.config.display.window_height
        player_color = self.config.player.color
        enemy_color = self.config.enemies.enemy_types["basic"].color_normal
        text_light = self.config.ui.text_light

        title = self.font.render("Square Survivor", True, player_color)
        screen.blit(title, title.get_rect(center=(win_w//2, win_h//3 - 40)))
        for i, btn in enumerate(self.diff_buttons):
            btn.hovered = (i == self.selected_index)
            btn.draw(screen)

        # Draw Leaderboard at the bottom
        hs_title = self.btn_font.render("Top Survivors", True, text_light)
        screen.blit(hs_title, hs_title.get_rect(center=(win_w//2, win_h//2 + 100)))
        
        start_y = win_h//2 + 130
        if not self.highscores:
            empty = self.hs_font.render("No records yet!", True, player_color)
            screen.blit(empty, empty.get_rect(center=(win_w//2, start_y)))
        else:
            for i, score in enumerate(self.highscores):
                s_name = score.get("name", "Unknown")
                s_kills = score.get("kills", 0)
                s_level = score.get("level", 1)
                s_won = score.get("won", False)
                s_time = score.get("time", 0.0)
                s_diff = score.get("difficulty", "Normal")
                
                out_time = "VICTORY" if s_won else f"{int(s_time//60)}:{int(s_time%60):02d}"
                color = player_color if s_won else enemy_color
                
                # Format: 1. Name (Easy) - Lvl 10 - 100 Kills - 5:20
                row = self.hs_font.render(f"{i+1}. {s_name} ({s_diff}) - Lvl {s_level} - {s_kills} Kills - {out_time}", True, color)
                screen.blit(row, row.get_rect(center=(win_w//2, start_y + i * 25)))

        # Confirmation hint
        hint_text = "Select Difficulty [W, A, S, D] and Confirm [SPACE] to Start Game"
        hint = self.hs_font.render(hint_text, True, player_color)
        screen.blit(hint, hint.get_rect(center=(win_w//2, win_h - 30)))
