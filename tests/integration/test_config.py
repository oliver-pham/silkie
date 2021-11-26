import pytest

from pathlib import Path

from silkie.options import GeneratorOptions
from silkie import get_html


@pytest.mark.parametrize(
    "config_file_path, expected_output_html",
    [
        (
            str(Path("tests", "data", "config", "single_text_file.json")),
            Path("tests", "fixture", "text", "Lorem Ipsum.html").read_text().strip(),
        ),
        (
            str(
                Path(
                    "tests", "data", "config", "single_text_file_custom_stylesheet.json"
                )
            ),
            Path("tests", "fixture", "text", "Lorem Ipsum (custom stylesheet).html")
            .read_text()
            .strip(),
        ),
        (
            str(Path("tests", "data", "config", "single_text_file_custom_lang.json")),
            Path("tests", "fixture", "text", "Lorem Ipsum (custom lang).html")
            .read_text()
            .strip(),
        ),
    ],
)
def test_config_to_html(config_file_path, expected_output_html):
    options = GeneratorOptions(input_path=None, config_file_path=config_file_path)
    output_html = get_html(options).strip()
    assert output_html == expected_output_html
