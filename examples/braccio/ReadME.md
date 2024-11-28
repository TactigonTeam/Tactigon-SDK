# Control Arduino Braccio device using Tactigon Skin

This README provides instructions to help you understand how to control the Arduino Braccio device using the Tactigon Skin device.

## Overview

The Tactigon Skin is a device that recognizes hand gestures and finger movements, allowing users to interact with various technologies in an intuitive way. The Braccio is a programmable mechanical arm that mimics the functions of a human arm. By connecting the Tactigon Skin to the Braccio via Bluetooth, users can control the Braccio arm using specific gestures made with their hands. This setup opens up innovative ways to operate the arm, making it accessible and interactive.

Here are some of the gestures and their corresponding actions:

 - SINGLE_TAP - Controls the opening and closing of the robotic gripper.
 - UP GESTURE - Moves the arm up within the Z axis.
 - DOWN GESTURE - Moves the arm down within the Z axis.
 - TWIST GESTURE - Rotates the Braccio wrist.
 - TAP_AND_HOLD - Moves the arm within the XY directions, by combination of the base and shoulder.
 - CIRCLE GESTURE - Terminate the Program.


## Hardware Requirements
- Braccio device: Ensure that you have a compatible Braccio device with Bluetooth module installed
- Tactigon Skin device: You need a Tactigon Skin device with you to control the Braccio device
- Bluetooth: Ensure you need a Bluetooth-enabled computer with a python installed.

## Software Requirements
- Python 3.8
- tactigon_arduino_braccio==1.0.0
- tactigon_gear==5.0.3


## Initial Configuration

You need both device's Bluetooth addresses inorder to connect. 

1. **You can run the following code to see the Mac addresses of both devices.**
```python
import argparse
import asyncio

from bleak import BleakScanner

async def main(args: argparse.Namespace):
    print("scanning for 5 seconds, please wait...\n")

    devices = await BleakScanner.discover(
        return_adv=True, cb=dict(use_bdaddr=args.macos_use_bdaddr)
    )

    for d, a in devices.values():
        name = str(d.name)
        if "TSKIN" in name or "ADA" in name:
            print(d)
            print("-" * len(str(d)))
            print(a)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()

    parser.add_argument(
        "--macos-use-bdaddr",
        action="store_true",
        help="when true use Bluetooth address instead of UUID on macOS",
    )

    args = parser.parse_args()

    asyncio.run(main(args))
```

2. **You can insert your Mac addresses where you can see "I need a Mac address".**

```python
def create_tskin() -> Tactigon Skin:
    model_folder = getcwd()

    # Tactigon Skin CONFIGURATION
    TSKIN_MAC = "I need a Mac address"
```

```python
def main():

    Tactigon Skin = create_tskin()
    Tactigon Skin.start()

    # BRACCIO CONFIGURATION
    braccio_config = BraccioConfig("I need a Mac address)
```

3. **Now you should be able to control the Braccio using the Tactigon Skin device. Have fun with robotics :)**

## Code Explanation

```python
def create_tskin() -> Tactigon Skin:
    model_folder = getcwd()
    
    TSKIN_MAC = "I need a Mac address"

    # Do not change the code below unless absolutely necessary. 
    TSKIN_HAND = Hand.RIGHT 
    TSKIN_NAME = "Tactigon Skin"
    
    gesture_config = GestureConfig(
        path.join(model_folder, "model.pickle"),
        path.join(model_folder, "encoder.pickle"),
        "demo",
        datetime.datetime.now(),
        ["up", "down", "push", "pull", "twist", "circle", "swipe_r", "swipe_l"]
    )

    Tactigon Skin = Tactigon Skin(TSkinConfig(TSKIN_MAC, TSKIN_HAND, TSKIN_NAME, gesture_config))
    return Tactigon Skin
```

The above function creates the Tactigon Skin object and returns to the main method. Here you can see the all the configurations related to Tactigon Skin device. 

```python
    if g and g.gesture == 'up':
        break
```

As you can see in each loop, we get t (touch), g (gesture), and a (angle). Then we check if the gesture is up, if it is then we break the loop. so if you want to terminate the program you can use up gesture to terminate the program.

```python
            if t and a and t.one_finger == OneFingerGesture.TAP_AND_HOLD:
                print(f"x = {x},y = {y}")

                # Y axis
                if 0 >= a.pitch >= -90:
                    new_y = int(abs(a.pitch) * 3.33)

                    if y != new_y:
                        y = abs(a.pitch) * 3
                        modified = True

                # X axis
                if 40 >= a.roll >= -30:
                    new_x = abs(a.roll * 10) if a.roll < 0 else -int(a.roll * 7.5)

                    if x != new_x:
                        x = new_x
                        modified = True
```

As we mentioned before, in each loop, we get **t** (touch), **g** (gesture), and **a** (angle) values. Inside this if statement we map **pitch** and **roll** into **Y** and **X** axis.

In this script, we utilize an if statement to verify whether the pitch and roll values fall within a specific range. If they do, we proceed to calculate new x and y values and set a variable called modified to True. In each iteration of the loop, we check if modified is True. If it is, we send a command to the Braccio device.
## Contributing
We welcome contributions to this project. Please follow the standard fork-and-pull request workflow.

## Links
🏠 - [Tactigon Home](https://www.thetactigon.com/) <br />
📝 - [Tactigon Gear](https://pypi.org/project/tactigon-gear/)  <br />
📔 - [Tactigon Speech](https://pypi.org/project/tactigon-speech/)  <br />

## Conclusion 
We hope you find the integration of Tactigon Skin and Braccio both innovative and intuitive, enhancing your ability to interact with technology through natural hand gestures. This setup is designed to make the control of the Braccio arm more accessible and engaging, whether for educational purposes, automation tasks, or hobbyist projects. 

You can enhance this project further by integrating voice commands using our Tactigon Speech package.

Let's continue to push the boundaries of what's possible with gesture-controlled technology together!



## Contact Information
Your feedback and contributions are invaluable as we continue to refine and expand the capabilities of these devices.
For further inquiries, contact us via email at info@thetactigon.com