# authorize.py
import os
from google_auth_oauthlib.flow import InstalledAppFlow

# This file should exist in your root directory
CLIENT_SECRETS_FILE = "client_secret.json"

# Scopes define the level of access you are requesting.
SCOPES = ["https://www.googleapis.com/auth/youtube.upload"]

def get_credentials():
    """
    Runs the authentication flow and saves the token.
    This function is meant to be run ONCE LOCALLY to generate token.json.
    """
    if not os.path.exists(CLIENT_SECRETS_FILE):
        print(f"❌ Error: {CLIENT_SECRETS_FILE} not found. Please download it from Google Cloud Console.")
        return

    flow = InstalledAppFlow.from_client_secrets_file(CLIENT_SECRETS_FILE, SCOPES)
    # This will open a browser window for you to log in and authorize the app.
    credentials = flow.run_local_server(port=8080)

    # Save the credentials for later use
    with open("token.json", "w") as token_file:
        token_file.write(credentials.to_json())

    print("✅ token.json has been created successfully. You can now use its content in your Render environment variables.")

if __name__ == "__main__":
    get_credentials()