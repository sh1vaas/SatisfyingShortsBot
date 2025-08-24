from gtts import gTTS
import os
from datetime import datetime

def make_voice(text):
    filename = f"audio_{datetime.now().date()}.mp3"
    path = f"assets/audio/{filename}"
    speech = gTTS(text, lang='en', slow=False)
    speech.save(path)
    return path