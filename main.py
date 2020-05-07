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
    # midis = set([])
    #
    # while True:
    #     res = max(app.get_user_audio(), 0)
    #     midis.add(int(res%12))
    #     print(midis)
    cont = True
    while cont:
        song = app.menu()
        if not song:
            app.quit()
            break
        else:
            res = app.play_song()
            if not res:
                app.quit()
                break

    # fini = True
