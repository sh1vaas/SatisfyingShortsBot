# scripts/upload.py
import os
import json
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build

def get_youtube_client():
    # Get client secret from environment
    client_secret_str = os.getenv("CLIENT_SECRET")
    
    if not client_secret_str:
        raise ValueError("CLIENT_SECRET environment variable not found!")

    # Write to temporary file (required by Google OAuth)
    with open("temp_client_secret.json", "w") as f:
        f.write(client_secret_str)

    # Initialize YouTube client
    flow = InstalledAppFlow.from_client_secrets_file(
        "temp_client_secret.json", 
        ["https://www.googleapis.com/auth/youtube.upload"]
    )
    credentials = flow.run_local_server(port=8080)
    
    # Clean up temporary file
    os.remove("temp_client_secret.json")
    
    return build("youtube", "v3", credentials=credentials)