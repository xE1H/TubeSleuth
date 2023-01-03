import configparser
import datetime

from bleach import clean
from flask import Flask, render_template, request, jsonify, send_file

from modules import downloader

# TubeSleuth
# xE1H, 2022

app = Flask(__name__)

# Load configuration.cfg
config = configparser.ConfigParser()
config.read("configuration.cfg")

# Create Downloader object
dl = downloader.Downloader(config)


# Logging
@app.before_request
def logRequest():
    logLevel = int(config["logging"]["logLevel"])
    logFile = config["logging"]["logFile"]

    if logLevel == -1:
        return

    try:
        request_addr = request.headers.getlist('X-Forwarded-For')[0].split(',')[0]
    except IndexError:
        request_addr = request.remote_addr

    if logLevel == 2 or (logLevel == 1 and "/static/" not in request.path) or (
            logLevel == 0 and request.path == "/download"):
        with open(logFile, "a") as f:
            f.write(
                f"{datetime.datetime.now()} {request.method} {request.path} {request_addr} {str(dict(request.args)) if request.args else ''}\n")


@app.route("/info")
def info():
    url = clean(request.args.get("url"))
    title, length, thumbnail, format = dl.getInfo(url)
    # Convert length to mm:ss from seconds
    length = str(length // 60) + ":" + str(length % 60)

    return 400 if title is None else jsonify(title=title, length=length, thumbnail=thumbnail, format=format)


@app.route("/download")
def download():
    url = clean(request.args.get("url"))
    format = clean(request.args.get("format"))
    if format == "audio":
        path, filename = dl.downloadAudio(url)
    else:
        path, filename = dl.downloadVideo(url, format)
    return send_file(path, as_attachment=True, download_name=filename)


@app.route("/")
def index():
    return render_template("index.html")


if __name__ == '__main__':
    app.run()
