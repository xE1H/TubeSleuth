# TubeSleuth
Welcome to TubeSleuth, a simple, clean and self-contained interface for downloading YouTube videos. This application is written in Flask and allows you to quickly and easily download videos from YouTube.

## Features

* Clean and simple interface
* Quick and easy downloading of YouTube videos
* Support for downloading videos in various formats and resolutions

![Screenshot](/static/demo.png)


## Requirements

* Python >= 3.8
* Flask >= 2.1.2
* pytube >= 12.1.0
* bleach >= 5.0.1
* ffmpeg


# Installation

To install TubeSleuth, follow these steps:

1. Clone the repository:

    `git clone https://github.com/xE1H/TubeSleuth.git`

2. Change into the project directory:

    `cd TubeSleuth`

3. Install the required dependencies:

    `pip install -r requirements.txt`
4. Make sure `ffmpeg` is in the same directory as the application or in your PATH. You can download `ffmpeg` [here](https://ffmpeg.org/download.html).


# Usage

To run TubeSleuth, use the following command:

`flask run`

This will start the application on your local machine for testing / development.
**DO NOT USE THIS FOR PRODUCTION!** 
You can then access the application by visiting http://localhost:5000 in your web browser.

### Production usage

For production usage, you should use a WSGI server such as Gunicorn. You can then use a reverse proxy such as Nginx to serve the application. For more information on this, see the [Flask documentation](https://flask.palletsprojects.com/en/2.0.x/deploying/).

# Contribution

If you want to contribute to TubeSleuth, please follow these guidelines:

    Fork the repository
    Create a new branch for your feature
    Make your changes
    Test your changes thoroughly
    Submit a pull request

# License

TubeSleuth is released under the [MIT License](https://opensource.org/licenses/MIT).