This project is a Streamlit-based web application that allows you to:

✅ Upload a video file.
✅ Generate subtitles in Hindi or English using advanced AI models (OpenAI Whisper).
✅ Burn the generated subtitles directly into the video.
✅ Download the final video with embedded captions and the separate SRT subtitle file.

It’s designed for content creators, educators, and anyone who needs quick and accurate subtitles for their videos.
✨ Features
🎙️ Hindi Mode: Transcribes videos with Hindi audio using Whisper-large for highly accurate results.

📝 English Mode: Transcribes videos with English audio using Whisper-large.

🔊 Audio Extraction: Automatically extracts audio from the video before transcription.

📜 SRT Support: Generates a standard .srt subtitle file for separate use.

📥 Download Options: Download videos with hardcoded subtitles and the standalone SRT file.

🌐 Simple Streamlit UI: Clean and user-friendly interface to make the process seamless.

⚡ Performance Notice: Processing time depends on video length and quality. The system may take some time, so please wait and avoid turning off your computer during processing.🛠️ Technologies Used
🤖 OpenAI Whisper for speech-to-text transcription.

🎥 MoviePy for audio extraction.

🔥 FFmpeg for burning subtitles directly into video files.

🖥️ Streamlit for building the interactive UI.

🚀 How to Run
1️⃣ Clone this repository
git clone https://github.com/Anasuya172/video-subtitle-generator.git
cd video-subtitle-generator
2️⃣ Install dependencies
pip install -r requirements.txt
3️⃣ Install FFmpeg
Make sure FFmpeg is installed and added to your system’s PATH. You can download it from:
https://ffmpeg.org/download.html
4️⃣ Run the app
streamlit run app.py
📁 Input and Output
| 📂 Input                             | 🎯 Output                             |
| ------------------------------------ | ------------------------------------- |
| Video files (.mp4, .mkv, .mov, etc.) | 🔥 Video with **burned-in subtitles** |
|                                      | 📜 Separate `.srt` subtitle file      |
