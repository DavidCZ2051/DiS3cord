from urllib.parse import quote
from discord import ui, enums
from uuid import uuid4
from os import getenv

class UploadRequest:
    channel_id: int
    channel_type: str
    channel_name: str # Can be the channel name or the user DM name
    user_id: int | None # If the upload is anonymous, user id will be None
    token: str
    permanent: bool

    def __init__(self, channel_id: int, channel_type: str, channel_name: str, user_id: int | None, permanent: bool):
        self.channel_id = channel_id
        self.channel_type = channel_type
        self.channel_name = channel_name
        if channel_type == "TextChannel":
            self.channel_name = f"#{channel_name}"
        self.user_id = user_id
        self.token = str(uuid4())
        self.permanent = permanent


class OpenButtonView(ui.View):
    def __init__(self, token: str):
        super().__init__(timeout=None)

        self.add_item(ui.Button(
            label="Open web interface",
            style=enums.ButtonStyle.link,
            url=f"{getenv("WEB_INTERFACE_URL")}/?token={token}"
        ))


class ShowButtonView(ui.View):
    def __init__(self, file_name: str):
        super().__init__(timeout=None)

        self.add_item(ui.Button(
            label="Show",
            style=enums.ButtonStyle.link,
            url=f"{getenv("OBJECT_STORAGE_URL")}/data/{quote(file_name)}"
        ))
