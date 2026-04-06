import pygame

# Colors (matching the CSS root vars)
BG_COLOR = (15, 15, 19)
PRIMARY = (0, 240, 255)
PRIMARY_DIM = (0, 240, 255, 76)
DANGER = (255, 0, 60)
XP_COLOR = (252, 238, 10)
TEXT_LIGHT = (255, 255, 255)
TEXT_MUTED = (136, 136, 153)
OBSTACLE_COLOR = (26, 26, 36)
OBSTACLE_BORDER = (42, 42, 58)
PANEL_BG = (22, 22, 30)
PANEL_BORDER = (45, 45, 60)
GRID_COLOR = (21, 21, 28)

# Game Settings
TOTAL_TIME_SEC = 10 * 60
MAP_SIZE = 4000
TILE_SIZE = 50

# Display Settings
WINDOW_WIDTH = 1200
WINDOW_HEIGHT = 800
FPS = 60

if __name__ == "__main__":
    print("Constants loaded successfully.")
    print("Map size:", MAP_SIZE)
