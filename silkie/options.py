import json
from pathlib import Path

import frontmatter

from silkie.utils import get_filename


class GeneratorOptions:
    def __init__(self, input_path: str, *args, **kwargs):
        self.config_file_path = kwargs.get("config_file_path", None)

        if self.config_file_path is None:
            input_file_path = Path(input_path)
            if not input_file_path.exists():
                raise FileNotFoundError("Error: Input file can't be found!")
            self.input_path = input_path
            self.content = input_file_path.read_text()
            self.stylesheet_url = kwargs.get("stylesheet_url", None)
            self.lang = kwargs.get("lang", "en-CA") or "en-CA"
        else:
            with open(self.config_file_path, "r", encoding="utf-8") as config_file:
                config_items = json.load(config_file)
                if "input" in config_items:
                    input_file_path = Path(config_items["input"])
                    if input_file_path.exists():
                        self.input_path = config_items["input"]
                        self.content = input_file_path.read_text()
                    else:
                        raise FileNotFoundError("Error: Input file can't be found!")
                else:
                    raise FileNotFoundError("Error: Missing 'input' option!")

                if "stylesheet" in config_items:
                    self.stylesheet_url = config_items["stylesheet"]
                else:
                    self.stylesheet_url = None

                if "lang" in config_items:
                    self.lang = config_items["lang"]
                else:
                    self.lang = "en-CA"

        # Initialize document metadata
        self.description = ""
        self.title = self.slug = get_filename(self.input_path)

    def load_metadata(self):
        """Load metadata for the static site from the document's front matter"""
        with open(self.input_path, "r", encoding="utf-8") as f:
            metadata, content = frontmatter.parse(f.read())

            self.content = content
            if "description" in metadata:
                self.description = metadata["description"]
            if "slug" in metadata:
                self.slug = metadata["slug"]
            if "title" in metadata:
                self.title = metadata["title"]
