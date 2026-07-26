import os
import json
from dotenv import load_dotenv

from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload


load_dotenv()

SCOPES = [
    "https://www.googleapis.com/auth/youtube.upload"
]


def get_youtube_service():

    oauth_json = os.getenv("YOUTUBE_OAUTH_JSON")

    if not oauth_json:
        raise Exception("Missing YOUTUBE_OAUTH_JSON secret")

    with open("client_secret.json", "w") as f:
        f.write(oauth_json)

    flow = InstalledAppFlow.from_client_secrets_file(
        "client_secret.json",
        SCOPES
    )

    credentials = flow.run_local_server(
        port=8080
    )

    youtube = build(
        "youtube",
        "v3",
        credentials=credentials
    )

    return youtube


if __name__ == "__main__":
    youtube = get_youtube_service()
    print("YouTube authentication successful")
