from pydantic import Field, ConfigDict
from .base_config import BaseConfig

class DisplayConfig(BaseConfig):
    """Configuration for window and rendering."""
    model_config = ConfigDict(frozen=False)
    
    window_width: int = Field(default=1200, description="Window width in pixels")
    window_height: int = Field(default=800, description="Window height in pixels")
    fullscreen: bool = Field(default=False, description="Whether to start in fullscreen mode")
    fps: int = Field(default=60, description="Target frames per second")
    title: str = Field(default="Square Survivor", description="Window title")
