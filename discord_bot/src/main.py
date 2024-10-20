if __name__ == "__main__":
    from bot import client
    from web_interface import app
    from os import getenv
    from threading import Thread

    def run_web():
        app.run(host="0.0.0.0", port=5000)

    def run_discord():
        client.run(getenv("DISCORD_TOKEN"))

    web_thread = Thread(target=run_web)
    discord_thread = Thread(target=run_discord)

    web_thread.start()
    discord_thread.start()

    web_thread.join()
    discord_thread.join()
