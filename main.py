import json
import os

from generator import generate_title, generate_description
from utils import get_next_video, save_uploaded
from youtube import get_youtube, upload_video


def load_config():
    with open("config.json", "r", encoding="utf-8") as file:
        return json.load(file)


def print_banner():
    print("=" * 60)
    print("         GoalVerse Auto Upload System")
    print("=" * 60)


def main():

    print_banner()

    config = load_config()

    channel_name = config.get("channel_name", "GoalVerse")

    video = get_next_video()

    if video is None:
        print("❌ No videos available for upload.")
        return

    print(f"🎥 Video : {os.path.basename(video)}")

    title = generate_title(channel_name)

    description = generate_description(channel_name)

    print("\nGenerated Title:")
    print(title)

    youtube = get_youtube()

    upload_video(
        youtube=youtube,
        video_path=video,
        title=title,
        description=description
    )

    save_uploaded(os.path.basename(video))

    print("\n✅ Upload completed successfully.")
    print("=" * 60)


if __name__ == "__main__":
    main()
