import pytest
from silkie.utils import get_filename


@pytest.mark.parametrize(
    "file_path, expected_file_name",
    [
        (r"C:\Documents\test.txt", "test"),
        ("/Users/anonymous/Documents/test.txt", "test"),
        ("/Users/anonymous/Documents/test.rc.txt", "test"),
    ],
)
def test_normal_file_path(file_path, expected_file_name):
    assert get_filename(file_path) == expected_file_name


def test_empty_file_path():
    with pytest.raises(ValueError):
        get_filename("")
