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
        self.api_key = json_config["assembly_ai_api_key"]
        self.font = json_config["font"]
        if not os.path.exists(json_config["font"]):
            print(colored(f"Font file {json_config['font']} does not exist.", "red"))
        elif not os.path.isfile(json_config["font"]):
            print(colored(f"Font file {json_config['font']} is not a file.", "red"))
        self.font_size = json_config["font_size"]
        if self.font_size < 0:
            print(colored("Font size cannot be negative.", "red"))
        self.font_color = json_config["font_color"]
        # if (not self.font_color.startswith("#") or not len(self.font_color) == 7) and self.font_color != "transparent":
        #     print(colored("Font color must start with #.", "red"))
        self.font_background_color = json_config["font_background_color"]
        self.threads = json_config["threads"]

