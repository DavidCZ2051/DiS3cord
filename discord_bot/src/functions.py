from minio import Minio, S3Error
from typing import IO


def get_stream_size(stream: IO[bytes]) -> int:
    size = len(stream.read())
    stream.seek(0)
    return size


def format_file_size(num: int, suffix="B") -> str:
    for unit in ("", "Ki", "Mi", "Gi", "Ti", "Pi", "Ei", "Zi"):
        if abs(num) < 1024.0:
            return f"{num:3.1f}{unit}{suffix}"
        num /= 1024.0
    return f"{num:.1f}Yi{suffix}"


def sanitize_from_discord_markdown(text: str) -> str:
    return text.replace("`", "\\`").replace("*", "\\*").replace("_", "\\_").replace("~", "\\~").replace("|", "\\|")


def check_if_file_exists(client: Minio, bucket_name: str, file_name: str) -> bool:
    file_exists = False
    try:
        client.get_object(bucket_name, file_name)
        file_exists = True
    except S3Error as e:
        if e.code == "NoSuchKey":
            pass
        else:
            raise e
    return file_exists
