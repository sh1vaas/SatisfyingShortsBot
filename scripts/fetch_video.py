# scripts/fetch_video.py

import os
import requests
import random
from dotenv import load_dotenv

load_dotenv()
PEXELS_API_KEY = os.getenv("PEXELS_API_KEY")

def get_pexels_video(query):
    if not PEXELS_API_KEY:
        print("⚠️ PEXELS_API_KEY not found.")
        return None

    headers = {"Authorization": PEXELS_API_KEY}
    params = {
        "query": query,
        "orientation": "portrait",
        "per_page": 15,
        "min_duration": 15
    }
    api_url = "https://api.pexels.com/videos/search"
    
    try:
        response = requests.get(api_url, headers=headers, params=params)
        response.raise_for_status()
        
        videos = response.json().get("videos", [])
        if not videos:
            print(f"❌ No videos found for query '{query}' with a minimum duration of 15 seconds.")
            print("Trying again without duration filter...")
            del params["min_duration"]
            response = requests.get(api_url, headers=headers, params=params)
            videos = response.json().get("videos", [])
            if not videos:
                 print(f"❌ Still no videos found for query: {query}")
                 return None

        video_data = random.choice(videos)
        photographer_name = video_data.get("user", {}).get("name")
        video_url = None
        
        for file in video_data.get("video_files", []):
            if file.get("quality") == "hd" and file.get("width") == 1080:
                video_url = file.get("link")
                break
        
        if not video_url and video_data.get("video_files"):
            video_url = video_data["video_files"][0].get("link")
        
        if not video_url:
            print("❌ Could not find any video link.")
            return None
            
        print(f"⬇️ Downloading video from Pexels (Duration: {video_data.get('duration')}s)...")
        video_response = requests.get(video_url)
        video_response.raise_for_status()
        
        output_dir = "output"
        os.makedirs(output_dir, exist_ok=True)
        video_path = os.path.join(output_dir, "background.mp4")
        
        with open(video_path, "wb") as f:
            f.write(video_response.content)
            
        print(f"✅ Background video saved to: {video_path}")
        return {"path": video_path, "photographer": photographer_name}
        
    except requests.exceptions.RequestException as e:
        print(f"❌ Error fetching video from Pexels: {e}")
        return None