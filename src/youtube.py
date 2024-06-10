import hashlib
import os

from pytube import YouTube as PyTube

from fileManager import FileManager

from status import *


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
        info("\t> Downloading video... This may take a while. More the video length, more the time.")
        pytube = PyTube(url)
        video = pytube.streams.get_highest_resolution()

        if pytube.age_restricted:
            error("Age restricted video. Cannot download.")
            error("Please download the video manually and use the 'Download video from Local File' option.")
            return ""

        video_title = pytube.title
        title_hash = hashlib.sha256(video_title.encode()).hexdigest()

        lines = self.file_manager.get_all_videos()
        for i, line in enumerate(lines):
            videos: tuple[str, str] = (line.split(" ")[0], lines[i].split(" ")[1])
            if videos[0] == title_hash:
                warning("Video already downloaded.")
                return title_hash

        video.download(self.DOWNLOAD_DIR, filename=title_hash + ".mp4")

        success(f"Downloaded video as {title_hash}.mp4")
        self.file_manager.write_to_file(f"{self.CONFIG}/video_titles.txt",
                                        f"{title_hash}+CharacterSplit+{video_title}\n", add_to_end=True)
        return title_hash
