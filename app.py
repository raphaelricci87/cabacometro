import os
from flask import Flask
from controllers.twitch_controller import TwitchBot
from views.vote_view import create_app

# Inicializar o Flask e integrar com o Twitch
flask_app = create_app()
twitch_bot = TwitchBot()

def start():
    # Iniciar o servidor Flask em uma thread separada
    from threading import Thread
    Thread(target=lambda: flask_app.run(host='0.0.0.0', port=5000, debug=False)).start()

    # Iniciar o bot do Twitch
    twitch_bot.run()

if __name__ == "__main__":
    start()
