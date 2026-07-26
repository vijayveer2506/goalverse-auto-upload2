import os
import json
from dotenv import load_dotenv

from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload


load_dotenv()


# Load config
with open("config.json", "r") as file:
    config = json.load(file)


CHANNEL_NAME = config["channel_name"]
VIDEOS_PER_DAY = config["videos_per_day"]
HASHTAGS = " ".join(config["hashtags"])


# Track uploaded videos
def load_uploaded():
    if not os.path.exists("uploaded.txt"):
        return []

    with open("uploaded.txt", "r") as file:
        return file.read().splitlines()


def save_uploaded(video_name):
    with open("uploaded.txt", "a") as file:
        file.write(video_name + "\n")


# Find next video
def get_next_video():

    uploaded = load_uploaded()

    video_folder = "videos"

    if not os.path.exists(video_folder):
        return None

    for file in os.listdir(video_folder):

        if file not in uploaded:
            return os.path.join(video_folder, file)

    return None


# YouTube authentication
SCOPES = [
    "https://www.googleapis.com/auth/youtube.upload"
]


def get_youtube_service():

    token_json = os.getenv("YOUTUBE_TOKEN_JSON")

    if not token_json:
        raise Exception("Missing YOUTUBE_TOKEN_JSON secret")

    with open("token.json", "w") as f:
        f.write(token_json)

    credentials = Credentials.from_authorized_user_file(
        "token.json",
        SCOPES
    )

    youtube = build(
        "youtube",
        "v3",
        credentials=credentials
    )

    return youtube
      


# Upload video
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
            "categoryId": "22"
        },

        "status": {
            "privacyStatus": "public"
        }
    }

    media = MediaFileUpload(
        file_path,
        chunksize=1024 * 1024,
        resumable=True
    )

    request = youtube.videos().insert(
        part="snippet,status",
        body=request_body,
        media_body=media
    )

    response = None

    while response is None:
        status, response = request.next_chunk()

        if status:
            print(f"Upload progress: {int(status.progress() * 100)}%")

    print("Upload completed!")
    print("Video ID:", response["id"])
  


# Main
# Main
if __name__ == "__main__":

    youtube = get_youtube_service()

    video = get_next_video()

    if video:

        title = f"{CHANNEL_NAME} Football Short"

        description = f"""
Amazing football moments by {CHANNEL_NAME}

{HASHTAGS}
"""

        upload_video(
            youtube,
            video,
            title,
            description
        )

        # Delete uploaded video after successful upload
        os.remove(video)

        print(f"Deleted uploaded video: {video}")

        print("Upload completed successfully")

    else:

        print("No new videos found")


   
