
 # Video Generation Project

This project allows you to create short videos based on a given topic.

## Requirements

### Python packages:

- `openai`: For interacting with the OpenAI API to generate text.
- `python-dotenv`: For loading environment variables from a `.env` file.
- `moviepy`: For video editing and manipulation.
- `pydub`: For audio manipulation.

### Brew packages:

- `ffmpeg`: For encoding and decoding video and audio.
- `ghostscript`: For converting PDF files to images.
- `imagemagick`: For image manipulation.

## Project Structure

```
├── img
│   └──
├── result
│   └──
├── root
│   └──
├── script
│   └──
├── video
│   └──
├── .DS_Store
├── .gitignore
├── README.md
├── main.py
├── output_subtitle.srt
├── requirements.txt
└── secrets.py
```

## Usage

1. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   brew install ffmpeg ghostscript imagemagick
   ```

2. **Create a `.env` file and set the following environment variables:**
   ```
   OPENAI_API_KEY=your_openai_api_key
   ```

3. **Run the script:**
   ```bash
   python main.py
   ```

4. **Enter the topic for your video.**

5. **The script will generate a video file in the `video` folder.**

## Notes

- Make sure you have a valid OpenAI API key.
- The video generation process may take some time depending on the length of the video and the complexity of the topic.
- You can customize the video output by modifying the script.

## Contributing

Contributions are welcome! Feel free to open an issue or submit a pull request.
 
