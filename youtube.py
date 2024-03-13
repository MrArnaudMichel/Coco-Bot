import hashlib

from selenium import webdriver
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.firefox.service import Service
from selenium.webdriver.firefox.firefox_profile import FirefoxProfile
from webdriver_manager.firefox import GeckoDriverManager
from pytube import YouTube as PyTube
import http.cookiejar
import requests

from fileManager import FileManager
from termcolor import colored


class YouTube:
    def __init__(self, file_manager: FileManager):
        self.file_manager = file_manager
        self.DOWNLOAD_DIR = "downloads"
        self.UPLOAD_DIR = "uploads"
        self.CONFIG = "config"

        # Path to the Firefox profile
        profile_directory = "/home/arnaud/.mozilla/firefox/t3t85tzx.default"

        # Create a new instance of FirefoxProfile with the profile directory
        profile = FirefoxProfile(profile_directory)

        self.options: Options = Options()
        self.options.add_argument("--headless")
        self.options.add_argument("-profile")
        self.options.add_argument(profile_directory)
        self.service: Service = Service(GeckoDriverManager().install())

        # Pass the FirefoxProfile instance to the Firefox webdriver
        self.browser: webdriver.Firefox = webdriver.Firefox(service=self.service, options=self.options)

    def download_video(self, url: str) -> str:
        """
        Downloads a video from YouTube.
        :param url:
        :return title_hash:
        """
        print(colored("> Downloading video...", "green"))

        cookie_jar = http.cookiejar.MozillaCookieJar('config/cookies.txt')
        cookie_jar.load()

        session = requests.Session()
        session.cookies = cookie_jar

        pytube = PyTube(url)
        video = pytube.streams.get_highest_resolution()

        # Get the video title and create a hash of it
        video_title = pytube.title
        title_hash = hashlib.sha256(video_title.encode()).hexdigest()

        # Use the hash as the output name
        video.download(self.DOWNLOAD_DIR, filename=title_hash+".mp4")
        self.file_manager.write_to_file(f"{self.CONFIG}/video_titles.txt", f"{title_hash} {video_title}\n")
        print(colored(f"> Downloaded video as {title_hash}.mp4", "green"))
        return title_hash
