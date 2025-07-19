from moviepy.editor import VideoFileClip
import os
def extract_audio(video_path,audio_path):
    try:
        video=VideoFileClip(video_path)
        audio=video.audio
        if audio:
            audio.write_audiofile(audio_path)
            print(f"Audio extracted successfully: {audio_path}")
        else:
            print("No audio found in the video")
    except Exception as e :
        print(f"An error occurred: {e}")
if __name__=="__main__":
    video_file="video\sample.vedio.mp4"
    audio_output="audio\sample_audio.wav"
    os.makedirs(os.path.dirname(audio_output),exist_ok=True)

    extract_audio(video_file,audio_output)