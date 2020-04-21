import matplotlib
matplotlib.use("TkAgg")
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure
from visualize_midi import init_midi, animate_midi

import tkinter as tk
from tkinter import ttk

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

        fig, x_data, y_data, line = init_midi("twinkle-twinkle-little-star.mid")

        canvas = FigureCanvasTkAgg(fig, self)
        canvas.get_tk_widget().pack(side=tk.BOTTOM, fill=tk.BOTH, expand=True)

        button0 = ttk.Button(self, text="Start Game",
                            command=lambda: animate_midi(fig, x_data, y_data, line))
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
