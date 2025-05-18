def format_file_size(num: int, suffix="B") -> str:
    for unit in ("", "Ki", "Mi", "Gi", "Ti", "Pi", "Ei", "Zi"):
        if abs(num) < 1024.0:
            return f"{num:3.1f}{unit}{suffix}"
        num /= 1024.0
    return f"{num:.1f}Yi{suffix}"


def sanitize_from_discord_markdown(text: str) -> str:
    return text.replace("`", "\\`").replace("*", "\\*").replace("_", "\\_").replace("~", "\\~").replace("|", "\\|")
