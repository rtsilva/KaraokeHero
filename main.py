"""6.835 Final Project Spring 2020"""
# Renee Silva, Magdalena Price

import sys
import matplotlib
import pygame
# pygame.init()

from app import KaraokeHeroApp

class App:
    user_id = None
    song_selection = None
    is_playing = False
    quit = False
    score = None
    # completed_song = False

    width = 200
    height = 100
    button_w = 40
    button_h = 20
    screen_w = 100
    screen_h = 50

    def __init__(self, user_id):
        self.user_id = user_id


    def menu(self):
        # display available songs and return selected song if song chosen
        # else False (user has chosen to quit)
        return

    def play_song(self): #
        # show lyric video, play song, capture audio
        # return True if song finishes else False
        # updates score
        return

    def upload_score(self):
        # uploads user's score
        return

    def song_visual(self): #lena
        return

    def song_audio(self): #renee
        return

    def result(self):
        # what the user should see after finishing song, button back to menu()
        return


if __name__ == '__main__':
    # app = KaraokeHeroApp()
    # app.mainloop()
    pygame.init()
    app = App(1)
