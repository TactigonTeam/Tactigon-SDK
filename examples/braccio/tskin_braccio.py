import datetime
import multiprocessing
import time
from os import path, getcwd

from tactigon_arduino_braccio import Braccio, BraccioConfig, Wrist, Gripper
from tactigon_gear import TSkin, TSkinConfig, Hand, GestureConfig, OneFingerGesture, TwoFingerGesture


def create_tskin() -> TSkin:
    model_folder = getcwd()

    # TSKIN CONFIGURATION

    TSKIN_MAC = "TSkin Mac address"

    # Do not change the code below unless absolutely necessary.
    TSKIN_HAND = Hand.RIGHT
    TSKIN_NAME = "TSKIN"

    gesture_config = GestureConfig(
        path.join(model_folder, "examples", "gear","model.pickle"), 
        path.join(model_folder, "examples", "gear", "encoder.pickle"),
        "demo",
        datetime.datetime.now(),
        ["up", "down", "push", "pull", "twist", "circle", "swipe_r", "swipe_l"]
    )

    tskin = TSkin(TSkinConfig(TSKIN_MAC, TSKIN_HAND, TSKIN_NAME, gesture_config))
    return tskin


def main():

    tskin = create_tskin()
    tskin.start()

    BRACCIO_MAC = "D1:EF:85:90:07:DE"

    # BRACCIO CONFIGURATION
    braccio_config = BraccioConfig(BRACCIO_MAC)

    with Braccio(braccio_config) as braccio:

        print("Connecting TSkin", tskin)
        while not tskin.connected:
            time.sleep(0.1)

        print("Connected TSkin")

        print("Connecting Braccio...")
        while not braccio.connected:
            time.sleep(0.1)

        print("Connected Braccio")

        x, y, z = 0, 0, 150
        wrist = Wrist.HORIZONTAL
        gripper = Gripper.CLOSE

        while True:
            modified = False

            if not tskin.connected:
                print("Connecting TSkin...")
                time.sleep(0.2)
                continue

            if not braccio.connected:
                print("Connecting Braccio...")
                time.sleep(0.2)
                continue

            t = tskin.touch
            a = tskin.angle
            g = tskin.gesture

            if g and g.gesture == "circle":
                break

            if g and g.gesture == 'up':
                z = 150
                modified = True

            if g and g.gesture == 'down':
                z = 0
                modified = True

            if g and g.gesture == 'twist':
                wrist = Wrist.VERTICAL if wrist == Wrist.HORIZONTAL else Wrist.HORIZONTAL
                modified = True

            if t and t.one_finger == OneFingerGesture.SINGLE_TAP:
                gripper = Gripper.OPEN if gripper == Gripper.CLOSE else Gripper.CLOSE
                modified = True

            if t and a and t.one_finger == OneFingerGesture.TAP_AND_HOLD:
                print(f"x = {x},y = {y}")

                # Y axis
                if 0 >= a.pitch >= -90:
                    new_y = int(abs(a.pitch) * 3.33)

                    if y != new_y:
                        y = new_y
                        modified = True

                # X axis
                if 40 >= a.roll >= -30:
                    new_x = abs(a.roll * 10) if a.roll < 0 else -int(a.roll * 7.5)

                    if x != new_x:
                        x = new_x
                        modified = True

            if modified:
                res, status, braccio_time = braccio.move(x, y, z, wrist, gripper)

                if res:
                    print("Command Succeeded")
                else:
                    print("Command Failed")

            time.sleep(0.02)

        print("Disconnected")
        braccio.home()
        tskin.terminate()


if __name__ == "__main__":
    multiprocessing.freeze_support()
    main()
