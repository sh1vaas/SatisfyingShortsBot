# scripts/fetch_music.py

import os
import requests
import random
from dotenv import load_dotenv

load_dotenv()
PIXABAY_API_KEY = os.getenv("PIXABAY_API_KEY")

def get_pixabay_music(query):
    if not PIXABAY_API_KEY:
        print("⚠️ PIXABAY_API_KEY not found.")
        return None

    api_url = "https://pixabay.com/api/music/"
    params = {
        "key": PIXABAY_API_KEY,
        "q": query,
        "safesearch": "true",
        "editors_choice": "true",
        "per_page": 20
    }

    try:
        response = requests.get(api_url, params=params)
        response.raise_for_status()
        
        tracks = response.json().get("hits", [])
        if not tracks:
            print(f"❌ No music found for query: {query}")
            return None
        
        music_data = random.choice(tracks)
        music_url = music_data.get("downloadURL")
        
        if not music_url:
            print("❌ Music track found, but no download URL was available.")
            return None
            
        print(f"⬇️ Downloading music from Pixabay...")
        music_response = requests.get(music_url)
        music_response.raise_for_status()
        
        output_dir = "output"
        os.makedirs(output_dir, exist_ok=True)
        music_path = os.path.join(output_dir, "background_music.mp3")
        
        with open(music_path, "wb") as f:
            f.write(music_response.content)
            
        print(f"✅ Background music saved to: {music_path}")
        return music_path
        
    except requests.exceptions.RequestException as e:
        print(f"❌ Error fetching music from Pixabay: {e}")
        return None