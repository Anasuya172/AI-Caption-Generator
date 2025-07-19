import subprocess
import os
import platform

def burn_subtitles(video_path, srt_path, output_path, overwrite=True):
    """
    Burn subtitles from SRT into the video using FFmpeg.
    
    Args:
        video_path (str): Path to the input video file.
        srt_path (str): Path to the subtitle (SRT) file.
        output_path (str): Path to save the output video with subtitles.
        overwrite (bool): Whether to overwrite the output file if it exists.
        
    Returns:
        str: Path to the output video if successful, None otherwise.
    """
    try:
        # Resolve full paths and fix slashes
        video_full = os.path.abspath(video_path).replace("\\", "/")
        srt_full = os.path.abspath(srt_path).replace("\\", "/").replace(":", "\\:")  # Escape colon
        output_full = os.path.abspath(output_path).replace("\\", "/")

        # Detect OS and locate ffmpeg binary
        if platform.system() == "Windows":
            ffmpeg_cmd = os.path.join(
                r"C:\ffmpeg-2025-07-17-git-bc8d06d541-essentials_build\bin",
                "ffmpeg.exe"
            )
        else:
            ffmpeg_cmd = "ffmpeg"  # On Linux/Streamlit Cloud

        # Overwrite or not
        overwrite_flag = "-y" if overwrite else "-n"

        # FFmpeg command with styling for subtitles
        command = (
            f'"{ffmpeg_cmd}" {overwrite_flag} -i "{video_full}" '
            f'-vf "subtitles=\'{srt_full}\':force_style=\'FontName=Arial,FontSize=20\'" '
            f'"{output_full}"'
        )

        print("⚙️ Running FFmpeg command:")
        print(command)

        # Run the command
        subprocess.run(command, shell=True, check=True)
        print(f"✅ The video with burned-in subtitles was created: {output_full}")
        return output_full

    except subprocess.CalledProcessError as e:
        print(f"❌ Error occurred while burning subtitles:\n{e}")
        return None

if __name__ == "__main__":
    # Example usage (for testing outside Streamlit)
    video_file = "temp_video.mp4"
    subtitle_file = "output.srt"
    output_file = "final_video.mp4"
    burn_subtitles(video_file, subtitle_file, output_file, overwrite=True)
