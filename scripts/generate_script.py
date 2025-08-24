import os
import requests
import json
from dotenv import load_dotenv

load_dotenv()
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

def generate_prompt():
    prompt = "Give me a satisfying idea for YouTube Shorts. Example: jelly cutting, soap carving, bottle breaking, etc."

    if not GEMINI_API_KEY:
        print("⚠️ GEMINI_API_KEY not found. Ensure it is set in your environment variables.")
        return None

    headers = {"Content-Type": "application/json"}
    api_url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-pro:generateContent?key={GEMINI_API_KEY}"

    try:
        response = requests.post(
            api_url,
            headers=headers,
            json={"contents": [{"parts": [{"text": prompt}]}]}
        )
        response.raise_for_status()  # Raise HTTPError for bad responses (4xx or 5xx)

        data = response.json()
        
        # Extract text from the new Gemini API format
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