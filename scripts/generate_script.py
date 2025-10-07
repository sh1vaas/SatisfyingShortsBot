# scripts/generate_script.py

import os
import requests
import json
import random
from dotenv import load_dotenv

load_dotenv()
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

def get_used_prompts():
    """Reads the list of previously used prompts from the log file."""
    try:
        with open("used_prompts.log", "r", encoding="utf-8") as f:
            return f.read().splitlines()[-50:]
    except FileNotFoundError:
        return []

def generate_content():
    theme = random.choice(["Nature", "Space"])
    print(f"🧠 Chosen Theme for the day: {theme}")
    
    used_prompts = get_used_prompts()
    avoidance_instruction = ""
    if used_prompts:
        avoidance_instruction = "Crucially, the 'spoken_text' MUST be unique and not similar to any of these previously used texts:\n" + "\n".join(used_prompts)

    prompt = f"""
    You are an expert YouTube SEO content strategist. Your task is to generate a viral content package for a 15-second YouTube Short about the theme '{theme}'.
    Provide the output in a clean JSON format with four keys: "search_query", "title", "description", and "spoken_text".

    1. "search_query": A simple, 2-3 word search term for the Pexels video API.
       - For Nature: 'forest waterfall', 'ocean waves', 'mountain sunrise'.
       - For Space: 'starry night sky', 'milky way galaxy', 'planet earth'.

    2. "title": A short, viral, SEO-optimized title (under 70 characters).
       - For Nature: 'The Most Peaceful Place on Earth 🌲✨', 'Is This Planet Earth?! 🤯'.
       - For Space: 'This is What Space Sounds Like 🚀', 'Feeling Small Yet? 🌌'.

    3. "description": A short, engaging, SEO-optimized description (2-3 sentences). Include 3-4 relevant hashtags.

    4. "spoken_text": A calming or profound script of approximately 35-40 words, lasting about 15 seconds when spoken.

    {avoidance_instruction}
    """
    if not GEMINI_API_KEY:
        print("⚠️ GEMINI_API_KEY not found.")
        return None

    headers = {"Content-Type": "application/json"}
    # THE FIX: Using the v1 stable API with the 'gemini-1.0-pro' model
    api_url = f"https://generativelanguage.googleapis.com/v1/models/gemini-1.0-pro:generateContent?key={GEMINI_API_KEY}"

    try:
        response = requests.post(
            api_url, headers=headers, json={"contents": [{"parts": [{"text": prompt}]}]}
        )
        response.raise_for_status()
        data = response.json()
        idea_text = data["candidates"][0]["content"]["parts"][0]["text"]
        
        clean_text = idea_text.strip().replace("```json", "").replace("```", "")
        content_data = json.loads(clean_text)
        
        print("✅ Content package generated successfully.")
        return content_data

    except Exception as e:
        print(f"❌ Error generating or parsing content: {e}")
        return None