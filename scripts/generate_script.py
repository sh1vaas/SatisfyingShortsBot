import os
import requests
from dotenv import load_dotenv

load_dotenv()
API_KEY = os.getenv("GEMINI_API_KEY")

def generate_prompt():
    prompt = "Give me a satisfying short video idea. Examples: bottle breaking in slow motion, jelly cutting, soap carving, paint mixing, etc. Randomize it and keep it under 20 words."

    response = requests.post(
        "https://generativelanguage.googleapis.com/v1beta/models/gemini-pro:generateContent",
        params={"key": API_KEY},
        json={"contents": [{"parts": [{"text": prompt}]}]}
    )
    idea = response.json()["candidates"][0]["content"]["parts"][0]["text"]
    return idea.strip()

if __name__ == "__main__":
    idea = generate_prompt()
    print("Today's idea:", idea)