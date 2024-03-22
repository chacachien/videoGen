import os
from moviepy.editor import *
from moviepy.video.tools.subtitles import SubtitlesClip
from openai import OpenAI
import json

class VideoBot:
    def __init__(self, time_str) -> None:
        self.audio_folder = f"result/{time_str}/audio"
        self.img_folder = f"result/{time_str}/image"
        self.video_folder = f"result/{time_str}/video"
        self.result = f"result/{time_str}"
        os.makedirs(self.video_folder, exist_ok=True)
        self.client = OpenAI()
        self.model = 'whisper-1'
        self.MaxWord = 7

    def merge(self):
        audio_files = os.listdir(self.audio_folder)
        img_files = os.listdir(self.img_folder)
        audio_files.sort()
        img_files.sort()
        print("audio files")
        print(audio_files)
        print("img files")
        print(img_files)
        video_clips = []
        for aud, img in zip(audio_files, img_files):
            aud_path = f"{self.audio_folder}/{aud}"
            img_path = f"{self.img_folder}/{img}"
            audio_clip = AudioFileClip(aud_path)
            img_clip = ImageClip(img_path)
            img_clip = img_clip.set_duration(audio_clip.duration)
            final_clip = CompositeVideoClip([img_clip.set_position('center')], size=(1920, 1080)).set_audio(audio_clip)
            final_clip = final_clip.set_audio(audio_clip)
            video_clips.append(final_clip)
        final_video = concatenate_videoclips(video_clips)
        final_video.write_videofile(f"{self.video_folder}/result.mp4", fps=24)
    
    def gen_subtitle(self):
        audio_file = open(f"{self.audio_folder}/result.mp3", "rb")
        transcript = self.client.audio.transcriptions.create(
            file=audio_file,
            model=self.model,
            response_format="verbose_json",
            timestamp_granularities=["word"]
        )
        # store this json file
        with open(f"{self.video_folder}/transcript.json", "w") as json_file:
            json.dump(transcript.words, json_file)

    def create_srt_file(self):
        json_file_path = f"{self.video_folder}/transcript.json"
        srt_file_path = f"{self.video_folder}/result.srt"
        voice_file_path = f"{self.result}/voiceover.txt"
        try:
            with open(voice_file_path, "r") as file:
                voiceovers = file.readlines()
                voiceovers = [voiceover.strip() for voiceover in voiceovers if voiceover.strip()]
            voiceovers_all = " ".join(voiceovers).split()

            voiceovers_filter = [''.join(filter(lambda char: char.isalpha(), word)) for word in voiceovers_all]

            with open(json_file_path, 'r', encoding='utf-8') as json_file:
                data = json.load(json_file)
                line = ""
                start_time = end_time = 0
                next = True
                with open(srt_file_path, 'w', encoding='utf-8') as srt_file:
                    subtitle_number = 1
                    for inx, word_data in enumerate(data):
                        if next:
                            start_time = self.format_time(word_data['start'])
                            next = False
                        end_time = self.format_time(word_data['end'])
                        #word = word_data['word'] 
                        word = voiceovers_filter[inx]
                        if len(line.split()) < self.MaxWord:
                            line += word + " "
                        else:
                            srt_file.write(f"{subtitle_number}\n{start_time} --> {end_time}\n{line.strip()}\n\n")
                            line = word + " "
                            subtitle_number += 1
                            next = True
                    if line:
                        srt_file.write(f"{subtitle_number}\n{start_time} --> {end_time}\n{line.strip()}\n")

        except FileNotFoundError:
            print(f"File {json_file_path} not found.")
        except json.JSONDecodeError as e:
            print(f"Error decoding JSON: {e}")
            
    @staticmethod
    def format_time(seconds):
        hours = int(seconds / 3600)
        minutes = int((seconds % 3600) / 60)
        seconds = seconds % 60
        milliseconds = int((seconds - int(seconds)) * 1000)
        return f"{hours:02d}:{minutes:02d}:{int(seconds):02d},{milliseconds:03d}"
        
    def add_subtitle(self):
        video = VideoFileClip(f"{self.video_folder}/result.mp4")
        generator = lambda txt: TextClip(txt, fontsize=24, color='white', bg_color='black')
        subtitle = SubtitlesClip(f"{self.video_folder}/result.srt", generator)
        subtitles = SubtitlesClip(subtitle, generator)
        video = CompositeVideoClip([video, subtitles.set_pos(('center', 'bottom'))])
        video.write_videofile(f"{self.video_folder}/result_with_subtitle.mp4")
