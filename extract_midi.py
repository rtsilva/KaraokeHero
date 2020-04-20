import midi
from audiolazy import midi2str

from names import NoteOn, NoteOff, End

pattern = midi.read_midifile("example.mid")

for track in pattern:
    for event in track:
        if (event.name == NoteOn):
            pitch = event.get_pitch()
            print(midi2str(pitch))
        elif(event.name == NoteOff):
            print(event.get_pitch())
