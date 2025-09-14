# scripts/text_to_speech.py

from gtts import gTTS
import os
from datetime import datetime

def make_voice(text):
    """
    Converts text to speech and saves it as an MP3 file.
    """
    audio_dir = "output" # Save in output for easier cleanup
    os.makedirs(audio_dir, exist_ok=True)

    # Use a unique timestamp in the filename
    filename = f"audio_{datetime.now().strftime('%Y-%m-%d_%H-%M-%S')}.mp3"
    path = os.path.join(audio_dir, filename)

    try:
        speech = gTTS(text=text, lang='en', slow=False)
        speech.save(path)
        print(f"✅ Audio created: {path}")
        return path
    except Exception as e:
        print(f"❌ gTTS Error: {e}")
        return None