import time

from tactigon_arduino_braccio import Braccio, BraccioConfig, Wrist, Gripper

if __name__ == "__main__":
    cfg = BraccioConfig("D1:EF:85:90:07:DE")

    with Braccio(cfg) as braccio:

        print("Connecting...")
        while not braccio.connected:
            time.sleep(0.1)

        print("Connected!")
        
        x = 120
        y = 50
        z = 150
        wrist = Wrist.HORIZONTAL
        gripper = Gripper.OPEN
        res, status, time = braccio.move(x, y, z, wrist, gripper)

        print(res, status, time)

    print("disconnected")