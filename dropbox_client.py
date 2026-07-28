import os
import dropbox

APP_KEY = os.getenv("DROPBOX_APP_KEY")
APP_SECRET = os.getenv("DROPBOX_APP_SECRET")
REFRESH_TOKEN = os.getenv("DROPBOX_REFRESH_TOKEN")

dbx = dropbox.Dropbox(
    oauth2_refresh_token=REFRESH_TOKEN,
    app_key=APP_KEY,
    app_secret=APP_SECRET
)

READY_FOLDER = "/GoalVerse/Ready"
UPLOADED_FOLDER = "/GoalVerse/Uploaded"
FAILED_FOLDER = "/GoalVerse/Failed"


def list_videos():

    result = dbx.files_list_folder(READY_FOLDER)

    videos = []

    for item in result.entries:

        if isinstance(item, dropbox.files.FileMetadata):

            if item.name.lower().endswith(".mp4"):
                videos.append(item)

    videos.sort(key=lambda x: x.server_modified)

    return videos


def download_first_video():

    videos = list_videos()

    if not videos:
        return None

    video = videos[0]

    os.makedirs("videos", exist_ok=True)

    local_path = os.path.join(
        "videos",
        video.name
    )

    dbx.files_download_to_file(
        local_path,
        video.path_lower
    )

    return {
        "local_path": local_path,
        "dropbox_path": video.path_lower,
        "filename": video.name
    }


def move_to_uploaded(dropbox_path, filename):

    destination = f"{UPLOADED_FOLDER}/{filename}"

    dbx.files_move_v2(
        dropbox_path,
        destination
    )


def move_to_failed(dropbox_path, filename):

    destination = f"{FAILED_FOLDER}/{filename}"

    dbx.files_move_v2(
        dropbox_path,
        destination
    )
