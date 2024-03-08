import time

from tactigon_gear import TSkin, TSkinConfig, Hand, OneFingerGesture

def main():
    TSKIN_MAC = "change-me"
    tskin_cfg = TSkinConfig(TSKIN_MAC, Hand.RIGHT) # Hand.LEFT if the TSkin is wear on left hand.

    tskin = TSkin(tskin_cfg)
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
        t = tskin.touch
        acc = tskin.acceleration
        gyro = tskin.gyro

        print(a, t, acc, gyro)

        if t and t.one_finger == OneFingerGesture.TAP_AND_HOLD:
            i += 1
        else:
            i = 0

        time.sleep(0.02)

    tskin.terminate()

        
if __name__ == "__main__":
    main()
