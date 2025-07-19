import streamlit as st
from moviepy.editor import VideoFileClip
import whisper
import srt
import subprocess
import os
import platform
from datetime import timedelta
import uuid

# Function to extract audio
def extract_audio(video_path, audio_path):
    try:
        video = VideoFileClip(video_path)
        audio = video.audio
        if audio:
            audio.write_audiofile(audio_path, logger=None)
            return audio_path
        else:
            st.error("⚠️ No audio found in the video.")
            return None
    except Exception as e:
        st.error(f"❌ Error extracting audio: {e}")
        return None

# Function to transcribe audio
def transcribe_audio(audio_path):
    try:
        st.info("📝 Loading Whisper model... (please wait ⏳)")
        model = whisper.load_model("base")
        # Detect language automatically
        result = model.transcribe(audio_path)  # No language forced
        return result
    except Exception as e:
        st.error(f"❌ Error during transcription: {e}")
        return None

# Function to convert transcription to SRT
def convert_to_srt(transcription_result):
    try:
        segments = transcription_result['segments']
        subtitles = []
        for i, seg in enumerate(segments):
            subtitle = srt.Subtitle(
                index=i + 1,
                start=timedelta(seconds=seg['start']),
                end=timedelta(seconds=seg['end']),
                content=seg['text'].strip()
            )
            subtitles.append(subtitle)
        return srt.compose(subtitles)
    except Exception as e:
        st.error(f"❌ Error generating SRT: {e}")
        return None

# Function to auto-generate unique filenames
def get_unique_filename(filename):
    unique_id = uuid.uuid4().hex[:6]
    base, ext = os.path.splitext(filename)
    return f"{base}_{unique_id}{ext}"

# Function to burn subtitles into video
def burn_subtitles(video_path, srt_path, output_path, overwrite=True):
    try:
        video_full = os.path.abspath(video_path).replace("\\", "/")
        srt_full = os.path.abspath(srt_path).replace("\\", "/").replace(":", "\\:")  # Escape colon for Windows
        output_full = os.path.abspath(output_path).replace("\\", "/")

        # Detect OS and set ffmpeg path
        if platform.system() == "Windows":
            ffmpeg_cmd = os.path.join(
                r"C:\ffmpeg-2025-07-17-git-bc8d06d541-essentials_build\bin",
                "ffmpeg.exe"
            )
        else:
            ffmpeg_cmd = "ffmpeg"  # On Linux/Streamlit Cloud

        # Handle overwrite flag
        overwrite_flag = "-y" if overwrite else "-n"

        # FFmpeg command
        command = (
            f'"{ffmpeg_cmd}" {overwrite_flag} -i "{video_full}" '
            f'-vf "subtitles=\'{srt_full}\':force_style=\'FontName=Arial,FontSize=20\'" '
            f'"{output_full}"'
        )

        st.text(f"🔧 Running FFmpeg command:\n{command}")  # Debug
        subprocess.run(command, shell=True, check=True)
        return output_full
    except subprocess.CalledProcessError as e:
        st.error(f"❌ Error burning subtitles: {e}")
        return None

# Streamlit App
def main():
    st.title("🎥 Auto Subtitles Generator (English) 🌍")
    st.markdown(
        """
        👋 **Welcome!**  
        📤 Upload a video, generate English captions using Whisper AI, and embed them into the video.  
        ⚡ *Note: Processing time depends on video length. Please wait and do not close the tab.*
        """
    )

    uploaded_video = st.file_uploader("📂 Upload your video", type=["mp4", "mov", "avi", "mkv"])

    if uploaded_video is not None:
        unique_video = get_unique_filename("temp_video.mp4")
        with open(unique_video, "wb") as f:
            f.write(uploaded_video.read())
        st.video(unique_video)

        overwrite = st.checkbox("✅ Overwrite existing output video?", value=True)

        if st.button("🚀 Process Video and Generate Captions"):
            audio_path = get_unique_filename("temp_audio.wav")
            srt_path = get_unique_filename("output.srt")
            output_video = get_unique_filename("output_video.mp4")

            # Step 1: Extract audio
            st.info("🔊 Extracting audio from video...")
            audio_file = extract_audio(unique_video, audio_path)
            if not audio_file:
                return

            # Step 2: Transcribe audio
            st.info("📝 Transcribing audio to text...")
            result = transcribe_audio(audio_file)
            if not result:
                return

            # Step 3: Generate SRT
            st.info("📜 Generating subtitle (SRT) file...")
            srt_content = convert_to_srt(result)
            if srt_content:
                with open(srt_path, "w", encoding="utf-8") as f:
                    f.write(srt_content)
                st.success("✅ SRT file created successfully!")

            # Step 4: Burn subtitles
            st.info("🔥 Embedding subtitles into video...")
            final_video = burn_subtitles(unique_video, srt_path, output_video, overwrite=overwrite)
            if final_video:
                st.success("🎉 Subtitled video is ready!")
                st.video(final_video)
                with open(final_video, "rb") as f:
                    st.download_button(
                        label="📥 Download Final Video",
                        data=f,
                        file_name=os.path.basename(final_video),
                        mime="video/mp4"
                    )

if __name__ == "__main__":
    main()
