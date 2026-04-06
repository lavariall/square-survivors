import sys
import os

# Add the src directory to the python path so absolute imports work correctly
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), 'src')))

from square_survivor.main import main

if __name__ == "__main__":
    main()
