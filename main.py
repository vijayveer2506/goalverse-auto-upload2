import os
from dotenv import load_dotenv
from googleapiclient.discovery import build

load_dotenv()

API_KEY = os.getenv("YOUTUBE_API_KEY")

youtube = build(
    "youtube",
    "v3",
    developerKey=API_KEY
)

def search_videos(keyword):
    request = youtube.search().list(
        part="snippet",
        q=keyword,
        maxResults=5
    )

    response = request.execute()

    for item in response["items"]:
        print(item["snippet"]["title"])

if __name__ == "__main__":
    search_videos("AI automation")
