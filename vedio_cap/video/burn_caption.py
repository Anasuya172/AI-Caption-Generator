# 

import subprocess
import os

def burn_subtitles(video_path, srt_relative, output_path, ffmpeg_path, overwrite=True):
    # Get absolute paths for video and output
    video_full = os.path.abspath(video_path)
    output_full = os.path.abspath(output_path)

    # Point directly to ffmpeg.exe
    ffmpeg_exe = os.path.join(ffmpeg_path, "ffmpeg.exe")

    # Fix backslashes for FFmpeg
    srt_fixed = srt_relative.replace("\\", "/")

    # Add -y flag if overwrite, else -n (don’t overwrite)
    overwrite_flag = "-y" if overwrite else "-n"

    # FFmpeg command
    command = f'"{ffmpeg_exe}" {overwrite_flag} -i "{video_full}" -vf "subtitles={srt_fixed}" "{output_full}"'

    print("Running command:")
    print(command)

    try:
        subprocess.run(command, shell=True, check=True)
        print(f"The video with burned-in captions was generated: {output_full}")
        return output_full
    except subprocess.CalledProcessError as e:
        print(f"Error occurred while burning subtitles into video:\n{e}")
        return None
