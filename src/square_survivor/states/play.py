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
from ..ui.components import ProgressBar
from ..constants import (WINDOW_WIDTH, WINDOW_HEIGHT, XP_ORB_COLOR, MAP_SIZE, 
                         OBSTACLE_DENSITY, DIFFICULTY_SETTINGS, MAX_XP_ORBS, 
                         XP_ORB_LIFESPAN, TEXT_LIGHT, PLAYER_COLOR, ENEMY_COLOR, 
                         TOTAL_TIME_SEC)

class PlayState(GameState):
    def __init__(self, engine, difficulty="Normal"):
        super().__init__(engine)
        self.player = Player()
        self.enemies: List[Enemy] = []
        self.xp_orbs: List[XPOrb] = []
        
        self.difficulty = difficulty
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

        self.combat_system = CombatSystem()
        self._init_saturn_squares()

    def _init_saturn_squares(self):
        """Initializes the rotating Saturn Squares."""
        for i in range(self.player.saturn_squares_count):
            angle = i * (360 / self.player.saturn_squares_count)
            offset = pygame.Vector2(100, 0).rotate(angle)
            square = SaturnSquare(
                self.player, 
                offset, 
                size=12, 
                damage=self.player.saturn_squares_damage,
                hp=self.player.saturn_squares_hp,
                knockback=50
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
        if self.time_survived >= TOTAL_TIME_SEC:
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
            # Simple logic to add missing ones (could be improved with a respawn timer)
            missing = self.player.saturn_squares_count - len(active_squares)
            for _ in range(missing):
                # Randomize starting angle for new squares if they were destroyed
                angle = random.uniform(0, 360)
                offset = pygame.Vector2(100, 0).rotate(angle)
                square = SaturnSquare(
                    self.player, 
                    offset, 
                    size=12, 
                    damage=self.player.saturn_squares_damage,
                    hp=self.player.saturn_squares_hp,
                    knockback=50
                )
                self.player.weapons.add(square)
        
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
                    # todo: please add a comment what jitter does
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
                        self.player.xp_required = int(10 * (self.player.level ** 1.5))
        
        # Cleanup inactive orbs periodically
        if len(self.xp_orbs) > 1000:
            self.xp_orbs = [x for x in self.xp_orbs if x.active]

        # Handle Level Up Transition at the end of the update
        if self.player.level_ups_pending > 0:
            from .level_up import LevelUpState
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
