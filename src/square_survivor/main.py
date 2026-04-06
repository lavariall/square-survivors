import pygame
from .core.engine import Engine
from .game_states import MenuState

def main():
    engine = Engine()
    engine.change_state(MenuState(engine))
    engine.run()

if __name__ == "__main__":
    main()
