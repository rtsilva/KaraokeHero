"""
PyAudio Example: Make a wire between input and output (i.e., record a
few samples and play them back immediately).

This is the callback (non-blocking) version.
"""
import pyaudio
import time

import aubio
import numpy as np

from audiolazy import freq2midi


CHUNK = 2048 #1024
FORMAT = pyaudio.paFloat32
WIDTH = 2
CHANNELS = 1
RATE = 44100
###
HOP_SIZE                = CHUNK//2
PERIOD_SIZE_IN_FRAME    = HOP_SIZE
METHOD                  = "default"


# instantiate PyAudio object
p = pyaudio.PyAudio()

# open mic stream
mic = p.open(format=FORMAT,
                channels=CHANNELS,
                rate=RATE,
                input=True,
                frames_per_buffer=PERIOD_SIZE_IN_FRAME)

# Initiating Aubio's pitch detection object.
pDetection = aubio.pitch(METHOD, CHUNK, HOP_SIZE, RATE)
# Set unit.
pDetection.set_unit("Hz")
# Frequency under 5 dB will considered
# as a silence (8 dB is a C1 or midi#0)
pDetection.set_silence(-40)


while mic.is_active():
    # Always listening to the microphone.
    data = mic.read(PERIOD_SIZE_IN_FRAME)
    print(data)
    # Convert into number that Aubio understand.
    samples = np.fromstring(data, dtype=aubio.float_type)
    # Finally get the pitch.
    pitch = pDetection(samples)[0]

    midi = freq2midi(pitch)

    print(str(pitch)+" "+str(midi))

mic.stop_stream()
mic.close()

p.terminate()
