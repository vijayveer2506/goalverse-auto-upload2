import os
import random


def read_lines(filename):
    """
    Reads all non-empty lines from a file inside the content folder.
    """
    path = os.path.join("content", filename)

    if not os.path.exists(path):
        return []

    with open(path, "r", encoding="utf-8") as file:
        return [
            line.strip()
            for line in file.readlines()
            if line.strip()
        ]


def random_line(filename, default=""):

    lines = read_lines(filename)

    if not lines:
        return default

    return random.choice(lines)


def load_list(file_name):

    if not os.path.exists(file_name):
        return []

    with open(file_name, "r", encoding="utf-8") as file:
        return file.read().splitlines()


def append_line(file_name, text):

    with open(file_name, "a", encoding="utf-8") as file:
        file.write(text + "\n")


def load_uploaded():

    return load_list("uploaded.txt")


def save_uploaded(video_name):

    append_line("uploaded.txt", video_name)


def load_used_titles():

    return load_list("used_titles.txt")


def save_used_title(title):

    append_line("used_titles.txt", title)


def get_video_files():

    folder = "videos"

    if not os.path.exists(folder):
        return []

    videos = []

    for file in sorted(os.listdir(folder)):

        if file.lower().endswith(".mp4"):
            videos.append(
                os.path.join(folder, file)
            )

    return videos


def get_next_video():

    uploaded = load_uploaded()

    for video in get_video_files():

        if os.path.basename(video) not in uploaded:
            return video

    return None
