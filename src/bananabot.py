from fileManager import FileManager
from youtube import YouTube
from edit import Edit
from termcolor import colored
from config import Config
from status import *


class Bananabot:
    """
    Bananabot class to run the bot.
    The bot can download a video from YouTube, see the downloaded video, upload a video to YouTube, download a video from
    local file, and show the help menu.
    """

    def __init__(self):
        self.edit = None
        self.config = Config()
        self.file_manager = FileManager()
        self.file_manager.create_all_dirs()
        self.youtube = YouTube(file_manager=self.file_manager)
        self.width = 540
        self.height2 = 960

    def run(self) -> None:
        """
        Runs the bot.
        print BananaBot in ASCII art
        """
        print(colored(open("config/logo", "r").read(), "yellow"))

        success("Welcome to BananaBot!", show_emoji=False)
        self.start()

    def start(self):
        """
        Starts the bot.
        """
        info("What do you want to do?")
        print("""
                1. Download video from YouTube
                2. See the downloaded video
                3. Upload video to YouTube
                4. Download video from Local File
                8. Help
                9. Exit
                """)
        choice = question("Enter the number of the choice you want to do: ")

        while True:
            if choice == "1":
                info("\t> Download video from YouTube")
                url = question("Enter the YouTube URL: ")
                if url == "":
                    error("Invalid YouTube URL. Please try again.")
                elif "youtube.com" not in url:
                    error("Invalid YouTube URL. Please try again.")
                elif "watch?v=" not in url:
                    error("Invalid YouTube URL. Please try again.")
                else:
                    title_hash = self.youtube.download_video(url)
                    self.edit_video(title_hash)
            elif choice == "2":
                info("\t> See the downloaded video")
                self.show_downloaded_video()
            elif choice == "3":
                info("\t> Upload video to YouTube")
                path = self.show_downloaded_video() + "part1.mp4"
                self.youtube.upload_video(path)
            elif choice == "4":
                info("\t> Download video from Local File")
                path = question("Enter the path of the video (Absolute path): ")
                title_hash = self.file_manager.download_video_from_local_file(path)
                self.edit_video(title_hash)
            elif choice == "8":
                info("\t> Help")
                self.help()
            elif choice == "9":
                info("\t> Exit")
                exit()
            else:
                error("Invalid choice. Please try again.")
            self.start()

    def edit_video(self, title_hash):
        """
        Edits the video. Calls the Edit class to split the video.
        :param title_hash:
        """
        self.edit = Edit(f"{title_hash}", self.file_manager, self.config)
        self.edit.split_video()

    def show_downloaded_video(self):
        """
        Shows the downloaded video.
        """
        lines = self.file_manager.get_all_videos()
        for i, line in enumerate(lines):
            video: tuple[str, str] = (line.split("CharacterSplit")[0], lines[i].split("CharacterSplit")[1])
            info(f"{i + 1}. {video[1]}")
        choice = question("Enter the number of the video you want to see: ")
        video = lines[int(choice) - 1].split("CharacterSplit")[0], lines[int(choice) - 1].split("CharacterSplit")[1]
        info(f"\t> Showing {video[1]}")
        print(colored(f"""
            Title: {video[1]}
            Id: {video[0]}
            Path: uploads/{video[0]}/
            Number of parts: {len(self.file_manager.get_all_files(f"uploads/{video[0]}"))}
            """, "blue"))
        return f'uploads/{video[0]}/'

    def help(self):
        """
        Shows the help menu.
        """
        print("""
                1. How to have my AssemblyAI API key?
                2. How to use the bot?
                3. How to change the configuration?
                4. How can I contribute to the bot?
                5. How can I report a bug?
                6. How to download the bot?
                7. How to edit the bot?
        """)
        choice = question("Enter the number of the question you want to see: ")
        if choice == "1":
            info("How to have my AssemblyAI API key?")
            info("\t> To have your AssemblyAI API key, go to https://www.assemblyai.com/dashboard/signup and sign up. Then, go to the dashboard and copy your API key.")
        elif choice == "2":
            info("How to use the bot?")
            info("\t> To use the bot, follow the instructions given in the README.md file.")
        elif choice == "3":
            info("How to change the configuration?")
            info("\t> To change the configuration, go to config/config.json and change the values.")
        elif choice == "4":
            info("How can I contribute to the bot?")
            info("\t> To contribute to the bot, go to the GitHub repository and create a pull request.")
        elif choice == "5":
            info("How can I report a bug?")
            info("\t> To report a bug, go to the GitHub repository and create an issue.")
        elif choice == "6":
            info("How to download the bot?")
            info("\t> To download the bot, go to the GitHub repository and download the source code.")
        elif choice == "7":
            info("How to edit the bot?")
            info("\t> To edit the bot, go to the src directory and edit the files.")
        else:
            error("Invalid choice. Please try again.")
        self.start()
