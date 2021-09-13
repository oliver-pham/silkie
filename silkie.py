import os
import pathlib
import shutil
import click


SUPORTED_FILETYPE = ".txt"
BLANK_TITLE = "Untitled"
DIST_DIRECTORY_PATH = os.path.join(
    os.path.dirname(os.path.realpath(__file__)), "dist")


@click.command()
@click.version_option("0.1.0", '-v', '--version')
@click.help_option('-h', '--help')
@click.option('-i', '--input', required=True, type=click.Path(exists=True, file_okay=True, dir_okay=True, readable=True), help='Path to the input file/folder')
@click.option('-s', '--stylesheet', help='URL path to a stylesheet')
def silkie(input, stylesheet):
    """Static site generator with the smoothness of silk"""
    # Clean build
    shutil.rmtree(DIST_DIRECTORY_PATH, ignore_errors=True)
    # Create build folder
    os.makedirs(DIST_DIRECTORY_PATH)
    # Generate static file(s)
    if os.path.isfile(input):
        generate_static_file(input, stylesheet)
    if os.path.isdir(input):
        for filename in os.listdir(input):
            if filename.endswith(SUPORTED_FILETYPE):
                generate_static_file(os.path.join(input, filename), stylesheet)


def get_html_paragraph(content: str) -> str:
    """Enclose the `content` with HTML paragraph tags (`<p></p>`) and return it"""
    if content == '':
        return ''

    return f"<p>{content}</p>"


def get_title(file_path: str) -> str:
    """
    Get the title of the file based on its position in the file.
    If there is a title, it will be the first line followed by two blank lines.
    """
    
    with open(file_path, 'r') as f:
        MAX_BLANK_LINES = 2
        blank_lines = 0
        lines = f.read().splitlines()

        for line in lines[:MAX_BLANK_LINES + 1]:
            if line.strip() == '':
                blank_lines += 1

        if (blank_lines == MAX_BLANK_LINES):
            return lines[0]

    return BLANK_TITLE


def process_text_file(file_path: str, first_line_is_title: bool = False) -> str:
    """
    Parse a single file and convert the paragraphs into HTML ones.
    If the first line in the file is the title, set `first_line_is_title` to `True`.
    """
    paragraphs = []

    with open(file_path, 'r') as f:
        lines = f.read().split("\n\n")
        paragraphs = list(map(get_html_paragraph, lines))

    if (first_line_is_title):
        paragraphs.pop(0)

    return ''.join(paragraphs)


def generate_static_file(file_path: str, stylesheet_url: str) -> None:
    """
    Generate a single HTML file inside `dist/` folder.
    """
    title = get_title(file_path)
    html = f"""
    <!doctype html>
    <html lang="en">
        <head>
            <meta charset="utf-8">
            <link rel="stylesheet" href="{stylesheet_url if stylesheet_url != None else ''}">
            <title>{title}</title>
            <meta name="viewport" content="width=device-width, initial-scale=1">
        </head>
        <body>
            <h1>{title}</h1>
            { process_text_file(file_path, title != BLANK_TITLE) }
        </body>
    </html>
    """

    with open(os.path.join(DIST_DIRECTORY_PATH, title + ".html"), 'w+') as static_file:
        static_file.write(html)


if __name__ == '__main__':
    silkie()
