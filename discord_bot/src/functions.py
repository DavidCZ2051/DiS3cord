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
