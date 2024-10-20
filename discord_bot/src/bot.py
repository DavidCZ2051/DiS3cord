import asyncio
from discord import app_commands, Embed, Client, Interaction, Message, Intents
from classes import UploadRequest, ShowButtonView
from functions import format_file_size
from os import getenv

# Holds all the upload requests that are currently active
# Each upload request has a unique token that is passed to the web interface instead of the channel ID
# This is to prevent the user from sending messages to a channel that didn't request the upload interface
upload_requests: list[UploadRequest] = []


class Client(Client):
    async def on_ready(self):
        print(f"Logged on as {self.user}!")
        await tree.sync()

    async def on_message(self, message: Message):
        if message.author == self.user:
            return

        if message.content == "ping":
            await message.channel.send("pong")


intents = Intents.default()
intents.message_content = True
intents.members = True

client = Client(intents=intents)

tree = app_commands.CommandTree(client)


@tree.command(
    name="upload",
    description="Opens a web interface for file upload.",
)
async def open_upload_interface(interaction: Interaction):
    upload_request = UploadRequest(interaction.channel_id, interaction.user.id)
    upload_requests.append(upload_request)

    await interaction.response.send_message(f"{getenv("WEB_INTERFACE_URL")}/?token={upload_request.token}", ephemeral=True)


def send_file_uploaded_message(file_name: str, file_size: int, content_type: str, token: str):
    upload_request = [request for request in upload_requests if request.token == token][0]

    channel = client.get_channel(upload_request.channel_id)
    user = client.get_user(upload_request.user_id)

    embed = Embed(title="File uploaded")
    embed.set_author(name=user.name, icon_url=user.avatar.url)
    embed.add_field(name="File name", value=file_name)
    embed.add_field(name="File size", value=format_file_size(file_size))
    embed.add_field(name="Content type", value=content_type)

    async def send_message(embed: Embed):
        await channel.send(embed=embed, view=ShowButtonView(file_name))

    client.loop.create_task(send_message(embed))

    upload_requests.remove(upload_request)
