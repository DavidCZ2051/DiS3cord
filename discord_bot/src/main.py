if __name__ == "__main__":
    from bot import client
    from web_interface import app
    from os import getenv
    import threading

    def run_flask():
        app.run(host="0.0.0.0", port=5000)

    def run_discord():
        client.run(getenv("DISCORD_TOKEN"))

    flask_thread = threading.Thread(target=run_flask)
    discord_thread = threading.Thread(target=run_discord)

    flask_thread.start()
    discord_thread.start()

    flask_thread.join()
    discord_thread.join()
