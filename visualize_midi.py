import midi
from names import NoteOn, NoteOff, End
from audiolazy import midi2str


def extract_notes(filename):
    '''
    input:
        - filename: path to midi file
    output:
        - notes: list of notes in chronological order, one timestep per note note: (pitch, loudness)
                 all on notes will have a loudness of 1, and all off notes will
                 have a loudness of 0, which will correlate with graph opacity later
        - ticks: tick number for each note
    '''
    pattern = midi.read_midifile(filename)
    print(pattern)
    notes = []

    total = 0
    for track in pattern:
        for event in track:
            for i in range(event.tick):
                total += 1
                if (event.name == NoteOn):
                    pitch = event.get_pitch()
                    # normalize notes by removing octave (2 octaves ok?)
                    norm_pitch = pitch%24
                    # for comparision purposes
                    print(midi2str(pitch))
                    print(midi2str(norm_pitch))
                    notes.append((norm_pitch, 1))
                else:
                    notes.append((0, 1))
    ticks = [i for i in range(total)]
    return notes, ticks

def animate_midi(filename):
    x_data, y_data = extract_notes(filename)

# print(extract_notes("example.mid"))
