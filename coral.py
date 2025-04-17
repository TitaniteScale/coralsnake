#!/usr/bin/env python3
"""
CoralSnake CLI Entrypoint

Reads a .dust file, parses it, estimates materials, and prints the analysis.
"""

import sys
import os

# Adjust the path to include the src directory
# This allows running the script from the project root directory
script_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(script_dir, 'src'))

from coralsnake.core import process_dust_file

def main():
    if len(sys.argv) < 2:
        print("Usage: python coral.py <filename.dust>")
        sys.exit(1)

    file_path = sys.argv[1]

    # Process the file using the core logic
    output = process_dust_file(file_path)

    if output:
        print(output)
    else:
        # Errors should have been printed to stderr by process_dust_file
        sys.exit(1) # Exit with error status if processing failed

if __name__ == "__main__":
    main() 