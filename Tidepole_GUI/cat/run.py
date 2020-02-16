import wx
import os
import sys

from cat.frames.gui_formatter import SelectRadio
from cat.gui import FrameMain
#from cat.gui import FrameMain

def resource_path(relative_path):
    """ Get absolute path to resource, works for dev and for PyInstaller """
    try:
        # PyInstaller creates a temp folder and stores path in _MEIPASS
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")

    return os.path.join(base_path, relative_path)

RADIOS = ('CP50', 'XRS330')

if __name__ == '__main__':
    app = wx.App(redirect=False)

    #app2 = wx.App(redirect=False)
    frame = FrameMain("XRS330")
    frame.Show(True)
    app.MainLoop()

