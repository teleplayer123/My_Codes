from flask import Flask, render_template, request, redirect
import flask
import requests
import os
from werkzeug.utils import secure_filename
import logging


from utils import save

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)


app = Flask(__name__)
db = "C:/path/to/uploads/"
if not os.path.exists(db):
    os.mkdir(db)

@app.route("/upload", methods=["GET", "POST"])
def upload():
    return render_template("upload_file.html")

@app.route("/uploads", methods=["POST", "GET"])
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

@app.route("/download", methods=["GET", "POST"])
def download():
    render_template("/download_file.html")



if __name__ == "__main__":
    app.run(host="localhost", port=5000)
