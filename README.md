# Tactigon SDK

This repository contains the Tactigon SDK interface for using Tactigon Gear SDK.
It is compatible with Tactigon Gear v. >= 5.0.3

## Architecture

Tactigon SDK is built upon Tactigon Gear python libraries.

![Tactigon SDK architecture definition](https://www.thetactigon.com/wp/wp-content/uploads/2023/11/Architecture_Tactigon_SDK.png "Tactigon SDK architecture definition")

To install Tactigon-Gear run

```
pip install tactigon-gear
```

## CLI
The Command Line Interface (CLI) is a simple interface that allow the user to collect, label and upload motion data. The server then generates a gesture model
that can be loaded inside of the Tactigon Gear to have gesture recognition.

## Examples
This repository has few example on how to use Tactigon Gear SDK:
 - Scan.py: a small script to find your device MAC address (or device UUID on macOS)
 - ble.py: a small script to check data streaming from Tactigon Skin
 - gesture: a small application that enables you to detect gestures executed from your Tactigon Skin
 - Flask: a small flask application that enables you to get data from your Tactigon Skin using websocket

## Links
:house: [Homepage](https://www.thetactigon.com)

:notebook: [Quick start guide](https://github.com/TactigonTeam/Tactigon-Soul/wiki)

:memo: [Tactigon Gear](https://pypi.org/project/tactigon-gear/)


