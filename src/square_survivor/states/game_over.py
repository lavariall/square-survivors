import pygame
import os
import json
from .base import GameState
from ..core.input_system import InputAction
from ..ui.components import Button, InputBox
from ..constants import (WINDOW_WIDTH, WINDOW_HEIGHT, PLAYER_COLOR, 
                         ENEMY_COLOR, TEXT_LIGHT, DIFF_PRIORITY)

class GameOverState(GameState):
    def __init__(self, engine, player, won, time_survived, difficulty):
        super().__init__(engine)
        self.player = player
        self.won = won
        self.time_survived = time_survived
        self.difficulty = difficulty
        
        self.font = pygame.font.SysFont("Arial", 64, bold=True)
        self.info_font = pygame.font.SysFont("Arial", 24)
        
        self.input_box = InputBox(WINDOW_WIDTH//2 - 100, WINDOW_HEIGHT//2, 200, 40, self.info_font)
        self.input_box.active = True
        self.save_btn = Button(WINDOW_WIDTH//2 - 100, WINDOW_HEIGHT//2 + 60, 200, 50, "Save & Restart", self.info_font, self.save_score)
        
    def save_score(self):
        scores = []
        if os.path.exists("highscores.json"):
            try:
                with open("highscores.json", "r") as f:
                    scores = json.load(f)
            except:
                pass
        name = self.input_box.text.strip()
        if not name: name = "Anonymous"
        
        scores.append({
            "name": name,
            "kills": self.player.kills,
            "level": self.player.level,
            "time": self.time_survived,
            "won": self.won,
            "difficulty": self.difficulty
        })
        
        # Sorting Hierarchy: 1. Difficulty, 2. Level, 3. Victory
        scores.sort(key=lambda x: (
            DIFF_PRIORITY.get(x.get("difficulty", "Normal"), 0),
            x.get("level", 0),
            1 if x.get("won", False) else 0
        ), reverse=True)
        scores = scores[:7]
        
        try:
            with open("highscores.json", "w") as f:
                json.dump(scores, f)
        except:
            pass
            
        from .menu import MenuState
        self.engine.change_state(MenuState(self.engine))

    def handle_event(self, event):
        self.input_box.handle_event(event)
        self.save_btn.handle_event(event)
        if self.engine.input.was_just_pressed(InputAction.CONFIRM):
            self.save_score()
        
    def update(self, dt):
        pass
        
    def draw(self, screen):
        title_str = "VICTORY!" if self.won else "YOU DIED"
        color = PLAYER_COLOR if self.won else ENEMY_COLOR
        title = self.font.render(title_str, True, color)
        screen.blit(title, title.get_rect(center=(WINDOW_WIDTH//2, WINDOW_HEIGHT//4)))
        
        mins = int(self.time_survived // 60)
        secs = int(self.time_survived % 60)
        info = f"Kills: {self.player.kills} | Survived: {mins}:{secs:02d} | Level: {self.player.level}"
        info_surf = self.info_font.render(info, True, TEXT_LIGHT)
        screen.blit(info_surf, info_surf.get_rect(center=(WINDOW_WIDTH//2, WINDOW_HEIGHT//4 + 60)))
        
        input_lbl = self.info_font.render("Enter Name:", True, TEXT_LIGHT)
        screen.blit(input_lbl, (self.input_box.rect.x, self.input_box.rect.y - 30))
        
        self.input_box.draw(screen)
        self.save_btn.draw(screen)
        
        # Keyboard hint
        hint = self.info_font.render("Press [ENTER] to Save & Restart", True, PLAYER_COLOR)
        screen.blit(hint, hint.get_rect(center=(WINDOW_WIDTH//2, WINDOW_HEIGHT - 40)))
