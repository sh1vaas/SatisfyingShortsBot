# scripts/fetch_video.py

import os
import requests
import random
from dotenv import load_dotenv

load_dotenv()
PEXELS_API_KEY = os.getenv("PEXELS_API_KEY")

def get_pexels_videos(query):
    """
    Searches for and downloads TWO unique videos from Pexels.
    Returns a list of dictionaries with local paths and photographer info.
    """
    if not PEXELS_API_KEY:
        print("⚠️ PEXELS_API_KEY not found.")
        return None

    headers = {"Authorization": PEXELS_API_KEY}
    params = {
        "query": query,
        "orientation": "portrait",
        "per_page": 40  # Request more results to ensure variety
    }
    api_url = "https://api.pexels.com/videos/search"
    
    try:
        response = requests.get(api_url, headers=headers, params=params)
        response.raise_for_status()
        
        videos = response.json().get("videos", [])
        if len(videos) < 2:
            print(f"❌ Not enough videos found for query '{query}' to combine two.")
            return None

        # Pick TWO unique random videos from the search results
        video_selection = random.sample(videos, 2)
        downloaded_videos = []
        
        for i, video_data in enumerate(video_selection):
            photographer_name = video_data.get("user", {}).get("name")
            video_url = None
            
            for file in video_data.get("video_files", []):
                if file.get("quality") == "hd" and file.get("width") == 1080:
                    video_url = file.get("link")
                    break
            
            if not video_url and video_data.get("video_files"):
                video_url = video_data["video_files"][0].get("link")
            
            if not video_url:
                print(f"❌ Could not find a video link for one of the selections. Skipping.")
                continue
            
            print(f"⬇️ Downloading video {i+1}/2 from Pexels...")
            video_response = requests.get(video_url)
            video_response.raise_for_status()
            
            output_dir = "output"
            os.makedirs(output_dir, exist_ok=True)
            video_path = os.path.join(output_dir, f"background_{i+1}.mp4")
            
            with open(video_path, "wb") as f:
                f.write(video_response.content)
            
            downloaded_videos.append({"path": video_path, "photographer": photographer_name})
            
        if len(downloaded_videos) < 2:
            print("❌ Failed to download two separate videos.")
            return None
            
        print("✅ Two background videos downloaded successfully.")
        return downloaded_videos
        
    except requests.exceptions.RequestException as e:
        print(f"❌ Error fetching videos from Pexels: {e}")
        return None