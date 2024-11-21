import time

from os import path, getcwd

from tactigon_speech import TSkin_Speech, TSkinConfig, Hand, VoiceConfig, OneFingerGesture, TSpeechObject, TSpeech, HotWord

def tspeech_obj():
    return TSpeechObject(
        [
            TSpeech(
                [HotWord("start"), HotWord("enter")],
                TSpeechObject(
                    [
                        TSpeech(
                            [HotWord("application")]
                        )
                    ]
                )
            )
        ]
    )

def main():
    model_folder = getcwd()

    TSKIN_MAC = "change-me"
    tskin_cfg = TSkinConfig(TSKIN_MAC, Hand.RIGHT) # Hand.LEFT if the TSkin is wear on left hand.

    voice_cfg = VoiceConfig(
        path.join(model_folder, "examples", "speech", "models.tflite"), 
        path.join(model_folder, "examples", "speech", "tos.scorer"),
    )

    tskin = TSkin_Speech(tskin_cfg, voice_cfg)
    tskin.start()

    i = 0

    while not tskin.connected:
        print("Connecting..")
        time.sleep(0.5)
    
    print("Single Tap to enable listening mode")

    while True:
        if not tskin.connected:
            print("Reconnecting..")
            time.sleep(0.5)
            continue

        if i > 2:
            break

        if tskin.is_listening:
            print("Listening...")
            time.sleep(0.5)
            continue

        touch = tskin.touch
        transcription = tskin.transcription

        if transcription:
            if transcription.timeout:
                if transcription.time == 0:
                    print("Silence timeout. No words found for", voice_cfg.silence_timeout, "seconds")
                else:
                    print("Voice timeout. Cannot process more than", voice_cfg.voice_timeout, "seconds")
            else:
                print("Transcription found!")

            print(transcription)

        if touch:
            if touch.one_finger == OneFingerGesture.TAP_AND_HOLD:
                i += 1
            elif touch.one_finger == OneFingerGesture.SINGLE_TAP:
                if tskin.listen(tspeech_obj()):
                    print("Waiting for voice commands...")
                    print("Try to say:\n - Start application\n - Enter application\n")
        else:
            i = 0

        time.sleep(0.02)

    print("Disconnecting...")
    tskin.terminate()
    print("Bye!")


if __name__ == "__main__":
    main()
