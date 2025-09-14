# main.py

import os
from scripts.generate_script import generate_content
from scripts.text_to_speech import make_voice
from scripts.fetch_video import get_pexels_videos
from scripts.create_video import create_video
from scripts.upload import upload_video

def log_used_content(spoken_text, video_ids):
    """Appends used content to the log files."""
    with open("used_prompts.log", "a", encoding="utf-8") as f:
        f.write(spoken_text + "\n")
    with open("used_videos.log", "a") as f:
        for video_id in video_ids:
            f.write(video_id + "\n")
    print("✅ Content logged successfully.")

def run_bot():
    print("🎯 STARTING AI VIDEO BOT PROCESS")
    
    # ... (Step 1: Generate Content is the same) ...
    content = generate_content()
    if not content: return
    search_query = content['search_query']
    video_title = content['title']
    video_description = content['description']
    spoken_text = content['spoken_text']

    # ... (Step 2: Fetch Videos is the same) ...
    video_info_list = get_pexels_videos(search_query)
    if not video_info_list: return
    
    background_video_paths = [info["path"] for info in video_info_list]
    video_ids_to_log = [info["id"] for info in video_info_list] # Get IDs for logging
    photographers = [info["photographer"] for info in video_info_list]
    photographer_credit = " & ".join(filter(None, photographers))
    full_description = f"{video_description}\n\nVideos by {photographer_credit} from Pexels."

    # ... (Step 3: Generate Audio is the same) ...
    audio_path = make_voice(spoken_text)
    if not audio_path: return

    # ... (Step 4: Combine Video/Audio is the same) ...
    try:
        output_video_path = create_video(background_video_paths, audio_path)
    except Exception as e:
        print(f"❌ Video creation failed: {e}")
        return

    # ... (Step 5: Upload to YouTube) ...
    try:
        upload_video(output_video_path, video_title, full_description)
        # Log content ONLY after a successful upload
        log_used_content(spoken_text, video_ids_to_log)
    except Exception as e:
        print(f"❌ Upload failed: {e}")
    finally:
        # ... (Step 6: Cleanup is the same) ...
        print("🗑️ Cleaning up temporary files...")
        for path in background_video_paths:
            if os.path.exists(path): os.remove(path)
        if os.path.exists(audio_path): os.remove(audio_path)
        if os.path.exists(output_video_path): os.remove(output_video_path)


if __name__ == "__main__":
    run_bot()