import os
import random
import subprocess


MUSIC_FOLDER = "music"


def process_video(video_path):
    # Find all MP3 files
    music_files = [
        os.path.join(MUSIC_FOLDER, file)
        for file in os.listdir(MUSIC_FOLDER)
        if file.lower().endswith(".mp3")
    ]

    if not music_files:
        raise Exception("No MP3 files found inside the music folder.")

    # Randomly choose one song
    selected_music = random.choice(music_files)

    print(f"🎵 Selected music: {os.path.basename(selected_music)}")

    output_path = os.path.join(
        os.path.dirname(video_path),
        "processed_" + os.path.basename(video_path)
    )

    command = [
        "ffmpeg",
        "-y",
        "-i", video_path,
        "-stream_loop", "-1",
        "-i", selected_music,
        "-map", "0:v:0",
        "-map", "1:a:0",
        "-c:v", "copy",
        "-shortest",
        output_path
    ]

    result = subprocess.run(
        command,
        capture_output=True,
        text=True
    )

    if result.returncode != 0:
        raise Exception(result.stderr)

    return output_path
