import json
from pathlib import Path
from typing import Any, Type, TypeVar
from pydantic import BaseModel, ConfigDict

T = TypeVar("T", bound="BaseConfig")

class BaseConfig(BaseModel):
    """Base class for all configuration models."""
    model_config = ConfigDict(frozen=True)

    @classmethod
    def from_json(cls: Type[T], path: str | Path) -> T:
        """Loads configuration from a JSON file."""
        with open(path, "r", encoding="utf-8") as f:
            data = json.load(f)
        return cls(**data)

    def to_pygame_color(self, color_list: list[int]) -> tuple[int, ...]:
        """Converts a list (from JSON) to a tuple (for Pygame)."""
        return tuple(color_list)
