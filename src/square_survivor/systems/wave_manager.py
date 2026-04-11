import math
import random
from typing import List
from ..entities.enemy import Enemy
from ..entities.player import Player
from ..core.config_manager import ConfigManager

class WaveManager:
    """Handles parsing time into enemy spawns safely outside the active viewport."""
    
    @staticmethod
    def spawn_wave(time_survived: float, viewport: tuple[float, float, float, float], player: Player, enemies: List[Enemy], difficulty_settings):
        """
        viewport is (camera_x, camera_y, width, height)
        """
        config = ConfigManager.get_instance()
        enemy_cfg = config.enemies
        basic_cfg = enemy_cfg.enemy_types["basic"]
        world_cfg = config.world
        
        active_enemies = sum(1 for e in enemies if e.active)
        
        # Difficulty-based numbers
        spawn_mult = difficulty_settings.spawn_mult
        target_enemies = int((enemy_cfg.spawn_base_count + int(time_survived * enemy_cfg.spawn_scale_per_sec)) * spawn_mult)
        
        if active_enemies >= target_enemies:
            return

        cx, cy, cw, ch = viewport
        
        # Spawn outside the viewport boundary
        angle = random.random() * math.pi * 2
        dist = max(cw, ch) / 2 + enemy_cfg.spawn_distance_margin
        
        sx = player.x + math.cos(angle) * dist
        sy = player.y + math.sin(angle) * dist
        
        # Clamp to map
        edge_margin = 20.0
        map_size = world_cfg.map_size
        sx = max(edge_margin, min(map_size - edge_margin, sx))
        sy = max(edge_margin, min(map_size - edge_margin, sy))
        
        # Elite logic
        endgame_time = difficulty_settings.endgame_time
        chance_max = difficulty_settings.elite_chance_max
        total_time = world_cfg.total_time_sec
        
        if time_survived >= total_time - endgame_time:
            elite_chance = chance_max
        else:
            # Linear scaling
            scale_progress = time_survived / (total_time - endgame_time)
            elite_chance = scale_progress * chance_max
            
        is_elite = random.random() < elite_chance
        
        # Calculate scaling stats
        hp = basic_cfg.hp_base + (time_survived * basic_cfg.hp_scale_per_sec)
        if is_elite:
            hp *= basic_cfg.elite_hp_mult
            
        speed = basic_cfg.speed_base + random.random() * basic_cfg.speed_variance + (time_survived * basic_cfg.speed_scale_per_sec)
        dmg = basic_cfg.damage_base + (time_survived * basic_cfg.damage_scale_per_sec)
        
        # Find inactive enemy object or create
        spawned = False
        for e in enemies:
            if not e.active:
                e.active = True
                e.is_elite = is_elite
                e.size = basic_cfg.size_elite if is_elite else basic_cfg.size_normal
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
