import pathlib
import shutil
import glob
from typing import AnyStr
import click
import re
from os import path, makedirs
from yattag import Doc, indent


SUPORTED_FILE_EXTENSION = ".txt"
SUPORTED_FILE_EXTENSION2 = ".md"
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
        # TODO: need to refactor the code to be shorter but should be fine for now
        if path.isfile(input):
            if stylesheet:
                generate_static_file(SUPORTED_FILE_EXTENSION, stylesheet)
            else:
                generate_static_file(input, SUPORTED_FILE_EXTENSION)
        if path.isfile(input):
            if stylesheet:
                generate_static_file(SUPORTED_FILE_EXTENSION2, stylesheet)
            else:
                generate_static_file(input, SUPORTED_FILE_EXTENSION2)
        if path.isdir(input):
           for filepath in glob.glob(path.join(input, "*" + SUPORTED_FILE_EXTENSION)):
                if stylesheet:
                    generate_static_file(filepath, SUPORTED_FILE_EXTENSION, stylesheet)
                else:
                    generate_static_file(filepath, SUPORTED_FILE_EXTENSION)
        if path.isdir(input):
            for filepath in glob.glob(path.join(input, "*" + SUPORTED_FILE_EXTENSION2)):
                if stylesheet:
                    generate_static_file(filepath, SUPORTED_FILE_EXTENSION2, stylesheet)
                else:
                    generate_static_file(filepath, SUPORTED_FILE_EXTENSION2)
    except OSError as e:
        click.echo(
            f"{TextColor.FAIL}\u2715 Error: Build directory can't be created!{TextColor.ENDC}")


def get_title(file_path: str) -> str:
    """
    Get the title of the file based on its position in the file.
    If there is a title, it will be the first line followed by two blank lines.
    """
    with open(file_path, 'r', encoding='utf-8') as f:
        # regEx matches everything except line terminators from the beginning and 3 line-feed characters (2 new lines)
        title = re.compile(r'^.+(\n\n\n)').search(f.read())
        if(title != None):
            return title.group(0).strip()
    return ''


def get_filename(file_path: str) -> str:
    file_path = re.compile(r'([^\/]+$)').search(file_path).group()
    """Extract the name of the file without (all) its extension(s)"""
    return pathlib.Path(file_path.split('.')[1]).stem


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
    with open(file_path, 'r', encoding='utf-8') as f:
        paragraphs = f.read()[len(title)+1 : -1].strip().split("\n\n")
        if title:
            line('h1', title)
        for p in paragraphs:
            line('p', p)

def get_html_paragraphs_parsewithmd(line, title: str, file_path: str) -> None:
    """ Append the approapriate markdown properties, .md headers, lists, links, images, tables"""
    with open(file_path, 'r',  encoding='utf-8') as f:
        paragraphs = f.read().split('\n')
        for p in paragraphs: 
            if p != '\n':
                if p.startswith('#'): # starts with certain headers in markdown
                    if p.startswith('# '):
                        p = p.replace('# ', '', 1)
                        line('h1', p)
                    elif p.startswith('## '):
                        p = p.replace('## ', '', 1)
                        line('h2', p)
                    elif p.startswith('### '):
                        p = p.replace('### ', '', 1)
                        line('h3', p)
                    else:
                        p = p.replace('#', '', 1)
                        line('h4', p)
                elif p.startswith('!['): # starts with image
                    p = p.replace('![', '<a href="', 1)
                    p = p.replace('](', '">', 1)
                    p = p.replace(')', '</a>', 1)
                    p = p.join('\n')
                    line('p', p)
                elif p.startswith('**'): # bold text
                    p = p.replace('__', '', 1)
                    line('b', p)
                elif p.startswith('__'): # bold text version 2
                    p = p.replace('**', '', 1)
                    line('b', p)
                else:
                    p = p.replace('\n', '<br>', 1)
                    line('p', p)
            


def get_html(file_path: str, stylesheet_url: str, extension: str) -> str:
    """Return an indented HTML document with the content of the file"""
    
    doc, tag, text, line = Doc().ttl()
    title = get_title(file_path)

    doc.asis('<!DOCTYPE html>')
    with tag('html'):
        doc.attr(lang='en')
        get_html_head(doc, title, file_path, stylesheet_url)
        with tag('body'):
            if extension == ".txt":
                get_html_paragraphs(line, title, file_path)
            elif extension == '.md':
                get_html_paragraphs_parsewithmd(line, title, file_path)
    return indent(doc.getvalue())


def write_static_file(filename: str, content: str) -> None:
    """Write the static file to `dist/` directory"""
    with open(path.join(DIST_DIRECTORY_PATH, filename + ".html"), 'w+', encoding='utf-8') as static_file:
        static_file.write(content)
        click.echo(
            f"{TextColor.OKGREEN}{TextColor.BOLD}\u2713 Success: Static file for '{filename}' is generated in dist/{TextColor.ENDC}")


def generate_static_file(file_path: str, extension: str, stylesheet_url: str = '') -> None:
    """
    Parse a text file and generate a single HTML file from its content.
    The generated files should be found inside `dist/` directory
    """
    html = get_html(file_path, stylesheet_url, extension)
    write_static_file(get_filename(file_path), content=html)

if __name__ == '__main__':
    silkie()
