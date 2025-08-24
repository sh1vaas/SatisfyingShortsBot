import os
import requests
from dotenv import load_dotenv

load_dotenv()
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

def generate_prompt():
    prompt = "Give me a satisfying idea for YouTube Shorts. Example: jelly cutting, soap carving, bottle breaking, etc."

    if not GEMINI_API_KEY:  # Check again for Render deployment
        print("⚠️ GEMINI_API_KEY not found. Check Render environment variables.")
        return None

    headers = {
       "Content-Type": "application/json"
    }

    try:
        response = requests.post(
            "https://generativelanguage.googleapis.com/v1beta2/models/text-bison-001:generateText",  # Check correct endpoint
            headers=headers,
            params={"key": GEMINI_API_KEY},
            json={
              "prompt": {
                "text": prompt
              },
              "temperature": 0.7 # Example setting
            }
        )
        response.raise_for_status()  # Raise HTTPError for bad responses (4xx or 5xx)

        data = response.json()

        # For debugging: print the whole JSON response
        print("Gemini Response:", json.dumps(data, indent=2))

        # Handle different Gemini response formats
        if "candidates" in data:
            idea = data["candidates"][0]["content"]["parts"][0]["text"]
        elif "results" in data:
            idea = data["results"][0]["text"]
        else:
            print("❌ Unexpected API response format:")
            print(json.dumps(data, indent=2))
            return None

        print("✅ Idea:", idea)
        return idea.strip()

    except requests.exceptions.RequestException as e:
        print(f"❌ API Request Error: {e}")
        return None
    except (KeyError, IndexError) as e:
        print(f"❌ JSON Parsing Error: {e}")
        print("Response:", response.text) # examine full response
        return None