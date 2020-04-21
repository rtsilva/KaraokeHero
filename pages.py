import matplotlib
matplotlib.use("TkAgg")
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure
from visualize_midi import init_midi, animate_midi

import tkinter as tk
import cv2
from PIL import Image, ImageTk
from tkinter import ttk

from Screen import Screen

LARGE_FONT= ("Verdana", 12)

class StartPage(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self,parent)

        label = tk.Label(self, text="Start Page", font=LARGE_FONT)
        label.pack(pady=10,padx=10)

        button = ttk.Button(self, text="Select Song",
                            command=lambda: controller.show_frame(PageOne))
        button.pack()

class PageOne(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)

        screen = Screen(self, parent, "twinkle-twinkle.mp4")
        screen.pack()

        # Create a canvas that can fit the above video source size
        # mov_canvas = tk.Canvas(self, width = 60, height = 50)
        # mov_canvas.pack()
        # # mov_canvas.grid(row=0, column=0, padx=10, pady=2)
        # lmain = tk.Label(mov_canvas)
        # lmain.grid(row=0, column=0)
        # cap = cv2.VideoCapture("twinkle-twinkle.mp4")
        #
        # _, frame = cap.read()
        # # frame = cv2.flip(frame, 1)
        # cv2image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGBA)
        # img = Image.fromarray(cv2image)
        # imgtk = ImageTk.PhotoImage(image=img)
        # lmain.imgtk = imgtk
        # lmain.configure(image=imgtk)
        #
        # def show_frame():
        #     _, frame = cap.read()
        #     # frame = cv2.flip(frame, 1)
        #     cv2image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGBA)
        #     img = Image.fromarray(cv2image)
        #     imgtk = ImageTk.PhotoImage(image=img)
        #     lmain.imgtk = imgtk
        #     lmain.configure(image=imgtk)
        #     lmain.after(1, show_frame)

        def play_song(fig, x_data, y_data, line):
            animate_midi(fig, x_data, y_data, line)
            screen.play("twinkle-twinkle.mp4")

        fig, x_data, y_data, line = init_midi("twinkle-twinkle-little-star.mid")

        canvas = FigureCanvasTkAgg(fig, self)
        canvas.get_tk_widget().pack(side=tk.BOTTOM, fill=tk.BOTH, expand=True)

        button0 = ttk.Button(self, text="Start Game",
                            command=lambda: play_song(fig, x_data, y_data, line))
        button0.pack()

        button1 = ttk.Button(self, text="Exit Game",
                            command=lambda: controller.show_frame(StartPage))
        button1.pack()

        button2 = ttk.Button(self, text="Show Score",
                            command=lambda: controller.show_frame(PageTwo))
        button2.pack()

class PageTwo(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self,parent)

        label = tk.Label(self, text="Score", font=LARGE_FONT)
        label.pack(pady=10,padx=10)

        button = ttk.Button(self, text="Back to Select Song",
                            command=lambda: controller.show_frame(StartPage))
        button.pack()

        button = ttk.Button(self, text="Exit Game",
                            command=lambda: controller.show_frame(StartPage))
        button.pack()
