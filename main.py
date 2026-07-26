import os
import json
from dotenv import load_dotenv
with open("config.json", "r") as file:
    config = json.load(file)

CHANNEL_NAME = config["channel_name"]
VIDEOS_PER_DAY = config["videos_per_day"]
HASHTAGS = " ".join(config["hashtags"])
def load_uploaded():
    if not os.path.exists("uploaded.txt"):
        return []

    with open("uploaded.txt", "r") as file:
        return file.read().splitlines()


def save_uploaded(video_name):
    with open("uploaded.txt", "a") as file:
        file.write(video_name + "\n")
        def get_next_video():
    uploaded = load_uploaded()

    video_folder = "videos"

    if not os.path.exists(video_folder):
        return None

    for file in os.listdir(video_folder):
        if file not in uploaded:
            return os.path.join(video_folder, file)

    return None
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
def upload_video(
    youtube,
    file_path,
    title,
    description
):

    request_body = {
        "snippet": {
            "title": title,
            "description": description,
            "categoryId": "17"
        },
        "status": {
            "privacyStatus": "public"
        }
    }

    media = MediaFileUpload(
        file_path,
        chunksize=-1,
        resumable=True
    )

    request = youtube.videos().insert(
        part="snippet,status",
        body=request_body,
        media_body=media
    )

    response = request.execute()

    print(
        "Uploaded video ID:",
        response["id"]
    )

if __name__ == "__main__":
    youtube = get_youtube_service()
    print("YouTube authentication successful")
