import pathlib
import shutil
import glob
from typing import AnyStr
import click
import re
from os import path, makedirs
from yattag import Doc, indent
import json
from configparser import ConfigParser

doc, tag, text = Doc().tagtext()

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
        if config is not None:
            with open(config, "r", encoding="utf-8") as f:
                config_item = json.load(f)
                if "input" in config_item:
                    input_path = config_item["input"]
                else:
                    input_path = None
                if "stylesheet" in config_item:
                    stylesheet = config_item["stylesheet"]
                if "lang" in config_item:
                    lang = config_item["lang"]

        kwargs = dict(input_path=input_path,
                      stylesheet_url=stylesheet, lang=lang)
        options = GeneratorOptions(
            **{k: v for k, v in kwargs.items() if v is not None})
        # Clean build
        shutil.rmtree(DIST_DIRECTORY_PATH, ignore_errors=True)
        makedirs(DIST_DIRECTORY_PATH, exist_ok=True)
        # Generate static file(s)
        if path.isfile(input_path) and is_filetype_supported(input_path):
            generate_static_file(options)
        if path.isdir(input_path):
            for extension in SUPORTED_FILE_EXTENSIONS:
                for filepath in glob.glob(path.join(input_path, "*" + extension)):
                    options.input_path = filepath
                    generate_static_file(options)
    except OSError as e:
        click.echo(
            f"{TextColor.FAIL}\u2715 Error: Build directory can't be created!{TextColor.ENDC}")
    except FileNotFoundError:
        print(f'Error: There is no Json File "{config}" !')
    except json.JSONDecodeError:
        print(f'Error:Invalid JSON syntax!" ')


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
    file_path = re.compile(r'([^\/]+$)').search(file_path).group()
    """Extract the name of the file without (all) its extension(s)"""
    # ISSUE
    # add a note to your potential issue with code here for empty name files
    if pathlib.Path(file_path.split('.')[0]).stem == ".md" or pathlib.Path(file_path.split('.')[0]).stem == ".txt":
        return pathlib.Path(file_path.split('.')[0]).stem
    elif pathlib.Path(file_path.split('.')[1]).stem == ".md" or pathlib.Path(file_path.split('.')[1]).stem == ".md":
        return pathlib.Path(file_path.split('.')[0]).stem
    elif pathlib.Path(file_path.split('.')[1]).stem == ".json" or pathlib.Path(file_path.split('.')[1]).stem == ".ini":
        return pathlib.Path(file_path.split('.')[0]).stem
    else:
        return pathlib.Path(file_path.split('.')[0]).stem
    """ 
    linux distribution - works
    Windows 11 -seems to be only a windows 11 issue with above line being pathlib.Path(file_path.split('.')[1]).stem to work"""


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


def get_html_paragraphs_parsewithmd(doc, line, title: str, tag, file_path: str) -> None:
    """ Append the approapriate markdown properties, .md headers, lists, links, images, tables"""
    with open(file_path, 'r',  encoding='utf-8') as f:
        paragraphs = f.read().strip().split("\n\n")
        for p in paragraphs:
            if p.startswith('#'):  # starts with certain headers in markdown
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
            elif p.startswith('!['):  # starts with image
                # TODO: image is not working as of yet
                p = p.replace('![', '', 1)
                parts = p.split('](')
                if len(parts) > 1:
                    temp = parts[1].split('alt')
                else:
                    temp = parts[0]
                with tag('p'):
                    line('p', temp)  # fix
                """
                    if len(parts) > 1:
                        if len(temp) > 1:
                            temp[1] = temp[1].replace(')', '', 1)
                            line('img', src=temp[1], text_content=parts[0], alt=temp[0])
                        else:
                            temp[0] = temp[0].replace(')', '', 1)
                            line('img', src=temp[0], text_content=parts[0], alt="image")
                    else:
                        line('img', text_content=parts[0], alt="image")
                """
            elif p.startswith('['):  # starts with links
                p = p.replace('[', '', 1)
                temp = p.split("](")
                imgtext = temp[0]
                link = ""
                atitle = ""
                if len(temp) > 1:
                    if temp[1].__contains__(' '):
                        temp2 = temp[1].split(' ')
                        if len(temp2) > 1:
                            temp2[0] = temp2[0].replace(')', '', 1)
                            link = temp2[0]
                            atitle = temp2[1]
                        else:
                            temp2[0] = temp2[0].replace(')', '', 1)
                            link = temp2[0]
                    else:
                        temp[1] = temp[1].replace(')', '', 1)
                        link = temp[1]
                else:
                    if temp[0].__contains__(']:'):
                        temp2 = temp[0].split(' ')
                        if len(temp2) > 2:  # build atitle
                            for i in range(2, len(temp2)):
                                atitle += temp2[i] + " "
                        if len(temp2) > 1:  # should work
                            temp2[2] = temp2[2].replace(')', '', 1)
                            link = temp2[2]  # link
                        # img text
                        imgtext = temp2[1]
                        # print(temp2[0]) # id
                with tag('p'):
                    line('a', href=link, text_content=imgtext, title=atitle)
            elif re.match('^\*{3,}$|^-{3,}$|^_{3,}$', p):
                doc.stag('hr')
            elif p.__contains__('**'):  # bold text
                pos_begin = 0
                pos_end = 0
                counter = p.count('**')
                with tag('p'):
                    while(counter >= 2):
                        pos_begin = p.index('**')
                        pos_end = p[pos_begin+2:].index('**') + pos_begin
                        if pos_begin > 0:
                            line('p', p[0:(pos_begin-1)])
                        p = p.replace('**', '', 2)
                        line('b', p[pos_begin:pos_end])
                        p = p[pos_end:]
                        counter -= 2
                    text(p)
            elif p.__contains__('__'):  # bold text version 2
                pos_begin = 0
                pos_end = 0
                counter = p.count('__')
                with tag('p'):
                    while(counter >= 2):
                        pos_begin = p.index('__')
                        pos_end = p[pos_begin+2:].index('__') + pos_begin
                        if pos_begin > 0:
                            line('p', p[0:(pos_begin-1)])
                        p = p.replace('__', '', 2)
                        line('b', p[pos_begin:pos_end])
                        p = p[pos_end:]
                        counter -= 2
                    text(p)
            elif p.__contains__('*'):  # italics text
                pos_begin = 0
                pos_end = 0
                counter = p.count('*')
                with tag('p'):
                    while(counter >= 2):
                        pos_begin = p.index('*')
                        pos_end = p[pos_begin+1:].index('*') + pos_begin
                        if pos_begin > 0:
                            line('p', p[0:(pos_begin-1)])
                        p = p.replace('*', '', 2)
                        line('i', p[pos_begin:pos_end])
                        p = p[pos_end:]
                        counter -= 2
                    text(p)
            elif p.__contains__('_'):  # italics text version 2
                pos_begin = 0
                pos_end = 0
                counter = p.count('_')
                with tag('p'):
                    while(counter >= 2):
                        pos_end = p[pos_begin+1:].index('_') + pos_begin
                        if pos_begin > 0:
                            line('p', p[0:(pos_begin-1)])
                        p = p.replace('_', '', 2)
                        line('i', p[pos_begin:pos_end])
                        p = p[pos_end:]
                        counter -= 2
                    text(p)
            else:
                p = p.replace('\n', '<br>', 1)
                line('p', p)
            p = p.replace('<p><p>', '<p>', 1)
            p = p.replace('</p></p>', '</p>', 1)


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
                get_html_paragraphs_parsewithmd(
                    doc, line, title, tag, file_path)
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
