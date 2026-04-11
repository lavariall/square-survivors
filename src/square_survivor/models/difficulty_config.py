from typing import Dict
from pydantic import Field
from .base_config import BaseConfig

class DifficultyTierConfig(BaseConfig):
    """Configuration for a specific difficulty level."""
    spawn_mult: float = Field(description="Multiplier for enemy spawn rates")
    elite_chance_max: float = Field(description="Maximum percentage of elite enemies")
    endgame_time: float = Field(description="Match seconds considered 'endgame'")
    obstacle_density: float = Field(description="Map obstacle coverage for this difficulty")

class DifficultyConfig(BaseConfig):
    """Container for all difficulty tiers and priorities."""
    tiers: Dict[str, DifficultyTierConfig] = Field(description="Map of difficulty names to settings")
    priorities: Dict[str, int] = Field(description="Ranking of difficulties (for UI sorting)")
    default_tier: str = Field(default="Normal", description="Initially selected difficulty")
