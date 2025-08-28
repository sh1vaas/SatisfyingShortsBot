# scripts/create_video.py

import os
import ffmpeg
from datetime import datetime

def create_video(video_paths, music_path, total_duration=15):
    output_dir = "output"
    os.makedirs(output_dir, exist_ok=True)
    out_file = os.path.join(output_dir, f"short_{datetime.now().strftime('%Y-%m-%d_%H-%M-%S')}.mp4")

    clip_duration = total_duration / len(video_paths)

    input_clips = []
    for path in video_paths:
        clip = (
            ffmpeg.input(path)
            .trim(duration=clip_duration)
            .setpts('PTS-STARTPTS')
            .filter('scale', '720', '1280')
        )
        input_clips.append(clip)

    concatenated_video = ffmpeg.concat(*input_clips, v=1, a=0)
    input_music = ffmpeg.input(music_path)

    # Combine the final stitched video with the music and set the exact duration
    # The audio will be cut to match the video's total duration
    ffmpeg.output(
        concatenated_video,
        input_music,
        out_file,
        vcodec='libx264',
        acodec='aac',
        t=total_duration
    ).run(overwrite_output=True)
        
    return out_file