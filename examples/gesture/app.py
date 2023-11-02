import time
import datetime
import multiprocessing
import logging
from os import path
from typing import Optional
from tgear_sdk import TSkin
from tgear_sdk.models import TSkinConfig, Button, Angle, Gesture, GestureConfig

def main():
    model_folder = path.join(path.abspath("."))

    TSKIN_MAC = "change-me"
    TSKIN_NAME = "TSKIN"

    gmodel = GestureConfig(
        path.join(model_folder, "model.pickle"), 
        path.join(model_folder, "encoder.pickle"),
        "demo",
        datetime.datetime.now(),
        ["up","down","push","pull","twist","circle","swipe_r","swipe_l"]
    )

    tskin = TSkin(TSkinConfig(TSKIN_MAC, TSKIN_NAME, gmodel))
    tskin.start()

    print("connecting tskin", tskin)

    while not tskin.connected:
        pass

    while True:
        if not tskin.connected:
            print("Connecting...")
            time.sleep(0.2)
            continue

        b: Button = tskin.button
        a: Angle = tskin.angle
        g = tskin.gesture

        print(b, a, g)

        if b == Button.CIRCLE:
            break

        time.sleep(0.1)

    print("exit")

    tskin.terminate()


if __name__ == "__main__":
    main()