import math
from typing import List
from ..entities.player import Player
from ..entities.enemy import Enemy

class CombatSystem:
    """Decoupled handler for explosions and combat logistics."""
    
    @staticmethod
    def process_explosions(player: Player, enemies: List[Enemy]):
        """Trigger an explosion if cooldown is met, dealing damage and knockback."""
        if player.explosion_timer <= 0:
            player.explosion_timer = player.explosion_cooldown_max
            player.explosion_effect_timer = 0.2
            # Play effect triggers should be routed via an event bus or handled in play_state.
            # Here we resolve simply math and HP logistics.
            
            for enemy in enemies:
                if not enemy.active: continue
                dist = math.hypot(player.x - enemy.x, player.y - enemy.y)
                if dist < player.explosion_radius + enemy.size/2:
                    enemy.hp -= player.explosion_damage
                    # Apply knockback safely
                    if enemy.hp > 0:
                        kx = (enemy.x - player.x) / dist
                        ky = (enemy.y - player.y) / dist
                        enemy.x += kx * player.explosion_knockback
                        enemy.y += ky * player.explosion_knockback

if __name__ == "__main__":
    p = Player()
    p.explosion_timer = -1
    e = Enemy(p.x + 50, p.y, 100, 50, 10)
    print("Enemy HP before explosion:", e.hp)
    CombatSystem.process_explosions(p, [e])
    print("Enemy HP after explosion:", e.hp)
    print("Enemy pushed to:", e.x, e.y)
