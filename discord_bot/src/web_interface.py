from bot import send_file_uploaded_message, upload_requests
from flask import Flask, render_template, request
from functions import get_stream_size
from minio import Minio
from os import getenv

app = Flask(__name__)
app.config["MAX_CONTENT_LENGTH"] = int(getenv("MAX_UPLOAD_SIZE_MEGABYTES")) * 1024 * 1024

client = Minio(
    "object-storage:9000",
    access_key=getenv("MINIO_ACCESS_KEY"),
    secret_key=getenv("MINIO_SECRET_KEY"),
    secure=False
)

@app.route("/", methods=["GET"])
def index():
    if request.args.get("token") not in [request.token for request in upload_requests]:
        return "Invalid token", 403
    return render_template("index.html")


@app.route("/", methods=["POST"])
def upload():
    if request.args.get("token") not in [request.token for request in upload_requests]:
        return "Invalid token", 403

    file = request.files["file"]

    if file.filename == "":
        return "No selected file"

    file_size = get_stream_size(file.stream)

    client.put_object(
        "data",
        file.filename,
        file.stream,
        file_size,
        file.content_type
    )

    send_file_uploaded_message(file.filename, file_size, file.content_type, request.args.get("token"))

    return file.filename


@app.errorhandler(413)
def request_entity_too_large(_):
    file_size = round(request.content_length / (1024 * 1024))
    return render_template("413.html", max_upload_file_size=getenv("MAX_UPLOAD_SIZE_MEGABYTES"), file_size=file_size), 413
