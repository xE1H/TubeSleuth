import os
from threading import Timer
from pytube import YouTube

# YouTube Downloader
# xE1H, 2022

# TODO: rewrite scheduleRm
# TODO: rewrite doesExist
# TODO: cache YouTube objects
# TODO: delete files on startup (cleanup)

# Look for ffmpeg in PATH or local dir
if "ffmpeg" not in os.listdir():
    try:
        os.system("ffmpeg -version")
    except:
        raise Exception("* ffmpeg not found in PATH or local dir.")

# Look for downloads folder
if "downloads" not in os.listdir():
    os.mkdir("downloads")


def getInfo(url):
    """
    Get info about a video
    :param url: url of the video
    :return: title, length, thumbnail, formats [{"format": "mp4", "resolution": "1080p"}]
    """
    yt = YouTube(url)
    # Only look for mp4
    streams = yt.streams.filter(mime_type="video/mp4", progressive=False).desc()
    formats = []  # {"format": f.subtype, "resolution": f.resolution}

    # Sort by resolution
    for stream in streams:
        duplicate = False
        for format in formats:
            if stream.resolution == format["resolution"]:
                duplicate = True
        if not duplicate:
            formats.append({"format": stream.subtype, "resolution": stream.resolution})

    return yt.title, yt.length, yt.thumbnail_url, formats


def downloadVideo(url, resolution):
    """
    Download a video
    :param url: url of the video
    :param resolution: resolution of the video
    :return: Video filename
    """
    yt = YouTube(url)
    # Only look for mp4
    streams = yt.streams.filter(mime_type="video/mp4", progressive=False).desc()
    for stream in streams:
        if stream.resolution == resolution:
            return download(yt, stream, audio=False, res=resolution)


def downloadAudio(url):
    """
    Download audio from a video
    :param url: url of the video
    :return: Audio filename
    """
    yt = YouTube(url)
    stream = yt.streams.filter(only_audio=True).desc().first()
    return download(yt, stream, audio=True)


def scheduleRm(path):
    """
    Schedule a file to be deleted
    :param path:
    :return:
    """
    thead = Timer(1800.0, os.remove, [path])
    thead.start()


def doesExist(path, stream=None):
    """
    Check if file exists. If not, download it
    :param path: Path of file in downloads folder
    :param stream: Stream to download it off of
    :return:
    """
    if path in os.listdir("downloads"):
        if stream is not None:
            return path
        else:
            return True
    else:
        if stream is not None:
            return stream.download(output_path="./downloads/", filename=path)
        else:
            return False


def download(yt, stream, audio=False, res=None):
    """
    Download a video
    :param yt: YouTube object
    :param stream: selected Stream object
    :param audio: true if audio only, default false
    :param res: resolution of the video, default None
    :return: Path of output file
    """

    # Check if file exists, then just send it
    if audio:
        path = str(yt.video_id) + ".mp3"
        if doesExist(path):
            return "./downloads/" + path, yt.title + ".mp3"
    else:
        path = str(yt.video_id) + "-" + res + "-av." + stream.subtype
        if doesExist(path):
            return "./downloads/" + path, yt.title + "." + stream.subtype

    if audio:
        # Download audio
        audioPath = doesExist(str(yt.video_id) + "." + stream.subtype, stream)
        scheduleRm(audioPath)  # Schedule file to be deleted

        # Use ffmpeg to convert audio (usually webm) to mp3
        mp3path = "./downloads/" + str(yt.video_id) + ".mp3"
        os.system("ffmpeg -i " + audioPath + " -acodec libmp3lame -ab 128k -hide_banner -loglevel error " + mp3path)
        scheduleRm(mp3path)  # Schedule file to be deleted

        return mp3path, yt.title + ".mp3"
    else:
        # Download video (without audio)
        videoPath = doesExist(str(yt.video_id) + res + "." + stream.subtype, stream)
        scheduleRm(videoPath)  # Schedule file to be deleted

        # Download audio
        audioPath = doesExist(str(yt.video_id) + "." + stream.subtype,
                              yt.streams.filter(only_audio=True).desc().first())

        # Combine audio and video with ffmpeg
        outPath = "./downloads/" + str(yt.video_id) + "-" + res + "-av.mp4"
        os.system(
            "ffmpeg -i " + videoPath + " -i " + audioPath + " -c copy -c:a aac -strict experimental -hide_banner -loglevel error " + outPath)
        scheduleRm(outPath)  # Schedule final file to be deleted

        return outPath, yt.title + "." + stream.subtype
