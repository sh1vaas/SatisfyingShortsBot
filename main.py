# main.py

import os
from scripts.generate_script import generate_content
from scripts.text_to_speech import make_voice
from scripts.fetch_video import get_pexels_video
from scripts.create_video import create_video
from scripts.upload import upload_video

def run_bot():
    print("🎯 STARTING AI VIDEO BOT PROCESS")

    # STEP 1: Generate the full content package (query, title, desc, voiceover)
    content = generate_content()
    if not content:
        print("❌ Content generation failed. Stopping.")
        return
        
    search_query = content['search_query']
    video_title = content['title']
    video_description = content['description']
    spoken_text = content['spoken_text']

    # STEP 2: Fetch background video from Pexels
    print(f"🎞️ Fetching video for '{search_query}' from Pexels...")
    video_info = get_pexels_video(search_query)
    if not video_info:
        print("❌ Video fetching failed. Stopping.")
        return
    
    background_video_path = video_info["path"]
    photographer = video_info["photographer"]
    
    # Add photographer credit to the description
    full_description = f"{video_description}\n\nVideo by {photographer} from Pexels."

    # STEP 3: Generate TTS audio
    print("🎙️ Generating TTS voice...")
    audio_path = make_voice(spoken_text)
    if not audio_path:
        print("❌ Audio creation failed. Stopping.")
        return

    # STEP 4: Combine video and audio
    print("🎬 Combining video and audio with FFmpeg...")
    try:
        output_video_path = create_video(background_video_path, audio_path)
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
        if os.path.exists(background_video_path):
            os.remove(background_video_path)
        if os.path.exists(audio_path):
            os.remove(audio_path)

if __name__ == "__main__":
    run_bot()