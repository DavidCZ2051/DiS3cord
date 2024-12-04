from discord import app_commands, Embed, Client, Interaction, Message, Intents
from functions import format_file_size, sanitize_from_discord_markdown
from classes import UploadRequest, ShowButtonView, OpenButtonView
from urllib.parse import quote
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
    name="about",
    description="Shows information about the bot and basic usage instructions.",
)
async def about_message(interaction: Interaction):
    embed = Embed(title="About", description="This is a simple Discord bot that allows users to upload files through a web interface.")
    embed.add_field(name="Source code", value="[GitHub](https://github.com/DavidCZ2051/DiS3cord)")
    embed.add_field(name="Author", value="DavidCZ2051")

    await interaction.response.send_message(embed=embed, ephemeral=True)


@tree.command(
    name="upload",
    description="Opens a web interface for file upload.",
)
@app_commands.describe(anonymous="Whether the upload should be anonymous.")
@app_commands.describe(permanent="Whether the upload request token is permanent. This allows for multiple uploads with the same token. WARNING: This can be a security risk if the token is shared.")
async def open_upload_interface(interaction: Interaction, anonymous: bool = False, permanent: bool = False):
    # Check if anonymous uploads are disabled
    if anonymous and getenv("ALLOW_ANONYMOUS_UPLOADS") == "false":
        await interaction.response.send_message("Anonymous uploads are disabled.", ephemeral=True)
        return

    # Check if permanent tokens are disabled
    if permanent and getenv("ALLOW_PERMANENT_TOKENS") == "false":
        await interaction.response.send_message("Permanent tokens are disabled.", ephemeral=True)
        return

    upload_request = UploadRequest(interaction.channel_id, interaction.channel.name, interaction.user.id if not anonymous else None, permanent)
    upload_requests.append(upload_request)

    await interaction.response.send_message("Upload request created successfully ✅\nClick the button bellow to continue to file upload.", ephemeral=True, view=OpenButtonView(upload_request.token))


def send_file_uploaded_message(file_name: str, file_size: int, content_type: str, token: str):
    upload_request = [request for request in upload_requests if request.token == token][0]

    channel = client.get_channel(upload_request.channel_id)

    embed = Embed(title="File uploaded")

    # Embed author
    if upload_request.user_id != None:
        user = client.get_user(upload_request.user_id)
        embed.set_author(name=user.name, icon_url=user.avatar.url)
    else:
        embed.set_author(name="Anonymous")

    embed.add_field(name="File name", value=sanitize_from_discord_markdown(file_name))
    embed.add_field(name="File size", value=format_file_size(file_size))
    embed.add_field(name="Content type", value=content_type)

    # Image preview
    if content_type.startswith("image/"):
        embed.set_image(url=f"{getenv("OBJECT_STORAGE_URL")}/data/{quote(file_name)}")

    async def send_message(embed: Embed):
        await channel.send(embed=embed, view=ShowButtonView(file_name))
        
    async def send_video_message(file_name: str):
        await channel.send(f"{getenv("OBJECT_STORAGE_URL")}/data/{quote(file_name)}")

    if not upload_request.permanent:
        upload_requests.remove(upload_request)

    client.loop.create_task(send_message(embed))
    
    # Video preview - needs to be sent in a separate message in order to be displayed by Discord
    if content_type.startswith("video/"):
        client.loop.create_task(send_video_message(file_name))
