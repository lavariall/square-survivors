import pygame

# Colors (matching the CSS root vars)
BG_COLOR = (15, 15, 19)
PRIMARY = (0, 240, 255)
PRIMARY_DIM = (0, 240, 255, 76)
DANGER = (255, 0, 60)
XP_COLOR = (252, 238, 10)
TEXT_LIGHT = (255, 255, 255)
TEXT_MUTED = (136, 136, 153)
OBSTACLE_COLOR = (255, 255, 255, 153)
OBSTACLE_BORDER = (255, 255, 255, 200)
PANEL_BG = (22, 22, 30)
PANEL_BORDER = (45, 45, 60)
GRID_COLOR = (21, 21, 28)
ELITE_COLOR = (255, 140, 0) # Orange

# Difficulty Settings
DIFFICULTY_SETTINGS = {
    "Easy": {
        "spawn_mult": 0.7,
        "elite_chance_max": 0.0,
        "endgame_time": 120,
        "obstacle_density": 0.005
    },
    "Normal": {
        "spawn_mult": 1.0,
        "elite_chance_max": 0.6,
        "endgame_time": 120,
        "obstacle_density": 0.015
    },
    "Hard": {
        "spawn_mult": 1.4,
        "elite_chance_max": 1.0,
        "endgame_time": 120,
        "obstacle_density": 0.02
    },
    "Ultra": {
        "spawn_mult": 1.4,
        "elite_chance_max": 1.0,
        "endgame_time": 240,
        "obstacle_density": 0.03
    }
}

DIFF_PRIORITY = {"Easy": 0, "Normal": 1, "Hard": 2, "Ultra": 3}

# Game Settings
TOTAL_TIME_SEC = 10 * 60
MAP_SIZE = 4000
TILE_SIZE = 50
OBSTACLE_DENSITY = 0.005  # is this still used at all?
MAX_XP_ORBS = 1000
XP_ORB_LIFESPAN = 10.0 # seconds

# Display Settings
WINDOW_WIDTH = 1200
WINDOW_HEIGHT = 800
FPS = 60

if __name__ == "__main__":
    print("Constants loaded successfully.")
    print("Map size:", MAP_SIZE)
