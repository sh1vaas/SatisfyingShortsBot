# main.py

import os
from scripts.generate_script import generate_content
from scripts.fetch_video import get_pexels_videos
from scripts.fetch_music import get_pixabay_music # <-- New import
from scripts.create_video import create_video
from scripts.upload import upload_video

def run_bot():
    print("🎯 STARTING AI VIDEO BOT PROCESS")

    # STEP 1: Generate the content package (query, title, desc)
    content = generate_content()
    if not content:
        print("❌ Content generation failed. Stopping.")
        return
        
    search_query = content['search_query']
    video_title = content['title']
    video_description = content['description']

    # STEP 2: Fetch TWO background videos from Pexels
    print(f"🎞️ Fetching 2 videos for '{search_query}' from Pexels...")
    video_info_list = get_pexels_videos(search_query)
    if not video_info_list:
        print("❌ Video fetching failed. Stopping.")
        return
    
    background_video_paths = [info["path"] for info in video_info_list]
    photographers = [info["photographer"] for info in video_info_list]
    photographer_credit = " & ".join(filter(None, photographers))
    full_description = f"{video_description}\n\nVideos by {photographer_credit} from Pexels."

    # STEP 3: Fetch background music from Pixabay
    print(f"🎵 Fetching music for '{search_query}' from Pixabay...")
    music_path = get_pixabay_music(search_query)
    if not music_path:
        print("❌ Music fetching failed. Stopping.")
        return

    # STEP 4: Combine videos and music
    print("🎬 Combining videos and music with FFmpeg...")
    try:
        output_video_path = create_video(background_video_paths, music_path)
        print(f"✅ Final video created: {output_video_path}")
    except Exception as e:
        print(f"❌ Video creation failed: {e}")
        return

    # STEP 5: Upload to YouTube
    print("📤 Uploading to YouTube...")
    try:
        upload_video(output_video_path, video_title, full_description)
    except Exception as e:
        print(f"❌ Upload failed: {e}")
    finally:
        # STEP 6: Clean up temporary files
        print("🗑️ Cleaning up temporary files...")
        for path in background_video_paths:
            if os.path.exists(path):
                os.remove(path)
        if os.path.exists(music_path):
            os.remove(music_path)

if __name__ == "__main__":
    run_bot()