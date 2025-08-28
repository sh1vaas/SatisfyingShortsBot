# scripts/create_video.py

import os
import ffmpeg
from datetime import datetime

def create_video(video_paths, audio_path, total_duration=15):
    """
    Trims, combines two videos, and overlays looped audio to create a 15-second Short.
    """
    output_dir = "output"
    os.makedirs(output_dir, exist_ok=True)
    out_file = os.path.join(output_dir, f"short_{datetime.now().strftime('%Y-%m-%d_%H-%M-%S')}.mp4")

    # Calculate duration for each clip
    clip_duration = total_duration / len(video_paths)

    # Process each video clip: trim, set timestamp, and scale to a consistent size
    input_clips = []
    for path in video_paths:
        clip = (
            ffmpeg.input(path)
            .trim(duration=clip_duration)
            .setpts('PTS-STARTPTS')
            .filter('scale', '720', '1280') # Standard portrait size for consistency
        )
        input_clips.append(clip)

    # Concatenate (stitch) the video streams together
    concatenated_video = ffmpeg.concat(*input_clips, v=1, a=0)

    # Loop the AI-generated voiceover
    input_audio = ffmpeg.input(audio_path).filter('aloop', loop=-1, size=2**24)

    # Combine the final stitched video with the looped audio and set the exact duration
    ffmpeg.output(
        concatenated_video,
        input_audio,
        out_file,
        vcodec='libx264',
        acodec='aac',
        t=total_duration  # Enforce the final duration (e.g., 15 seconds)
    ).run(overwrite_output=True)
        
    return out_file