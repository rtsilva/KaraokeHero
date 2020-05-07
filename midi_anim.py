# code provided by MajorThird https://github.com/MajorThird/quick-midi-animation/blob/master/main.py
import numpy as np
import cv2
import subprocess
import sys
import shutil
import os
import argparse
import configparser

import midi
import note
import pygame

main_screen_w = 1500
main_screen_h = 750

beat_screen_w = 1000
beat_screen_h = 300

def is_note_on(event):
    """
    Sometimes Note Offs are marked by
    event.name = "Note On" and velocity = 0.
    That's why we have to check both event.name and
    velocity.
    """
    velocity = event.data[1]
    return event.name == "Note On" and velocity > 0


def read_midi(filename):
    """
    Returns a list of tracks.
    Each track is a list containing 128 lists of notes.
    """
    midi_tracks = midi.read_midifile(filename)
    resolution = midi_tracks.resolution
    tempo_bpm = 120.0  # may be changed repeatedly in the loop
    note_tracks = []
    for t_index, t in enumerate(midi_tracks):
        notes_pitchwise = [[] for i in range(128)]
        total_ticks = 0
        for elem in t:
            total_ticks += elem.tick
            if elem.name in ["Note On", "Note Off"]:
                pitch = elem.data[0]
                if is_note_on(elem):
                    n = note.Note(
                        velocity=elem.data[1],
                        pitch=pitch,
                        start_ticks=total_ticks,
                        track=t_index)
                    notes_pitchwise[pitch].append(n)
                else:
                    for n in reversed(notes_pitchwise[pitch]):
                        if not n.finished:
                            n.end_ticks = total_ticks
                            n.finished = True
                        else:
                            break
            elif elem.name == "Set Tempo":
                tempo_bpm = elem.get_bpm()
        note_tracks.append(notes_pitchwise)
    return note_tracks, tempo_bpm, resolution


def calculate_note_times(note_tracks, tempo_bpm, resolution):
    """
    Calculate start_time and end_time for all notes.
    This only works if the MIDI file does not contain
    any tempo changes.
    """
    for t in note_tracks:
        for pl in t:
            for n in pl:
                n.calculate_start_and_end_time(tempo_bpm, resolution)


def get_maximum_time(note_tracks):
    """
    Determines the largest value of end_time
    among all notes. This is required to know
    when the video should end.
    """
    maximum_time = -999999.9
    for t in note_tracks:
        for pitch_list in t:
            if pitch_list != []:
                if pitch_list[-1].end_time > maximum_time:
                    maximum_time = pitch_list[-1].end_time
    return maximum_time


def get_pitch_min_max(note_tracks):
    """
    In order not to waste space,
    we may want to know in advance what the highest and lowest
    pitches of the MIDI notes are.
    """
    pitch_min = 128
    pitch_max = 0
    for t in note_tracks:
        for pitch_list in t:
            for note in pitch_list:
                pitch = note.pitch
                if pitch > pitch_max:
                    pitch_max = pitch
                if pitch < pitch_min:
                    pitch_min = pitch
    return pitch_min, pitch_max


def print_progress(msg, current, total):
    """
    This keeps the output on the same line.
    """
    text = "\r" + msg + " {:9.1f}/{:.1f}".format(current, total)
    sys.stdout.write(text)
    sys.stdout.flush()


