import streamlit as st
from moviepy.editor import VideoFileClip
import subprocess
import os
import whisper
import srt
from datetime import timedelta

# Use system ffmpeg for Streamlit Cloud
os.environ["PATH"] += os.pathsep + "/usr/bin"

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

# Hindi Transcription (Whisper large for better results)
def transcribe_audio_hindi(audio_path):
    try:
        st.info("📝 Loading Whisper-large for Hindi transcription... (this may take time ⏳)")
        model = whisper.load_model("large")
        result = model.transcribe(audio_path, language="hi", task="transcribe")
        return result['text']
    except Exception as e:
        st.error(f"❌ Error during Hindi transcription: {e}")
        return None

# English Transcription (Whisper base for speed)
def transcribe_audio_english(audio_path):
    try:
        st.info("📝 Loading Whisper-base for English transcription... (please wait ⏳)")
        model = whisper.load_model("base")
        result = model.transcribe(audio_path, language="en", task="transcribe")
        return result['text']
    except Exception as e:
        st.error(f"❌ Error during English transcription: {e}")
        return None

# Convert transcription to SRT format
def convert_to_srt(transcription_text):
    try:
        words = transcription_text.split()
        avg_words_per_line = 8
        subtitles = []
        for i in range(0, len(words), avg_words_per_line):
            line_words = words[i:i+avg_words_per_line]
            start_time = i // avg_words_per_line * 5
            end_time = start_time + 5
            subtitle = srt.Subtitle(
                index=(i // avg_words_per_line) + 1,
                start=timedelta(seconds=start_time),
                end=timedelta(seconds=end_time),
                content=" ".join(line_words)
            )
            subtitles.append(subtitle)
        return srt.compose(subtitles)
    except Exception as e:
        st.error(f"❌ Error generating SRT: {e}")
        return None

# Burn subtitles into video
def burn_subtitles(video_path, srt_path, output_path):
    try:
        video_full = os.path.abspath(video_path)
        srt_fixed = os.path.abspath(srt_path).replace("\\", "/")
        output_full = os.path.abspath(output_path)
        command = f'ffmpeg -y -i "{video_full}" -vf "subtitles={srt_fixed}" "{output_full}"'
        subprocess.run(command, shell=True, check=True)
        return output_full
    except subprocess.CalledProcessError as e:
        st.error(f"❌ Error burning subtitles: {e}")
        return None

# Streamlit App
def main():
    st.title("🎥 AI Subtitle Generator: Hindi & English Modes")
    st.markdown(
        """
        👋 **Welcome to the Subtitle Generator App!**  
        📌 Upload your video and choose a mode to generate and embed subtitles.  
        🕒 *Note: Hindi Mode uses Whisper-large for better accuracy and may take more time to process.*  
        """
    )

    uploaded_video = st.file_uploader("📤 **Upload a video file**", type=["mp4", "mov", "avi", "mkv"])

    language_mode = st.radio(
        "🌐 **Choose Language Mode:**",
        ("Hindi Mode 🎙️ (high accuracy)", "English Mode 📝 (faster)")
    )

    if uploaded_video is not None:
        with open("temp_video.mp4", "wb") as f:
            f.write(uploaded_video.read())
        st.video("temp_video.mp4")

        if st.button("🚀 **Start Processing**"):
            audio_path = "temp_audio.wav"
            srt_path = "output.srt"
            output_video = "output_video.mp4"

            # Step 1: Extract audio
            st.info("🔊 Extracting audio from video...")
            audio_file = extract_audio("temp_video.mp4", audio_path)
            if not audio_file:
                return

            # Allow user to download raw audio
            with open(audio_path, "rb") as f:
                st.download_button(
                    label="🎧 Download Extracted Audio",
                    data=f,
                    file_name="extracted_audio.wav",
                    mime="audio/wav"
                )

            # Step 2: Transcription
            if language_mode.startswith("Hindi"):
                transcription_text = transcribe_audio_hindi(audio_file)
            else:
                transcription_text = transcribe_audio_english(audio_file)

            if not transcription_text:
                st.error("❌ Transcription failed.")
                return

            # Step 3: Generate SRT
            st.info("📜 Generating SRT file...")
            srt_content = convert_to_srt(transcription_text)
            if srt_content:
                with open(srt_path, "w", encoding="utf-8") as f:
                    f.write(srt_content)
                st.success("✅ SRT file generated successfully!")

                # Allow user to download SRT file
                with open(srt_path, "rb") as f:
                    st.download_button(
                        label="📝 Download SRT File",
                        data=f,
                        file_name="captions.srt",
                        mime="text/plain"
                    )

            # Step 4: Burn subtitles into video
            st.info("🔥 Embedding subtitles into video... (this may take time ⏳)")
            final_video = burn_subtitles("temp_video.mp4", srt_path, output_video)
            if final_video:
                st.success("🎉 Video with subtitles is ready!")
                st.video(final_video)
                with open(final_video, "rb") as f:
                    st.download_button(
                        label="📥 Download Final Video",
                        data=f,
                        file_name="video_with_subtitles.mp4",
                        mime="video/mp4"
                    )

if __name__ == "__main__":
    main()
