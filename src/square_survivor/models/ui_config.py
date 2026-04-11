from pydantic import Field
from .base_config import BaseConfig

class UIConfig(BaseConfig):
    """Configuration for UI theme and colors."""
    panel_bg_color: list[int] = Field(default=[22, 22, 30], description="Main panel background color")
    panel_border_color: list[int] = Field(default=[45, 45, 60], description="Control border color")
    text_light: list[int] = Field(default=[255, 255, 255], description="Primary text color")
    text_muted: list[int] = Field(default=[136, 136, 153], description="Secondary/de-emphasized text color")
    player_color_dim: list[int] = Field(default=[0, 240, 255, 76], description="Dimmed player color for UI")
    explosion_color: list[int] = Field(default=[0, 240, 255], description="Color for explosion effect (RGB)")
