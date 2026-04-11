from pydantic import Field
from .base_config import BaseConfig

class XPOrbConfig(BaseConfig):
    """Configuration for Experience Orbs."""
    lifespan: float = Field(default=10.0, description="Lifespan in seconds before disappearing")
    size: int = Field(default=8, description="Diameter of the orb in pixels")
    color: list[int] = Field(default=[252, 238, 10], description="Orb color (R, G, B)")
    default_value: float = Field(default=1.0, description="Base experience value")
