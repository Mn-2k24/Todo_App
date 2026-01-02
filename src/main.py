"""Entry point for Phase I Todo App.

Run this module to start the application:
    python src/main.py
"""

import sys
from src.cli.menu import main_loop


if __name__ == "__main__":
    try:
        main_loop()
    except Exception as e:
        # Last resort error handling for unexpected errors
        print(f"Error: An unexpected error occurred: {e}", file=sys.stderr)
        sys.exit(1)
