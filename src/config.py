import os
import json

from imageio.testing import ROOT_DIR
from termcolor import colored


class Config:
    """
    Config class to store all the configuration variables.
    """

    def __init__(self):
        """
        Initializes the Config class.
        """
        json_config = json.load(open(os.path.join(ROOT_DIR, "../config/config.json"), "r"))
        if "assembly_ai_api_key" not in json_config or json_config["assembly_ai_api_key"] == "":
            print(colored("ERROR: AssemblyAI API key not found in config.json.", "red"))
            exit(1)
        self.api_key = json_config["assembly_ai_api_key"]
        self.font = json_config["font"]
        if not os.path.exists(json_config["font"]):
            print(colored(f"ERROR: Font file {json_config['font']} does not exist.", "red"))
            exit(1)
        elif not os.path.isfile(json_config["font"]):
            print(colored(f"ERROR: Font file {json_config['font']} is not a file.", "red"))
            exit(1)
        self.font_size = json_config["font_size"]
        if self.font_size < 0:
            print(colored("ERROR: Font size cannot be negative.", "red"))
            exit(1)
        self.font_color = json_config["font_color"]
        self.font_background_color = json_config["font_background_color"]
        self.threads = json_config["threads"]

        self.transcribe = json_config["transcribe"]
        self.satisfying = json_config["satisfying"]

        self.width = json_config["width"]
        self.height = json_config["height"]

        self.music = json_config["music"]
        self.music_volume = json_config["music_volume"]
        if not os.path.exists("../" + json_config["music"]):
            print(colored(f"ERROR: Music file {json_config['music']} does not exist.", "red"))
            exit(1)
        self.fp = json_config["fps"]
        if self.fp < 0:
            print(colored("ERROR: FPS cannot be negative.", "red"))
            exit(1)
        elif self.fp > 60:
            print(colored("WARNING: FPS more than 60 can increase file size and time to render.", "yellow"))

    @classmethod
    def get_headless(cls):
        """
        Gets the headless mode.
        """
        json_config = json.load(open(os.path.join(ROOT_DIR, "../config/config.json"), "r"))
        return json_config["headless"]

    @classmethod
    def get_firefox_profile_path(cls):
        """
        Gets the Firefox profile path.
        """
        json_config = json.load(open(os.path.join(ROOT_DIR, "../config/config.json"), "r"))
        return json_config["firefox_profile"]

    @classmethod
    def get_title(cls):
        """
        Gets the title.
        """
        json_config = json.load(open(os.path.join(ROOT_DIR, "../config/config.json"), "r"))
        return json_config["title"]
