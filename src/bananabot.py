from fileManager import FileManager
from youtube import YouTube
from edit import Edit
from termcolor import colored
from config import Config


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
        print(colored("""
        ██████╗  █████╗ ███╗   ██╗ █████╗ ███╗   ██╗ █████╗ ██████╗  ██████╗ ████████╗
        ██╔══██╗██╔══██╗████╗  ██║██╔══██╗████╗  ██║██╔══██╗██╔══██╗██╔═══██╗╚══██╔══╝
        ██████╔╝███████║██╔██╗ ██║███████║██╔██╗ ██║███████║██████╔╝██║   ██║   ██║   
        ██╔══██╗██╔══██║██║╚██╗██║██╔══██║██║╚██╗██║██╔══██║██╔══██╗██║   ██║   ██║   
        ██████╔╝██║  ██║██║ ╚████║██║  ██║██║ ╚████║██║  ██║██████╔╝╚██████╔╝   ██║   
        ╚═════╝ ╚═╝  ╚═╝╚═╝  ╚═══╝╚═╝  ╚═╝╚═╝  ╚═══╝╚═╝  ╚═╝╚═════╝  ╚═════╝    ╚═╝   """, "yellow"))

        print(colored("Welcome to BananaBot!", "green"))
        print(colored("What would you like to do?", "green"))
        self.start()

    def start(self):
        """
        Starts the bot.
        """
        print("""
                1. Download video from YouTube
                2. See the downloaded video
                3. Upload video to YouTube
                4. Download video from Local File
                8. Help
                9. Exit
                """)
        choice = input("Enter your choice: ")

        while True:
            if choice == "1":
                print(colored("\t -> Download video from YouTube", "blue"))
                url = input("Enter the YouTube URL: ")
                if url == "":
                    print(colored("URL cannot be empty.", "red"))
                elif "youtube.com" not in url:
                    print(colored("Invalid YouTube URL.", "red"))
                elif "watch?v=" not in url:
                    print(colored("Invalid YouTube URL.", "red"))
                else:
                    title_hash = self.youtube.download_video(url)
                    self.edit_video(title_hash)
            elif choice == "2":
                print(colored("\t -> Downloaded video", "blue"))
                self.show_downloaded_video()
            elif choice == "3":
                print(colored("\t -> Upload video to YouTube", "blue"))
                print("Upload video to YouTube")
            elif choice == "4":
                print(colored("\t -> Download video from Local File", "blue"))
                path = input("Enter the path of the video (Absolute path): ")
                print(colored(f"Downloading {path}...", "blue"))
            elif choice == "8":
                print(colored("\t -> Help", "blue"))
                self.help()

            elif choice == "9":
                print(colored("Exiting...", "red"))
                exit()
            else:
                print(colored("ERROR: Invalid choice. Please try again.", "red"))
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
            video: tuple[str, str] = (line.split(" ")[0], lines[i].split(" ")[1])
            print(f"{i + 1}. {video[1]}")
        choice = input("Enter the number of the video you want to see: ")
        video = lines[int(choice) - 1].split("+CharacterSplit+")[0]
        print(colored(f"> Showing {video}...", "blue"))
        print(colored(f"""
            Name: {video}
            Path: uploads/{video}/
            Number of parts: {len(self.file_manager.get_all_files(f"uploads/{video}"))}
            """, "blue"))

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
        choice = input("Enter the number of the question you want to see: ")
        if choice == "1":
            print(colored(
                "To have your AssemblyAI API key, go to https://www.assemblyai.com/dashboard/signup and sign up. Then, go to the dashboard and copy your API key."),
                "green")
        elif choice == "2":
            print(colored("To use the bot, follow the instructions given in the README.md file."), "green")
        elif choice == "3":
            print(colored("To change the configuration, go to config/config.json and change the values."), "green")
        elif choice == "4":
            print(colored(
                "To contribute to the bot, go to https://github.com/MrArnaudMichel/BananaBot and fork the repository. Then, make your changes and create a pull request."),
                "green")
        elif choice == "5":
            print(colored(
                "To report a bug, go to https://github.com/MrArnaudMichel/BananaBot/issues and create a new issue."),
                "green")
        elif choice == "6":
            print(colored("To download the bot, go to LinkDiscord and click on the download button."), "green")
        elif choice == "7":
            print(colored("It's not allowed to edit the bot.", "red"))
        else:
            print(colored("ERROR: Invalid choice. Please try again.", "red"))
        self.start()
