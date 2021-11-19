from silkie.utils import is_filetype_supported


def test_txt_extension_with_absolute_path():
    file_path = r"C:\Documents\test.txt"
    assert is_filetype_supported(file_path) == True


def test_txt_extension_with_relative_path():
    file_path = "/Users/anonymous/Documents/test.txt"
    assert is_filetype_supported(file_path) == True


def test_path_to_directory():
    file_path = "/Users/anonymous/Documents/test/"
    assert is_filetype_supported(file_path) == False, "path to a directory error"


def test_invalid_extension():
    file_path = "/Users/anonymous/Documents/test.rc"
    assert is_filetype_supported(file_path) == False, "Invalid extension error"


def test_md_extension_with_relative_path():
    file_path = "/Users/anonymous/Documents/test.md"
    assert is_filetype_supported(file_path) == True


def test_empty_extension():
    file_path = "/Users/anonymous/Documents/test"
    assert is_filetype_supported(file_path) == False, "empty extension error"
