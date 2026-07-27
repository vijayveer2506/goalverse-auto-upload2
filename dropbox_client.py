import os
import dropbox

ACCESS_TOKEN = os.getenv("DROPBOX_ACCESS_TOKEN")

dbx = dropbox.Dropbox(ACCESS_TOKEN)


READY_FOLDER = "/GoalVerse/Ready"


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

    local_path = os.path.join("videos", video.name)

    os.makedirs("videos", exist_ok=True)

    dbx.files_download_to_file(
        local_path,
        video.path_lower
    )

    return local_path, video.path_lower
