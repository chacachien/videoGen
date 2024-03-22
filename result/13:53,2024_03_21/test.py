import json
voice_file_path = "voiceover.txt"
json_file_path = "video/transcript.json"
srt_file_path = "video/result.srt"
MaxWord = 7

def format_time(seconds):
    hours = int(seconds / 3600)
    minutes = int((seconds % 3600) / 60)
    seconds = seconds % 60
    milliseconds = int((seconds - int(seconds)) * 1000)
    return f"{hours:02d}:{minutes:02d}:{int(seconds):02d},{milliseconds:03d}"
with open(voice_file_path, "r") as file:
    voiceovers = file.readlines()
    voiceovers = [voiceover.strip() for voiceover in voiceovers if voiceover.strip()]
voiceovers_all = " ".join(voiceovers).split()
print(voiceovers_all)
voiceovers_filter = [''.join(filter(lambda char: char.isalpha(), word)) for word in voiceovers_all]
print(voiceovers_filter)
with open(json_file_path, 'r', encoding='utf-8') as json_file:
    data = json.load(json_file)
    line = ""
    start_time = end_time = 0
    next = True
    with open(srt_file_path, 'w', encoding='utf-8') as srt_file:
        subtitle_number = 1
        for inx, word_data in enumerate(data):
            if next:
                start_time = format_time(word_data['start'])
                next = False
            end_time = format_time(word_data['end'])
            #word = word_data['word'] 
            print(inx, voiceovers_filter[inx])
            try: 
                word = voiceovers_filter[inx]
            except:
                word = " "
            if len(line.split()) < MaxWord:
                line += word + " "
            else:
                srt_file.write(f"{subtitle_number}\n{start_time} --> {end_time}\n{line.strip()}\n\n")
                line = word + " "
                subtitle_number += 1
                next = True
        if line:
            srt_file.write(f"{subtitle_number}\n{start_time} --> {end_time}\n{line.strip()}\n")
