#!/usr/bin/python3
"""
markdown 2 html
"""
import sys
import os
import hashlib


def main():
    """
    Start the script
    """

    # Check if the number of arguments is correct
    if len(sys.argv) < 3:
        print("Usage: ./markdown2html.py README.md README.html",
              file=sys.stderr)
        sys.exit(1)

    # Check if the input file exists
    if not os.path.isfile(sys.argv[1]):
        print(f'Missing {sys.argv[1]}', file=sys.stderr)
        sys.exit(1)

    sys.exit(0)


if __name__ == "__main__":
    main()
