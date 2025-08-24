# scripts/upload.py

import os
import json
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload


def upload_video(video_path, title, description):
    print("🎬 Starting upload to YouTube...")

    # Load YouTube OAuth client secret from environment variable
    client_secret_raw = os.getenv("CLIENT_SECRET")
    if not client_secret_raw:
        raise RuntimeError("❌ CLIENT_SECRET environment variable not found.")

    # Save environment JSON string to a temporary file
    temp_secret_filename = "temp_client_secret.json"
    with open(temp_secret_filename, "w") as f:
        f.write(client_secret_raw)

    # Define API scopes
    SCOPES = ["https://www.googleapis.com/auth/youtube.upload"]

    # Start OAuth flow
    flow = InstalledAppFlow.from_client_secrets_file(temp_secret_filename, SCOPES)
    credentials = flow.run_local_server(port=8080)

    youtube = build("youtube", "v3", credentials=credentials)
    print("✅ Authentication successful.")

    # Create video metadata
    request_body = {
        "snippet": {
            "title": title,
            "description": description,
            "tags": ["shorts", "satisfying", "relaxing"],
            "categoryId": "22"  # People & Blogs
        },
        "status": {
            "privacyStatus": "public",  # or "unlisted"/"private"
            "selfDeclaredMadeForKids": False
        }
    }

    # Prepare the actual file to upload
    media = MediaFileUpload(video_path, mimetype="video/mp4", resumable=True)

    # Upload the video
    print("⬆️ Uploading video:", video_path)
    request = youtube.videos().insert(
        part="snippet,status",
        body=request_body,
        media_body=media
    )

    response = request.execute()

    # Clean up temp file
    os.remove(temp_secret_filename)

    # Output uploaded video details
    video_id = response.get("id")
    print(f"🎉 Video uploaded successfully!")
    print(f"▶️ Watch here: https://www.youtube.com/watch?v={video_id}")