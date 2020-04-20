"""
PyAudio Example: Make a wire between input and output (i.e., record a
few samples and play them back immediately).

This is the callback (non-blocking) version.
"""
import pyaudio
import wave
import time
import struct

CHUNK = 1024
FORMAT = pyaudio.paFloat32
WIDTH = 2
CHANNELS = 1
RATE = 44100

# instantiate PyAudio
p = pyaudio.PyAudio()

def callback(in_data, frame_count, time_info, status):
    # print(struct.unpack(str(1024)+'B', in_data))
    return (in_data, pyaudio.paContinue)

# open stream
#format=p.get_format_from_width(WIDTH),
stream = p.open(format=FORMAT,
                channels=CHANNELS,
                rate=RATE,
                input=True,
                output=True)#,
                #stream_callback=callback)

stream.start_stream()

while stream.is_active(): #while song is not over
    data = stream.read(CHUNK)
    print(len(data))
    print(struct.unpack('4096B', data))
    time.sleep(0.1)

stream.stop_stream()
stream.close()

p.terminate()
