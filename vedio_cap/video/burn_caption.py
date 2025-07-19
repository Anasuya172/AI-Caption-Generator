import subprocess
import os

def burn_subtitles(video_path, srt_relative, output_path, ffmpeg_path=None, overwrite=True):
    """
    Burns subtitles into a video file using FFmpeg.
    
    Args:
        video_path (str): Path to the input video.
        srt_relative (str): Path to the SRT subtitles file.
        output_path (str): Path where the output video will be saved.
        ffmpeg_path (str, optional): Path to FFmpeg folder (only needed for Windows).
        overwrite (bool): Whether to overwrite the output file if it exists.
    
    Returns:
        str: Path to the generated video or None if error.
    """
    # Get absolute paths
    video_full = os.path.abspath(video_path)
    output_full = os.path.abspath(output_path)

    # Fix path separators for Linux/Windows
    srt_fixed = srt_relative.replace("\\", "/")
    video_fixed = video_full.replace("\\", "/")
    output_fixed = output_full.replace("\\", "/")

    # Detect OS and set ffmpeg command
    if os.name == "nt":  # Windows
        if ffmpeg_path:
            ffmpeg_exe = os.path.join(ffmpeg_path, "ffmpeg.exe")
        else:
            ffmpeg_exe = "ffmpeg.exe"
    else:  # Linux/Mac (Streamlit Cloud)
        ffmpeg_exe = "ffmpeg"

    # Overwrite flag
    overwrite_flag = "-y" if overwrite else "-n"

    # FFmpeg command with font handling for subtitles
    command = (
        f'"{ffmpeg_exe}" {overwrite_flag} -i "{video_fixed}" '
        f'-vf "subtitles={srt_fixed}:force_style=\'FontName=Arial,FontSize=20\'" '
        f'"{output_fixed}"'
    )

    print("Running command:")
    print(command)

    try:
        subprocess.run(command, shell=True, check=True)
        print(f"✅ Video with burned-in captions generated: {output_full}")
        return output_full
    except subprocess.CalledProcessError as e:
        print(f"❌ Error occurred while burning subtitles into video:\n{e}")
        return None
