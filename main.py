import json
import os

from generator import generate_title, generate_description
from youtube import get_youtube, upload_video
from audio_processor import process_video

from dropbox_client import (
    download_first_video,
    move_to_uploaded,
    move_to_failed
)


def load_config():

    with open(
        "config.json",
        "r",
        encoding="utf-8"
    ) as file:

        return json.load(file)


def print_banner():

    print("=" * 60)
    print("         GoalVerse Auto Upload System")
    print("=" * 60)


def main():

    print_banner()

    config = load_config()

    channel_name = config.get(
        "channel_name",
        "GoalVerse"
    )

    video = download_first_video()

    if video is None:

        print("❌ No videos found in Dropbox.")

        return

    local_path = video["local_path"]

    dropbox_path = video["dropbox_path"]

    filename = video["filename"]

    print(f"🎥 Video : {filename}")

    print("🎵 Processing video...")

    processed_path = process_video(local_path)

    print("✅ Audio replaced successfully.")

    title = generate_title(channel_name)

    description = generate_description(channel_name)

    print()

    print("Generated Title:")

    print(title)

    youtube = get_youtube()

    try:

        upload_video(

            youtube=youtube,

            video_path=processed_path,

            title=title,

            description=description

        )

        move_to_uploaded(

            dropbox_path,

            filename

        )

        print()

        print("✅ Video moved to Uploaded folder.")

    except Exception as error:

        print()

        print(error)

        move_to_failed(

            dropbox_path,

            filename

        )

        print("❌ Video moved to Failed folder.")

    finally:

        for path in [local_path, processed_path]:

            if os.path.exists(path):

                os.remove(path)

                print(f"🗑 Deleted: {path}")

    print()

    print("Upload process completed.")

    print("=" * 60)


if __name__ == "__main__":

    main()
