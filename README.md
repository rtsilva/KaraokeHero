# Karaoke Hero
## Final project for 6.835 Multimodal User Interfaces

KaraokeHero is a interactive karaoke coach which allows users to see the notes of a song juxtaposed with their own voice in real time. Created in Python 3.6, and tested only on macOS.

In order to run the program, simply download all code, and in terminal, run the following:
python main.py

## Code Summary

### Code Related to Final Edition

main.py - instantiates application
classes.py - defines application and calls necessary helper classes and functions
midi_anim.py - parses and extracts necessary information from a MIDI file
\*.mid - MIDI files
\*.mp4 - MP4 files
media - contains ogg and mp3 versions of audio files
output - holds mp4 version of animation (if relevant code is run)
tmp_images - images used to create output's mp4
options.cfg - defines values for midi_anim
values.py - defines colors for UI

### Code Related to Prior Iterations

app.py - defines the application utilizing tkinter format
pages.py - defines pages of the application, calling necessary helper functions
visualize_midi - extracts MIDI information and user audio to visualize the beatmap
extract_midi.py - provides guidance on reading a MIDI file
gen_midi.py - provides guidance on generating a MIDI file
capture_audio.py/capture_audio_exp.py - provides guidance on audio manipulation
note.py - defines a note to help with MIDI parsing
names.py - defines variable names
Screen.py - attempts to embed a vlc screen widget in tkinter

## Libraries Used + Installation Requirements

- python midi
	- run pip install git+https://github.com/vishnubob/python-midi@feature/python3

- python audiolazy
	- run pip install audiolazy

- python pyaudio
	- brew install portaudio
	- pip install pyaudio

	- once installed, check to see if there is at least one input and output device:
	- python
	- `>>> import pyaudio`
	- `>>> pa = pyaudio.PyAudio()`
	- `>>> pa.get_default_input_device_info()`
	- `>>> pa.get_default_output_device_info()`

- python tkinter
	- should already be installed, run the following to check:
	- $ python -m tkinter

- python aubio
	- $ pip install aubio

- python OpenCV (cv2)
	- pip install opencv-python

- python vlc
	- pip install python-vlc
	- brew cask install vlc

- pygame
	- pip install pygame

- ffmpeg (for mp4 making)
	- brew install ffmpeg

- moviepy
	- pip install moviepy

<!-- - python cocoa
	- >>> pip install pycocoa -->
