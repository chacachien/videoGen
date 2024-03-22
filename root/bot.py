from openai import OpenAI
import dotenv
import os

class Bot:
    def __init__(self):
        dotenv.load_dotenv()
        self.client = OpenAI()
    
    def execute(self, input):
        pass
