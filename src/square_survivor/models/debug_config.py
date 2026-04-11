from pydantic import Field
from .base_config import BaseConfig

class DebugConfig(BaseConfig):
    """Configuration for developers and debugging."""
    hot_reloading_enabled: bool = Field(default=False, description="Enable automatic config reload on file change")
    show_fps: bool = Field(default=False, description="Display FPS in the corner")
    god_mode: bool = Field(default=False, description="Player is invincible")
