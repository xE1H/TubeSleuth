from bleach import clean
from flask import Flask, render_template, request, jsonify, send_file

import ytdownload as yt

# YouTube Downloader
# xE1H, 2022

app = Flask(__name__)


@app.route("/info")
def info():
    url = clean(request.args.get("url"))
    title, length, thumbnail, format = yt.getInfo(url)
    # Convert length to mm:ss from seconds
    length = str(length // 60) + ":" + str(length % 60)

    return 400 if title is None else jsonify(title=title, length=length, thumbnail=thumbnail, format=format)


@app.route("/download")
def download():
    url = clean(request.args.get("url"))
    format = clean(request.args.get("format"))
    if format == "audio":
        path, filename = yt.downloadAudio(url)
    else:
        path, filename = yt.download(url, format)
    return send_file(path, as_attachment=True, download_name=filename)


@app.route("/")
def index():
    return render_template("index.html")


if __name__ == '__main__':
    app.run()
