import PyInstaller.__main__
import sys
import os

if __name__ == "__main__":
    print("Building Square Survivor .exe...")
    PyInstaller.__main__.run([
        'run_game.py',
        '--name', 'SquareSurvivor',
        '--onefile',
        '--noconsole',  # Don't open a terminal window when running the exe
        '--clean'
    ])
    print("Build complete. Check the 'dist' directory.")
