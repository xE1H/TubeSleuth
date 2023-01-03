import os
import subprocess
from threading import Timer

from pytube import YouTube


# YouTube Downloader
# xE1H, 2022

class Downloader:
    def __init__(self, config):
        self.config = config
        self.dlPath = config["downloads"]["downloadDir"]
        self.fileTimeout = config["downloads"]["deleteAfter"]

        # Look for ffmpeg in PATH or local dir
        if "ffmpeg" not in os.listdir():
            try:
                subprocess.check_output("ffmpeg -version", shell=True)
            except:
                raise Exception("* ffmpeg not found in PATH or local dir.")

        # Create download directory if it doesn't exist
        if not os.path.exists(self.dlPath):
            os.mkdir(self.dlPath)

        # Delete files on startup
        for file in os.listdir(self.dlPath):
            os.remove(os.path.join(self.dlPath, file))

    @staticmethod
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

    def downloadVideo(self, url, resolution):
        """
        Download a video
        :param url: url of the video
        :param resolution: resolution of the video
        :return: Video filename
        """
        yt = YouTube(url)
        # Only look for mp4
        streams = yt.streams
        videoStream = None

        for s in streams.filter(mime_type="video/mp4", progressive=False).desc():
            if s.resolution == resolution:
                videoStream = s

        path = str(yt.video_id) + "-" + resolution + "-av.mp4"
        if self.doesExist(path):
            return os.path.join(self.dlPath, path), yt.title + ".mp4"

        # Download video (without audio)
        videoPath = self.downloadIfNotExists(str(yt.video_id) + "-" + resolution + "-video." + videoStream.subtype,
                                             videoStream)

        # Download audio
        audioStream = streams.filter(only_audio=True).desc().first()
        audioPath = self.downloadIfNotExists(str(yt.video_id) + "-audio." + audioStream.subtype, audioStream)

        # Combine audio and video with ffmpeg
        outPath = os.path.join(self.dlPath, path)
        subprocess.check_output(
            "ffmpeg -i " + videoPath + " -i " + audioPath + " -c copy -c:a aac -strict experimental -hide_banner -loglevel error " + outPath,
            shell=True)

        self.scheduleRm({videoPath, audioPath, outPath})

        return outPath, yt.title + ".mp4"

    def downloadAudio(self, url):
        """
        Download audio from a video
        :param url: url of the video
        :return: audio filename
        """
        yt = YouTube(url)
        stream = yt.streams.filter(only_audio=True).desc().first()

        outPath = str(yt.video_id) + ".mp3"
        if self.doesExist(outPath):
            return os.path.join(self.dlPath, outPath), yt.title + ".mp3"

        # Download audio
        audioPath = self.downloadIfNotExists(str(yt.video_id) + "." + stream.subtype, stream)

        # Use ffmpeg to convert audio (usually webm) to mp3
        mp3path = os.path.join(self.dlPath, outPath)
        subprocess.check_output(
            "ffmpeg -i " + audioPath + " -acodec libmp3lame -ab 128k -hide_banner -loglevel error " + mp3path,  # NOQA
            shell=True)

        self.scheduleRm({audioPath, mp3path})

        return mp3path, yt.title + ".mp3"

    @staticmethod
    def removeFile(path):
        """
        Remove a file
        :param path: path of file
        :return:
        """
        try:
            os.remove(path)
        except:
            print(f" * Failed to remove file {path}. It may have already been removed.")

    def scheduleRm(self, path):
        """
        Schedule a file to be deleted
        :param path: path of file in downloads folder
        :return:
        """
        for p in path:
            thead = Timer(float(self.fileTimeout), self.removeFile, [p])
            thead.start()

    def doesExist(self, path):
        """
        Check if file exists.
        :param path:
        :return:
        """
        if path in os.listdir(self.dlPath):
            return True
        else:
            return False

    def downloadIfNotExists(self, path, stream):
        """
        Download a file if it doesn't exist
        :param path: path of file
        :param stream: stream to download it off of
        :return: path of file
        """
        if self.doesExist(path):
            return path
        else:
            return stream.download(output_path=self.dlPath, filename=path)
