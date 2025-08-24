import os
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from datetime import datetime

SCOPES = ["https://www.googleapis.com/auth/youtube.upload"]

def authenticate():
    flow = InstalledAppFlow.from_client_secrets_file("client_secret.json", SCOPES)
    credentials = flow.run_local_server()
    return build("youtube", "v3", credentials=credentials)

def upload(file_path, title, description):
    youtube = authenticate()
    request = youtube.videos().insert(
        part="snippet,status",
        body={
            "snippet": {
                "title": title,
                "description": description,
                "tags": ["satisfying", "shorts", "asmr"],
                "categoryId": "22"
            },
            "status": {
                "privacyStatus": "public"
            }
        },
        media_body=file_path
    )
    response = request.execute()
    print("Uploaded to YouTube:", response['id'])