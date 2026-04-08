import pygame
import sys
import math
from typing import List

from .core.states import GameState
from .core.input_system import InputAction
from .entities.player import Player
from .entities.enemy import Enemy
from .entities.xp_orb import XPOrb
from .systems.map_generator import MapGenerator
from .systems.combat_system import CombatSystem
from .systems.wave_manager import WaveManager
from .systems.upgrade_system import UpgradeManager

from .ui.components import Button, ProgressBar, InputBox
from .constants import (WINDOW_WIDTH, WINDOW_HEIGHT, 
                        XP_ORB_COLOR, TILE_SIZE, MAP_SIZE, OBSTACLE_DENSITY,
                        DIFFICULTY_SETTINGS, MAX_XP_ORBS, XP_ORB_LIFESPAN, TEXT_LIGHT,
                        PLAYER_COLOR, ENEMY_COLOR, TOTAL_TIME_SEC, DIFF_PRIORITY)
import json
import os

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
        
        from .constants import DIFFICULTY_SETTINGS
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

class LevelUpState(GameState):
    def __init__(self, engine, play_state):
        super().__init__(engine)
        self.play_state = play_state
        self.font = pygame.font.SysFont("Arial", 48, bold=True)
        self.btn_font = pygame.font.SysFont("Arial", 18, bold=True)
        self.desc_font = pygame.font.SysFont("Arial", 14)
        
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
        grid_start_y = (WINDOW_HEIGHT - total_grid_h) // 2 + 50
        
        for i, upgrade in enumerate(self.choices):
            row = i // max_cols
            col = i % max_cols
            
            items_in_row = min(max_cols, num_choices - row * max_cols)
            row_w = items_in_row * btn_w + (items_in_row - 1) * spacing_x
            row_start_x = (WINDOW_WIDTH - row_w) // 2
            
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
        
        # Transparent overlay
        overlay = pygame.Surface((WINDOW_WIDTH, WINDOW_HEIGHT))
        overlay.set_alpha(200)
        overlay.fill((0, 0, 0))
        screen.blit(overlay, (0, 0))
        
        title = self.font.render("LEVEL UP!", True, PLAYER_COLOR)
        screen.blit(title, title.get_rect(center=(WINDOW_WIDTH//2, WINDOW_HEIGHT//3)))
        
        for i, btn in enumerate(self.buttons):
            btn.hovered = (i == self.selected_index)
            btn.draw(screen)
            desc_surf = self.desc_font.render(self.choices[i].description, True, TEXT_LIGHT)
            screen.blit(desc_surf, desc_surf.get_rect(center=(btn.rect.centerx, btn.rect.bottom + 20)))

        # Confirmation hint
        hint = self.btn_font.render("Press [SPACE] to Confirm Choice", True, PLAYER_COLOR)
        screen.blit(hint, hint.get_rect(center=(WINDOW_WIDTH//2, WINDOW_HEIGHT - 40)))


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
        
        from .constants import DIFF_PRIORITY
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

class PlayState(GameState):
    def __init__(self, engine, difficulty="Normal"):
        super().__init__(engine)
        self.player = Player()
        self.enemies: List[Enemy] = []
        self.xp_orbs: List[XPOrb] = []
        
        self.difficulty = difficulty
        from .constants import DIFFICULTY_SETTINGS, OBSTACLE_DENSITY
        self.difficulty_settings = DIFFICULTY_SETTINGS.get(difficulty, DIFFICULTY_SETTINGS["Normal"])
        
        self.map_generator = MapGenerator(density=self.difficulty_settings.get("obstacle_density", OBSTACLE_DENSITY))
        self.map_generator.generate((MAP_SIZE//2, MAP_SIZE//2))
        
        self.time_survived = 0.0
        self.camera_offset = [0.0, 0.0]
        
        # UI
        self.font = pygame.font.SysFont("Arial", 24, bold=True)
        self.hp_bar = ProgressBar(20, 20, 200, 20, ENEMY_COLOR)
        self.stamina_bar = ProgressBar(20, 50, 200, 20, PLAYER_COLOR)
        self.xp_bar = ProgressBar(20, WINDOW_HEIGHT - 40, WINDOW_WIDTH - 40, 10, XP_ORB_COLOR)

    def handle_event(self, event: pygame.event.Event):
        if self.engine.input.was_just_pressed(InputAction.DASH):
            self.player.attempt_dash(0.016, self.engine.input)

    def update(self, dt: float):
        self.time_survived += dt
        if self.time_survived >= TOTAL_TIME_SEC:
            # Win logic
            self.engine.change_state(GameOverState(self.engine, self.player, True, self.time_survived, self.difficulty))
            return

        self.player.update(dt, self.engine.input)
        self.map_generator.compute_collisions(self.player)


        # Update enemies
        for e in self.enemies:
            e.update(dt, self.player.x, self.player.y)
            if e.active:
                self.map_generator.compute_collisions(e)

        # Combat Process
        CombatSystem.process_explosions(self.player, self.enemies)
        
        # Enemy Death / XP Spawning / Damage
        player_rect = self.player.get_rect()
        for e in self.enemies:
            if not e.active: continue
            
            # Enemy death
            if e.hp <= 0:
                e.active = False
                self.player.kills += 1
                
                # Choose orb: Inactive -> New (if under cap) -> Oldest Active (force recycle)
                xp_val = 2 if e.is_elite else 1
                xp = next((x for x in self.xp_orbs if not x.active), None)
                
                if not xp:
                    if len(self.xp_orbs) < MAX_XP_ORBS:
                        xp = XPOrb(e.x, e.y, xp_val)
                        self.xp_orbs.append(xp)
                    else:
                        # Force recycle the oldest active one (lowest timer)
                        xp = min(self.xp_orbs, key=lambda x: x.timer)
                
                if xp:
                    import random
                    jitter = 15
                    xp.x, xp.y = e.x + random.randint(-jitter, jitter), e.y + random.randint(-jitter, jitter)
                    xp.value = xp_val
                    xp.active = True
                    xp.timer = XP_ORB_LIFESPAN
                
                continue

            # Player takes damage
            if e.rect.colliderect(player_rect):
                if self.player.invuln_timer <= 0:
                    self.player.hp -= e.damage
                    self.player.invuln_timer = 0.5
                    if self.player.hp <= 0:
                        self.engine.change_state(GameOverState(self.engine, self.player, False, self.time_survived, self.difficulty))
                        return

        # XP Update
        for xp in self.xp_orbs:
            if not xp.active: continue
            xp.update(dt) # Update lifespan
            if not xp.active: continue # Check if it just died
            
            dist = math.hypot(self.player.x - xp.x, self.player.y - xp.y)
            if dist < self.player.pickup_radius:
                dx, dy = (self.player.x - xp.x)/dist, (self.player.y - xp.y)/dist
                xp.x += dx * 400 * dt
                xp.y += dy * 400 * dt
                
                if dist < self.player.size:
                    xp.active = False
                    self.player.xp += xp.value * self.player.experience_booster
                    while self.player.xp >= self.player.xp_required:
                        self.player.xp -= self.player.xp_required
                        self.player.level_ups_pending += 1
                        self.player.level += 1
                        self.player.xp_required = int(10 * (self.player.level ** 1.5))
        
        # Cleanup inactive orbs periodically
        if len(self.xp_orbs) > 1000:
            self.xp_orbs = [x for x in self.xp_orbs if x.active]

        # Handle Level Up Transition at the end of the update
        if self.player.level_ups_pending > 0:
            self.engine.change_state(LevelUpState(self.engine, self))
            return 

        # Spawn new enemies at the end of the frame
        viewport = (self.camera_offset[0], self.camera_offset[1], WINDOW_WIDTH, WINDOW_HEIGHT)
        WaveManager.spawn_wave(self.time_survived, viewport, self.player, self.enemies, self.difficulty_settings)

    def draw(self, screen: pygame.Surface):
        # Update camera (simple follow)
        self.camera_offset[0] += (self.player.x - WINDOW_WIDTH/2 - self.camera_offset[0]) * 0.1
        self.camera_offset[1] += (self.player.y - WINDOW_HEIGHT/2 - self.camera_offset[1]) * 0.1
        
        # clamping camera
        self.camera_offset[0] = max(0.0, min(MAP_SIZE - WINDOW_WIDTH, self.camera_offset[0]))
        self.camera_offset[1] = max(0.0, min(MAP_SIZE - WINDOW_HEIGHT, self.camera_offset[1]))
        
        viewport = pygame.Rect(self.camera_offset[0], self.camera_offset[1], WINDOW_WIDTH, WINDOW_HEIGHT)
        
        self.map_generator.draw(screen, self.camera_offset, viewport)
        
        for xp in self.xp_orbs:
            xp.draw(screen, self.camera_offset)
            
        for e in self.enemies:
            e.draw(screen, self.camera_offset)
            
        self.player.draw(screen, self.camera_offset)
        
        # UI
        self.hp_bar.set_progress(self.player.hp, self.player.max_hp)
        self.stamina_bar.set_progress(self.player.stamina, self.player.max_stamina)
        self.xp_bar.set_progress(self.player.xp, self.player.xp_required)
        
        self.hp_bar.draw(screen)
        self.stamina_bar.draw(screen)
        self.xp_bar.draw(screen)
        
        # XP Text
        xp_text = f"{int(self.player.xp)} / {self.player.xp_required}"
        xp_surf = self.font.render(xp_text, True, TEXT_LIGHT)
        screen.blit(xp_surf, (WINDOW_WIDTH - 20 - xp_surf.get_width(), WINDOW_HEIGHT - 70))
        
        info = self.font.render(f"Lvl: {self.player.level}  Kills: {self.player.kills}", True, TEXT_LIGHT)
        screen.blit(info, (WINDOW_WIDTH - 200, 20))
        
        # Remaining Time Timer
        rem_time = max(0.0, TOTAL_TIME_SEC - self.time_survived)
        mins = int(rem_time // 60)
        secs = int(rem_time % 60)
        timer_surf = self.font.render(f"{mins}:{secs:02d}", True, TEXT_LIGHT)
        screen.blit(timer_surf, timer_surf.get_rect(center=(WINDOW_WIDTH // 2, 30)))

if __name__ == "__main__":
    import math
    print("Game States parsed successfully.")
