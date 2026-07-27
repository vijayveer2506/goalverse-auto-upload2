from dropbox_client import download_first_video

video = download_first_video()

if video is None:

    print("No videos found.")

else:

    print("=" * 50)
    print("DOWNLOAD SUCCESSFUL")
    print("=" * 50)
    print("Local File :", video["local_path"])
    print("Dropbox File :", video["dropbox_path"])
    print("=" * 50)
