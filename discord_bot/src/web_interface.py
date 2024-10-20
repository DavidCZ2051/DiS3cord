from flask import Flask, render_template, request
from bot import send_file_uploaded_message, upload_requests
from os import getenv
from minio import Minio

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

    print(f"Uploading file {file.filename} to MinIO")
    print(f"File size: {file.content_length}")

    file.stream.seek(0)

    # TODO: Fix file upload not working - file gets uploaded to MinIO but has 0 bytes

    client.put_object(
        "data",
        file.filename,
        file.stream,
        file.content_length,
        file.content_type
    )

    send_file_uploaded_message(file.filename, request.args.get("token"))

    return file.filename


@app.errorhandler(413)
def request_entity_too_large(_):
    file_size = round(request.content_length / (1024 * 1024))
    return render_template("413.html", max_upload_file_size=getenv("MAX_UPLOAD_SIZE_MEGABYTES"), file_size=file_size), 413
