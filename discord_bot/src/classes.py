from urllib.parse import quote
from discord import ui, enums
from uuid import uuid4
from os import getenv

class UploadRequest:
    channel_id: int
    channel_name: str
    user_id: int | None # If the upload is anonymous, user id will be None
    token: str
    permanent: bool

    def __init__(self, channel_id: int, channel_name: str, user_id: int | None, permanent: bool):
        self.channel_id = channel_id
        self.channel_name = channel_name
        self.user_id = user_id
        self.token = str(uuid4())
        self.permanent = permanent


class ShowButtonView(ui.View):
    def __init__(self, file_name: str):
        super().__init__(timeout=None)

        self.add_item(ui.Button(
            label="Show",
            style=enums.ButtonStyle.link,
            url=f"{getenv("OBJECT_STORAGE_URL")}/data/{quote(file_name)}"
        ))
