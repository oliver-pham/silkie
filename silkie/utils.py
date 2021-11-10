from pathlib import Path

import silkie.definitions as definitions


class TextColor:
    HEADER = "\033[95m"
    OKBLUE = "\033[94m"
    OKCYAN = "\033[96m"
    OKGREEN = "\033[92m"
    WARNING = "\033[93m"
    FAIL = "\033[91m"
    ENDC = "\033[0m"
    BOLD = "\033[1m"
    UNDERLINE = "\033[4m"


def get_filename(file_path: str) -> str:
    """Extract the name of the file from a file path and exclude any file extension"""
    if not file_path:
        raise ValueError("Invalid file/folder path")
    # Replace any backslash(es) in Windows file path with forwardslash(es)
    file_path = file_path.replace("\\", "/")
    return Path(file_path).stem.split(".")[0]


def is_filetype_supported(file_path: str) -> bool:
    file_extension = Path(file_path).suffix
    return definitions.SUPORTED_FILE_EXTENSIONS.count(file_extension) > 0
