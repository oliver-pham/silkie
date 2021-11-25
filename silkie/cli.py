import glob
import shutil
from json.decoder import JSONDecodeError
from os import makedirs, path

import click

from . import generate_static_file
from .definitions import DIST_DIRECTORY_PATH, SUPORTED_FILE_EXTENSIONS
from .options import GeneratorOptions
from .utils import TextColor, is_filetype_supported


@click.command()
@click.version_option("1.0.5", "-v", "--version")
@click.help_option("-h", "--help")
@click.option(
    "-i",
    "--input",
    "input_path",
    type=click.Path(exists=True, file_okay=True, dir_okay=True, readable=True),
    help="Path to the input file/folder",
)
@click.option("-s", "--stylesheet", help="URL path to a stylesheet")
@click.option("-l", "--lang", help="Language of the HTML document [en-CA by default]")
@click.option(
    "-c",
    "--config",
    type=click.Path(exists=True, file_okay=True, dir_okay=False, readable=True),
    help="Read option defaults from the specified INI file",
)
def silkie(input_path, stylesheet, lang, config):
    """Static site generator with the smoothness of silk"""
    try:
        options = GeneratorOptions(
            input_path,
            stylesheet_url=stylesheet,
            lang=lang,
            config_file_path=config,
        )
        # Clean build
        shutil.rmtree(DIST_DIRECTORY_PATH, ignore_errors=True)
        makedirs(DIST_DIRECTORY_PATH, exist_ok=True)
        # Generate static file(s)
        if path.isfile(options.input_path) and is_filetype_supported(
            options.input_path
        ):
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
        click.echo(f"{TextColor.FAIL}\u2715 {str(file_error)}{TextColor.ENDC}")
    except JSONDecodeError as json_error:
        click.echo(f"{TextColor.FAIL}\u2715 {str(json_error)}{TextColor.ENDC}")
    except OSError as os_error:
        click.echo(f"{TextColor.FAIL}\u2715 {str(os_error)}{TextColor.ENDC}")
