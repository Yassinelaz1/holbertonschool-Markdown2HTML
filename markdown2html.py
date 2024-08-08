#!/usr/bin/env python3
"""
mardown 2 html
    """
import sys
import os
import re
import hashlib


def parse_heading(line):
    """
    markdown 2 html
    """
    heading_level = len(line) - len(line.lstrip('#'))
    heading_text = line[heading_level:].strip()
    return f"<h{heading_level}>{heading_text}</h{heading_level}>"


def parse_unordered_list(lines):
    """
    markdown 2 html
    """
    ul = []
    for line in lines:
        if line.startswith('- '):
            ul.append(f"<li>{line[2:].strip()}</li>")
    if ul:
        return "<ul>\n" + "\n".join(ul) + "\n</ul>"
    return ""


def parse_ordered_list(lines):
    """
    markdown 2 html
    """
    ol = []
    for line in lines:
        if line.startswith('* '):
            ol.append(f"<li>{line[2:].strip()}</li>")
    if ol:
        return "<ol>\n" + "\n".join(ol) + "\n</ol>"
    return ""


def parse_paragraph(lines):
    """
    markdown 2 html
    """
    paragraphs = []
    paragraph = []
    for line in lines:
        line = line.strip()
        if line:
            paragraph.append(line)
        else:
            if paragraph:
                paragraphs.append(
                    "<p>\n" + "<br/>\n".join(paragraph) + "\n</p>")
                paragraph = []
    if paragraph:
        paragraphs.append("<p>\n" + "<br/>\n".join(paragraph) + "\n</p>")
    return "\n".join(paragraphs)


def parse_bold_emphasis(text):
    """
    markdown 2 html
    """
    text = re.sub(r'\*\*(.*?)\*\*', r'<b>\1</b>', text)
    text = re.sub(r'__(.*?)__', r'<em>\1</em>', text)
    return text


def parse_custom_syntax(text):
    """
    markdown 2 html
    """
    text = re.sub(
        r'\[\[(.*?)\]\]',
        lambda m: hashlib.md5(
            m.group(1).encode()).hexdigest(),
        text)
    text = re.sub(
        r'\(\((.*?)\)\)',
        lambda m: m.group(1).replace(
            'c',
            '').replace(
            'C',
            ''),
        text)
    return text


if __name__ == "__main__":
    """
    markdown 2 html
    """
    if len(sys.argv) < 3:
        print("Usage: ./markdown2html.py README.md README.html",
              file=sys.stderr)
        sys.exit(1)

    markdown_file = sys.argv[1]
    html_file = sys.argv[2]

    if not os.path.exists(markdown_file):
        print(f"Missing {markdown_file}", file=sys.stderr)
        sys.exit(1)

    with open(markdown_file,
              'r') as md_file, open(html_file, 'w') as html_file:
        lines = md_file.readlines()
        in_ulist, in_olist = False, False
        paragraph_lines = []
        for i, line in enumerate(lines):
            stripped_line = parse_bold_emphasis(line.strip())
            stripped_line = parse_custom_syntax(stripped_line)

            if stripped_line.startswith('#'):
                if paragraph_lines:
                    html_file.write(parse_paragraph(paragraph_lines) + '\n')
                    paragraph_lines = []
                html_file.write(parse_heading(stripped_line) + '\n')
            elif stripped_line.startswith('- '):
                if paragraph_lines:
                    html_file.write(parse_paragraph(paragraph_lines) + '\n')
                    paragraph_lines = []
                if in_olist:
                    html_file.write("</ol>\n")
                    in_olist = False
                if not in_ulist:
                    in_ulist = True
                    html_file.write("<ul>\n")
                html_file.write(f"<li>{stripped_line[2:]}</li>\n")
                if i + 1 >= len(lines) or not lines[i + 1].startswith('- '):
                    html_file.write("</ul>\n")
                    in_ulist = False
            elif stripped_line.startswith('* '):
                if paragraph_lines:
                    html_file.write(parse_paragraph(paragraph_lines) + '\n')
                    paragraph_lines = []
                if in_ulist:
                    html_file.write("</ul>\n")
                    in_ulist = False
                if not in_olist:
                    in_olist = True
                    html_file.write("<ol>\n")
                html_file.write(f"<li>{stripped_line[2:]}</li>\n")
                if i + 1 >= len(lines) or not lines[i + 1].startswith('* '):
                    html_file.write("</ol>\n")
                    in_olist = False
            else:
                paragraph_lines.append(stripped_line)
        if paragraph_lines:
            html_file.write(parse_paragraph(paragraph_lines) + '\n')

    sys.exit(0)
