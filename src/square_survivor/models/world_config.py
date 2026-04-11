from pydantic import Field
from .base_config import BaseConfig

class WorldConfig(BaseConfig):
    """Configuration for the game world and map."""
    map_size: int = Field(default=4000, description="Size of the square map in pixels")
    tile_size: int = Field(default=50, description="Size of background grid tiles")
    total_time_sec: float = Field(default=600.0, description="Total match duration in seconds")
    max_xp_orbs: int = Field(default=1000, description="Maximum number of active XP orbs")
    obstacle_density: float = Field(default=0.005, description="Percentage of tiles that are obstacles")
    
    # Visuals
    bg_color: list[int] = Field(default=[15, 15, 19], description="Background color (R, G, B)")
    grid_color: list[int] = Field(default=[121, 121, 128], description="Grid line color (R, G, B)")
    obstacle_color: list[int] = Field(default=[255, 255, 255, 153], description="Obstacle fill (R, G, B, A)")
    obstacle_border_color: list[int] = Field(default=[255, 255, 255, 200], description="Obstacle border (R, G, B, A)")
