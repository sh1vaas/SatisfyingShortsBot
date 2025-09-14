# scripts/fetch_video.py

import os
import requests
import random
from dotenv import load_dotenv

load_dotenv()
PEXELS_API_KEY = os.getenv("PEXELS_API_KEY")

def get_used_video_ids():
    """Reads the list of previously used Pexels video IDs from the log file."""
    try:
        with open("used_videos.log", "r") as f:
            return [line.strip() for line in f]
    except FileNotFoundError:
        return []

def get_pexels_videos(query):
    if not PEXELS_API_KEY:
        print("⚠️ PEXELS_API_KEY not found.")
        return None

    used_ids = get_used_video_ids()
    headers = {"Authorization": PEXELS_API_KEY}
    params = {"query": query, "orientation": "portrait", "per_page": 80}
    api_url = "https://api.pexels.com/videos/search"
    
    try:
        response = requests.get(api_url, headers=headers, params=params)
        response.raise_for_status()
        
        all_videos = response.json().get("videos", [])
        # Filter out videos that have already been used
        fresh_videos = [v for v in all_videos if str(v['id']) not in used_ids]
        
        if len(fresh_videos) < 2:
            print(f"❌ Not enough fresh (unused) videos found for query '{query}'.")
            return None

        video_selection = random.sample(fresh_videos, 2)
        downloaded_videos = []
        
        for i, video_data in enumerate(video_selection):
            # ... (The rest of the downloading logic is the same) ...
            photographer_name = video_data.get("user", {}).get("name")
            video_id = video_data.get("id") # Get the video ID to log it later
            video_url = None
            
            for file in video_data.get("video_files", []):
                if file.get("quality") == "hd" and file.get("width") == 1080:
                    video_url = file.get("link")
                    break
            
            if not video_url and video_data.get("video_files"):
                video_url = video_data["video_files"][0].get("link")
            
            if not video_url: continue
            
            print(f"⬇️ Downloading video {i+1}/2 from Pexels (ID: {video_id})...")
            video_response = requests.get(video_url)
            video_response.raise_for_status()
            
            output_dir = "output"
            os.makedirs(output_dir, exist_ok=True)
            video_path = os.path.join(output_dir, f"background_{i+1}.mp4")
            
            with open(video_path, "wb") as f:
                f.write(video_response.content)
            
            downloaded_videos.append({"path": video_path, "photographer": photographer_name, "id": str(video_id)})
            
        if len(downloaded_videos) < 2:
            print("❌ Failed to download two separate videos.")
            return None
            
        print("✅ Two background videos downloaded successfully.")
        return downloaded_videos
        
    except requests.exceptions.RequestException as e:
        print(f"❌ Error fetching videos from Pexels: {e}")
        return None