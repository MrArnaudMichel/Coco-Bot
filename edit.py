import os
from datetime import timedelta

import assemblyai as aai
from moviepy.editor import *
from moviepy.video.tools.subtitles import SubtitlesClip
from termcolor import colored
import srt
import copy

class Edit:
    def __init__(self, video_name, fileManager, config):
        aai.settings.api_key = config.api_key
        self.config = config
        self.fileManager = fileManager
        self.video_name = video_name
        self.video = VideoFileClip("downloads/" + video_name + ".mp4")
        self.transcript = None

    def transcribe_video(self):
        print(colored("> Transcribing video...", "green"))
        self.transcript = aai.Transcriber().transcribe("downloads/" + self.video_name + ".mp4")

    def get_subtitles(self, start_end, index=0):
        start, end = start_end
        subtitles = copy.copy(self.transcript.export_subtitles_srt())

        subs = list(srt.parse(subtitles))

        subs = [sub for sub in subs if start <= sub.start.total_seconds() <= end]

        # Subtract 1 minute * index from each subtitle
        for i, sub in enumerate(subs):
            sub.start -= timedelta(minutes=index)
            sub.end -= timedelta(minutes=index)

        subtitles = srt.compose(subs)
        print(subtitles)
        return subtitles

    def split_part(self, video_path, start_end, subtitles, i):
        print(colored(f"> Splitting part {i}...", "green"))
        start, end = start_end
        video = VideoFileClip(video_path).subclip(start, end)

        f = open("subtitles.srt", "w")
        f.write(subtitles)
        f.close()
        print(colored("> Adding subtitles...", "green"))
        subtitles_clip = SubtitlesClip("subtitles.srt",
                                       lambda txt: TextClip(txt, font=self.config.font, fontsize=self.config.font_size,
                                                            color=self.config.font_color)).set_duration(video.duration)
        final = CompositeVideoClip([video, subtitles_clip.set_position(('center', 400))])
        print(colored(f"> Rendering part {i}...", "green"))
        final.write_videofile(f"uploads/{self.video_name}_part{i}.mp4", threads=self.config.threads)

    def split_video(self, seconds: int = 60, from_end: int = 5):
        video_path = "downloads/" + self.video_name + ".mp4"
        start = 0
        end = seconds
        i = 1
        tasks = []
        if self.transcript is None:
            self.transcribe_video()
        while end < self.video.duration:
            subtitles = self.get_subtitles((start, end), i - 1)
            tasks.append((video_path, (start, end), subtitles, i))
            start = end - from_end
            end += seconds - from_end

            i += 1
        tasks.append((video_path, (start, self.video.duration), subtitles, i))
        for task in tasks:
            self.split_part(*task)
        os.remove("subtitles.srt")
        print(colored("> Done splitting video.", "green"))

