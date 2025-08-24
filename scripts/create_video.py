import os
import ffmpeg
import random
from datetime import datetime

def create_video(audio=None):
    bg_folder = "assets/backgrounds/"
    background = random.choice([
        f for f in os.listdir(bg_folder) if f.endswith(".mp4")
    ])
    background_path = os.path.join(bg_folder, background)

    # Define the output directory
    output_dir = "output"
    # Ensure the output directory exists before saving the file
    os.makedirs(output_dir, exist_ok=True)

    # Define the full path for the output file
    out_file = os.path.join(output_dir, f"short_{datetime.now().date()}.mp4")

    input_video = ffmpeg.input(background_path)
    
    if audio:
        input_audio = ffmpeg.input(audio)
        # Combine video and audio
        ffmpeg.output(input_video, input_audio, out_file, vcodec='libx264', acodec='aac', shortest=None).run(overwrite_output=True)
    else:
        # Just process the video
        ffmpeg.output(input_video, out_file).run(overwrite_output=True)
        
    return out_file