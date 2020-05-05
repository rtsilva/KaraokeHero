import pygame
from values import colors

class Button:
    x = None
    y = None
    width = None
    height = None

    def __init__(self, x, y, width, height):
        self.x = x
        self.y = y
        self.width = width
        self.height = height

    def is_clicked(self, x, y):

        if self.x - self.width > x or self.x + self.width < x:
            return False
        if self.y - self.height > y or self.y + self.height < x:
            return False

        return True

class App:
    user_id = None
    game_display = None
    song_selection = None
    is_playing = False
    quit = False
    score = None
    font = None

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
                        self.song_selection = "Twinkle Twinkle"
                        menu = False
                        break
                    elif buns.is_clicked(x, y):
                        self.shade_button(buns.x, buns.y, colors["dark blue"], "Hot Cross Buns")
                        self.song_selection = "Hot Cross Buns"
                        menu = False
                        break
                    elif quit.is_clicked(x, y):
                        self.shade_button(quit.x, quit.y, colors["dark red"], "QUIT")
                        pygame.quit()
                        exit()
                        menu = False
                        break

            # self.game_display.update()
        return self.song_selection

    def draw_button(self, x, y, color, name):
        button = Button(x, y, self.button_w, self.button_h)
        rect = pygame.draw.rect(self.game_display, color, (x, y, self.button_w, self.button_h))
        textSurface = self.font.render(name, True, colors["black"])

        self.game_display.blit(textSurface, (x, y))
        pygame.display.update()

        return button

    def shade_button(self, x, y, color, name):

        rect = pygame.draw.rect(self.game_display, color, (x, y, self.button_w, self.button_h))
        textSurface = self.font.render(name, True, colors["black"])

        self.game_display.blit(textSurface, (x, y))
        pygame.display.update()

        return


    def play_song(self): #
        # show lyric video, play song, capture audio
        # return True if song finishes else False
        # updates score
        play = True
        self.game_display.fill(colors["white"])
        pygame.display.set_caption('Now Playing:', self.song_selection)
        menu = self.draw_button(25, 300, colors["red"], "MENU")
        quit = self.draw_button(25, 500, colors["red"], "QUIT")

        while play:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    exit()
                if event.type == pygame.MOUSEBUTTONDOWN:

                    x, y = pygame.mouse.get_pos()
                    if quit.is_clicked(x, y):
                        self.shade_button(quit.x, quit.y, colors["dark red"], "QUIT")
                        pygame.quit()
                        exit()
                        play = False
                        break
                        # quit()
                    elif menu.is_clicked(x, y):
                        self.shade_button(menu.x, menu.y, colors["dark red"], "MENU")
                        play = False
                        break
        return False

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
