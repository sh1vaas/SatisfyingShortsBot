# scripts/text_to_speech.py

from gtts import gTTS
import os
from datetime import datetime

def make_voice(text):
    audio_dir = "assets/audio"
    os.makedirs(audio_dir, exist_ok=True)

    filename = f"audio_{datetime.now().strftime('%Y-%m-%d_%H-%M-%S')}.mp3"
    path = os.path.join(audio_dir, filename)

    speech = gTTS(text=text, lang='en', slow=False)
    speech.save(path)
    
    return path