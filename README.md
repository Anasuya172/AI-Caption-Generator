🎥 AI Caption Generator
This project is a Streamlit-based application that:
✅ Extracts audio from a video.
✅ Transcribes the audio to text using OpenAI Whisper.
✅ Generates SRT subtitle files.
✅ Burns subtitles directly into the video using FFmpeg.
✅ Allows downloading both the SRT file and final video.
✨ Features
🎙️ Automatic Transcription: Supports Hindi and English audio using Whisper’s AI model.

🔊 Audio Extraction: Pulls audio out of your uploaded video file.

📝 Subtitle Generation: Creates properly timed .srt files.

🔥 Subtitles Burn-in: Embeds captions directly into the video.

📥 Downloads: Export the final captioned video or just the SRT.

🌐 Simple Streamlit UI for user-friendly interaction.
🛠️ Technologies Used
OpenAI Whisper – Speech-to-text transcription.

MoviePy – Audio extraction.

FFmpeg – Subtitles burn-in.

Streamlit – Web-based app interface.

Python Libraries: whisper, moviepy, srt, subprocess, etc.

🚀 How to Run
🖥️ Local Setup
Clone this repository:  git clone https://github.com/<your-username>/ai-caption-generator.git
cd ai-caption-generator
 Install dependencies:   pip install -r requirements.txt
  Install FFmpeg:

Download FFmpeg.

Add it to your system PATH.

Run the app:  streamlit run app.py
Open http://localhost:8501 in your browser.    
☁️ Streamlit Cloud Deployment
This project is Streamlit Cloud-ready:

requirements.txt includes Python dependencies.

packages.txt adds system-level libraries (like ffmpeg).

Simply upload this repo to GitHub and deploy on Streamlit Cloud.

📥 Inputs & Outputs
| 📂 Input                       | 📁 Output                             |
| ------------------------------ | ------------------------------------- |
| Video files (.mp4, .mov, .avi) | Video with hardcoded subtitles (.mp4) |
|                                | Subtitle file (.srt)                  |
 ⚠️ Notes
Transcription time depends on video length and system resources.

On Streamlit Cloud, large Whisper models may not run due to memory limits.

  📜 License
This project is licensed under the MIT License.

