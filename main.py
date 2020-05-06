"""6.835 Final Project Spring 2020"""
# Renee Silva, Magdalena Price

import sys
import matplotlib
import pygame
# pygame.init()

from app import KaraokeHeroApp
from classes import Button, App


if __name__ == '__main__':
    # app = KaraokeHeroApp()
    # app.mainloop()

    app = App(1)
    cont = True
    while cont:
        song = app.menu()
        if song == False:
            app.quit()
            break
        else:
            res = app.play_song()
            if not res:
                app.quit()
                break

    fini = True
