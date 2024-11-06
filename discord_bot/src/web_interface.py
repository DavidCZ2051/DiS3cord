from bot import send_file_uploaded_message, upload_requests
from functions import get_stream_size, check_if_file_exists
from flask import Flask, render_template, request
from classes import UploadRequest
from minio import Minio
from os import getenv

app = Flask(__name__)
if max_file_size := int(getenv("MAX_UPLOAD_SIZE_MEGABYTES")) > -1:
    app.config["MAX_CONTENT_LENGTH"] = max_file_size * 1024 * 1024


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
    token = request.args.get("token")

    if token not in [request.token for request in upload_requests]:
        return "Invalid token", 403

    file = request.files["file"]

    if file.filename == "":
        return "No selected file"

    file_size = get_stream_size(file.stream)

    upload_request = [request for request in upload_requests if request.token == token][0]

    if check_if_file_exists(client, "data", file.filename):
        return {"error": "File with this name already exists"}, 409

    result = client.put_object(
        "data",
        file.filename,
        file.stream,
        file_size,
        file.content_type,
        metadata={
            "user_id": upload_request.user_id,
            "channel_id": upload_request.channel_id,
        }
    )

    send_file_uploaded_message(file.filename, file_size, file.content_type, token)

    # Object location is not returned - we're assuming the object is in the root of the bucket.
    # Needs later refactoring if we decide to store objects in directories.
    return {"url": f"{getenv("OBJECT_STORAGE_URL")}/{result.bucket_name}/{result.object_name}"}, 201


@app.errorhandler(413)
def request_entity_too_large(_):
    file_size = round(request.content_length / (1024 * 1024))
    return render_template("413.html", max_upload_file_size=getenv("MAX_UPLOAD_SIZE_MEGABYTES"), file_size=file_size), 413
