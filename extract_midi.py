import midi
from audiolazy import midi2str

from names import NoteOn, NoteOff, End

pattern = midi.read_midifile("twinkle-twinkle-little-star.mid")

for track in pattern:
    print("Next Track")
    for event in track:
        print("Next Event")
        if (event.name == NoteOn):
            pitch = event.get_pitch()
            # this is how loud the sound is, in the range (0, 127)
            # velocity = event.data[1]
            print("Note:",midi2str(pitch))
        elif(event.name == NoteOff):
            print("Silence")
        elif(event.name == End):
            print("End of Event")
        print("Length of time:", event.tick)
