import time
import datetime
from os import path, getcwd
from tactigon_gear import TSkin, TSkinConfig, Hand, GestureConfig, OneFingerGesture

tskin: TSkin = None

def main():
    model_folder = getcwd()

    TSKIN_MAC = "C0:83:43:39:21:57"
    TSKIN_HAND = Hand.RIGHT # Hand.LEFT if hand is left
    TSKIN_NAME = "TSKIN"

    gesture_config = GestureConfig(
        path.join(model_folder, "examples", "gear","model.pickle"), 
        path.join(model_folder, "examples", "gear", "encoder.pickle"),
        "demo",
        datetime.datetime.now(),
        ["up","down","push","pull","twist","circle","swipe_r","swipe_l"]
    )

    global tskin
    tskin = TSkin(TSkinConfig(TSKIN_MAC, TSKIN_HAND, TSKIN_NAME, gesture_config))
    tskin.start()

    print(f"connecting tskin {tskin}")

    while not tskin.connected:
        pass

    i = 0

    while True:
        if not tskin.connected:
            print("Connecting...")
            time.sleep(0.2)
            continue

        if i > 5:
            break

        t = tskin.touch
        a = tskin.angle
        g = tskin.gesture

        print(a)

        if g or t:
            print(g if g else t)
            time.sleep(1)

        if t and t.one_finger == OneFingerGesture.TAP_AND_HOLD:
            i += 1
        else:
            i = 0

        time.sleep(0.02)

    print("exit")

    tskin.terminate()


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        if tskin and tskin.connected:
            tskin.terminate()