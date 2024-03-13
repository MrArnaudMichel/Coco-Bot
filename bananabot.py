from fileManager import FileManager
from youtube import YouTube
from edit import Edit
from termcolor import colored
from config import Config
class Bananabot:
    def __init__(self):
        self.edit = None
        self.config = Config()
        self.file_manager = FileManager()
        self.file_manager.create_all_dirs()
        self.youtube = YouTube(file_manager=self.file_manager)

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
        ╚═════╝ ╚═╝  ╚═╝╚═╝  ╚═══╝╚═╝  ╚═╝╚═╝  ╚═══╝╚═╝  ╚═╝╚═════╝  ╚═════╝    ╚═╝   """ , "yellow"))

        print(colored("Welcome to BananaBot!", "green"))
        print(colored("What would you like to do?", "green"))
        print("""
        1. Download video from YouTube
        2. See the downloaded video
        3. Upload video to YouTube
        9. Download video from Local File
        K. Exit
        """)
        self.start()

    def start(self):
        """
        Starts the bot.
        """
        choice = input("Enter your choice: ")

        while True:
            if choice == "1":
                print(colored("\t -> Downloading video from YouTube", "blue"))
                url = input("Enter the YouTube URL: ")
                title_hash = self.youtube.download_video(url)
                self.edit = Edit(f"{title_hash}", self.file_manager, self.config)
                self.edit.split_video()
            elif choice == "2":
                print(colored("\t -> Downloaded video", "blue"))
                print(self.file_manager.get_all_files())
            elif choice == "3":
                print(colored("\t -> Uploading video to YouTube", "blue"))
                print("Upload video to YouTube")
            elif choice == "9":
                print(colored("Exiting...", "red"))
                exit()
            else:
                print(colored("Invalid choice. Please try again.", "red"))
                choice = input("Enter your choice: ")

