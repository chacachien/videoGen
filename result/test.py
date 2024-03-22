import re
with open("result/script.txt", "r") as file:
    text = file.read()
# Sử dụng regex để tách Scene và Voiceover
# scene_pattern = re.compile(r'Scene:.*?Voiceover:', re.DOTALL)
# voiceover_pattern = re.compile(r'Voiceover:.*?(?:Scene:|$)', re.DOTALL)

# scenes = scene_pattern.findall(text)
# voiceovers = voiceover_pattern.findall(text)
# Sử dụng regex để tách Scene và Voiceover
scene_pattern = re.compile(r'Scene:(.*?)(?:Voiceover:|$)', re.DOTALL)
voiceover_pattern = re.compile(r'Voiceover:(.*?)(?:Scene:|$)', re.DOTALL)

scenes = scene_pattern.findall(text)
voiceovers = voiceover_pattern.findall(text)

scenes = [scene.strip() for scene in scenes if scene.strip()]
voiceovers = [voiceover.strip() for voiceover in voiceovers if voiceover.strip()]

# In kết quả
# for i, (scene, voiceover) in enumerate(zip(scenes, voiceovers), start=1):
#     print(f"Scene {i}:\n{scene.strip()}\n")
#     print(f"Voiceover {i}:\n{voiceover.strip()}\n")
print(scenes)
print(voiceovers)