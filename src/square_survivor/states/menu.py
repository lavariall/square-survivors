import pygame
import os
import json
from .base import GameState
from ..core.input_system import InputAction
from ..ui.components import Button
from ..constants import WINDOW_WIDTH, WINDOW_HEIGHT, PLAYER_COLOR, TEXT_LIGHT, ENEMY_COLOR

class MenuState(GameState):
    def __init__(self, engine):
        super().__init__(engine)
        self.font = pygame.font.SysFont("Arial", 48, bold=True)
        self.btn_font = pygame.font.SysFont("Arial", 22, bold=True)
        self.hs_font = pygame.font.SysFont("Arial", 18)
        
        btn_w, btn_h = 160, 50
        spacing = 20
        difficulties = ["Easy", "Normal", "Hard", "Ultra"]
        self.diff_buttons = []
        
        self.difficulties = difficulties
        for i, diff in enumerate(difficulties):
            bx = WINDOW_WIDTH//2 - (btn_w * 2 + spacing * 1.5)//2 + (i % 2) * (btn_w + spacing)
            by = WINDOW_HEIGHT//2 - 40 + (i // 2) * (btn_h + spacing)
            
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
        title = self.font.render("Square Survivor", True, PLAYER_COLOR)
        screen.blit(title, title.get_rect(center=(WINDOW_WIDTH//2, WINDOW_HEIGHT//3 - 40)))
        for i, btn in enumerate(self.diff_buttons):
            btn.hovered = (i == self.selected_index)
            btn.draw(screen)

        # Draw Leaderboard at the bottom
        hs_title = self.btn_font.render("Top Survivors", True, TEXT_LIGHT)
        screen.blit(hs_title, hs_title.get_rect(center=(WINDOW_WIDTH//2, WINDOW_HEIGHT//2 + 100)))
        
        start_y = WINDOW_HEIGHT//2 + 130
        if not self.highscores:
            empty = self.hs_font.render("No records yet!", True, PLAYER_COLOR)
            screen.blit(empty, empty.get_rect(center=(WINDOW_WIDTH//2, start_y)))
        else:
            for i, score in enumerate(self.highscores):
                s_name = score.get("name", "Unknown")
                s_kills = score.get("kills", 0)
                s_level = score.get("level", 1)
                s_won = score.get("won", False)
                s_time = score.get("time", 0.0)
                s_diff = score.get("difficulty", "Normal")
                
                out_time = "VICTORY" if s_won else f"{int(s_time//60)}:{int(s_time%60):02d}"
                color = PLAYER_COLOR if s_won else ENEMY_COLOR
                
                # Format: 1. Name (Easy) - Lvl 10 - 100 Kills - 5:20
                row = self.hs_font.render(f"{i+1}. {s_name} ({s_diff}) - Lvl {s_level} - {s_kills} Kills - {out_time}", True, color)
                screen.blit(row, row.get_rect(center=(WINDOW_WIDTH//2, start_y + i * 25)))

        # Confirmation hint
        hint_text = "Select Difficulty [W, A, S, D] and Confirm [SPACE] to Start Game"
        hint = self.hs_font.render(hint_text, True, PLAYER_COLOR)
        screen.blit(hint, hint.get_rect(center=(WINDOW_WIDTH//2, WINDOW_HEIGHT - 30)))
