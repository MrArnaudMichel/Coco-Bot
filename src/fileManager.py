import json
import os

from imageio.testing import ROOT_DIR


class FileManager:
    """
    This class is responsible for managing the file.
    """
    def __init__(self):
        self.ROOT_DIR = os.path.dirname(os.path.abspath(__file__))
        print(self.ROOT_DIR)
        self.DOWNLOAD_DIR = "downloads"
        self.UPLOAD_DIR = "uploads"
        self.ASSETS_DIR = "assets"
        self.CONFIG_DIR = "config"

    def create_download_dir(self) -> None:
        """
        Creates the download directory if it does not exist.
        :return:
        """
        if not os.path.exists(self.DOWNLOAD_DIR):
            os.makedirs(self.DOWNLOAD_DIR)

    def create_upload_dir(self) -> None:
        """
        Creates the upload directory if it does not exist.
        :return:
        """
        if not os.path.exists(self.UPLOAD_DIR):
            os.makedirs(self.UPLOAD_DIR)

    def create_assets_dir(self) -> None:
        """
        Creates the assets directory if it does not exist.
        :return:
        """
        if not os.path.exists(self.ASSETS_DIR):
            os.makedirs(self.ASSETS_DIR)

    def create_config_dir(self) -> None:
        """
        Creates the config directory if it does not exist.
        :return:
        """
        if not os.path.exists(self.CONFIG_DIR):
            os.makedirs(self.CONFIG_DIR)

    def create_all_dirs(self) -> None:
        """
        Creates all the directories if they do not exist.
        :return:
        """
        self.create_download_dir()
        self.create_upload_dir()
        self.create_assets_dir()
        self.create_config_dir()

    def get_all_files(self, directory: str = "downloads") -> list:
        """
        Gets all the files in the given directory.
        :param directory:
        :return:
        """
        return os.listdir(os.path.join(self.ROOT_DIR, directory))

    def get_all_videos(self) -> list:
        """
        Gets all the videos in the given directory.
        :param directory:
        :return:
        """
        f = open("config/video_titles.txt", "r")
        lines = f.readlines()
        f.close()

        return lines

    def write_to_file(self, file: str, data: str) -> None:
        """
        Writes data to a file.
        :param file:
        :param data:
        :return:
        """
        with open(file, "w") as f:
            f.write(data)
