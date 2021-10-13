import pathlib
import shutil
import glob
import click
import json
import markdown
import re
from os import path, makedirs
from yattag import Doc, indent


SUPORTED_FILE_EXTENSIONS = ['.txt', '.md', '.ini']
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


class GeneratorOptions:
    def __init__(self, input_path, stylesheet_url=None, lang='en-CA'):
        self.input_path = input_path
        self.stylesheet_url = stylesheet_url
        self.lang = lang
    
    def __init__(self, config_file_path: str):
        with open(config_file_path, "r", encoding="utf-8") as config_file:
            config_items = json.load(config_file)
            if "input" in config_items:
                if path.exists(config_items["input"]):
                    self.input_path = config_items["input"]
                else:
                    raise FileNotFoundError("Error: Input file can't be found!")
            else:
                raise FileNotFoundError("Error: Missing 'input' option!")
            if "stylesheet" in config_items:
                self.stylesheet_url = config_items["stylesheet"]
            if "lang" in config_items:
                self.lang = config_items["lang"]


@click.command()
@click.version_option("0.1.0", '-v', '--version')
@click.help_option('-h', '--help')
@click.option('-i', '--input', 'input_path', type=click.Path(exists=True, file_okay=True, dir_okay=True, readable=True), help='Path to the input file/folder')
@click.option('-s', '--stylesheet', help='URL path to a stylesheet')
@click.option('-l', '--lang', help='Language of the HTML document [en-CA by default]')
@click.option("-c", "--config", type=click.Path(exists=True, file_okay=True, dir_okay=False, readable=True), help='Read option defaults from the specified INI file')
def silkie(input_path, stylesheet, lang, config):
    """Static site generator with the smoothness of silk"""
    try:    
        if config is None:
            kwargs = dict(input_path=input_path,
                          stylesheet_url=stylesheet, lang=lang)
            options = GeneratorOptions(
                **{k: v for k, v in kwargs.items() if v is not None})
        else:
            options = GeneratorOptions(config)
        # Clean build
        shutil.rmtree(DIST_DIRECTORY_PATH, ignore_errors=True)
        makedirs(DIST_DIRECTORY_PATH, exist_ok=True)
        # Generate static file(s)
        if path.isfile(options.input_path) and is_filetype_supported(options.input_path):
            generate_static_file(options)
        if path.isdir(options.input_path):
            for extension in SUPORTED_FILE_EXTENSIONS:
                for filepath in glob.glob(path.join(options.input_path, "*" + extension)):
                    options.input_path = filepath
                    generate_static_file(options)
    except FileNotFoundError as file_error:
        click.echo(f'{TextColor.FAIL}\u2715 {str(file_error)}{TextColor.ENDC}')
    except json.JSONDecodeError as json_error:
        click.echo(f'{TextColor.FAIL}\u2715 {str(json_error)}{TextColor.ENDC}')
    except OSError as os_error:
        click.echo(f'{TextColor.FAIL}\u2715 {str(os_error)}{TextColor.ENDC}')


def is_filetype_supported(file_path: str) -> bool:
    file_extension = pathlib.Path(file_path).suffix
    return SUPORTED_FILE_EXTENSIONS.count(file_extension) > 0


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
    return pathlib.Path(file_path).stem.split('.')[0]


def get_html_head(doc, title: str, file_path: str, stylesheet_url: str = None) -> None:
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
        if stylesheet_url is not None:
            doc.stag('link', rel='stylesheet', href=stylesheet_url)


def get_html_paragraphs(line, title: str, file_path: str) -> None:
    """Get all paragraphs from text file and append them to the HTML document"""
    with open(file_path, 'r', encoding='utf-8') as f:
        paragraphs = f.read()[len(title)+1: -1].strip().split("\n\n")
        if title:
            line('h1', title)
        for p in paragraphs:
            line('p', p)


def parse_markdown(doc, file_path: str) -> None:
    """Convert Markdown to HTML and append it to the HTML document"""
    with open(file_path, 'r',  encoding='utf-8') as markdown_file:
        doc.asis(markdown.markdown(markdown_file.read().strip()))


def get_html(file_path: str, stylesheet_url: str, lang: str) -> str:
    """Return an indented HTML document with the content of the file"""
    doc, tag, text, line = Doc().ttl()
    title = get_title(file_path)
    doc.asis('<!DOCTYPE html>')
    with tag('html'):
        doc.attr(lang=lang)
        get_html_head(doc, title, file_path, stylesheet_url)
        with tag('body'):
            file_extension = pathlib.Path(file_path).suffix
            if file_extension == ".txt":
                get_html_paragraphs(line, title, file_path)
            elif file_extension == ".md":
                parse_markdown(doc, file_path)
    return indent(doc.getvalue())


def write_static_file(filename: str, content: str) -> None:
    """Write the static file to `dist/` directory"""
    with open(path.join(DIST_DIRECTORY_PATH, filename + ".html"), 'w+', encoding='utf-8') as static_file:
        static_file.write(content)
        click.echo(
            f"{TextColor.OKGREEN}{TextColor.BOLD}\u2713 Success: Static file for '{filename}' is generated in dist/{TextColor.ENDC}")


def generate_static_file(options: GeneratorOptions) -> None:
    """
    Parse a text file and generate a single HTML file from its content.
    The generated files should be found inside `dist/` directory
    """
    html = get_html(options.input_path, options.stylesheet_url, options.lang)
    write_static_file(get_filename(options.input_path), content=html)


if __name__ == '__main__':
    silkie()
