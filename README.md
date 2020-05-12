# Karaoke Hero
## Final project for 6.835 Multimodal User Interfaces

KaraokeHero is a interactive karaoke coach which allows users to see the notes of a song juxtaposed with their own voice in real time. Created in Python 3.6, only tested on macOS.

In order to run the program, simply download all code, and in terminal, run the following:
python main.py

## Code Summary

### Code Related to Final Edition
main.py - instantiates application
classes.py - defines application and class necessary helper classes and functions
midi_anim.py - parses and extracts necessary information from a MIDI file
\*.mid - MIDI files
\*.mp4 - MP4 files
media - contains ogg and mp3 versions of audio files
output - holds mp4 version of animation (if relevant code is run)
tmp_images - images used to create output's mp4

### Code Related to Prior Iterations


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
