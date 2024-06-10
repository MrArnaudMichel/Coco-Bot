import hashlib
import json
import os



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
        :return: None
        """
        if not os.path.exists(self.DOWNLOAD_DIR):
            os.makedirs(self.DOWNLOAD_DIR)

    def create_upload_dir(self) -> None:
        """
        Creates the upload directory if it does not exist.
        :return: None
        """
        if not os.path.exists(self.UPLOAD_DIR):
            os.makedirs(self.UPLOAD_DIR)

    def create_assets_dir(self) -> None:
        """
        Creates the assets directory if it does not exist.
        :return: None
        """
        if not os.path.exists(self.ASSETS_DIR):
            os.makedirs(self.ASSETS_DIR)

    def create_config_dir(self) -> None:
        """
        Creates the config directory if it does not exist.
        :return: None
        """
        if not os.path.exists(self.CONFIG_DIR):
            os.makedirs(self.CONFIG_DIR)

    def create_all_dirs(self) -> None:
        """
        Creates all the directories if they do not exist.
        :return: None
        """
        self.create_download_dir()
        self.create_upload_dir()
        self.create_assets_dir()
        self.create_config_dir()

    def get_all_files(self, directory: str = "downloads") -> list:
        """
        Gets all the files in the given directory.
        :param directory: Directory to get the files from.
        :return: List of files.
        """
        return os.listdir(os.path.join(directory))

    def get_all_videos(self) -> list:
        """
        Gets all the videos in the given directory.
        :param directory: Directory to get the videos from.
        :return: List of videos.
        """
        f = open("config/video_titles.txt", "r")
        lines = f.readlines()
        f.close()

        return lines

    def write_to_file(self, file: str, data: str, add_to_end=False) -> None:
        """
        Writes data to a file.
        :param add_to_end: Whether to add to the end of the file.
        :param file: File to write to.
        :param data: Data to write.
        :return: None
        """
        if add_to_end:
            with open(file, "a") as f:
                f.write(data)
        else:
            with open(file, "w") as f:
                f.write(data)

    def download_video_from_local_file(self, path: str) -> str:
        """
        Downloads the video from the local file.
        :param path: Path to the video file.
        :return: Hash of the video.
        """
        os.makedirs(self.DOWNLOAD_DIR, exist_ok=True)
        title_hash = hashlib.sha256(path.encode()).hexdigest()
        os.system(f"cp {path} {self.DOWNLOAD_DIR}/{title_hash}.mp4")
        self.write_to_file(f"{self.CONFIG_DIR}/video_titles.txt",
                           f"{title_hash}+CharacterSplit+{path}\n", add_to_end=True)
        print(f"> Downloaded video as {title_hash}.mp4")
        return title_hash
