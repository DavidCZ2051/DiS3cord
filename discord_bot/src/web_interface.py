from flask import Flask, render_template, request
from bot import send_file_uploaded_message
from os import getenv

app = Flask(__name__)
#app.config["MAX_CONTENT_LENGTH"] = int(getenv("MAX_UPLOAD_SIZE_MEGABYTES")) * 1024 * 1024

@app.route("/", methods=["GET"])
def index():
    return render_template("index.html")

@app.route("/", methods=["POST"])
def upload():
    file = request.files["file"]

    if file.filename == '':
        return "No selected file"

    # TODO: Upload file to minio

    #send_file_uploaded_message(f"File uploaded: {file.filename}", int(request.args.get("token")))

    return file.filename

""" @app.errorhandler(413)
def request_entity_too_large(_):
    return render_template("413.html", max_upload_file_size=int(getenv("MAX_UPLOAD_SIZE_MEGABYTES"))) * 1024 * 1024, 400

app.register_error_handler(413, request_entity_too_large)
"""
