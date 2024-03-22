# import re

# text = """Voiceover: Welcome to the forefront of technological innovation, where the boundaries of what machines can do are pushed further every day. Meet OpenAI, a pioneering research organization dedicated to advancing artificial intelligence in a safe and beneficial manner.
# Voiceover: Since its inception, OpenAI has been on a remarkable journey, achieving milestone after milestone in the field of AI. From groundbreaking research papers to the development of powerful AI models, OpenAI's contributions have been both diverse and impactful.
# """

# voiceover_pattern = re.compile(r'Voiceover:(.*?)\n', re.DOTALL | re.IGNORECASE)

# matches = voiceover_pattern.findall(text)
# text = ''
# for match in matches:
#     text += match.strip() + '\n'
# print(text)


# from openai import OpenAI
# client = OpenAI()
# from pydub import AudioSegment
# import json 

# audio_file = open("/Users/phatnguyen/Document/work/video/result/09:15,2024_03_21/audio/result.mp3", "rb")

# transcript = client.audio.transcriptions.create(
#   file=audio_file,
#   model="whisper-1",
#   response_format="verbose_json",
#   timestamp_granularities=["word"]
# )

# print(transcript.words)
# with open(f"result/09:15,2024_03_21/transcript.json", "w") as json_file:
#     json.dump(transcript.words, json_file)
import json
# try:
#     json_file_path = "result/09:15,2024_03_21/transcript.json"
#     with open(json_file_path, 'r', encoding='utf-8') as json_file:
#         data = json.load(json_file)
#         # Process the JSON data
#         for word_data in data:
#             print(f"Word: {word_data['word']}, Start: {word_data['start']}, End: {word_data['end']}")
# except FileNotFoundError:
#     print(f"File {json_file_path} not found.")
# except json.JSONDecodeError as e:
#     print(f"Error decoding JSON: {e}")

def create_srt_file(json_file_path, srt_file_path, max_words_per_line=7):
    try:
        with open(json_file_path, 'r', encoding='utf-8') as json_file:
            data = json.load(json_file)
            line = ""
            start_time = end_time = 0
            with open(srt_file_path, 'w', encoding='utf-8') as srt_file:
                subtitle_number = 1
                for word_data in data:
                    start_time = format_time(word_data['start'])
                    end_time = format_time(word_data['end'])
                    word = word_data['word']
                    if len(line.split()) < max_words_per_line:
                        line += word + " "
                    else:
                        srt_file.write(f"{subtitle_number}\n{start_time} --> {end_time}\n{line.strip()}\n\n")
                        line = word + " "
                        subtitle_number += 1
                if line:
                    srt_file.write(f"{subtitle_number}\n{start_time} --> {end_time}\n{line.strip()}\n")
    except FileNotFoundError:
        print(f"File {json_file_path} not found.")
    except json.JSONDecodeError as e:
        print(f"Error decoding JSON: {e}")

def format_time(seconds):
    hours = int(seconds / 3600)
    minutes = int((seconds % 3600) / 60)
    seconds = seconds % 60
    milliseconds = int((seconds - int(seconds)) * 1000)
    return f"{hours:02d}:{minutes:02d}:{int(seconds):02d},{milliseconds:03d}"

# Example usage:
json_file_path = "result/09:15,2024_03_21/transcript.json"
srt_file_path = "output_subtitle.srt"

create_srt_file(json_file_path, srt_file_path)