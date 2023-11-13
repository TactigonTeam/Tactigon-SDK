import json
from datetime import datetime
from functools import wraps
from os import path, getcwd
from flask import Flask, current_app
from flask_socketio import SocketIO, emit
from typing import Optional

from tactigon_speech import TSkin_Speech, TSkinConfig, VoiceConfig, AudioSource, TSpeechObject, TSpeech, HotWord
from tactigon_gear.models import Hand, GestureConfig

def get_tskin() -> TSkin_Speech:
    base_folder = path.abspath(path.dirname(__file__))

    TSKIN_MAC = "change-me"
    TSKIN_MAC = "C0:83:4B:32:4E:36"
    TSKIN_NAME = "TSKIN"

    tskin_cfg = TSkinConfig(TSKIN_MAC, TSKIN_NAME, GestureConfig(
        path.join(base_folder, "model.pickle"),
        path.join(base_folder, "encoder.pickle"),
        "MODEL",
        datetime.now(),
        ["up","down","push","pull","twist","circle","swipe_r","swipe_l"]
    ))
    voice_cfg = VoiceConfig(
        path.join(base_folder, "deepspeech-0.9.3-models.tflite"),
        path.join(base_folder, "0220_f.scorer"),
    )

    return TSkin_Speech(tskin_cfg, voice_cfg, AudioSource.TSKIN, debug=False)

def tspeech_obj():
    return TSpeechObject(
        [
            TSpeech(
                [HotWord("draw")],
                TSpeechObject(
                    [
                        TSpeech(
                            [HotWord("circle"), HotWord("triangle"), HotWord("box")]
                        )
                    ]
                )
            )
        ]
    )

socketio_app = SocketIO()

@socketio_app.on('connect')
def on_connect():
    resp = {
        "tskin_right": True,
        "tskin_left": False
    }

    emit("config", resp)

@socketio_app.on("tskin_connection")
def get_tskin_connection_state(req):
    hand = Hand(req["hand"])
    tskin_right: Optional[TSkin_Speech] = current_app.extensions["tskin_right"]
    tskin_left: Optional[TSkin_Speech] = current_app.extensions["tskin_left"]

    if hand == Hand.RIGHT and tskin_right:
        json_object = {
            "connected": tskin_right.connected,
            "selector": tskin_right.selector.value
        }

        emit("right_tskin_conn", json_object)
    elif hand == Hand.LEFT and tskin_left:
        json_object = {
            "connected": tskin_left.connected,
            "selector": tskin_left.selector.value
        }

        emit("left_tskin_conn", json_object)

@socketio_app.on("tskin_state")
def get_tskin_state(req):
    hand = Hand(req["hand"])
    tskin_right: Optional[TSkin_Speech] = current_app.extensions["tskin_right"]
    tskin_left: Optional[TSkin_Speech] = current_app.extensions["tskin_left"]

    if hand == Hand.RIGHT and tskin_right:
        emit("right_tskin_state", tskin_right.state.toJSON())
        tskin_right.transcription
    elif hand == Hand.LEFT and tskin_left:
        emit("left_tskin_state", tskin_left.state.toJSON())
        tskin_left.transcription
    else:
        pass


@socketio_app.on("voice_state")
def on_voice_state(req):
    hand = Hand(req["hand"])
    tskin_right: Optional[TSkin_Speech] = current_app.extensions["tskin_right"]
    tskin_left: Optional[TSkin_Speech] = current_app.extensions["tskin_left"]

    if hand == Hand.RIGHT and tskin_right:
        emit("right_voice_state", tskin_right.transcription.toJSON() if tskin_right.transcription else None)
    elif hand == Hand.LEFT and tskin_left:
        emit("left_voice_state", tskin_left.transcription.toJSON() if tskin_left.transcription else None)
    else:
        pass

@socketio_app.on("play")
def on_play(req):
    hand = Hand(req["hand"])
    filename = req["filename"]

    base_folder = path.abspath(path.dirname(__file__))
    
    tskin_right: Optional[TSkin_Speech] = current_app.extensions["tskin_right"]
    tskin_left: Optional[TSkin_Speech] = current_app.extensions["tskin_left"]

    if hand == Hand.RIGHT and tskin_right:
        tskin_right.play(path.join(base_folder, filename))
    elif hand == Hand.LEFT and tskin_left:
        tskin_left.play(path.join(base_folder, filename))

@socketio_app.on("listen")
def on_listen(req):
    hand = Hand(req["hand"])
    
    tskin_right: Optional[TSkin_Speech] = current_app.extensions["tskin_right"]
    tskin_left: Optional[TSkin_Speech] = current_app.extensions["tskin_left"]

    if hand == Hand.RIGHT and tskin_right:
        tskin_right.listen(tspeech_obj())
    elif hand == Hand.LEFT and tskin_left:
        tskin_left.listen(tspeech_obj())

@socketio_app.on("record")
def on_record(req):
    hand = Hand(req["hand"])
    filename = req["filename"]

    base_folder = path.abspath(path.dirname(__file__))
    
    tskin_right: Optional[TSkin_Speech] = current_app.extensions["tskin_right"]
    tskin_left: Optional[TSkin_Speech] = current_app.extensions["tskin_left"]

    if hand == Hand.RIGHT and tskin_right:
        tskin_right.record(path.join(base_folder, filename))
    elif hand == Hand.LEFT and tskin_left:
        tskin_left.record(path.join(base_folder, filename))

def create_app(debug: bool = True):

    flask_app = Flask(__name__, template_folder="templates", static_folder="static")

    with flask_app.app_context():

        flask_app.secret_key = b'_5#y2L"F4Q8z\n\xec]/'

        flask_app.extensions["tskin_right"] = get_tskin()
        flask_app.extensions["tskin_right"].start()
        # flask_app.extensions["tskin_right"] = None
        flask_app.extensions["tskin_left"] = None

        socketio_app.init_app(flask_app)

        import main

        flask_app.register_blueprint(main.bp)

    return flask_app

if __name__ == "__main__":
    app = create_app()
    app.run(debug=False)