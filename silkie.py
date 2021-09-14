import pathlib
import shutil
import glob
import click
from os import path, makedirs
from yattag import Doc, indent


SUPORTED_FILE_EXTENSION = ".txt"
DIST_DIRECTORY_PATH = path.join(
    path.dirname(path.realpath(__file__)), "dist")


class TextColor:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKCYAN = '\033[96m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'


@click.command()
@click.version_option("0.1.0", '-v', '--version')
@click.help_option('-h', '--help')
@click.option('-i', '--input', required=True, type=click.Path(exists=True, file_okay=True, dir_okay=True, readable=True), help='Path to the input file/folder')
@click.option('-s', '--stylesheet', help='URL path to a stylesheet')
def silkie(input, stylesheet):
    """Static site generator with the smoothness of silk"""
    # Clean build
    shutil.rmtree(DIST_DIRECTORY_PATH, ignore_errors=True)

    try:
        # Create build folder
        makedirs(DIST_DIRECTORY_PATH, exist_ok=True)
        # Generate static file(s)
        if path.isfile(input):
            if stylesheet:
                generate_static_file(input, stylesheet)
            else:
                generate_static_file(input)
        if path.isdir(input):
            for filepath in glob.glob(path.join(input, "*" + SUPORTED_FILE_EXTENSION)):
                if stylesheet:
                    generate_static_file(filepath, stylesheet)
                else:
                    generate_static_file(filepath)
    except OSError as e:
        click.echo(
            f"{TextColor.FAIL}\u2715 Error: Build directory can't be created!{TextColor.ENDC}")


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

    return ''


def get_filename(file_path: str) -> str:
    """Extract the name of the file without (all) its extension(s)"""
    return pathlib.Path(file_path.split('.')[0]).stem


def get_html_head(doc, title: str, file_path: str, stylesheet_url: str) -> None:
    """Get the metadata of the file and append them to the HTML document"""
    with doc.tag('head'):
        doc.stag('meta', charset='utf-8')
        doc.stag('meta', name='viewport',
                 content='width=device-width, initial-scale=1')
        with doc.tag('title'):
            if title:
                doc.text(title)
            else:
                doc.text(get_filename(file_path))
        if stylesheet_url:
            doc.stag('link', rel='stylesheet', href=stylesheet_url)


def get_html_paragraphs(line, title: str, file_path: str) -> None:
    """Get all paragraphs from text file and append them to the HTML document"""
    with open(file_path, 'r') as f:
        paragraphs = f.read().split("\n\n")

        if title:
            paragraphs.remove(title)
            line('h1', title)

        for p in paragraphs:
            line('p', p)


def get_html(file_path: str, stylesheet_url: str) -> str:
    """Return an indented HTML document with the content of the file"""
    doc, tag, text, line = Doc().ttl()
    title = get_title(file_path)

    doc.asis('<!DOCTYPE html>')
    with tag('html'):
        doc.attr(lang='en')
        get_html_head(doc, title, file_path, stylesheet_url)
        with tag('body'):
            get_html_paragraphs(line, title, file_path)

    return indent(doc.getvalue())


def write_static_file(filename: str, content: str) -> None:
    """Write the static file to `dist/` directory"""
    with open(path.join(DIST_DIRECTORY_PATH, filename + ".html"), 'w+') as static_file:
        static_file.write(content)
        click.echo(
            f"{TextColor.OKGREEN}{TextColor.BOLD}\u2713 Success: Static file for '{filename}' is generated in dist/{TextColor.ENDC}")


def generate_static_file(file_path: str, stylesheet_url: str = '') -> None:
    """
    Parse a text file and generate a single HTML file from its content.
    The generated files should be found inside `dist/` directory
    """
    html = get_html(file_path, stylesheet_url)
    write_static_file(get_filename(file_path), content=html)


if __name__ == '__main__':
    silkie()
