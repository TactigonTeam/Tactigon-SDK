import asyncio
from threading import Thread, Event
from bleak import BleakScanner
from flask import Flask, url_for
from flask_socketio import SocketIO, emit

from typing import Optional

from tactigon_gear import TSkin, OneFingerGesture

class SocketApp(SocketIO):
    _TICK: float = 0.02
    socket_thread: Optional[Thread]
    _stop_event: Event
    _admin: Optional[str] = None

    def __init__(self, app: Optional[Flask] = None, **kwargs):
        SocketIO.__init__(self, app, **kwargs)

        self.socket_thread = None
        self._stop_event = Event()
        self._stop_event.set()

        @self.on("scan")
        def scan():
            async def find_devices():
                devices = await BleakScanner.discover()
                return filter(lambda d: str(d.name).startswith("TACTI") , devices)

            devices = asyncio.run(find_devices())
            tskins = [{"name": d.name, "address": d.address, "url": url_for("main.device", address=d.address)} for d in devices]

            emit("devices", tskins)

        if app:
            self.init_app(app)

    def init_app(self, app: Flask, admin: Optional[str] = None):
        super().init_app(app)
        self._admin = admin
        app.extensions["socket_app"] = self

    def emit_tskin_state(self, tskin: TSkin, operator: Optional[str] = None):
        self._stop_event.clear()
        self.socket_thread = self.start_background_task(self.socket_emit_function, tskin, operator)

    @property
    def is_running(self) -> bool:
        return not self._stop_event.is_set()

    def stop(self):
        self._stop_event.set()

    def socket_emit_function(self, tskin: TSkin, operator: Optional[str] = None):
        while not self._stop_event.is_set():
            t = tskin.touch
            a = tskin.angle
            g = tskin.gesture
            payload = {
                "isAdmin": operator == self._admin,
                "tskin": {
                    "connected": tskin.connected,
                    "battery": tskin.battery,
                    "selector": tskin.selector.value,
                    "touchpad": {
                        "name": t.one_finger.name if t.one_finger is not OneFingerGesture.NONE else t.two_finger.name,
                        "x": t.x_pos,
                        "y": t.y_pos
                    }if t else None,
                    "angle": a.toJSON() if a else None,
                    "gesture": g.toJSON() if g else None
                }
            }

            self.emit("tskin_state", payload)
            self.sleep(self._TICK) # type: ignore