import midi
import numpy as np

from matplotlib import pyplot as plt
from matplotlib.animation import FuncAnimation

from names import NoteOn, NoteOff, End
from audiolazy import midi2str


def extract_notes(filename):
    '''
    input:
        - filename: path to midi file
    output:
        - ticks: tick number for each note
        - notes: list of notes in chronological order, one timestep per note note: (pitch, loudness)
                 all on notes will have a loudness of 1, and all off notes will
                 have a loudness of 0, which will correlate with graph opacity later
    '''
    pattern = midi.read_midifile(filename)
    # print(pattern)
    notes = []

    total = 0
    for track in pattern:
        for event in track:
            for i in range(event.tick):
                total += 1
                if (event.name == NoteOn):
                    pitch = event.get_pitch()

                    # normalize notes by removing octave (1 octave ok?)
                    norm_pitch = pitch%12

                    # for comparision purposes
                    # print(midi2str(pitch))
                    # print(midi2str(norm_pitch))

                    notes.append((norm_pitch, 1))
                else:
                    notes.append((0, 0))
    ticks = [i for i in range(total)]
    return ticks, notes

def init_midi(filename):
    '''
    input:
        - filename: path to midi file
    output:
        - initializes figure
    '''
    x_data, y_data = extract_notes(filename)

    fig = plt.figure()
    ax = plt.axes(xlim=(0, 10), ylim=(0, 35))
    x = []
    y = []
    line, = ax.plot(x, y, 'bs', markersize=20)

    # add note lines for reference, can remove later
    plt.plot([0, 10], [30, 30], 'k-', lw=3)
    plt.plot([0, 10], [25, 25], 'k-', lw=3)
    plt.plot([0, 10], [20, 20], 'k-', lw=3)
    plt.plot([0, 10], [15, 15], 'k-', lw=3)
    plt.plot([0, 10], [10, 10], 'k-', lw=3)
    plt.plot([0, 10], [5, 5], 'k-', lw=3)

    return fig, x_data, y_data, line

def animate_midi(fig, x_data, y_data, line):
    '''
    input:
        - fig: where animation will be shown
    output:
        - shows plot of on notes of midi file with appropriate spacing. This animation
          can be saved as an mp4, or we can plot on top of it for our project.
    '''

    x_range = np.linspace(0,10,20)
    y_data_space = [(0,0) for i in range(10)] + y_data + [(0,0) for i in range(10)]

    def init():
        line.set_data([i for i in x_range], [0 for i in range(20)])
        return line,

    def animate(i):
        k = i
        l = i+10

        x = [j for j in x_range]
        y = [((y_data_space[j][0]+1)*2.5, y_data_space[j][1]) for j in range(k, l) for _ in range(2)]

        new_x = []
        new_y = []

        for i in range(20):
            # only take on notes
            if y[i][1] == 1:
                new_x.append(x[i])
                new_y.append(y[i][0])

        line.set_data(new_x, new_y)
        return line,

    # frames is number of notes we are showing, interval is time(ms) between each note
    anim = FuncAnimation(fig, animate, init_func=init,
                               frames=len(x_data) + 10, interval=100, blit=True, repeat = False)

    # plt.show()
    return None

fig, x_data, y_data, line = init_midi("example.mid")
animate_midi(fig, x_data, y_data, line)
