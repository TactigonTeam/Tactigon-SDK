import json
from datetime import datetime
from functools import wraps
from os import path, getcwd
from flask import Flask, current_app
from typing import Optional
from threading import Thread
from gevent.pywsgi import WSGIServer

from tactigon_gear import TSkin, TSkinConfig, Hand, GestureConfig
from extensions.socketio import SocketApp

def get_tskin() -> TSkin:
    base_folder = path.abspath(path.dirname(__file__))

    TSKIN_MAC = "change-me"
    TSKIN_HAND = Hand.RIGHT # Hand.LEFT
    TSKIN_NAME = "TSKIN"

    tskin_cfg = TSkinConfig(TSKIN_MAC, TSKIN_HAND, TSKIN_NAME, GestureConfig(
        path.join(base_folder, "model.pickle"),
        path.join(base_folder, "encoder.pickle"),
        "MODEL",
        datetime.now(),
        ["up","down","push","pull","twist","circle","swipe_r","swipe_l"]
    ))

    return TSkin(tskin_cfg)

def create_app():

    flask_app = Flask(__name__, template_folder="templates", static_folder="static")
    socket_app = SocketApp()

    with flask_app.app_context():

        flask_app.secret_key = b'_5#y2L"F4Q8z\n\xec]/'

        flask_app.extensions["tskin"] = get_tskin()
        flask_app.extensions["tskin"].start()

        socket_app.init_app(flask_app)
        socket_app.emit_tskin_state(flask_app.extensions["tskin"])

        import main

        flask_app.register_blueprint(main.bp)

    return flask_app

class GuiApp(Thread):
    _app: Flask
    _server: WSGIServer

    def __init__(self, address: str, port: int):
        Thread.__init__(self, daemon=True)

        self.address = address
        self.port = port

    def run(self):
        self._app = create_app()
        self._server = WSGIServer((self.address, self.port), self._app)
        self._server.serve_forever()

    def stop(self):
        if "socket_app" in self._app.extensions and isinstance(self._app.extensions["socket_app"], SocketApp):
            if self._app.extensions["socket_app"].is_running:
                self._app.extensions["socket_app"].stop()

        if "tskin" in self._app.extensions and isinstance(self._app.extensions["tskin"], TSkin):
            self._app.extensions["tskin"].terminate()

        self._server.stop(5)
        Thread.join(self)

if __name__ == "__main__":
    print(F"Starting application test on 127.0.0.1:5001")
    app = GuiApp("127.0.0.1", 5001)
    app.start()

    input("Press any button to stop the application")

    app.stop()

