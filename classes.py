import pygame
import numpy as np
import math

import vlc
from moviepy.editor import *
import sys

from values import colors

from names import NoteOn, NoteOff, End
from audiolazy import midi2str, freq2midi
import midi_anim

import pyaudio
import time

import aubio

CHUNK = 2048 #1024
FORMAT = pyaudio.paFloat32
WIDTH = 2
CHANNELS = 1
RATE = 44100
###
HOP_SIZE                = CHUNK//2
PERIOD_SIZE_IN_FRAME    = HOP_SIZE
METHOD                  = "default"
x_r = 80

FPS = 30

class Button:
    name = None
    x = None
    y = None
    width = None
    height = None

    # positions are left, top, width, height
    # remember screen y goes from 0 to max, downwards
    def __init__(self, x, y, width, height, name):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.name = name

    def is_clicked(self, x, y):

        if self.x > x or self.x + self.width < x:
            return False
        if self.y + self.height < y or self.y > y:
            return False

        return True

    def __str__(self):
        return "X: " +  str(self.x) + "\nY: " + str(self.y) + "\nWidth: " + str(self.width) + "\nHeight: "+ str(self.height)

class App:
    user_id = None
    game_display = None
    # video_display = None
    song_selection = None
    is_playing = False
    quit = False
    score = None
    font = None
    movie = None
    wm_info = None

    width = 1500
    height = 750
    button_w = 150
    button_h = 100
    screen_w = 1500
    screen_h = 750

    # FPS = 60

    def __init__(self, user_id):
        pygame.init()
        self.user_id = user_id
        self.font = pygame.font.SysFont('Arial', 25)
        self.game_display = pygame.display.set_mode((self.width, self.height))
        # self.video = pygame.display.set_mode((self.width, self.height))
        # pygame.display.get_wm_info()
        pygame.display.set_caption('KaraokeHero')
        pygame.mixer.quit()

    def quit(self):
        pygame.quit()
        exit()
        sys.exit()

    def menu(self):
        # display available songs and return selected song if song chosen
        # else False (user has chosen to quit)
        menu = True
        self.game_display.fill(colors["white"])
        pygame.display.set_caption('Select a Song')
        twinkle = self.draw_button(25, 100, colors["blue"], "Twinkle Twinkle")
        buns = self.draw_button(25, 300, colors["blue"], "Hot Cross Buns")
        quit = self.draw_button(25, 500, colors["red"], "QUIT")

        while menu:
            for event in pygame.event.get():

                if event.type == pygame.QUIT:
                    pygame.quit()
                    exit()
                if event.type == pygame.MOUSEBUTTONDOWN:
                    x, y = pygame.mouse.get_pos()

                    if twinkle.is_clicked(x, y):
                        self.shade_button(twinkle.x, twinkle.y, colors["dark blue"], "Twinkle Twinkle")
                        print("hit MENU TWINKLE")
                        self.song_selection = "Twinkle Twinkle"
                        # self.movie = './twinkle-twinkle.mp4'
                        # self.movie = pygame.movie.Movie('./twinkle-twinkle.mp4')
                        menu = False
                        break
                    elif buns.is_clicked(x, y):
                        print("hit MENU BUNS")
                        self.shade_button(buns.x, buns.y, colors["dark blue"], "Hot Cross Buns")
                        self.song_selection = "Hot Cross Buns"
                        # self.movie = './twinkle-twinkle.mp4' # TODO - fix
                        # self.movie = pygame.movie.Movie('./twinkle-twinkle.mp4')
                        menu = False
                        break
                    elif quit.is_clicked(x, y):
                        self.shade_button(quit.x, quit.y, colors["dark red"], "QUIT")
                        print("hit MENU QUIT")
                        return False

        return self.song_selection

    def draw_button(self, x, y, color, name):
        button = Button(x, y, self.button_w, self.button_h, name)
        # positions are left, top, width, height
        # remember screen y goes from 0 to max, downwards
        rect = pygame.draw.rect(self.game_display, color, (x, y, self.button_w, self.button_h))

        textSurface = self.font.render(name, True, colors["black"])
        h = textSurface.get_rect().height
        w = textSurface.get_rect().width

        self.game_display.blit(textSurface, (x+(self.button_w - w)//2, y + (self.button_h - h)//2))
        pygame.display.update()

        return button

    def shade_button(self, x, y, color, name):
        # positions are left, top, width, height
        # remember screen y goes from 0 to max, downwards
        rect = pygame.draw.rect(self.game_display, color, (x, y, self.button_w, self.button_h))
        textSurface = self.font.render(name, True, colors["black"])

        h = textSurface.get_rect().height
        w = textSurface.get_rect().width

        self.game_display.blit(textSurface, (x+(self.button_w - w)//2, y + (self.button_h - h)//2))
        pygame.display.update()

        return

    def get_user_audio(self):
        '''
        Using pyaudio, this function takes in mic input and returns the respective midi pitch value.
        '''
        # instantiate PyAudio object
        p = pyaudio.PyAudio()

        # open mic stream
        mic = p.open(format=FORMAT,
                        channels=CHANNELS,
                        rate=RATE,
                        input=True,
                        frames_per_buffer=PERIOD_SIZE_IN_FRAME)

        # Initiating Aubio's pitch detection object.
        pDetection = aubio.pitch(METHOD, CHUNK, HOP_SIZE, RATE)
        # Set unit.
        pDetection.set_unit("Hz")
        # Frequency under 5 dB will considered
        # as a silence (8 dB is a C1 or midi#0)
        pDetection.set_silence(-40)

        data = mic.read(PERIOD_SIZE_IN_FRAME)
        # Convert into number that Aubio understand.
        samples = np.fromstring(data, dtype=aubio.float_type)

        # Finally get the pitch.
        pitch = pDetection(samples)[0]

        midi = freq2midi(pitch)
        print(midi)

        mic.stop_stream()
        mic.close()
        p.terminate()

        return midi

    def play_song(self): #
        # show lyric video, play song, capture audio
        # return True if song finishes else False
        # updates score
        # clock = pygame.time.Clock()

        # Create instane of VLC and create reference to movie.
        # vlcInstance = vlc.Instance()
        # media = vlcInstance.media_new(self.movie)

        # Create new instance of vlc player
        # player = vlcInstance.media_player_new()

        # disable vlc's key bindings
        # player.video_set_mouse_input(False)
        # player.video_set_key_input(False)

        # movie_screen = pygame.Surface((300, 250)).convert()
        # Pass pygame window id to vlc player, so it can render its contents there.
        # print(pygame.display.get_wm_info())
        # set_hwnd for windows
        # player.set_agl(pygame.display.get_wm_info()['window'])
        # player.set_hwnd(pygame.display.get_wm_info()['window'])
        # Load movie into vlc player instance
        # player.set_media(media)

        play = True
        title = 'Now Playing: ' + str(self.song_selection)
        self.game_display.fill(colors["white"])
        pygame.display.set_caption(title)
        menu = self.draw_button(25, 300, colors["red"], "MENU")
        quit = self.draw_button(25, 500, colors["red"], "QUIT")
        start = self.draw_button(25, 100, colors["green"], "START")

        # visualize beatmap
        beat_map_x = 350
        beat_map_y = 50

        start_song = False

        beat_map = pygame.draw.rect(self.game_display, colors["black"], (beat_map_x, beat_map_y , self.width - self.button_w*3, self.height - self.button_h*2))
        for i in range(0, self.height - self.button_h*2, 46):
            pygame.draw.line(self.game_display, colors["white"], (beat_map_x, beat_map_y  + i), (beat_map_x + (self.width - self.button_w*3), beat_map_y  + i), 4)
        pygame.draw.line(self.game_display, colors["blue"], (beat_map_x + 50, beat_map_y), (beat_map_x + 50, beat_map_y + (self.height - self.button_h*2)), 4)

        # user = pygame.draw.rect(self.game_display, colors["red"], (beat_map_x + 40, beat_map_y, 20, 20))

        # clip = VideoFileClip(self.movie)
        # pygame.display.update()

        # movie.set_display(movie_screen)
        # movie.show()

        while play:



            # pygame.display.update()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    exit()
                    # clip.close()
                if event.type == pygame.MOUSEBUTTONDOWN:
                    x, y = pygame.mouse.get_pos()
                    if quit.is_clicked(x, y):
                        self.shade_button(quit.x, quit.y, colors["dark red"], "QUIT")
                        # clip.close()
                        # movie.stop()
                        # sys.exit()
                        # sys.exit(2)
                        print("hit SONG QUIT")
                        return False
                    elif menu.is_clicked(x, y):
                        self.shade_button(menu.x, menu.y, colors["dark red"], "MENU")
                        print("hit SONG MENU")
                        return True
                    elif start.is_clicked(x, y):
                        self.shade_button(start.x, start.y, colors["dark green"], "START")
                        # start_song = True
            # while start_song:
                # reset EVERYTHING and REDRAW :))))))
            self.game_display.fill(colors["white"])

            menu = self.draw_button(25, 300, colors["red"], "MENU")
            quit = self.draw_button(25, 500, colors["red"], "QUIT")
            start = self.draw_button(25, 100, colors["green"], "START")

            beat_map = pygame.draw.rect(self.game_display, colors["black"], (beat_map_x, beat_map_y , self.width - self.button_w*3, self.height - self.button_h*2))
            for i in range(0, self.height - self.button_h*2, 46):
                pygame.draw.line(self.game_display, colors["white"], (beat_map_x, beat_map_y  + i), (beat_map_x + (self.width - self.button_w*3), beat_map_y  + i), 4)
            pygame.draw.line(self.game_display, colors["blue"], (beat_map_x + 50, beat_map_y), (beat_map_x + 50, beat_map_y + (self.height - self.button_h*2)), 4)

            audio = self.get_user_audio()
            final_audio = max(audio, 0)

            normalized_pitch = final_audio%13
            # print(normalized_pitch)
            # print(self.height - self.button_h*2)
            y_val = int((self.height + self.button_h*2)/46*normalized_pitch)

            pygame.draw.rect(self.game_display, colors["red"], (beat_map_x + 50, y_val, 20, 20))
            # pygame.draw.circle(self.game_display, colors["red"], (beat_map_x + 50, y_val), 15)
            # user.move_ip(0, user.y - y_val)
            pygame.display.flip()
            pygame.display.update()
            pygame.time.delay(10)

            # movie.play()
            # Start movie playback
            # player.play()
            # clip.resize(width=500).preview()
            # clip.preview()
            # display = ipython_display(clip, autoplay=1, loop=1)
            # self.game_display.blit(movie_screen,(100,100))

        # clock.tick(FPS)
        # self.video_display.blit(player,(100,150))
        pygame.display.update()

        return False

    def upload_score(self):
        # uploads user's score
        return

    def song_visual(self): #lena
        # play midi mp4 and twinkle-twinkle mp4, silence midi mp4 (files already converted, TODO)
        rectangles = midi_anim.main()
        start = pygame.time.get_ticks()
        cont = True
        while cont:
            now = pygame.time.get_ticks()
            rect = rectangles.pop(0)


        for rectangle, time in rectangles:
            now = pygame.time.get_ticks()
            while now-start < time:
                # do nothing
                print(' ')
            self.game_display.blit(rectangle, (rectangle.x, rectangle.y))




    def song_audio(self): #renee
        return

    def result(self):
        # what the user should see after finishing song, button back to menu()
        return
