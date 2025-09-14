# main.py

import os
from scripts.generate_script import generate_content
from scripts.text_to_speech import make_voice # <-- Re-added import
from scripts.fetch_video import get_pexels_videos
from scripts.create_video import create_video
from scripts.upload import upload_video

def run_bot():
    print("🎯 STARTING AI VIDEO BOT PROCESS")

    # STEP 1: Generate the full content package
    content = generate_content()
    if not content:
        print("❌ Content generation failed. Stopping.")
        return
        
    search_query = content['search_query']
    video_title = content['title']
    video_description = content['description']
    spoken_text = content['spoken_text'] # <-- Using the new long script

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

    # STEP 3: Generate TTS audio from the long script
    print("🎙️ Generating full-length TTS voice...")
    audio_path = make_voice(spoken_text)
    if not audio_path:
        print("❌ Audio creation failed. Stopping.")
        return

    # STEP 4: Combine videos and audio
    print("🎬 Combining videos and audio with FFmpeg...")
    try:
        output_video_path = create_video(background_video_paths, audio_path)
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
        if os.path.exists(audio_path):
            os.remove(audio_path)

if __name__ == "__main__":
    run_bot()