def create_beatmap(note_tracks, config):
    #SETUP
    frame_rate = float(config["frame_rate"])
    waiting_time_before_end = float(config["waiting_time_before_end"])
    start_time = float(config["start_time"])
    time_before_current = float(config["time_before_current"])
    time_after_current = float(config["time_after_current"])
    pitch_min, pitch_max = get_pitch_min_max(note_tracks)
    if config["pitch_min"] != "auto":
        pitch_min = int(config["pitch_min"])
    if config["pitch_max"] != "auto":
        pitch_max = int(config["pitch_max"])
    if config["end_time"] == "auto":
        end_time = get_maximum_time(note_tracks) + waiting_time_before_end
    else:
        end_time = float(config["end_time"])
    note_tracks, tempo_bpm, resolution = read_midi(config["midi_filename"])
    ############## end setup

    
    rowsNum = pitch_max - pitch_min + 1
    #beatmap = [[] * rowsNum] #at each index/pitch, list of notes (rectangle object, length, time to be sung at) 
    #self.rect = pygame.Rect(x, y, width, height)
    rectHight = int( beat_screen_h/rowsNum )
    rectWidth = 75 #however long the beat is
    initX = beat_screen_w #start rectangle at the right of the beatmap screen
    initY = 500 #beat_screen_h-beatRow*rectHight #start rectangle in the correct row

    current_note_indices = [ [0 for i in range(128)] for k in range(len(note_tracks))]
    beatmap = [] # list of tuples: (pygame.Rect, time to appear/be sung at)

    #for every note in every track...
    calculate_note_times(note_tracks, tempo_bpm, resolution)    
    for track in note_tracks:
        for pitch_list in track:
            for note in pitch_list:
                rectWidth = (note.end_time-note.start_time)*100 #scale/multiply by tempo
                Y = get_note_Y(note, pitch_min, pitch_max, config)
                temp_rect = pygame.Rect(initX, Y, rectWidth, rectHight)
                beatmap.append( (temp_rect, note.start_time) )
    ##TODO LOOK AT create_image TO IMPROVE THE CODE TODO
    return beatmap
    
def get_note_Y(note, pitch_min, pitch_max, config):
    margin_y = int(config["margin_y"])
    size_x = int(config["size_x"])
    size_y = int(config["size_y"])
    pixels_to_remove_from_notes_x = float(
        config["pixels_to_remove_from_notes_x"])
    pixels_to_remove_from_notes_y = float(
        config["pixels_to_remove_from_notes_y"])

    no_of_rows = pitch_max - pitch_min + 1
    row_height = (size_y - 2.0 * margin_y) / no_of_rows
    # pixels_per_second = size_x / (time_before_current + time_after_current)
    note_height = int(
        round(max(1, row_height - pixels_to_remove_from_notes_y)))
    note_pos_y_offset = 0.5 * (row_height - note_height)

    row_no = note.pitch - pitch_min
    y_pos = int(round(size_y - margin_y - (row_no + 1)
                        * row_height + note_pos_y_offset))
    # x_pos = int(round((note.start_time - time_left) * pixels_per_second))
    # x_length = int(round((note.end_time - note.start_time)
    #                         * pixels_per_second - pixels_to_remove_from_notes_x))

    # p1 = (x_pos, y_pos)
    # p2 = (x_pos + x_length, y_pos + note_height)

    return y_pos


def create_video(note_tracks, config):
    frame_rate = float(config["frame_rate"])
    waiting_time_before_end = float(config["waiting_time_before_end"])
    start_time = float(config["start_time"])
    time_before_current = float(config["time_before_current"])
    time_after_current = float(config["time_after_current"])

    pitch_min, pitch_max = get_pitch_min_max(note_tracks)
    if config["pitch_min"] != "auto":
        pitch_min = int(config["pitch_min"])
    if config["pitch_max"] != "auto":
        pitch_max = int(config["pitch_max"])

    if config["end_time"] == "auto":
        end_time = get_maximum_time(note_tracks) + waiting_time_before_end
    else:
        end_time = float(config["end_time"])

    current_note_indices = [
        [0 for i in range(128)] for k in range(len(note_tracks))]
    img_index = 0
    dt = 1.0 / frame_rate
    time = start_time
    while time < end_time:
        time_left = time - time_before_current
        time_right = time + time_after_current

        current_notes = []
        for track_index, track in enumerate(note_tracks):
            for pitch_index in range(128):
                min_note_index = current_note_indices[track_index][pitch_index]
                max_note_index = len(track[pitch_index])
                for note_index in range(min_note_index, max_note_index):
                    note = track[pitch_index][note_index]
                    if note.end_time < time_left:
                        current_note_indices[track_index][pitch_index] += 1
                    elif note.start_time < time_right:
                        current_notes.append(note)
                    else:
                        break

        img = create_image(current_notes, time, time_left, time_right, time_before_current,
                            time_after_current, pitch_min, pitch_max, config)
        cv2.imwrite("./tmp_images/%08i.png" % img_index, img)
        time += dt
        img_index += 1
        print_progress("Current time:", time, end_time)
    print("")

    size_x = int(config["size_x"])
    size_y = int(config["size_y"])
    run_ffmpeg(frame_rate, size_x, size_y)


