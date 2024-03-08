import time
import struct
import pyaudio

from multiprocessing import Pipe
from threading import Thread, Event
from collections import deque

from tactigon_gear import TSkin, TSkinConfig, Hand, OneFingerGesture

class ADPCMEngine(object):
    """DPCM Engine class.
    It contains all the operations and parameters necessary to decompress the
    received audio.
    """
    
    DATA_LENGTH_BYTES = 20
    AUDIO_PACKAGE_SIZE = 40
    
    def __init__(self): 
        """Constructor."""

        # Quantizer step size lookup table .
        self._step_size_table=[7,8,9,10,11,12,13,14,16,17,
            19,21,23,25,28,31,34,37,41,45,
            50,55,60,66,73,80,88,97,107,118,
            130,143,157,173,190,209,230,253,279,307,
            337,371,408,449,494,544,598,658,724,796,
            876,963,1060,1166,1282,1411,1552,1707,1878,2066,
            2272,2499,2749,3024,3327,3660,4026,4428,4871,5358,
            5894,6484,7132,7845,8630,9493,10442,11487,12635,13899,
            15289,16818,18500,20350,22385,24623,27086,29794,32767]

        # Table of index changes.
        self._index_table = [-1,-1,-1,-1,2,4,6,8,-1,-1,-1,-1,2,4,6,8]
        
        self._index = 0
        self._pred_sample = 0

    def decode(self, code) -> int: 
        """ADPCM_Decode.
        
        Args:
            code (byte): It contains a 4-bit ADPCM sample.
        
        Returns:
            int: A 16-bit ADPCM sample.
        """
        # 1. get sample
        step = self._step_size_table[self._index]

        # 2. inverse code into diff 
        diffq = step>> 3
        if ((code&4)!=0):
            diffq += step
        
        if ((code&2)!=0):
            diffq += step>>1
        

        if ((code&1)!=0):
            diffq += step>>2

        # 3. add diff to predicted sample
        if ((code&8)!=0):
            self._pred_sample -= diffq
        
        else:
            self._pred_sample += diffq
        
        # check for overflow
        if (self._pred_sample > 32767):
            self._pred_sample = 32767

        elif (self._pred_sample < -32768):
            self._pred_sample = -32768

        # 4. find new quantizer step size 
        self._index += self._index_table [code]
        #check for overflow
        if (self._index < 0):
            self._index = 0
            
        if (self._index > 88):
            self._index = 88

        # 5. save predict sample and index for next iteration 
        # done! static variables 

        # 6. return speech sample
        return self._pred_sample
    
    def extract_data(self, data: bytearray) -> bytes:
        """Extract the data from the feature's raw data.

        Args:
            data (bytearray): The data read from the feature (a 20 bytes array).
        """
              
        decoded_data = [0] * self.AUDIO_PACKAGE_SIZE
        for x in range(0, int(self.AUDIO_PACKAGE_SIZE / 2)):
            decoded_data[2*x] = self.decode((data[x] & 0x0F))
            decoded_data[(2*x)+1] = self.decode(((data[x] >> 4) & 0x0F))
        
        return b''.join(map(self.int16_to_bytes, decoded_data))

    @staticmethod
    def int16_to_bytes(value: int) -> bytes:
        return struct.pack("<i", value)[0:2]

class TSkinAudio(TSkin):
    """TSkin Audio class.
    It contains all the methods and parameters to stream audio from TSkin
    """

    SAMPLE_WIDTH = 2
    N_CHANNEL = 1
    FRAMERATE = 16000

    def __init__(self, config: TSkinConfig, debug: bool = False):
        """
        This constructor must be called with the following parameters:

        *config* a TSkinConfig object.

        *debug* a boolean to debug bluetooth configurations and actions
        """
        self.adpcm = ADPCMEngine()
        self.adpcm_rx, self.adpcm_tx = Pipe(duplex=False)

        TSkin.__init__(self, config, debug)

        self.stop_flag = Event()
        self.audio_flag = Event()
        self.audio_stream = deque()

        self.audio_thread = Thread(target=self.handle_audio, daemon=True)
        self.audio_thread.start()

    @property
    def has_audio(self):
        """
        A boolean indicating if it is storing some audio
        """
        return len(self.audio_stream) > 0

    def select_sensors(self) -> None:
        """
        Set the selector for reading sensor charateristics
        """
        self.audio_flag.clear()
        TSkin.select_sensors(self)

    def select_voice(self) -> None:
        """
        Set the selector for reading voice charateristics
        """
        TSkin.select_voice(self)
        self.audio_flag.set()

    def handle_audio(self):
        """
        The routine that reads audio from the background process pipe and save the audio stream in memory
        """
        if not self.adpcm_rx:
            return
        while not self.stop_flag.is_set():
            if self.audio_flag.is_set():
                while self.adpcm_rx.poll():
                    self.audio_stream.append(self.adpcm.extract_data(self.adpcm_rx.recv()))
            
                time.sleep(0.02)
            else:
                time.sleep(0.1)

    def play(self):
        """
        Plays the in memory audio stream, if present.
        """

        if len(self.audio_stream) == 0:
            return

        p = pyaudio.PyAudio()  
        stream = p.open(format = p.get_format_from_width(self.SAMPLE_WIDTH),  
                        channels = self.N_CHANNEL,  
                        rate = self.FRAMERATE,  
                        output = True) 
            
        for frame in self.audio_stream:
            stream.write(frame)
        
        stream.stop_stream()
        stream.close()
        p.terminate()

    def record(self, seconds: float):
        """
        Records a new audio stream.

        *seconds* the number of seconds to record
        """

        self.audio_stream.clear()

        self.select_voice()
        time.sleep(seconds)
        self.select_sensors()

    def terminate(self):
        """
        Gracefully shut down the TSkin interface
        """
        self.stop_flag.set()
        self.audio_thread.join(1)
        TSkin.terminate(self)

def main():
    TSKIN_MAC = "change-me"
    tskin_cfg = TSkinConfig(TSKIN_MAC, Hand.RIGHT) # Hand.LEFT if the TSkin is wear on left hand.

    tskin = TSkinAudio(tskin_cfg, False)
    tskin.start()

    i = 0
    while not tskin.connected:
        print("Connecting..")
        time.sleep(0.5)
    
    print("Connected!")

    while True:
        if not tskin.connected:
            print("Reconnecting..")
            time.sleep(0.5)
            continue

        if i > 2:
            break

        a = tskin.angle
        t = tskin.touch

        if t:
            if t.one_finger == OneFingerGesture.TAP_AND_HOLD:
                i += 1
            elif t.one_finger == OneFingerGesture.SINGLE_TAP:
                if tskin.has_audio:
                    print("Play")
                    tskin.play()
                    print("Done!")
                else:
                    print("Record 5 seconds of audio")
                    tskin.record(5)
                    print("Done!")
        else:
            i = 0

        time.sleep(0.02)

    print("Disconnecting...")
    tskin.terminate()
    print("Bye!")
        
if __name__ == "__main__":
    main()
