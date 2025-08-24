# main.py
from scripts.generate_script import generate_prompt
from scripts.text_to_speech import make_voice
from scripts.create_video import create_video
from scripts.upload import upload_video

from datetime import date
import os

def run_bot():
    print("🎯 Starting AI YouTube Shorts Bot")

    # Step 1: Generate script idea
    prompt = generate_prompt()
    print("✅ Prompt:", prompt)

    # Step 2: Create voice (optional)
    audio_path = make_voice(prompt)

    # Step 3: Generate video
    final_video = create_video(audio_path)

    # Step 4: Upload
    title = f"Satisfying Short – {date.today().strftime('%B %d, %Y')}"
    description = f"Automatically generated and uploaded satisfying video.\n\nPrompt: {prompt}"
    
    upload_video(final_video, title, description)

    print("✅ Upload complete, check your YouTube channel!")

if __name__ == "__main__":
    run_bot()