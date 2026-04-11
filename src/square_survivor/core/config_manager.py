import os
import time
from pathlib import Path
from typing import Optional

from ..models.player_config import PlayerConfig
from ..models.enemy_config import EnemiesConfig
from ..models.xp_orb_config import XPOrbConfig
from ..models.world_config import WorldConfig
from ..models.display_config import DisplayConfig
from ..models.difficulty_config import DifficultyConfig
from ..models.ui_config import UIConfig
from ..models.debug_config import DebugConfig

class ConfigManager:
    """Handles loading and hot-reloading of all game configuration files."""
    
    _instance: Optional["ConfigManager"] = None

    def __init__(self):
        # Resolve config directory relative to this file
        self.config_dir = Path(__file__).parent.parent / "configs"
        
        # Config Objects
        self.player: PlayerConfig = PlayerConfig()
        self.enemies: EnemiesConfig = EnemiesConfig(enemy_types={})
        self.xp_orbs: XPOrbConfig = XPOrbConfig()
        self.world: WorldConfig = WorldConfig()
        self.display: DisplayConfig = DisplayConfig()
        self.difficulty: DifficultyConfig = DifficultyConfig(tiers={}, priorities={})
        self.ui: UIConfig = UIConfig()
        self.debug: DebugConfig = DebugConfig()
        
        # File modification tracking
        self._last_loaded: dict[str, float] = {}
        
        self.load_all()

    @classmethod
    def get_instance(cls) -> "ConfigManager":
        if cls._instance is None:
            cls._instance = ConfigManager()
        return cls._instance

    def load_all(self):
        """Loads all JSON files into their respective models."""
        self.player = PlayerConfig.from_json(self.config_dir / "player.json")
        self.enemies = EnemiesConfig.from_json(self.config_dir / "enemies.json")
        self.xp_orbs = XPOrbConfig.from_json(self.config_dir / "xp_orbs.json")
        self.world = WorldConfig.from_json(self.config_dir / "world.json")
        self.display = DisplayConfig.from_json(self.config_dir / "display.json")
        self.difficulty = DifficultyConfig.from_json(self.config_dir / "difficulty.json")
        self.ui = UIConfig.from_json(self.config_dir / "ui_theme.json")
        self.debug = DebugConfig.from_json(self.config_dir / "debug_settings.json")
        
        # Update modification times
        for config_file in self.config_dir.glob("*.json"):
            self._last_loaded[config_file.name] = config_file.stat().st_mtime

    def check_for_updates(self):
        """Checks if any config files have changed and reloads them if hot-reloading is enabled."""
        if not self.debug.hot_reloading_enabled:
            return

        changed = False
        for config_file in self.config_dir.glob("*.json"):
            mtime = config_file.stat().st_mtime
            if mtime > self._last_loaded.get(config_file.name, 0):
                print(f"[ConfigManager] Reloading {config_file.name} due to change...")
                changed = True
                break
        
        if changed:
            try:
                self.load_all()
            except Exception as e:
                print(f"[ConfigManager] Error reloading configs: {e}")
