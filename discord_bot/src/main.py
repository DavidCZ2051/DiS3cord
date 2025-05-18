if __name__ == "__main__":
    from bot import client
    from os import getenv

    client.run(getenv("DISCORD_TOKEN"))
