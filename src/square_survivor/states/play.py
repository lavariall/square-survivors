import pygame
import math
import random
from typing import List
from .base import GameState
from ..core.input_system import InputAction
from ..entities.player import Player
from ..entities.enemy import Enemy
from ..entities.xp_orb import XPOrb
from ..systems.map_generator import MapGenerator
from ..systems.combat_system import CombatSystem
from ..systems.wave_manager import WaveManager
from ..entities.weapons.explosion import Explosion
from ..entities.weapons.saturn_square import SaturnSquare
from ..entities.weapons.healing_magic import HealingMagic
from ..entities.weapons.sprint_magic import SprintMagic
from ..ui.components import ProgressBar
from ..core.config_manager import ConfigManager

class PlayState(GameState):
    def __init__(self, engine, difficulty="Normal"):
        super().__init__(engine)
        self.config = ConfigManager.get_instance()
        self.player = Player()
        self.enemies: List[Enemy] = []
        self.xp_orbs: List[XPOrb] = []
        
        self.difficulty = difficulty
        self.difficulty_settings = self.config.difficulty.tiers.get(difficulty, self.config.difficulty.tiers["Normal"])
        
        self.map_generator = MapGenerator(density=self.difficulty_settings.obstacle_density)
        self.map_generator.generate((self.config.world.map_size//2, self.config.world.map_size//2))
        
        self.time_survived = 0.0
        self.camera_offset = [0.0, 0.0]
        
        # UI
        self.font = pygame.font.SysFont("Arial", 24, bold=True)
        self.hp_bar = ProgressBar(20, 20, 200, 20, self.config.enemies.enemy_types["basic"].color_normal)
        self.stamina_bar = ProgressBar(20, 50, 200, 20, self.config.player.color)
        win_w, win_h = self.config.display.window_width, self.config.display.window_height
        self.xp_bar = ProgressBar(20, win_h - 40, win_w - 40, 10, self.config.xp_orbs.color)

        self.combat_system = CombatSystem()
        self._init_saturn_squares()

    def _init_saturn_squares(self):
        """Initializes the rotating Saturn Squares with slot indices."""
        for i in range(self.player.saturn_squares_count):
            square = SaturnSquare(
                self.player, 
                i, 
                size=self.player.saturn_squares_size, 
                damage=self.player.saturn_squares_damage,
                hp=self.player.saturn_squares_hp,
                knockback=self.player.saturn_squares_knockback
            )
            self.player.weapons.add(square)

    def handle_event(self, event: pygame.event.Event):
        if self.engine.input.was_just_pressed(InputAction.DASH):
            self.player.attempt_dash(0.016, self.engine.input)

    def update(self, dt: float):
        if self.engine.input.was_just_pressed(InputAction.PAUSE):
            from .pause import PauseState
            self.engine.change_state(PauseState(self.engine, self))
            return

        self.time_survived += dt
        if self.time_survived >= self.config.world.total_time_sec:
            # Win logic
            from .game_over import GameOverState
            self.engine.change_state(GameOverState(self.engine, self.player, True, self.time_survived, self.difficulty))
            return

        self.player.update(dt, self.engine.input)
        self.map_generator.compute_collisions(self.player)


        # Update enemies
        for e in self.enemies:
            e.update(dt, self.player.x, self.player.y)
            if e.active:
                self.map_generator.compute_collisions(e)

        # Combat Process: Trigger Explosion
        if self.player.explosion_timer <= 0:
            self.player.explosion_timer = self.player.explosion_cooldown_max
            explosion = Explosion(
                self.player.x, 
                self.player.y, 
                self.player.explosion_radius, 
                self.player.explosion_damage, 
                self.player.explosion_knockback
            )
            self.player.weapons.add(explosion)

        # Process all Materialized Weapons
        self.combat_system.process_weapons(self.player, self.enemies, dt)
        
        # Responsible for respawning Saturn Squares if they are active in the build
        active_squares = [w for w in self.player.weapons if isinstance(w, SaturnSquare)]
        if len(active_squares) < self.player.saturn_squares_count:
            # Fill missing indices to maintain even spread
            current_indices = {w.index for w in active_squares}
            all_indices = set(range(self.player.saturn_squares_count))
            missing_indices = all_indices - current_indices
            
            for idx in missing_indices:
                square = SaturnSquare(
                    self.player, 
                    idx, 
                    size=self.player.saturn_squares_size, 
                    damage=self.player.saturn_squares_damage,
                    hp=self.player.saturn_squares_hp,
                    knockback=self.player.saturn_squares_knockback
                )
                self.player.weapons.add(square)
                
        # Handle Invisible Magic Weapons
        if self.player.dash_heal_amount > 0:
            if not any(isinstance(w, HealingMagic) for w in self.player.weapons):
                self.player.weapons.add(HealingMagic(self.player))
        
        if self.player.dash_sprint_boost > 1.0:
            if not any(isinstance(w, SprintMagic) for w in self.player.weapons):
                self.player.weapons.add(SprintMagic(self.player))
        
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
                    if len(self.xp_orbs) < self.config.world.max_xp_orbs:
                        xp = XPOrb(e.x, e.y, xp_val)
                        self.xp_orbs.append(xp)
                    else:
                        # Force recycle the oldest active one (lowest timer)
                        xp = min(self.xp_orbs, key=lambda x: x.timer)
                
                if xp:
                    # todo: please add a comment what jitter does
                    jitter = 15
                    xp.x, xp.y = e.x + random.randint(-jitter, jitter), e.y + random.randint(-jitter, jitter)
                    xp.value = xp_val
                    xp.active = True
                    xp.timer = self.config.xp_orbs.lifespan
                
                continue

            # Player takes damage
            if e.rect.colliderect(player_rect):
                if self.player.invuln_timer <= 0:
                    damage_taken = max(1.0, e.damage - self.player.armor)
                    self.player.hp -= damage_taken
                    self.player.invuln_timer = 0.5
                    if self.player.hp <= 0:
                        from .game_over import GameOverState
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
                        self.player.xp_required = int(self.config.player.xp_required_base * (self.player.level ** 1.5))
        
        # Cleanup inactive orbs periodically
        if len(self.xp_orbs) > self.config.world.max_xp_orbs:
            self.xp_orbs = [x for x in self.xp_orbs if x.active]

        # Handle Level Up Transition at the end of the update
        if self.player.level_ups_pending > 0:
            from .level_up import LevelUpState
            self.engine.change_state(LevelUpState(self.engine, self))
            return 

        # Spawn new enemies at the end of the frame
        win_w, win_h = self.config.display.window_width, self.config.display.window_height
        viewport = (self.camera_offset[0], self.camera_offset[1], win_w, win_h)
        WaveManager.spawn_wave(self.time_survived, viewport, self.player, self.enemies, self.difficulty_settings)

    def draw(self, screen: pygame.Surface):
        win_w, win_h = self.config.display.window_width, self.config.display.window_height
        map_size = self.config.world.map_size
        
        # Update camera (simple follow)
        self.camera_offset[0] += (self.player.x - win_w/2 - self.camera_offset[0]) * 0.1
        self.camera_offset[1] += (self.player.y - win_h/2 - self.camera_offset[1]) * 0.1
        
        # clamping camera
        self.camera_offset[0] = max(0.0, min(map_size - win_w, self.camera_offset[0]))
        self.camera_offset[1] = max(0.0, min(map_size - win_h, self.camera_offset[1]))
        
        viewport = pygame.Rect(self.camera_offset[0], self.camera_offset[1], win_w, win_h)
        
        self.map_generator.draw(screen, self.camera_offset, viewport)
        
        for xp in self.xp_orbs:
            xp.draw(screen, self.camera_offset)
            
        for e in self.enemies:
            e.draw(screen, self.camera_offset)
            
        for w in self.player.weapons:
            w.draw(screen, self.camera_offset)
            
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
        text_color = self.config.ui.text_light
        xp_surf = self.font.render(xp_text, True, text_color)
        screen.blit(xp_surf, (win_w - 20 - xp_surf.get_width(), win_h - 70))
        
        info = self.font.render(f"Lvl: {self.player.level}  Kills: {self.player.kills}", True, text_color)
        screen.blit(info, (win_w - 200, 20))
        
        # Remaining Time Timer
        rem_time = max(0.0, self.config.world.total_time_sec - self.time_survived)
        mins = int(rem_time // 60)
        secs = int(rem_time % 60)
        timer_surf = self.font.render(f"{mins}:{secs:02d}", True, text_color)
        screen.blit(timer_surf, timer_surf.get_rect(center=(win_w // 2, 30)))
