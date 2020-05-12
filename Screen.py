from tkinter import Frame, Canvas

import vlc

class Screen(Frame): # https://stackoverflow.com/questions/55197752/playing-video-with-audio-on-a-tkinter-frame
    '''
    Screen widget: Embedded video player from local or youtube
    '''
    def __init__(self, parent, path, *args):
        Frame.__init__(self, parent, bg = 'black')
        self.settings = { # Initialazing dictionary settings
            "width" : 1024//2,
            "height" : 576//2
        }
        # self.settings.update(kwargs) # Changing the default settings
        # Open the video source |temporary
        self.video_source = path

        # Canvas where to draw video output
        self.canvas = Canvas(self, width = self.settings['width'], height = self.settings['height'], bg = "black", highlightthickness = 0)
        self.canvas.pack()

        # Creating VLC player
        self.instance = vlc.Instance()
        self.player = self.instance.media_player_new()


    def GetHandle(self):
        # Getting frame ID
        return self.winfo_id()

    def play(self, _source):
        # Function to start player from given source
        Media = self.instance.media_new(_source)
        Media.get_mrl()
        self.player.set_media(Media)

        # Mac Version (doesn't work)
        # self.player.set_nsobject(self.GetHandle())
        # tragic: https://github.com/oaubert/python-vlc/issues/91
        # from ctypes import c_void_p, cdll
        # try:
        #     # libtk = cdll.LoadLibrary(ctypes.util.find_library('tk'))
        #     # returns the tk library /usr/lib/libtk.dylib from macOS,
        #     # but we need the tkX.Y library bundled with Python 3+
        #     # and matching the version of tkinter, _tkinter, etc.
        #     libtk = 'libtk%s.dylib' % (Tk.TkVersion,)
        #     libtk = os.path.join(sys.prefix, 'lib', libtk)
        #     libtk = cdll.LoadLibrary(libtk)
        #     # getNSView = libtk.TkMacOSXDrawableView  # XXX not found?
        #     getNSView = libtk.TkMacOSXGetRootControl
        #     getNSView.restype = c_void_p
        #     getNSView.argtypes = c_void_p,
        #     self.player.set_nsobject(getNSView(self.GetHandle()))
        # except (NameError, OSError):
        #     self.player.set_xwindow(self.GetHandle())  # audio, no video
        self.player.set_hwnd(self.GetHandle()) # Windows Version
        self.player.play()
