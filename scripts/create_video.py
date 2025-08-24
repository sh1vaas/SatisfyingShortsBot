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
    out_file = f"output/short_{datetime.now().date()}.mp4"

    input_video = ffmpeg.input(background_path)
    if audio:
        input_audio = ffmpeg.input(audio)
        ffmpeg.output(input_video, input_audio, out_file, shortest=None, vcodec='libx264').run(overwrite_output=True)
    else:
        ffmpeg.output(input_video, out_file).run(overwrite_output=True)
    return out_file