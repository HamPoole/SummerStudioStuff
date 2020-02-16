import numpy as np
import functools
import time
import logging
import sys

import wx
import wx.lib.agw.aui as aui

import wx.lib.plot

import os

from cat import radio

from cat.frames.frame_connection import FrameConnection


EVT_HARDWARE_ID = wx.Window.NewControlId()

logger = logging.getLogger('GUI')
logging.basicConfig(format='[%(filename)s:%(lineno)d] %(message)s',
    datefmt='%Y-%m-%d:%H:%M:%S',
    level=logging.INFO)



class HardwareEvent(wx.PyEvent):
    # Responses / results / data from the radio and test equipment, posted back to the GUI
    def __init__(self, handler, *args):
        wx.PyEvent.__init__(self)
        self.SetEventType(EVT_HARDWARE_ID)
        self.handler_with_args = functools.partial(handler, *args)


class FrameMain(wx.Frame, radio.Observer):

    def __init__(self, sel):
        wx.Frame.__init__(self, None,
                          title='Tidepole Image Tool (Faster R-CNN)',
                          style=(wx.MINIMIZE_BOX
                                 | wx.MAXIMIZE_BOX
                                 | wx.SYSTEM_MENU
                                 | wx.CAPTION
                                 | wx.CLOSE_BOX
                                 | wx.CLIP_CHILDREN),
                          size=(1200, 800))


        self.init_gui_layout()

        self.frame_connection = FrameConnection(self)

        path = os.path.abspath("LRSS.ico")
        icon = wx.Icon(path, wx.BITMAP_TYPE_ICO)
        self.SetIcon(icon)

        self.sizer.Add(self.nb, 1, wx.EXPAND | wx.ALL, 2)
        self.SetSizer(self.sizer)
        self.Bind(aui.EVT_AUINOTEBOOK_PAGE_CHANGED, self.on_page_changed)
        self.Bind(wx.EVT_CLOSE, self.on_close)
        self.Bind(wx.EVT_TIMER, self.on_timer)

        self.prev_page_title = self.current_page_title()

        self.Layout()
        self.Centre(wx.BOTH)

    def add_page(self, p, title, enable_when_radio_connected = True):
        self.nb.AddPage(p, title)
        self.page_dict[title] = self.nb.GetPageCount() - 1

    def init_gui_layout(self):

        self.sizer = wx.BoxSizer(wx.VERTICAL)
        self.nb = aui.AuiNotebook(self, agwStyle=aui.AUI_NB_DEFAULT_STYLE ^ aui.AUI_NB_CLOSE_ON_ACTIVE_TAB)
        self.page_dict = {}
        self.pages_to_enable_when_connected = []


    def current_page_title(self):
        s = self.nb.GetSelection()
        for t in self.page_dict:
            if self.page_dict[t] == s:
                return t
        return '-'


    def enable_pages(self, enable, titles):
        for title in titles:
            if title in self.page_dict:
                self.nb.EnableTab(self.page_dict[title], enable)

    def on_close(self, event):
        self.close_now()

    def close_now(self):

        self.Destroy()
        sys.exit(0)

    def on_timer(self, event):
        if self.frame_connection.closing:

            if self.radio_selection == 'XRS330':
                self.frame_dac.dac_poll_timer.Stop()

            self.close_now()

    def on_page_changed(self, event):
        # Turn off the frequency poll timer when leaving the page that uses it


        self.prev_page_title = self.current_page_title()

    def evt_error_msg(self, msg):
        pass
