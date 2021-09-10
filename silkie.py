import os
import pathlib
import click


SUPORTED_FILETYPE = ".txt"


@click.command()
@click.version_option("0.1.0", '-v', '--version')
@click.help_option('-h', '--help')
@click.option('-i', '--input', required=True, type=click.Path(exists=True, file_okay=True, dir_okay=True, readable=True), help='Path to the file/folder to be processed')
def silkie(input):
    """Static site generator with the smoothness of silk"""
    if os.path.isfile(input):
        generate_static_file(input)
    if os.path.isdir(input):
        for filename in os.listdir(input):
            if filename.endswith(SUPORTED_FILETYPE):
                generate_static_file(os.path.join(input, filename))


def process_text_file(file_path):
    with open(file_path, 'r') as f:
        lines = f.readlines()
        body = ["</p><p>" if l == "\n" else l for l in lines]
        body.insert(0, "<p>")
        body.append("</p>")

    return ''.join(body)


def generate_static_file(file_path):
    title = pathlib.Path(file_path).stem
    html = f"""
    <!doctype html>
    <html lang="en">
        <head>
            <meta charset="utf-8">
            <title>{title}</title>
            <meta name="viewport" content="width=device-width, initial-scale=1">
        </head>
        <body>
            { process_text_file(file_path) }
        </body>
    </html>
    """
    dist_directory_path = os.path.join(
        os.path.dirname(os.path.realpath(__file__)), "dist")
    os.makedirs(dist_directory_path, exist_ok=True)
    with open(os.path.join(dist_directory_path, title + ".html"), 'w') as static_file:
        static_file.write(html)


if __name__ == '__main__':
    silkie()
