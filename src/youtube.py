import hashlib
import json
import os
import time
from datetime import datetime

from imageio.testing import ROOT_DIR
from pytube import YouTube as PyTube

from fileManager import FileManager
from termcolor import colored

from config import Config

from selenium import webdriver
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.firefox.service import Service
from selenium.webdriver.common.by import By

from webdriver_manager.firefox import GeckoDriverManager

from status import *
from constants import *
from utils import build_url


def get_cache_path() -> str:
    """
    Gets the path to the cache file.

    Returns:
        path (str): The path to the cache folder
    """
    print(ROOT_DIR)
    return os.path.join(ROOT_DIR, '.mp')


class YouTube:
    """
    YouTube class to download a video from YouTube.
    """

    def __init__(self, file_manager: FileManager):
        self.file_manager = file_manager
        self.DOWNLOAD_DIR = "downloads"
        self.UPLOAD_DIR = "uploads"
        self.CONFIG = "config"

        self._account_uuid: str = Config.get_account_uuid()
        self._account_nickname: str = Config.get_account_nickname()
        self._fp_profile_path: str = Config.get_firefox_profile_path()

        self.images = []

        self.options: Options = Options()

        if Config.get_headless():
            self.options.add_argument("--headless")

        self.options.add_argument("-profile")
        self.options.add_argument(self._fp_profile_path)

        self.service: Service = Service(GeckoDriverManager().install())

        # Initialize the browser
        self.browser: webdriver.Firefox = webdriver.Firefox(service=self.service, options=self.options)

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

        video.download(self.DOWNLOAD_DIR, filename=title_hash + ".mp4")

        success(f"Downloaded video as {title_hash}.mp4")
        lines = self.file_manager.get_all_videos()
        for i, line in enumerate(lines):
            videos: tuple[str, str] = (line.split(" ")[0], lines[i].split(" ")[1])
            if videos[0] == title_hash:
                warning("Video already downloaded.")
                return title_hash
        self.file_manager.write_to_file(f"{self.CONFIG}/video_titles.txt",
                                        f"{title_hash}+CharacterSplit+{video_title}\n", add_to_end=True)
        return title_hash

    def upload_video(self, video_path: str) -> bool:
        """
        Uploads a video to YouTube.
        :param video_path:
        :return bool:
        """
        try:
            self.get_channel_id()

            driver = self.browser
            verbose = Config.get_verbose()

            # Go to youtube.com/upload
            driver.get("https://www.youtube.com/upload")

            # Set video file
            FILE_PICKER_TAG = "ytcp-uploads-file-picker"
            file_picker = driver.find_element(By.TAG_NAME, FILE_PICKER_TAG)
            INPUT_TAG = "input"
            file_input = file_picker.find_element(By.TAG_NAME, INPUT_TAG)
            file_input.send_keys(video_path)

            # Wait for upload to finish
            time.sleep(5)

            # Set title
            textboxes = driver.find_elements(By.ID, YOUTUBE_TEXTBOX_ID)

            title_el = textboxes[0]
            description_el = textboxes[-1]

            if verbose:
                info("\t=> Setting title...")

            title_el.click()
            time.sleep(1)
            title_el.clear()
            title_el.send_keys(self.metadata["title"])

            if verbose:
                info("\t=> Setting description...")

            # Set description
            time.sleep(10)
            description_el.click()
            time.sleep(0.5)
            description_el.clear()
            description_el.send_keys(self.metadata["description"])

            time.sleep(0.5)

            # Set `made for kids` option
            if verbose:
                info("\t=> Setting `made for kids` option...")

            is_for_kids_checkbox = driver.find_element(By.NAME, YOUTUBE_MADE_FOR_KIDS_NAME)
            is_not_for_kids_checkbox = driver.find_element(By.NAME, YOUTUBE_NOT_MADE_FOR_KIDS_NAME)

            if not Config.get_is_for_kids():
                is_not_for_kids_checkbox.click()
            else:
                is_for_kids_checkbox.click()

            time.sleep(0.5)

            # Click next
            if verbose:
                info("\t=> Clicking next...")

            next_button = driver.find_element(By.ID, YOUTUBE_NEXT_BUTTON_ID)
            next_button.click()

            # Click next again
            if verbose:
                info("\t=> Clicking next again...")
            next_button = driver.find_element(By.ID, YOUTUBE_NEXT_BUTTON_ID)
            next_button.click()

            # Wait for 2 seconds
            time.sleep(2)

            # Click next again
            if verbose:
                info("\t=> Clicking next again...")
            next_button = driver.find_element(By.ID, YOUTUBE_NEXT_BUTTON_ID)
            next_button.click()

            # Set as unlisted
            if verbose:
                info("\t=> Setting as unlisted...")

            radio_button = driver.find_elements(By.XPATH, YOUTUBE_RADIO_BUTTON_XPATH)
            radio_button[2].click()

            if verbose:
                info("\t=> Clicking done button...")

            # Click done button
            done_button = driver.find_element(By.ID, YOUTUBE_DONE_BUTTON_ID)
            done_button.click()

            # Wait for 2 seconds
            time.sleep(2)

            # Get latest video
            if verbose:
                info("\t=> Getting video URL...")

            # Get the latest uploaded video URL
            driver.get(f"https://studio.youtube.com/channel/{self.channel_id}/videos/short")
            time.sleep(2)
            videos = driver.find_elements(By.TAG_NAME, "ytcp-video-row")
            first_video = videos[0]
            anchor_tag = first_video.find_element(By.TAG_NAME, "a")
            href = anchor_tag.get_attribute("href")
            if verbose:
                info(f"\t=> Extracting video ID from URL: {href}")
            video_id = href.split("/")[-2]

            # Build URL
            url = build_url(video_id)

            self.uploaded_video_url = url

            if verbose:
                success(f" => Uploaded Video: {url}")

            # Add video to cache
            self.add_video({
                "title": self.metadata["title"],
                "description": self.metadata["description"],
                "url": url,
                "date": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            })

            # Close the browser
            driver.quit()

            return True
        except:
            self.browser.quit()
            return False

    def get_channel_id(self) -> str:
        """
        Gets the Channel ID of the YouTube Account.

        Returns:
            channel_id (str): The Channel ID.
        """
        driver = self.browser
        driver.get("https://studio.youtube.com")
        time.sleep(2)
        channel_id = driver.current_url.split("/")[-1]
        self.channel_id = channel_id

        return channel_id

    def add_video(self, video: dict) -> None:
        """
        Adds a video to the cache.

        Args:
            video (dict): The video to add

        Returns:
            None
        """
        videos = self.get_videos()
        videos.append(video)

        cache = self.get_youtube_cache_path()

        with open(cache, "r") as file:
            previous_json = json.loads(file.read())

            # Find our account
            accounts = previous_json["accounts"]
            for account in accounts:
                if account["id"] == self._account_uuid:
                    account["videos"].append(video)

            # Commit changes
            with open(cache, "w") as f:
                f.write(
                    json.dumps(previous_json))

    def get_youtube_cache_path(self) -> str:
        """
        Gets the path to the YouTube cache file.

        Returns:
            path (str): The path to the YouTube cache folder
        """
        return os.path.join(get_cache_path(), 'youtube.json')

    def get_videos(self) -> list[dict]:
        """
        Gets the uploaded videos from the YouTube Channel.

        Returns:
            videos (List[dict]): The uploaded videos.
        """
        if not os.path.exists(self.get_youtube_cache_path()):
            # Create the cache file
            with open(self.get_youtube_cache_path(), 'w') as file:
                json.dump({
                    "videos": []
                }, file, indent=4)
            return []

        videos = []
        # Read the cache file
        with open(self.get_youtube_cache_path(), 'r') as file:
            previous_json = json.loads(file.read())
            # Find our account
            accounts = previous_json["accounts"]
            for account in accounts:
                if account["id"] == self._account_uuid:
                    videos = account["videos"]

        return videos

