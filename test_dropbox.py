from dropbox_client import list_videos

videos = list_videos()

print("=" * 50)

if not videos:
    print("No videos found in Dropbox.")
else:
    print(f"Found {len(videos)} video(s):\n")

    for video in videos:
        print(video.name)

print("=" * 50)
