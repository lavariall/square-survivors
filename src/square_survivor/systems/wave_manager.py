import math
import random
from typing import List
from ..entities.enemy import Enemy
from ..entities.player import Player
from ..constants import MAP_SIZE

class WaveManager:
    """Handles parsing time into enemy spawns safely outside the active viewport."""
    
    @staticmethod
    def spawn_wave(time_survived: float, viewport: tuple[float, float, float, float], player: Player, enemies: List[Enemy], difficulty_settings: dict):
        """
        viewport is (camera_x, camera_y, width, height)
        """
        active_enemies = sum(1 for e in enemies if e.active)
        
        # Difficulty-based numbers
        spawn_mult = difficulty_settings.get("spawn_mult", 1.0)
        target_enemies = int((20 + int(time_survived * 0.5)) * spawn_mult)
        
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
        
        # Elite logic
        from ..constants import TOTAL_TIME_SEC
        endgame_time = difficulty_settings.get("endgame_time", 120)
        chance_max = difficulty_settings.get("elite_chance_max", 0.0)
        
        if time_survived >= TOTAL_TIME_SEC - endgame_time:
            elite_chance = chance_max
        else:
            # Linear scaling
            scale_progress = time_survived / (TOTAL_TIME_SEC - endgame_time)
            elite_chance = scale_progress * chance_max
            
        is_elite = random.random() < elite_chance
        
        # Calculate scaling stats
        hp = 30 + (time_survived * 0.3)
        if is_elite:
            hp *= 2.0
            
        speed = 80 + random.random() * 40 + (time_survived * 0.05)
        dmg = 10 + (time_survived * 0.05)
        
        # Find inactive enemy object or create
        spawned = False
        for e in enemies:
            if not e.active:
                e.active = True
                e.is_elite = is_elite
                e.size = 30 if is_elite else 20
                e.x, e.y = sx, sy
                e.hp, e.max_hp = hp, hp
                e.speed = speed
                e.damage = dmg
                spawned = True
                break
                
        if not spawned:
            enemies.append(Enemy(sx, sy, hp, speed, dmg, is_elite=is_elite))

if __name__ == "__main__":
    p = Player()
    enemies = []
    WaveManager.spawn_wave(10.0, (0,0, 1200, 800), p, enemies)
    print("Enemies in list:", len(enemies))
    print("Enemy active:", enemies[0].active)
