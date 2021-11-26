# Silkie

```
     __//
cf  /.__.\
    \ \/ /
 '__/    \
  \-      )
   \_____/
_____|_|_____
     " "
 S I L K I E
```
[Chicken ASCII Art](http://www.ascii-art.de/ascii/c/chicken.txt)

[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)
[![pre-commit](https://img.shields.io/badge/pre--commit-enabled-brightgreen?logo=pre-commit&logoColor=white)](https://github.com/pre-commit/pre-commit)

> Static site generator with the smoothness of silk

Silkie is a simple and smooth static site generator. It can parse text files (".txt") and Markdown files (".md") and generate HTML files from them.

Check out the [demo](https://oliver-pham.github.io/silkie/dist/The%20Adventure%20of%20the%20Speckled%20Band) generated from this [text file](https://raw.githubusercontent.com/Seneca-CDOT/topics-in-open-source-2021/main/release-1/Sherlock-Holmes-Selected-Stories/The%20Adventure%20of%20the%20Speckled%20Band.txt) (with help from [new.css](https://newcss.net/)).

```
$ silkie -h
Usage: silkie [OPTIONS]

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

## Installation

```
$ pip install silkie
```

Check if you already have installed Silkie:

```
$ silkie -v
```

You can also run Silkie as a package:

```
$ python -m silkie -v
```

## Usage

### Input file

```
$ silkie -i tests/data/text/The Adventure of the Speckled Band.txt
```

### Input directory

```
$ silkie -i tests/data/text
```

### Custom stylesheet

```
$ silkie -i tests/data/text/Silver Blaze.txt -s https://cdn.jsdelivr.net/npm/@exampledev/new.css@1.1.2/new.min.css
```

### Custom document language

```
$ silkie -i tests/data/text/Silver Blaze.txt -l fr
```

### JSON configuration file

```
$ silkie -c tests/data/config/all_markdown_files.json
```

Like how you specify the options verbosely for a regular input file, there are keywords can be set in your JSON file: `input`, `lang`, and `stylesheet`

```json
{
    "input": "tests/data/text/Lorem Ipsum.txt",
    "stylesheet": "https://cdn.jsdelivr.net/npm/@exampledev/new.css@1.1.2/new.min.css",
    "lang": "fr"
}
```

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
