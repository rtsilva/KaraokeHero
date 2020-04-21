import midi
import numpy as np

from matplotlib import pyplot as plt
from matplotlib.animation import FuncAnimation

from names import NoteOn, NoteOff, End
from audiolazy import midi2str

x_r = 80

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
    notes = []

    total = 0
    for track in pattern:
        for event in track:
            # print(event.name)
            if (event.name == "Set Tempo"):
                event.set_bpm(event.data[0])
            for i in range(event.tick+1):
                if (event.name == NoteOn):
                    pitch = event.get_pitch()
                    # normalize notes by removing octave (1 octave ok?)
                    norm_pitch = pitch%12
                    # for comparision purposes
                    # print(midi2str(pitch))
                    # print(midi2str(norm_pitch))
                    notes.append((norm_pitch, 1))
                    total += 1
                elif (event.name == NoteOff):
                    notes.append((0, 0))
                    total += 1
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
    ax = plt.axes(xlim=(0, x_r), ylim=(0, 35))
    ax.axes.xaxis.set_visible(False)
    ax.axes.yaxis.set_visible(False)
    x = []
    y = []
    line, = ax.plot(x, y, 'bs', markersize=20)

    # add note lines for reference, can remove later
    plt.plot([0, x_r], [30, 30], 'k-', lw=3)
    plt.plot([0, x_r], [25, 25], 'k-', lw=3)
    plt.plot([0, x_r], [20, 20], 'k-', lw=3)
    plt.plot([0, x_r], [15, 15], 'k-', lw=3)
    plt.plot([0, x_r], [10, 10], 'k-', lw=3)
    plt.plot([0, x_r], [5, 5], 'k-', lw=3)
    plt.plot([10, 10], [0, 35], 'r-', lw=3)

    return fig, x_data, y_data, line

def animate_midi(fig, x_data, y_data, line):
    '''
    input:
        - fig: where animation will be shown
    output:
        - shows plot of on notes of midi file with appropriate spacing. This animation
          can be saved as an mp4, or we can plot on top of it for our project.
    '''

    x_range = np.linspace(0,x_r,x_r*2)
    y_data_space = [(0,0) for i in range(x_r)] + y_data + [(0,0) for i in range(x_r)]

    def init():
        line.set_data([i for i in x_range], [0 for i in range(x_r*2)])
        return line,

    def animate(i):
        k = i
        l = i+x_r

        x = [j for j in x_range]
        y = [((y_data_space[j][0]+1)*2.5, y_data_space[j][1]) for j in range(k, l) for _ in range(2)]

        new_x = []
        new_y = []

        for i in range(x_r*2):
            # only take on notes
            if y[i][1] == 1:
                new_x.append(x[i])
                new_y.append(y[i][0])

        line.set_data(new_x, new_y)
        return line,

    # frames is number of notes we are showing, interval is time(ms) between each note
    anim = FuncAnimation(fig, animate, init_func=init,
                               frames=len(x_data) + x_r, interval=1, blit=True, repeat = False)

    # plt.show()
    return None

# fig, x_data, y_data, line = init_midi("twinkle-twinkle-little-star.mid")
# animate_midi(fig, x_data, y_data, line)
