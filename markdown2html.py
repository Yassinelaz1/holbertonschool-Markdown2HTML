#!/usr/bin/python3
"""This script convert a markdown file into html file"""

import sys


def convert_markdown_to_html(input_file, output_file):
    try:
        with open(input_file, 'r') as md_file:
            markdown_content = md_file.read()
            converted = []
            for line in markdown_content:
                converted.append(line)
            with open(output_file, 'w') as html_file:
                for line in converted:
                    html_file.write(line)
    except FileNotFoundError:
        sys.stderr.write(f"Missing {input_file}\n")
        sys.exit(1)


if __name__ == "__main__":
    if len(sys.argv) < 3:
        sys.stderr.write("Usage: ./markdown2html.py README.md README.html\n")
        sys.exit(1)

    input_file = sys.argv[1]
    output_file = sys.argv[2]

    convert_markdown_to_html(input_file, output_file)
    sys.exit(0)
