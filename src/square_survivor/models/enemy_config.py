from typing import Dict
from pydantic import Field
from .base_config import BaseConfig

class EnemyTypeConfig(BaseConfig):
    """Configuration for a specific enemy type."""
    # Base Stats
    hp_base: float = Field(default=30.0, description="Base health points")
    hp_scale_per_sec: float = Field(default=0.3, description="Health increase per second of survival")
    
    speed_base: float = Field(default=80.0, description="Minimum base movement speed")
    speed_variance: float = Field(default=40.0, description="Random variance added to speed")
    speed_scale_per_sec: float = Field(default=0.05, description="Speed increase per second of survival")
    
    damage_base: float = Field(default=10.0, description="Base damage dealt to player")
    damage_scale_per_sec: float = Field(default=0.05, description="Damage increase per second of survival")
    
    armor_base: float = Field(default=5.0, description="Base armor points")
    armor_scale_per_sec: float = Field(default=0.0, description="Armor increase per second of survival")
    
    # Visuals & Size
    size_normal: int = Field(default=20, description="Pixel size of normal version")
    size_elite: int = Field(default=30, description="Pixel size of elite version")
    color_normal: list[int] = Field(default=[255, 0, 60], description="Base color (R, G, B)")
    color_elite: list[int] = Field(default=[255, 140, 0], description="Elite variant color (R, G, B)")
    xp_value: int = Field(default=1, description="Base XP granted when killed")
    
    # Elite Scaling
    elite_hp_mult: float = Field(default=2.0, description="Multiplier for elite health")
    elite_armor_mult: float = Field(default=1.5, description="Multiplier for elite armor")

class EnemiesConfig(BaseConfig):
    """Configuration for all enemies and spawn limits."""
    enemy_types: Dict[str, EnemyTypeConfig] = Field(description="Dictionary of enemy configurations")
    spawn_base_count: int = Field(default=20, description="Base number of enemies to target")
    spawn_scale_per_sec: float = Field(default=0.5, description="Target enemy count increase per second")
    spawn_distance_margin: float = Field(default=100.0, description="Margin outside viewport to spawn enemies")
