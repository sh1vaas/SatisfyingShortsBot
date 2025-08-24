import os
import requests
import json
from dotenv import load_dotenv

load_dotenv()
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

def generate_prompt():
    # UPDATED: This new prompt asks for a general quote or message for any type of video.
    prompt = "Generate a short, captivating piece of text for a YouTube Short voiceover. It can be a thought-provoking quote, a deep question, or a brief, inspiring message. The tone should be calm, motivational, or mysterious. The text must be very general so it can be paired with any random video clip (nature, space, weather, etc.). Example: 'Find the beauty in the small moments; they are what make a life.'"

    if not GEMINI_API_KEY:
        print("⚠️ GEMINI_API_KEY not found. Ensure it is set in your environment variables.")
        return None

    headers = {"Content-Type": "application/json"}
    
    api_url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash-latest:generateContent?key={GEMINI_API_KEY}"

    try:
        response = requests.post(
            api_url,
            headers=headers,
            json={"contents": [{"parts": [{"text": prompt}]}]}
        )
        response.raise_for_status()

        data = response.json()
        
        idea = data["candidates"][0]["content"]["parts"][0]["text"]
        
        print("✅ Idea:", idea)
        return idea.strip()

    except requests.exceptions.RequestException as e:
        print(f"❌ API Request Error: {e}")
        return None
    except (KeyError, IndexError) as e:
        print(f"❌ JSON Parsing Error: {e}")
        print("Response received from API:", json.dumps(data, indent=2))
        return None