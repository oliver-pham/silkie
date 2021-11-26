import pytest

from pathlib import Path

from silkie.options import GeneratorOptions
from silkie import get_html


@pytest.mark.parametrize(
    "input_path, expected_output_html",
    [
        (
            str(Path("tests", "data", "markdown", "test_paragraphs.md")),
            Path("tests", "fixture", "markdown", "test_paragraphs.html")
            .read_text()
            .strip(),
        )
    ],
)
def test_markdown_to_html(input_path, expected_output_html):
    options = GeneratorOptions(input_path=input_path)
    output_html = get_html(options).strip()
    assert output_html == expected_output_html
