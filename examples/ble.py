import time

from tgear_sdk import TSkin
from tgear_sdk.models import TSkinConfig, Button

def main():
    TSKIN_MAC = "change-me"
    tskin_cfg = TSkinConfig(TSKIN_MAC)

    tskin = TSkin(tskin_cfg, debug=True)
    tskin.start()

    i = 0

    while True:
        if not tskin.connected:
            print("Connecting..")
            time.sleep(0.5)
            continue

        if i > 5:
            break

        a = tskin.angle
        b = tskin.button
        acc = tskin.acceleration
        gyro = tskin.gyro

        print(a, b, acc, gyro)

        if b == Button.CIRCLE:
            tskin.select_voice()
            time.sleep(5)
            tskin.select_sensors()

        if b == Button.TRIANGLE:
            i += 1

        time.sleep(0.1)

    tskin.terminate()

        
if __name__ == "__main__":
    main()
