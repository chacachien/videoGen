from root.bot import Bot
import urllib.request
import os
from pydub import AudioSegment
class ImgBot(Bot):
    def __init__(self, time_str):
        super().__init__()
        self.prompt = """
        ## Persona: 
        You are a image generate assistand, and your job is to come up with engaging image for videos.

        ## Goal:
        Create image from the given script.

        ## Constraints:
        The image should be engaging and informative.

        ## Requirement:
        """.strip()
        self.folder = f"result/{time_str}"
        self.model = "dall-e-3"

    def execute(self, script):
        os.makedirs(f"{self.folder}/image", exist_ok=True)
        for i in range(len(script)):
            response = self.client.images.generate(
                model = self.model,
                prompt = self.prompt + script[i],
                size = "1792x1024",
                quality="standard",
                n = 1,
            )
            url = response.data[0].url
            urllib.request.urlretrieve(url, f"{self.folder}/image/{i+1}.jpg")

class AudioBot(Bot):
    def __init__(self, time_str):
        super().__init__()
        self.folder = f"result/{time_str}"
        self.model = "tts-1"
        self.voice = "alloy"
    def execute(self, audios):
        os.makedirs(f"{self.folder}/audio", exist_ok=True)
        for i in range(len(audios)):
            response = self.client.audio.speech.create(
                model = self.model,
                voice = self.voice,
                input = audios[i]
            )
            response.stream_to_file(f"{self.folder}/audio/{i+1}.mp3")
            merged_audio = AudioSegment.from_file(f"{self.folder}/audio/{i+1}.mp3") if i == 0 else merged_audio + AudioSegment.from_file(f"{self.folder}/audio/{i+1}.mp3")
        merged_audio.export(f"{self.folder}/audio/result.mp3", format="mp3")
        