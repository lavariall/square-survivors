import math
import random
from typing import List
from ..entities.enemy import Enemy
from ..entities.player import Player
from ..constants import MAP_SIZE

class WaveManager:
    """Handles parsing time into enemy spawns safely outside the active viewport."""
    
    @staticmethod
    def spawn_wave(time_survived: float, viewport: tuple[float, float, float, float], player: Player, enemies: List[Enemy]):
        """
        viewport is (camera_x, camera_y, width, height)
        """
        active_enemies = sum(1 for e in enemies if e.active)
        target_enemies = 20 + int(time_survived * 0.5)
        
        if active_enemies >= target_enemies:
            return

        cx, cy, cw, ch = viewport
        
        # Spawn outside the viewport boundary
        angle = random.random() * math.pi * 2
        dist = max(cw, ch) / 2 + 100
        
        sx = player.x + math.cos(angle) * dist
        sy = player.y + math.sin(angle) * dist
        
        # Clamp to map
        sx = max(20.0, min(MAP_SIZE - 20.0, sx))
        sy = max(20.0, min(MAP_SIZE - 20.0, sy))
        
        # Calculate scaling stats
        hp = 30 + (time_survived * 0.3)
        speed = 80 + random.random() * 40 + (time_survived * 0.05)
        dmg = 10 + (time_survived * 0.05)
        
        # Find inactive enemy object or create
        spawned = False
        for e in enemies:
            if not e.active:
                e.active = True
                e.x, e.y = sx, sy
                e.hp, e.max_hp = hp, hp
                e.speed = speed
                e.damage = dmg
                spawned = True
                break
                
        if not spawned:
            enemies.append(Enemy(sx, sy, hp, speed, dmg))

if __name__ == "__main__":
    p = Player()
    enemies = []
    WaveManager.spawn_wave(10.0, (0,0, 1200, 800), p, enemies)
    print("Enemies in list:", len(enemies))
    print("Enemy active:", enemies[0].active)
