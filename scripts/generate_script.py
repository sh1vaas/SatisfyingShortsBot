# scripts/generate_script.py

import os
import requests
import json
import random
from dotenv import load_dotenv

load_dotenv()
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

def generate_content():
    theme = random.choice(["Nature", "Space"])
    print(f"🧠 Chosen Theme for the day: {theme}")

    prompt = f"""
    You are an expert YouTube SEO content strategist. Your task is to generate a viral content package for a YouTube Short about the theme '{theme}'.
    Provide the output in a clean JSON format with three keys: "search_query", "title", and "description".

    1.  "search_query": A simple, 2-3 word search term for Pexels (video) and Pixabay (music) APIs. It should be evocative and specific.
        - For Nature, examples: 'forest waterfall', 'ocean waves', 'mountain sunrise'.
        - For Space, examples: 'starry night sky', 'milky way galaxy', 'planet earth'.

    2.  "title": A short, viral, SEO-optimized title for a YouTube Short (under 70 characters).
        - For Nature, examples: 'The Most Peaceful Place on Earth 🌲✨', 'Is This Planet Earth?! 🤯', 'Wait for the view... 🏔️'.
        - For Space, examples: 'This is What Space Sounds Like 🚀', 'Feeling Small Yet? 🌌', 'Our Universe is STUNNING ✨'.

    3.  "description": A short, engaging, SEO-optimized description (2-3 sentences). Include 3-4 relevant hashtags at the end.
        - Example Description: "Take a moment to breathe and witness the incredible beauty of our universe. What's your favorite thing about space? #Space #Universe #Galaxy #Stars"
    """
    if not GEMINI_API_KEY:
        print("⚠️ GEMINI_API_KEY not found.")
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
        idea_text = data["candidates"][0]["content"]["parts"][0]["text"]
        
        clean_text = idea_text.strip().replace("```json", "").replace("```", "")
        content_data = json.loads(clean_text)
        
        print("✅ Content package generated successfully.")
        return content_data

    except (requests.exceptions.RequestException, KeyError, IndexError, json.JSONDecodeError) as e:
        print(f"❌ Error generating or parsing content: {e}")
        return None