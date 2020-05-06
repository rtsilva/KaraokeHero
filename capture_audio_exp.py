# import pyaudio
# import pylab
# import time
# import sys
# import matplotlib.pyplot as plt
# import numpy as np

# import sounddevice as sd
# #from audiolazy import freq2midi
# #import aubio


# RATE = 48000 #44100
# CHUNK = 1024*4 #int(RATE/20)#1024*4 #2048
# FORMAT = pyaudio.paInt16
# CHANNELS = 1
# ###
# # HOP_SIZE                = CHUNK//2
# # PERIOD_SIZE_IN_FRAME    = HOP_SIZE
# #METHOD                  = "default"


# def soundplot(stream):
#     t1=time.time()
#     data = np.fromstring(stream.read(CHUNK),dtype=np.int16)
#     print(stream.read(CHUNK))
#     print(data)

#     pylab.plot(data)
#     pylab.title(i)
#     pylab.grid()
#     pylab.axis([0,len(data),-2**16/2,2**16/2])
#     pylab.savefig("03.png",dpi=50)
#     pylab.close('all')
#     print("took %.02f ms"%((time.time()-t1)*1000))

# if __name__=="__main__":
#     p=pyaudio.PyAudio()
#     try:
#         # stream=p.open(format=FORMAT,channels=CHANNELS,rate=RATE,input=True,
#         #             frames_per_buffer=CHUNK,input_device_index=0)
#         stream=sd.InputStream(channels=CHANNELS,samplerate=RATE,dtype =np.int16,
#                      blocksize=CHUNK,device=0)
#         print("hiihihihih")
#         for i in range(sys.maxsize**10):
#             soundplot(stream)
#             time.sleep(2)
#         print("sad")
#         stream.stop_stream()
#         stream.close()
#         p.terminate()
#     except Exception as e:
#         print(type(e).__name__ + ': ' + str(e))


# import sounddevice as sd
# fs = 44100

# duration = 10.5  # seconds
# myrecording = sd.rec(int(duration * fs), samplerate=fs, channels=1)



import argparse
import tempfile
import queue
import sys

import sounddevice as sd
import soundfile as sf
import numpy  # Make sure NumPy is loaded before it is used in the callback
assert numpy  # avoid "imported but unused" message (W0611)


try:
    q = queue.Queue()

    #device_info = sd.query_devices(args.device, 'input')
    samplerate = 44100 #int(device_info['default_samplerate'])
    filename = tempfile.mktemp(prefix='delme_rec_unlimited_',
                                        suffix='.wav', dir='')

    # Make sure the file is opened before recording anything:
    with sf.SoundFile(filename, mode='x', samplerate=samplerate,
                      channels=1, subtype='PCM_16') as file:
        with sd.InputStream(samplerate=samplerate, device=0,
                            channels=1): #, callback=False
            print('#' * 80)
            print('press Ctrl+C to stop the recording')
            print('#' * 80)
            while True:
                file.write(q.get())
except KeyboardInterrupt:
    print('\nRecording finished: ' + repr(filename))
except Exception as e:
    print(type(e).__name__ + ': ' + str(e))
