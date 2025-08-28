# scripts/create_video.py

import os
import ffmpeg
from datetime import datetime

def create_video(video_path, audio_path):
    output_dir = "output"
    os.makedirs(output_dir, exist_ok=True)
    out_file = os.path.join(output_dir, f"short_{datetime.now().strftime('%Y-%m-%d_%H-%M-%S')}.mp4")

    input_video = ffmpeg.input(video_path)
    input_audio = ffmpeg.input(audio_path)
    
    ffmpeg.output(input_video, input_audio, out_file, vcodec='libx264', acodec='aac', shortest=None).run(overwrite_output=True)
        
    return out_file