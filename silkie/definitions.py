import pathlib

ROOT_DIR = pathlib.Path(__file__).parent.parent.absolute()
DIST_DIRECTORY_PATH = ROOT_DIR.joinpath("dist")
SUPORTED_FILE_EXTENSIONS = [".txt", ".md"]
