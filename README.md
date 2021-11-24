# Silkie

[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)
[![pre-commit](https://img.shields.io/badge/pre--commit-enabled-brightgreen?logo=pre-commit&logoColor=white)](https://github.com/pre-commit/pre-commit)

> Static site generator with the smoothness of silk

Silkie is a simple and smooth static site generator. It can parse text files (".txt") and Markdown files (".md") and generate HTML files from them.

Check out the [demo](https://oliver-pham.github.io/silkie/dist/The%20Adventure%20of%20the%20Speckled%20Band) generated from this [text file](https://raw.githubusercontent.com/Seneca-CDOT/topics-in-open-source-2021/main/release-1/Sherlock-Holmes-Selected-Stories/The%20Adventure%20of%20the%20Speckled%20Band.txt) (with help from [new.css](https://newcss.net/)).

```
$ python -m silkie -h
Usage: python -m silkie [OPTIONS]

  Static site generator with the smoothness of silk

Options:
  -v, --version          Show the version and exit.
  -h, --help             Show this message and exit.
  -i, --input PATH       Path to the input file/folder  [required]
  -s, --stylesheet TEXT  URL path to a stylesheet
  -l, --lang TEXT        Language of the HTML document [en-CA by default]
  -c, --config FILE      Read option defaults from the specified INI file
```

## Features

- Generate HTML file(s) from a specified text file/directory
- Detect the title of a file if it's the first line followed by two blank lines
- Add custom styling to static site
- Change HTML document language (`<html lang="{your-language}">`, `en-CA` by default)
- Generate HTML file from a Markdown file (**Need Testing**)
- Allow user to supply a JSON formatted configuration file
- Parse front matter and apply the corresponding metadata fields (**Prototype Feature**)
  - Check out [#21](https://github.com/oliver-pham/silkie/issues/21) to see which fields are supported

## Getting Started

### Prerequisites

- Python >= 3.9.0
- Pip >= 21.2.4

### Installation

**Note**: if you have both versions of Python (2 & 3) installed, then you should replace every `python` command with `python3` and `pip` command with `pip3`.

1. Clone the repository
2. Create a virtual environment
  ```
  cd silkie && python -m venv .venv
  ```
3. Activate your virtual environment
  - **Windows:** `.venv\Scripts\activate.bat`
  - **Unix or MacOS**: `source .venv/bin/activate`
4. Install the dependency packages
  ```
  pip install -r requirements.txt
  ```

## Usage

1. Activate your virtual environment (only if you have not done that)
2. Run the program

### Input file
```
python -m silkie -i tests/data/text/The Adventure of the Six Napoleans.txt
```
### Input directory
```
python -m silkie -i tests/data/text
```
### Custom stylesheet
```
python -m silkie -i tests/data/text/Silver Blaze.txt -s https://cdn.jsdelivr.net/npm/@exampledev/new.css@1.1.2/new.min.css
```
### Custom document language
```
python -m silkie -i tests/data/text/Silver Blaze.txt -l fr
```
### JSON configuration file
```
python -m silkie -c tests/data/config/all_text_files.json
```
Available attributes of a configuration file include: `input`, `lang`, and `stylesheet`
### Frontmatter
Supported keywords:  

|      Name     |   Type   |           Default           |                                                         Usage                                                         |
|:-------------:|:--------:|:---------------------------:|:---------------------------------------------------------------------------------------------------------------------:|
| `slug`        | `string` | File path                   | Customize the document URL route, e.g. `/docs/example.html`                                                           |
| `title`       | `string` | Markdown title or file name | The text title of the document. Automatically added at the top of your doc if it does not contain any Markdown title. |
| `description` | `string` |                             | The description of your document, which will added to document metadata for search engine optimization.               |


## Contributing
Please read the [Contribution Guide](CONTRIBUTING.md) before developing any changes.

## License

[MIT](LICENSE)
