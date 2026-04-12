import pygame
from math import hypot
from .base_entity import Entity
from ..core.config_manager import ConfigManager

class Player(Entity):
    def __init__(self):
        self.config = ConfigManager.get_instance()
        player_cfg = self.config.player
        world_cfg = self.config.world
        
        super().__init__(world_cfg.map_size // 2, world_cfg.map_size // 2, 24)
        
        # Stats
        self.base_speed = player_cfg.base_speed
        self.max_hp = player_cfg.max_hp
        self.hp = self.max_hp
        self.health_regen = player_cfg.health_regen
        self.armor = player_cfg.armor
        self.max_stamina = player_cfg.max_stamina
        self.stamina = self.max_stamina
        self.stamina_regen = player_cfg.stamina_regen
        self.level = 1
        self.xp = 0
        self.xp_required = player_cfg.xp_required_base
        self.kills = 0
        self.upgrade_choices = player_cfg.upgrade_choices
        self.level_ups_pending = 0
        
        # Combat / Dash
        self.dash_cooldown_max = player_cfg.dash_cooldown_max
        self.dash_cooldown = 0.0
        self.dash_cost = player_cfg.dash_cost
        self.dash_distance = player_cfg.dash_distance
        self.invuln_after_dash = player_cfg.invuln_after_dash
        
        # Weapons Group
        self.weapons = pygame.sprite.Group()
        
        # Explosion Stats
        self.explosion_radius = player_cfg.explosion_radius
        self.explosion_damage = player_cfg.explosion_damage
        self.explosion_cooldown_max = player_cfg.explosion_cooldown_max
        self.explosion_timer = 0.0
        self.explosion_knockback = player_cfg.explosion_knockback
        
        # Saturn Square Stats
        self.saturn_squares_count = player_cfg.saturn_squares_count
        self.saturn_squares_size = player_cfg.saturn_squares_size
        self.saturn_squares_hp = player_cfg.saturn_squares_hp
        self.saturn_squares_damage = player_cfg.saturn_squares_damage
        self.saturn_squares_knockback = player_cfg.saturn_squares_knockback
        self.saturn_squares_lifespan_active = True
        self.saturn_squares_rotation_speed = player_cfg.saturn_squares_rotation_speed
        self.saturn_squares_dash_boost = player_cfg.saturn_squares_dash_boost
        self.saturn_squares_dash_boost_duration = player_cfg.saturn_squares_dash_boost_duration
        self.saturn_squares_angle = 0.0
        
        # Magic Dash Stats
        self.dash_heal_amount = player_cfg.dash_heal_amount
        self.dash_sprint_boost = player_cfg.dash_sprint_boost
        self.dash_sprint_duration = player_cfg.dash_sprint_duration
        
        self.pickup_radius = player_cfg.pickup_radius
        self.experience_booster = 1.0
        self.invuln_timer = 0.0
        self.move_speed_modifier = 1.0

    def update(self, dt: float, input_system):
        # Use centralized movement vector
        move_vec = input_system.get_movement_vector()
        dx, dy = move_vec.x, move_vec.y

        length = hypot(dx, dy)
        if length > 0:
            dx /= length
            dy /= length

        # Update timers
        if self.dash_cooldown > 0:
            self.dash_cooldown -= dt
        if self.invuln_timer > 0:
            self.invuln_timer -= dt
            
        self.explosion_timer -= dt
        self.saturn_squares_angle = (self.saturn_squares_angle + self.saturn_squares_rotation_speed * dt) % 360
            
        # Stamina & Health Regen
        self.stamina = min(self.max_stamina, self.stamina + self.stamina_regen * dt)
        if self.health_regen > 0:
            self.hp = min(self.max_hp, self.hp + self.health_regen * dt)

        # Movement
        current_speed = self.base_speed * self.move_speed_modifier
        self.x += dx * current_speed * dt
        self.y += dy * current_speed * dt
        
        # Clamp bounds
        map_size = self.config.world.map_size
        self.x = max(self.size/2, min(map_size - self.size/2, self.x))
        self.y = max(self.size/2, min(map_size - self.size/2, self.y))

    def attempt_dash(self, dt: float, input_system):
        if self.dash_cooldown <= 0 and self.stamina >= self.dash_cost:
            self.stamina -= self.dash_cost
            self.dash_cooldown = self.dash_cooldown_max
            
            move_vec = input_system.get_movement_vector()
            dx, dy = move_vec.x, move_vec.y
            
            if dx == 0 and dy == 0:
                dx = 1 # Default

            length = hypot(dx, dy)
            if length > 0:
                dx /= length; dy /= length
                
            self.x += dx * self.dash_distance
            self.y += dy * self.dash_distance

            # Player after dash effects
            self.invuln_timer = self.invuln_after_dash
            
            # Weapon after dash effects
            for weapon in self.weapons:
                weapon.on_after_dash(dt)
            return True
        return False
        
    def draw(self, screen: pygame.Surface, camera_offset: tuple[float, float]):
        render_x = int(self.x - camera_offset[0] - self.size/2)
        render_y = int(self.y - camera_offset[1] - self.size/2)
        
        # Blink when invulnerable
        if self.invuln_timer > 0 and (pygame.time.get_ticks() // 100) % 2 == 0:
            return

        pygame.draw.rect(screen, self.config.player.color, (render_x, render_y, self.size, self.size))

