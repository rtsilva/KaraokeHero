Karaoke Hero project for 6.835

Libraries Used + Installation Requirements

- python midi - run pip install git+https://github.com/vishnubob/python-midi@feature/python3

- python pyaudio - run the following commands: - $ brew install portaudio
		- $ pip install pyaudio

      	- once installed, check to see if there is at least one input and output device:
      		- $ python
      		- >>> import pyaudio
      		- >>> pa = pyaudio.PyAudio()
      		- >>> pa.get_default_input_device_info()
      		- >>> pa.get_default_output_device_info()
