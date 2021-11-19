from silkie.utils import is_filetype_supported


def test_is_filetype_supported1():
    file_path = r"C:\Documents\test.txt"
    assert is_filetype_supported(file_path) == True


def test_is_filetype_supported2():
    file_path = "/Users/anonymous/Documents/test.txt"
    assert is_filetype_supported(file_path) == True


def test_is_filetype_supported3():
    file_path = "/Users/anonymous/Documents/test/"
    assert is_filetype_supported(file_path) == False, "path to a directory error"


def test_is_filetype_supported4():
    file_path = "/Users/anonymous/Documents/test.rc"
    assert is_filetype_supported(file_path) == False, "Invalid extension error"


def test_is_filetype_supported5():
    file_path = "/Users/anonymous/Documents/test.md"
    assert is_filetype_supported(file_path) == True


def test_is_filetype_supported6():
    file_path = "/Users/anonymous/Documents/test"
    assert is_filetype_supported(file_path) == False, "empty extension error"
