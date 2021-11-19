from silkie.utils import is_filetype_supported


def test_supported_windows_file_path1():
    file_path = r"C:\Documents\test.txt"
    assert is_filetype_supported(file_path) == True


def test_supported_windows_file_path2():
    file_path = "/Users/anonymous/Documents/test.txt"
    assert is_filetype_supported(file_path) == True


def test_supported_windows_file_path3():
    file_path = "/Users/anonymous/Documents/test/"
    assert is_filetype_supported(file_path) == False, "path to a directory error"


def ttest_supported_windows_file_path4():
    file_path = "/Users/anonymous/Documents/test.rc"
    assert is_filetype_supported(file_path) == False, "Invalid extension error"


def test_supported_windows_file_path5():
    file_path = "/Users/anonymous/Documents/test.md"
    assert is_filetype_supported(file_path) == True


def test_supported_windows_file_path6():
    file_path = "/Users/anonymous/Documents/test"
    assert is_filetype_supported(file_path) == False, "empty extension error"
