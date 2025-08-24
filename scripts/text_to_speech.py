from gtts import gTTS
import os
from datetime import datetime

def make_voice(text):
    # Define the directory where the audio will be saved
    audio_dir = "assets/audio"

    # Ensure the directory exists. Create it if it doesn't.
    os.makedirs(audio_dir, exist_ok=True)

    # Create the filename and the full path
    filename = f"audio_{datetime.now().date()}.mp3"
    path = os.path.join(audio_dir, filename)

    # Generate and save the speech file
    speech = gTTS(text=text, lang='en', slow=False)
    speech.save(path)
    
    return path