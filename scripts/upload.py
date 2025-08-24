# scripts/upload.py

import os
import json
import google.oauth2.credentials
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload

def get_youtube_service():
    """
    Builds the YouTube service object from environment variables.
    This function is designed for a non-interactive server environment.
    """
    # Get credentials from environment variables
    client_secret_json_str = os.getenv("CLIENT_SECRET_JSON")
    token_json_str = os.getenv("GOOGLE_TOKEN_JSON")

    if not client_secret_json_str or not token_json_str:
        raise ValueError("❌ Missing CLIENT_SECRET_JSON or GOOGLE_TOKEN_JSON environment variables.")

    # Load the credentials from the JSON strings
    client_config = json.loads(client_secret_json_str)
    token_info = json.loads(token_json_str)

    # Create credentials object
    credentials = google.oauth2.credentials.Credentials.from_authorized_user_info(
        token_info,
        scopes=["https://www.googleapis.com/auth/youtube.upload"]
    )

    # If the token is expired, refresh it.
    # The client_id, client_secret, and refresh_token are needed for this.
    if credentials.expired and credentials.refresh_token:
        credentials.client_id = client_config["installed"]["client_id"]
        credentials.client_secret = client_config["installed"]["client_secret"]
        # The refresh() method is implicitly called when making an API request if the token is expired.
        # We build the service to ensure the credentials are valid.
    
    return build("youtube", "v3", credentials=credentials)


def upload_video(video_path, title, description):
    print("🎬 Starting upload to YouTube...")

    try:
        youtube = get_youtube_service()
        print("✅ Authentication successful.")

        request_body = {
            "snippet": {
                "title": title,
                "description": description,
                "tags": ["shorts", "satisfying", "relaxing", "ai"],
                "categoryId": "22"  # People & Blogs
            },
            "status": {
                "privacyStatus": "public",
                "selfDeclaredMadeForKids": False
            }
        }

        media = MediaFileUpload(video_path, mimetype="video/mp4", resumable=True)

        print(f"⬆️ Uploading video: {video_path}")
        request = youtube.videos().insert(
            part="snippet,status",
            body=request_body,
            media_body=media
        )

        response = request.execute()
        video_id = response.get("id")

        print("🎉 Video uploaded successfully!")
        print(f"▶️ Watch here: https://www.youtube.com/watch?v={video_id}")

    except Exception as e:
        print(f"❌ An error occurred during the upload process: {e}")
        raise