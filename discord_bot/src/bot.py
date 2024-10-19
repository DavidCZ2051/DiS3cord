from discord import app_commands
import discord
from uuid import uuid4
from os import getenv

class Client(discord.Client):
    async def on_ready(self):
        print(f"Logged on as {self.user}!")
        await tree.sync()

    async def on_message(self, message):
        if message.author == self.user:
            return
        
        if message.content == "ping":
            await message.channel.send("pong")

def send_file_uploaded_message(msg: str, token: str):
    upload_request = [request for request in upload_requests if request.token == token][0]

    channel = client.get_channel(upload_request.channel_id)

    # Await the message to be sent in a non async function
    client.loop.create_task(channel.send(msg))

    upload_requests.remove(upload_request)

intents = discord.Intents.default()
intents.message_content = True

client = Client(intents=intents)

tree = app_commands.CommandTree(client)

upload_requests: list = []

class UploadRequest:
    channel_id: int
    token: str

    def __init__(self, channel_id: int):
        self.channel_id = channel_id
        self.token = str(uuid4())

@tree.command(
    name="upload",
    description="Opens a web interface for file upload."
)
async def open_upload_interface(interaction: discord.Interaction):
    # Maybe pass the channel ID in the URL as a query parameter
    # Use randomly generated tokens to prevent sending messages to a channel that didn't request the upload interface

    upload_request = UploadRequest(interaction.channel_id)
    upload_requests.append(upload_request)

    await interaction.response.send_message(f"{getenv("WEB_INTERFACE_URL")}/?token={upload_request.token}", ephemeral=True)
