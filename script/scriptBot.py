from openai import OpenAI
import dotenv
import os
import re
from root.bot import Bot

class ScriptBot(Bot):
    def __init__(self, time_str):
        super().__init__()
        self.prompt = """
            ##Persona:
            You are an image generation assistant tasked with creating captivating images for videos.

            ##Goal:
            Compile a list of commands to generate images that align with the provided script.

            ##Format:
            Scene: //Describe the image here//
            Voiceover: //Narrator dialogue here//
            
            ##Constraints:
            Ensure the images are engaging and informative.
            Strictly adhere to the specified format.
            Answer in the same language as the prompt. 
            Remember add the "\n" at the end of each scene and voiceover.

            ##Example:
            Scene: A bright, futuristic lab filled with advanced computers and holographic displays. In the center, a large, glowing, digital brain symbolizes artificial intelligence.
            Voiceover: Welcome to the forefront of technological innovation, where the boundaries of what machines can do are pushed further every day. Meet OpenAI, a pioneering research organization dedicated to advancing artificial intelligence in a safe and beneficial manner.

            Scene: A timeline graphic illustrating the key milestones of OpenAI, starting from its founding year to its most recent achievements.
            Voiceover: Since its inception, OpenAI has been on a remarkable journey, achieving milestone after milestone in the field of AI. From groundbreaking research papers to the development of powerful AI models, OpenAI's contributions have been both diverse and impactful.

            Scene: A vibrant, animated depiction of diverse AI applications, showing robots assisting in healthcare, AI in environmental protection, and AI-powered education tools.
            Voiceover: OpenAI's vision extends far beyond the laboratory. It's about creating AI that can benefit humanity in diverse ways—enhancing healthcare, aiding in the fight against climate change, and revolutionizing the way we learn.\n

            """
        self.folder = f"result/{time_str}"
    def seperate(self):
        with open(f"{self.folder}/script.txt", "r") as file:
            text = file.read()

        scene_pattern = re.compile(r'Scene:(.*?)(?:Voiceover:|$)', re.DOTALL)
        voiceover_pattern = re.compile(r'Voiceover:(.*?)(?:Scene:|$)', re.DOTALL)

        scenes = scene_pattern.findall(text)
        voiceovers = voiceover_pattern.findall(text)


        scenes = [scene.strip() for scene in scenes if scene.strip()]
        voiceovers = [voiceover.strip() for voiceover in voiceovers if voiceover.strip()]

        with open(f"{self.folder}/voiceover.txt", "w") as file:
            for voice in voiceovers:
                file.write(voice + "\n")
        return scenes, voiceovers

    def execute(self, input):
        completion = self.client.chat.completions.create(
            model="gpt-4-turbo-preview",
            messages=[
                {"role": "system", "content": self.prompt},
                {"role": "user", "content": input}
            ]
        )
        print(completion.choices[0].message.content)
        with open(f"{self.folder}/script.txt", "w") as file:
            file.write(completion.choices[0].message.content)
        return completion.choices[0].message


