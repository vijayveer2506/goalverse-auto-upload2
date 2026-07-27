import os
from dotenv import load_dotenv

from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload

load_dotenv()

SCOPES = [
    "https://www.googleapis.com/auth/youtube.upload"
]


def get_youtube():

    token_json = os.getenv("YOUTUBE_TOKEN_JSON")

    if not token_json:
        raise Exception("Missing YOUTUBE_TOKEN_JSON secret")

    with open("token.json", "w", encoding="utf-8") as file:
        file.write(token_json)

    credentials = Credentials.from_authorized_user_file(
        "token.json",
        SCOPES
    )

    return build(
        "youtube",
        "v3",
        credentials=credentials
    )


def upload_video(
    youtube,
    video_path,
    title,
    description
):

    body = {
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
        video_path,
        resumable=True
    )

    request = youtube.videos().insert(
        part="snippet,status",
        body=body,
        media_body=media
    )

    response = None

    while response is None:

        status, response = request.next_chunk()

        if status:
            print(
                f"Uploading... {int(status.progress()*100)}%"
            )

    print()
    print("=" * 50)
    print("UPLOAD SUCCESSFUL")
    print("=" * 50)
    print("Video ID :", response["id"])
    print("Title    :", title)
    print("=" * 50)

    return response
