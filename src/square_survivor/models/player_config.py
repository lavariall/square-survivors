from pydantic import Field
from .base_config import BaseConfig

class PlayerConfig(BaseConfig):
    """Configuration for Player stats and weapons."""
    # Base Stats
    base_speed: float = Field(default=200.0, description="Movement speed in pixels per second")
    max_hp: float = Field(default=100.0, description="Maximum health points")
    health_regen: float = Field(default=0.0, description="Health regenerated per second")
    max_stamina: float = Field(default=100.0, description="Maximum stamina points")
    stamina_regen: float = Field(default=20.0, description="Stamina regenerated per second")
    xp_required_base: int = Field(default=10, description="Base XP required for the first level up")
    upgrade_choices: int = Field(default=3, description="Number of upgrade choices offered on level up")
    pickup_radius: float = Field(default=100.0, description="Radius for picking up XP orbs")
    
    # Dash Stats
    dash_cooldown_max: float = Field(default=1.5, description="Seconds between dashes")
    dash_cost: float = Field(default=30.0, description="Stamina cost per dash")
    dash_distance: float = Field(default=100.0, description="Distance covered in one dash")
    
    # Weapon: Explosion Stats
    explosion_radius: float = Field(default=150.0, description="Radius of effect")
    explosion_damage: float = Field(default=50.0, description="Damage dealt")
    explosion_cooldown_max: float = Field(default=2.0, description="Seconds between explosions")
    explosion_knockback: float = Field(default=300.0, description="Knockback force")
    
    # Weapon: Saturn Square Stats
    saturn_squares_count: int = Field(default=3, description="Initial number of orbiting squares")
    saturn_squares_size: float = Field(default=50.0, description="Size of each square")
    saturn_squares_hp: float = Field(default=50.0, description="Durability of each square")
    saturn_squares_damage: float = Field(default=10.0, description="Damage per hit")
    saturn_squares_knockback: float = Field(default=50.0, description="Knockback force")
    saturn_squares_rotation_speed: float = Field(default=180.0, description="Degrees per second")
    
    # Visuals
    color: list[int] = Field(default=[0, 240, 255], description="Main player color (R, G, B)")
    color_dim: list[int] = Field(default=[0, 240, 255, 76], description="Dimmed player color (R, G, B, A)")
