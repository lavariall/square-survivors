import pygame
from math import hypot
from .base_entity import Entity
from ..constants import PLAYER_COLOR, MAP_SIZE

class Player(Entity):
    def __init__(self):
        super().__init__(MAP_SIZE // 2, MAP_SIZE // 2, 24)
        
        # Stats
        self.base_speed = 200
        self.max_hp = 100
        self.hp = 100
        self.health_regen = 0
        self.max_stamina = 100
        self.stamina = 100
        self.stamina_regen = 20
        self.level = 1
        self.xp = 0
        self.xp_required = 10
        self.kills = 0
        self.upgrade_choices = 3
        self.level_ups_pending = 0
        
        # Combat / Dash
        self.dash_cooldown_max = 1.5
        self.dash_cooldown = 0.0
        self.dash_cost = 30
        self.dash_distance = 100
        
        # Weapons Group
        self.weapons = pygame.sprite.Group()
        
        # Explosion Stats
        self.explosion_radius = 150
        self.explosion_damage = 50
        self.explosion_cooldown_max = 2.0
        self.explosion_timer = 0.0
        self.explosion_knockback = 300
        
        # Saturn Square Stats
        self.saturn_squares_count = 3
        self.saturn_squares_hp = 50
        self.saturn_squares_damage = 10
        self.saturn_squares_lifespan_active = True
        self.saturn_squares_rotation_speed = 180.0
        
        self.pickup_radius = 100
        self.experience_booster = 1.0
        self.invuln_timer = 0.0

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
            
        # Stamina & Health Regen
        self.stamina = min(self.max_stamina, self.stamina + self.stamina_regen * dt)
        if self.health_regen > 0:
            self.hp = min(self.max_hp, self.hp + self.health_regen * dt)

        # Movement
        self.x += dx * self.base_speed * dt
        self.y += dy * self.base_speed * dt
        
        # Clamp bounds
        self.x = max(self.size/2, min(MAP_SIZE - self.size/2, self.x))
        self.y = max(self.size/2, min(MAP_SIZE - self.size/2, self.y))

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
            return True
        return False
        
    def draw(self, screen: pygame.Surface, camera_offset: tuple[float, float]):
        render_x = int(self.x - camera_offset[0] - self.size/2)
        render_y = int(self.y - camera_offset[1] - self.size/2)
        
        # Blink when invulnerable
        if self.invuln_timer > 0 and (pygame.time.get_ticks() // 100) % 2 == 0:
            return

        pygame.draw.rect(screen, PLAYER_COLOR, (render_x, render_y, self.size, self.size))

if __name__ == "__main__":
    p = Player()
    p.update(0.16)
    print("Player x, y:", p.x, p.y)
    print("Player instantiated successfully.")
