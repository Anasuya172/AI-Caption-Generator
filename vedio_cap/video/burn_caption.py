import subprocess
import os

def burn_subtitles(video_path, srt_relative, output_path, overwrite=True):
    """
    Burns subtitles into a video file using FFmpeg.
    Works both locally and on Streamlit Cloud.
    """
    # Get absolute paths
    video_full = os.path.abspath(video_path)
    srt_full = os.path.abspath(srt_relative)
    output_full = os.path.abspath(output_path)

    # Replace backslashes for FFmpeg (important for Windows/Cloud)
    video_fixed = video_full.replace("\\", "/")
    srt_fixed = srt_full.replace("\\", "/")
    output_fixed = output_full.replace("\\", "/")

    # Add overwrite flag
    overwrite_flag = "-y" if overwrite else "-n"

    # FFmpeg command
    command = (
        f'ffmpeg {overwrite_flag} -i "{video_fixed}" '
        f'-vf "subtitles={srt_fixed}:force_style=\'FontName=Arial,FontSize=20\'" '
        f'"{output_fixed}"'
    )

    print("Running FFmpeg command:")
    print(command)

    try:
        subprocess.run(command, shell=True, check=True)
        print(f"✅ Video created: {output_full}")
        return output_full
    except subprocess.CalledProcessError as e:
        print(f"❌ FFmpeg failed:\n{e}")
        return None
