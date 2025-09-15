# scripts/create_video.py

import os
import ffmpeg
from datetime import datetime

def create_video(video_paths, audio_path):
    """
    Trims, combines two videos, and overlays the audio track, ensuring the
    final output is exactly 15 seconds long.
    """
    output_dir = "output"
    os.makedirs(output_dir, exist_ok=True)
    out_file = os.path.join(output_dir, f"short_{datetime.now().strftime('%Y-%m-%d_%H-%M-%S')}.mp4")

    total_duration = 15
    clip_duration = total_duration / len(video_paths)

    # Process and concatenate video clips
    input_clips = []
    for path in video_paths:
        clip = (
            ffmpeg.input(path)
            .trim(duration=clip_duration)
            .setpts('PTS-STARTPTS')
            .filter('scale', '720', '1280') # Standardize resolution
            .filter('setsar', '1')          # THE FIX: Standardize pixel aspect ratio
        )
        input_clips.append(clip)
    concatenated_video = ffmpeg.concat(*input_clips, v=1, a=0)

    # Input the full-length audio
    input_audio = ffmpeg.input(audio_path)

    # Combine video and audio, and explicitly set the final duration.
    ffmpeg.output(
        concatenated_video,
        input_audio,
        filename=out_file,
        vcodec='libx264',
        acodec='aac',
        t=total_duration
    ).run(overwrite_output=True)
        
    return out_file