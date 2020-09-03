from flask import Flask, render_template, request, redirect, send_file, send_from_directory
import flask
import requests
import os
import gzip
import zipfile
from werkzeug.utils import secure_filename
import logging

from utils import create_zip


logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)


app = Flask(__name__)
db = "/path/to/uploads/"
if not os.path.exists(db):
    os.mkdir(db)

@app.route("/upload", methods=["GET", "POST"])
def upload():
    return render_template("upload_file.html")

@app.route("/upload/files", methods=["POST", "GET"])
def upload_file():
    filenames = request.files.getlist("file")
    file_list = []
    for file in filenames:
        filename = secure_filename(file.filename)
        logger.info("uploading... " + os.path.abspath(file.filename))
        if not file:
            logger.info("No files selected")
            redirect("/upload")
        file_list.append(filename)
        file.save(os.path.join(db, filename))
    if file_list:
        return render_template("/upload_file.html", filenames=file_list)
    else:
        logger.info("error with file handling")
        redirect("/upload")

@app.route("/upload_files", methods=["GET" ,"POST"])
def uploadbd():
    filenames = os.listdir("C:/path/to/uploads")
    return render_template("/uploadbd_files.html", filenames=filenames)

@app.route("/files/upload", methods=["POST"])
def upload_bdfiles():
    path = "C:/path/to/dist/runbd"
    dir_path = "C:/path/to/uploads"
    if not os.path.exists(dir_path):
        os.mkdir(dir_path)
    files = request.files.getlist("file")
    filenames = []
    for file in files:
        filenames.append(file.filename)
        with open(os.path.join(dir_path, file.filename), "wb") as fh:
            with open(os.path.join(path, file.filename), "rb") as rf:
                for line in rf:
                    fh.write(line)
    return render_template("/uploadbd_files.html", filenames=filenames)

@app.route("/download_files", methods=["GET"])
def download():
    dpath = "C:/path/to/downloads"
    if not os.path.exists(dpath):
        os.mkdir(dpath)
    if len(os.listdir(db)) == 0:
        logger.error("no files to download")
        return
    if len(os.listdir(db)) == 1:
        file = str(db + os.listdir(db)[0])
    else:
        file = create_zip(db, "C:/path/to/downloads/uploads.zip")
    return send_file(file, as_attachment=True)

if __name__ == "__main__":
    app.run(host="localhost", port=5000)
