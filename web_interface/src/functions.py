from minio import Minio, S3Error
from typing import IO


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


def get_stream_size(stream: IO[bytes]) -> int:
    size = len(stream.read())
    stream.seek(0)
    return size
