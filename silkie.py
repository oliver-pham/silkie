import shutil
import glob
import click
import json
import markdown
import re
import frontmatter
from os import path, makedirs
from pathlib import Path
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
    def __init__(self, input_path: str, *args, **kwargs):
        self.config_file_path = kwargs.get('config_file_path', None)

        if self.config_file_path is None:
            self.input_path = input_path
            self.stylesheet_url = kwargs.get('stylesheet_url', None)
            self.lang = kwargs.get('lang', 'en-CA') or 'en-CA'
        else:
            with open(self.config_file_path, "r", encoding="utf-8") as config_file:
                config_items = json.load(config_file)
                if "input" in config_items:
                    if path.exists(config_items["input"]):
                        self.input_path = config_items["input"]
                    else:
                        raise FileNotFoundError(
                            "Error: Input file can't be found!")
                else:
                    raise FileNotFoundError("Error: Missing 'input' option!")
                if "stylesheet" in config_items:
                    self.stylesheet_url = config_items["stylesheet"]
                if "lang" in config_items:
                    self.lang = config_items["lang"]

    def load_metadata(self):
        """Load metadata for the static site from the document's front matter"""
        with open(self.input_path, 'r', encoding='utf-8') as f:
            metadata, content = frontmatter.parse(f.read())
            filename = get_filename(self.input_path)

            self.description = metadata["description"] if "description" in metadata else ''
            self.slug = metadata["slug"] if "slug" in metadata else filename
            self.title = metadata["title"] if "title" in metadata else filename
            self.content = content or ''


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
        options = GeneratorOptions(
            input_path, stylesheet_url=stylesheet, lang=lang, config_file_path=config)
        # Clean build
        shutil.rmtree(DIST_DIRECTORY_PATH, ignore_errors=True)
        makedirs(DIST_DIRECTORY_PATH, exist_ok=True)
        # Generate static file(s)
        if path.isfile(options.input_path) and is_filetype_supported(options.input_path):
            options.load_metadata()
            generate_static_file(options)
        if path.isdir(options.input_path):
            dir_path = options.input_path
            for extension in SUPORTED_FILE_EXTENSIONS:
                for filepath in glob.glob(path.join(dir_path, "*" + extension)):
                    options.input_path = filepath
                    options.load_metadata()
                    generate_static_file(options)
    except FileNotFoundError as file_error:
        click.echo(f'{TextColor.FAIL}\u2715 {str(file_error)}{TextColor.ENDC}')
    except json.JSONDecodeError as json_error:
        click.echo(f'{TextColor.FAIL}\u2715 {str(json_error)}{TextColor.ENDC}')
    except OSError as os_error:
        click.echo(f'{TextColor.FAIL}\u2715 {str(os_error)}{TextColor.ENDC}')


def is_filetype_supported(file_path: str) -> bool:
    file_extension = Path(file_path).suffix
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
    return Path(file_path).stem.split('.')[0]


def get_html_head(doc: Doc, options: GeneratorOptions) -> None:
    """Get the metadata of the file and append them to the HTML document"""
    with doc.tag('head'):
        doc.stag('meta', charset='utf-8')
        doc.stag('meta', name='viewport',
                 content='width=device-width, initial-scale=1')
        doc.stag('meta', name='description', content=options.description)
        doc.stag('meta', property='og:description', content=options.description)
        with doc.tag('title'):
            doc.text(options.title)
        if options.stylesheet_url is not None:
            doc.stag('link', rel='stylesheet', href=options.stylesheet_url)


def parse_text(line, options: GeneratorOptions) -> None:
    """Get all paragraphs from text file and append them to the HTML document"""
    options.title = get_title(options.input_path)
    paragraphs = options.content[len(options.title)+1: -1].strip().split("\n\n")

    if options.title:
        line('h1', options.title)

    for paragraph_text in paragraphs:
        line('p', paragraph_text)


def parse_markdown(doc: Doc, content: str) -> None:
    """Convert Markdown to HTML and append it to the HTML document"""
    doc.asis(markdown.markdown(content.strip()))


def get_html(options: GeneratorOptions) -> str:
    doc, tag, text, line = Doc().ttl()

    doc.asis('<!DOCTYPE html>')
    with tag('html'):
        doc.attr(lang=options.lang)
        get_html_head(doc, options)
        with tag('body'):
            line('h1', options.title)
            file_extension = Path(options.input_path).suffix
            if file_extension == ".txt":
                parse_text(line, options)
            elif file_extension == ".md":
                parse_markdown(doc, options.content)

    return indent(doc.getvalue())


def write_static_file(content: str, destination: Path, options: GeneratorOptions) -> None:
    """Write the static file to the destination path"""
    with destination.open('w+', encoding='utf-8') as static_file:
        static_file.write(content)
        click.echo(
            f"{TextColor.OKGREEN}{TextColor.BOLD}\u2713 Success: Static file for '{options.slug}' is generated in dist/{TextColor.ENDC}")


def build_folder_structure(options: GeneratorOptions) -> Path:
    """
    Set up folder structure of the build folder `dist/` based on 
    the value of `slug` inside `GeneratorOptions`
    
    :returns: the file path to the generated file
    """
    route = Path(DIST_DIRECTORY_PATH).joinpath(Path(options.slug + ".html"))

    if route.exists():
        raise FileExistsError(
            f'warn: Duplicate routes found!\n {options.slug} is already taken by another document')
    dir_path = route.parent
    dir_path.mkdir(parents=True, exist_ok=True)

    return route


def generate_static_file(options: GeneratorOptions) -> None:
    """
    Parse a text file and generate a single HTML file from its content.
    The generated files should be found inside `dist/` directory
    """
    html = get_html(options)
    file_path = build_folder_structure(options)
    write_static_file(content=html, destination=file_path, options=options)


if __name__ == '__main__':
    silkie()
