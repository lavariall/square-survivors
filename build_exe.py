import PyInstaller.__main__
import sys
import os

if __name__ == "__main__":
    print("Building Square Survivor .exe...")
    PyInstaller.__main__.run([
        'SquareSurvivor.spec',
        '--distpath', 'dist/windows',
        '--workpath', 'build/windows',
        '--clean'
    ])
    print("Build complete. Check the 'dist/windows' directory.")
