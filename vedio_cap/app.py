import streamlit as st
from moviepy.editor import VideoFileClip
import whisper
import srt
import subprocess
import os
import platform
from datetime import timedelta

# Function to extract audio
def extract_audio(video_path, audio_path):
    try:
        video = VideoFileClip(video_path)
        audio = video.audio
        if audio:
            audio.write_audiofile(audio_path)
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
        result = model.transcribe(audio_path, language="hi")  # force Hindi
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
def get_unique_filename(filepath):
    base, ext = os.path.splitext(filepath)
    counter = 1
    new_filepath = filepath
    while os.path.exists(new_filepath):
        new_filepath = f"{base}_{counter}{ext}"
        counter += 1
    return new_filepath

# Function to burn subtitles into video
def burn_subtitles(video_path, srt_path, output_path, overwrite=True):
    try:
        video_full = os.path.abspath(video_path)
        srt_fixed = srt_path.replace("\\", "/")
        output_full = os.path.abspath(output_path)

        # Detect OS and set ffmpeg
        if platform.system() == "Windows":
            ffmpeg_cmd = os.path.join(r"C:\ffmpeg-2025-07-17-git-bc8d06d541-essentials_build\bin", "ffmpeg.exe")
        else:
            ffmpeg_cmd = "ffmpeg"  # On Linux (Streamlit Cloud), use global ffmpeg

        # Add overwrite flag
        overwrite_flag = "-y" if overwrite else "-n"
        command = f'"{ffmpeg_cmd}" {overwrite_flag} -i "{video_full}" -vf "subtitles={srt_fixed}" "{output_full}"'

        subprocess.run(command, shell=True, check=True)
        return output_full
    except subprocess.CalledProcessError as e:
        st.error(f"❌ Error burning subtitles: {e}")
        return None

# Streamlit app
def main():
    st.title("🎥 Auto Subtitles Generator and Burner")
    st.markdown(
        """
        👋 **Welcome!**  
        📤 Upload a video, generate Hindi captions using Whisper AI, and embed them into the video.  
        ⚡ *Note: Processing time depends on video length. Please wait and do not close the tab.*
        """
    )

    uploaded_video = st.file_uploader("📂 Upload your video", type=["mp4", "mov", "avi", "mkv"])

    if uploaded_video is not None:
        with open("temp_video.mp4", "wb") as f:
            f.write(uploaded_video.read())
        st.video("temp_video.mp4")

        overwrite = st.checkbox("✅ Overwrite existing output video?", value=True)

        if st.button("🚀 Process Video and Generate Captions"):
            audio_path = "temp_audio.wav"
            srt_path = "output.srt"
            output_video = "output_video.mp4"

            # Step 1: Extract audio
            st.info("🔊 Extracting audio from video...")
            audio_file = extract_audio("temp_video.mp4", audio_path)
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
            final_video = burn_subtitles("temp_video.mp4", srt_path, output_video, overwrite=overwrite)
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
