import pygame
from math import hypot
from .base_entity import Entity
from ..constants import PRIMARY, MAP_SIZE

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
        
        # Combat / Dash
        self.dash_cooldown_max = 1.5
        self.dash_cooldown = 0.0
        self.dash_cost = 30
        self.dash_distance = 100
        
        self.explosion_radius = 150
        self.explosion_damage = 50
        self.explosion_cooldown_max = 2.0
        self.explosion_timer = 0.0
        self.explosion_effect_timer = 0.0
        self.explosion_knockback = 300
        
        self.pickup_radius = 100
        self.invuln_timer = 0.0

    def update(self, dt: float):
        keys = pygame.key.get_pressed()
        dx, dy = 0, 0
        if keys[pygame.K_w] or keys[pygame.K_UP]: dy -= 1
        if keys[pygame.K_s] or keys[pygame.K_DOWN]: dy += 1
        if keys[pygame.K_a] or keys[pygame.K_LEFT]: dx -= 1
        if keys[pygame.K_d] or keys[pygame.K_RIGHT]: dx += 1

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
        if self.explosion_effect_timer > 0:
            self.explosion_effect_timer -= dt
            
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

    def attempt_dash(self, dt: float):
        keys = pygame.key.get_pressed()
        if self.dash_cooldown <= 0 and self.stamina >= self.dash_cost:
            self.stamina -= self.dash_cost
            self.dash_cooldown = self.dash_cooldown_max
            
            dx, dy = 0, 0
            if keys[pygame.K_w] or keys[pygame.K_UP]: dy -= 1
            if keys[pygame.K_s] or keys[pygame.K_DOWN]: dy += 1
            if keys[pygame.K_a] or keys[pygame.K_LEFT]: dx -= 1
            if keys[pygame.K_d] or keys[pygame.K_RIGHT]: dx += 1
            
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

        pygame.draw.rect(screen, PRIMARY, (render_x, render_y, self.size, self.size))

        if self.explosion_effect_timer > 0:
            pygame.draw.circle(screen, PRIMARY, (render_x + int(self.size/2), render_y + int(self.size/2)), int(self.explosion_radius), 2)

if __name__ == "__main__":
    p = Player()
    p.update(0.16)
    print("Player x, y:", p.x, p.y)
    print("Player instantiated successfully.")
