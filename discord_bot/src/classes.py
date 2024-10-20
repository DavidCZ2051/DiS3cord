from uuid import uuid4


class UploadRequest:
    channel_id: int
    user_id: int
    token: str

    def __init__(self, channel_id: int, user_id: int):
        self.channel_id = channel_id
        self.user_id = user_id
        self.token = str(uuid4())