def run_ffmpeg(frame_rate, size_x, size_y):
    """
    Convert all images into a video.
    """
    call_list = []
    call_list.append("ffmpeg")
    call_list.append("-r")
    call_list.append("{:f}".format(frame_rate))
    call_list.append("-f")
    call_list.append("image2")
    call_list.append("-s")
    call_list.append("{:d}x{:d}".format(size_x, size_y))
    call_list.append("-i")
    call_list.append("./tmp_images/%08d.png")
    call_list.append("-vcodec")
    call_list.append("libx264")
    call_list.append("-crf")
    call_list.append("25")
    call_list.append("-pix_fmt")
    call_list.append("yuv420p")
    call_list.append("./output/final.mp4")
    subprocess.call(call_list)


def create_empty_image(bg_color, size_x=1920, size_y=1080):
    """
    This returns the array on which will be drawn.
    """
    bg = np.array(bg_color, dtype=np.uint8)
    img = bg * np.ones((size_y, size_x, 3),
            dtype=np.uint8) * np.ones((size_y, size_x, 1), dtype=np.uint8)
    return img


def get_color_from_string(color_str):
    """
    This converts the colors from the options file
    to a list of ints: [b,g,r].
    """
    return [int(c) for c in color_str.split(",")]


def create_image(current_notes, time, time_left, time_right, time_before_current,
                    time_after_current, pitch_min, pitch_max, config):
    """
    For each frame, this function is called.
    The notes which appear in this image (current_notes) have
    already been selected.
    """
    margin_y = int(config["margin_y"])
    size_x = int(config["size_x"])
    size_y = int(config["size_y"])
    color_active = get_color_from_string(config["color_active"])
    color_silent = get_color_from_string(config["color_silent"])
    bg_color = get_color_from_string(config["bg_color"])
    pixels_to_remove_from_notes_x = float(
        config["pixels_to_remove_from_notes_x"])
    pixels_to_remove_from_notes_y = float(
        config["pixels_to_remove_from_notes_y"])

    no_of_rows = pitch_max - pitch_min + 1
    row_height = (size_y - 2.0 * margin_y) / no_of_rows
    pixels_per_second = size_x / (time_before_current + time_after_current)
    note_height = int(
        round(max(1, row_height - pixels_to_remove_from_notes_y)))
    note_pos_y_offset = 0.5 * (row_height - note_height)

    img = create_empty_image(bg_color)
    for note in current_notes:
        row_no = note.pitch - pitch_min
        y_pos = int(round(size_y - margin_y - (row_no + 1)
                          * row_height + note_pos_y_offset))
        x_pos = int(round((note.start_time - time_left) * pixels_per_second))
        x_length = int(round((note.end_time - note.start_time)
                             * pixels_per_second - pixels_to_remove_from_notes_x))

        p1 = (x_pos, y_pos)
        p2 = (x_pos + x_length, y_pos + note_height)
        if is_note_active(note, time):
            note_color = color_active
        else:
            note_color = color_silent
        cv2.rectangle(img, p1, p2, note_color, -1)
    return img


def is_note_active(note, time):
    """
    Notes that are currently playing may be treated differently.
    """
    if note.start_time < time and note.end_time >= time:
        return True
    else:
        return False


def delete_and_create_folders():
    """
    Clean everything up first.
    """
    foldernames = ["./output", "./tmp_images"]
    for f in foldernames:
        if os.path.isdir(f):
            shutil.rmtree(f)
        os.mkdir(f)


def get_config(filename):
    """
    All settings are stored in an external text file.
    """
    config = configparser.ConfigParser()
    config.read(filename)
    return config


def main():
    # creates video (series of images) and stores in tmp_images, then finally
    # puts in output folder as final.mp4
    delete_and_create_folders()
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "-c",
        "--config",
        required=False,
        default="options.cfg",
        help="path to program options file")
    arguments = vars(parser.parse_args())
    filename = arguments["config"]
    config = get_config(filename)["DEFAULT"]

    note_tracks, tempo_bpm, resolution = read_midi(config["midi_filename"])
    print(create_beatmap(note_tracks, config))

    #for making the video
    # calculate_note_times(note_tracks, tempo_bpm, resolution)
    # create_video(note_tracks, config)
    # shutil.rmtree("./tmp_images")


if __name__ == '__main__':
    main()
