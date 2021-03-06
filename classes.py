import pygame
import numpy as np
import math

#import vlc
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
    '''
    This class creates a button folllowing the definition of a pygame rectangle, and includes
    functionality pertaining to state of being clicked.
    '''
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
    '''
    This class creates shell for the KaraokeHero user interface and utilizes key methods and classes
    to implement the program.
    '''
    user_id = None
    game_display = None
    # video_display = None
    song = None
    song_selection = None
    midi = None
    is_playing = False
    quit = False
    score = None
    font = None
    movie = None
    wm_info = None
    start_song = False
    rectangles = None

    width = 1500
    height = 750
    button_w = 150
    button_h = 100
    screen_w = 1500
    screen_h = 750

    def __init__(self, user_id):
        pygame.init()
        self.user_id = user_id
        self.font = pygame.font.SysFont('Arial', 25)
        self.game_display = pygame.display.set_mode((self.width, self.height))

        pygame.display.set_caption('KaraokeHero')
        pygame.mixer.init(buffer=128)

        # self.video = pygame.display.set_mode((self.width, self.height))
        # pygame.display.get_wm_info()
        # pygame.mixer.quit()



    def quit(self):
        pygame.quit()
        exit()
        sys.exit()

    def menu(self):
        '''
        Displays available songs and update selected song if song chosen, else returns
        False (user has chosen to leave screen)
        '''
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
                        self.song = 'media/twinkle-twinkle2.ogg'
                        self.midi = "midi_filename_twinkle"
                        # self.movie = './twinkle-twinkle.mp4'
                        # self.movie = pygame.movie.Movie('./twinkle-twinkle.mp4')
                        menu = False
                        break
                    elif buns.is_clicked(x, y):
                        print("hit MENU BUNS")
                        self.shade_button(buns.x, buns.y, colors["dark blue"], "Hot Cross Buns")
                        self.song_selection = "Hot Cross Buns"
                        self.song = 'media/hot-cross-bunsPNO.ogg'
                        self.midi = "midi_filename_buns"
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
        '''
        Draws a rectangular button at (x, y) in a color with text (name) written on it in black.
        '''
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
        '''
        Shades a rectangular button at (x, y) in a color with text (name) written on it in black.
        '''
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
        # print("pitch:", pitch)

        midi = freq2midi(pitch)
        # print("midi note: ", midi)

        mic.stop_stream()
        mic.close()
        p.terminate()

        return midi

    def play_song(self):
        '''
        Displays beatmap and relevant screen components. If a user select start, begins the betamap and
        related audio. If the user wishes to return to menu, returns True. If the user exits or quits, returns False.
        Otherwise, continuously loops.
        '''
        # attempts at loading lyric video

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

        self.is_playing = True
        title = 'Now Playing: ' + str(self.song_selection)
        self.game_display.fill(colors["white"])
        pygame.display.set_caption(title)
        menu = self.draw_button(25, 300, colors["red"], "MENU")
        quit = self.draw_button(25, 500, colors["red"], "QUIT")
        start = self.draw_button(25, 100, colors["green"], "START")

        # visualize beatmap
        beat_map_x = 350
        beat_map_y = 50

        self.start_song = False

        beat_map = pygame.draw.rect(self.game_display, colors["black"], (beat_map_x, beat_map_y , self.width - self.button_w*3, self.height - self.button_h*2))
        for i in range(0, self.height - self.button_h*2, 46):
            pygame.draw.line(self.game_display, colors["white"], (beat_map_x, beat_map_y  + i), (beat_map_x + (self.width - self.button_w*3), beat_map_y  + i), 4)
        pygame.draw.line(self.game_display, colors["blue"], (beat_map_x + 50, beat_map_y), (beat_map_x + 50, beat_map_y + (self.height - self.button_h*2)), 4)

        # further attempts at displaying lyric video
        # clip = VideoFileClip(self.movie)
        # pygame.display.update()

        # movie.set_display(movie_screen)
        # movie.show()

        # determine which audio to play
        print(self.midi)
        self.rectangles = midi_anim.main(self.midi)
        pygame.mixer.music.load(self.song)

        startTime = -1
        pitches = set([])
        while self.is_playing:

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.mixer.music.stop()
                    pygame.mixer.music.unload()
                    pygame.quit()
                    exit()
                    # clip.close()
                if event.type == pygame.MOUSEBUTTONDOWN:
                    x, y = pygame.mouse.get_pos()
                    if quit.is_clicked(x, y):
                        self.shade_button(quit.x, quit.y, colors["dark red"], "QUIT")

                        pygame.mixer.music.stop()
                        # pygame.mixer.music.unload()
                        # clip.close()
                        # movie.stop()
                        # sys.exit()
                        # sys.exit(2)
                        print("hit SONG QUIT")
                        self.is_playing = False
                        self.start_song = False
                        return False
                    elif menu.is_clicked(x, y):
                        self.shade_button(menu.x, menu.y, colors["dark red"], "MENU")
                        pygame.mixer.music.stop()
                        # pygame.mixer.music.unload()
                        print("hit SONG MENU")
                        self.start_song = False
                        print(pitches)
                        return True
                    elif start.is_clicked(x, y):
                        self.shade_button(start.x, start.y, colors["dark green"], "START")
                        print("hit SONG START")
                        pygame.mixer.music.play(start=0.0)
                        startTime = pygame.time.get_ticks()
                        self.start_song = True

            # clear everything and re-draw
            self.game_display.fill(colors["white"], (beat_map_x, 0 , self.width - beat_map_x, self.height))

            beat_map = pygame.draw.rect(self.game_display, colors["black"], (beat_map_x, beat_map_y , self.width - self.button_w*3, self.height - self.button_h*2))
            for i in range(0, self.height - self.button_h*2, 46):
                pygame.draw.line(self.game_display, colors["white"], (beat_map_x, beat_map_y  + i), (beat_map_x + (self.width - self.button_w*3), beat_map_y  + i), 4)
            pygame.draw.line(self.game_display, colors["blue"], (beat_map_x + 50, beat_map_y), (beat_map_x + 50, beat_map_y + (self.height - self.button_h*2)), 4)

            audio = self.get_user_audio()
            final_audio = max(audio, 1)

            normalized_pitch = max(int(final_audio%13), 1)

            pitches.add(normalized_pitch)

            y_val = int((self.height - self.button_h*2)/normalized_pitch)

            active_rects = []
            active_rects.append( pygame.draw.rect(self.game_display, colors["red"], (beat_map_x + 50, beat_map_y + y_val, 20, 20))
            )


            # show beats on beatmap
            # gets current rectangles and their positions
            # self.song_visual(startTime)
            if self.start_song: #only while a song is playing
                for rectangle, rectStart, rectEnd in self.rectangles: #update coords of rectangles
                    rectangle.move_ip(-120, 0) #move to the left
                    if rectangle.x >= beat_map_x and rectangle.x+rectangle.width <= self.width - self.button_w*3:
                        active_rects.append( pygame.draw.rect(self.game_display, colors["blue"], rectangle)
                        )

            pygame.display.update(active_rects)
            pygame.time.delay(120)

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
        print(pitches)

        return False

    def upload_score(self):
        # uploads user's score

        # file = open("data/hs.txt","w")
        # file.write(str(high_score))
        # file.close()
        return

    def song_visual(self, startTime):
        # play midi mp4 and twinkle-twinkle mp4, silence midi mp4 (files already converted, TODO)
        if self.start_song: #only while a song is playing
            now = pygame.time.get_ticks()
            #rect = rectangles.pop(0)

            for rectangle, rectStart, rectEnd in self.rectangles: #update coords of rectangles
                now = pygame.time.get_ticks()
                # while now-startTime < rectTime:
                #     # do nothing
                #     print(' ')
                #if now-startTime < rectEnd : # only move+draw rectangles that havent ended yet
                rectangle.move_ip(-100, 0) #move to the left

                #TODO add rectangle.x and .y offset since the visual screen is smaller than the game screen
                #self.game_display.blit(rectangle, (rectangle.x, rectangle.y))
                pygame.draw.rect(self.game_display, colors["red"], rectangle)


    def song_audio_input(self): #renee
        return

    def result(self):
        # what the user should see after finishing song, button back to menu()
        return
