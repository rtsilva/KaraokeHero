# Karaoke Hero 
## Final project for 6.835 Multimodal User Interfaces

Karaoke is a interactive karaoke coach which allows users to see the notes of a song juxtaposed with their own voice in real time.

## Libraries Used + Installation Requirements

- python midi
	- run pip install git+https://github.com/vishnubob/python-midi@feature/python3

- python audiolazy
	- run pip install audiolazy

- python pyaudio
	- $ brew install portaudio
	- $ pip install pyaudio

	- once installed, check to see if there is at least one input and output device:
	- $ python
	- `>>> import pyaudio`
	- `>>> pa = pyaudio.PyAudio()`
	- `>>> pa.get_default_input_device_info()`
	- `>>> pa.get_default_output_device_info()`

<!-- - python tkinter
	- should already be installed, run the following to check:
	- $ python -m tkinter
-->

- python  aubio
	- $ pip install aubio

- python OpenCV (cv2)
	- pip install opencv-python

- python vlc (I scoured the interwebs to try and get this to work... last command alone might be enough)
	- pip install python-vlc
	- pip install --upgrade billiard
	- pip install --upgrade celery
	- pip install --upgrade kombu
	- pip install --upgrade amqp
	- pip install --upgrade redis
	- brew cask install vlc

- pygame
	- pip install pygame

- ffmpeg (for mp4 making)
	- brew install ffmpeg

- moviepy
	- pip install moviepy

<!-- - python cocoa
	- >>> pip install pycocoa -->
