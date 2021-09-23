# Silkie
> Static site generator with the smoothness of silk

Silkie is a simple and smooth static site generator. It can parse text files (".txt" or ".md" files) and 
generate HTML files from them.

Check out the [demo](https://oliver-pham.github.io/silkie/dist/The%20Adventure%20of%20the%20Speckled%20Band) generated from this [text file](https://raw.githubusercontent.com/Seneca-CDOT/topics-in-open-source-2021/main/release-1/Sherlock-Holmes-Selected-Stories/The%20Adventure%20of%20the%20Speckled%20Band.txt) (with help from [new.css](https://newcss.net/)).

```
$ python3 silkie.py -h
Usage: silkie.py [OPTIONS]

  Static site generator with the smoothness of silk

Options:
  -v, --version          Show the version and exit.
  -h, --help             Show this message and exit.
  -i, --input PATH       Path to the input file/folder  [required]
  -s, --stylesheet TEXT  URL path to a stylesheet
```

## Features
- Generate HTML file(s) from a specified text file/directory
- Detect the title of a file if it's the first line followed by two blank lines
- Add custom styling to static site

## Getting Started

### Prerequisites

- Python >= 3.9.0
- Pip >= 21.2.4

### Installation
**Note**: if you have both versions of Python (2 & 3) installed, then you should replace every `python` command with `python3` and `pip` command with `pip3`.
1. Clone the repository
2. Create a virtual environment
    ```
    cd silkie && python -m venv .
    ```
3. Activate your virtual environment  
    - **Windows:** `bin\Scripts\activate.bat`
    - **Unix or MacOS**: `source bin/activate`
4. Install the dependency packages
    ```
    pip install -r requirements.txt
    ```

## Usage
1. Activate your virtual environment (only if you have not done that)
2. Run the program
    ```
    python silkie.py -h

    Other examples:
      python silkie.py -i examples/md/markdowntest1.md 
    ```

## Contributing
Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.

## License
[MIT](LICENSE)
