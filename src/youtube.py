import hashlib
from pytube import YouTube as PyTube

from fileManager import FileManager
from termcolor import colored


class YouTube:
    """
    YouTube class to download a video from YouTube.
    """

    def __init__(self, file_manager: FileManager):
        self.file_manager = file_manager
        self.DOWNLOAD_DIR = "downloads"
        self.UPLOAD_DIR = "uploads"
        self.CONFIG = "config"

    def download_video(self, url: str) -> str:
        """
        Downloads a video from YouTube.
        :param url:
        :return title_hash:
        """
        print(colored("> Downloading video... This may take a while.", "green"))
        pytube = PyTube(url)
        video = pytube.streams.get_highest_resolution()

        if pytube.age_restricted:
            print(colored("ERROR: Age restricted video. Cannot download.", "red"))
            print(colored("Please download the video manually and use the 'Download video from Local File' option.", "red"))
            return ""

        # Get the video title and create a hash of it
        video_title = pytube.title
        title_hash = hashlib.sha256(video_title.encode()).hexdigest()

        # Use the hash as the output name
        video.download(self.DOWNLOAD_DIR, filename=title_hash + ".mp4")
        self.file_manager.write_to_file(f"{self.CONFIG}/video_titles.txt",
                                        f"{title_hash}+CharacterSplit+{video_title}\n", add_to_end=True)
        print(colored(f"> Downloaded video as {title_hash}.mp4", "green"))
        return title_hash
