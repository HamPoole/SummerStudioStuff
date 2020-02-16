import wx
from enum import Enum

import os
import cv2

import numpy as np
from helper import helper

# Note: The current assumption is based on the first reference click being 0.7, the second being 0.8, and the third being 0.9.

class ConnectionStates(Enum):
    off = 1
    connecting = 2
    connected = 3


class FrameConnection:

    def __init__(self, frame_main):

        self.frame_main = frame_main
        self.resized_dimensions = (1120, 651)
        self.img_index = 1
        self.path = ""
        self.dir = ""
        self.ref_clicks = 0
        self.pixel_clicks = []

        self.closing = False
        self.init_page_connections()

    def init_page_connections(self):
        self.pnl = wx.Panel(self.frame_main.nb)
        self.frame_main.add_page(self.pnl, 'Analyse Data', False)

        x_offset = 160
        x1 = 10
        x2 = 165
        x33 = 320
        x3 = 320 + x_offset
        x4 = 385 + x_offset
        x5 = 500 + x_offset

        x6 = 720

        y_adjust = 105
        y1 = 560 + y_adjust
        y3 = 565 + y_adjust
        y2 = 590 + y_adjust
        y4 = 595 + y_adjust


        self.btn_set_ref = wx.Button(self.pnl, wx.ID_ANY, 'Set Reference Height', (x1, y1), (150, -1))
        self.btn_set_ref.SetForegroundColour((128, 0, 0))

        self.btn_select_folder = wx.Button(self.pnl, wx.ID_ANY, 'Select Folder', (x1, y2), (150, -1))
        self.btn_select_image = wx.Button(self.pnl, wx.ID_ANY, 'Select Image', (x2, y1), (150, -1))
        self.btn_export_csv = wx.Button(self.pnl, wx.ID_ANY, 'Export CSV', (x2, y2), (150, -1))


        self.btn_next = wx.Button(self.pnl, wx.ID_ANY, 'Next Image', (x33, y1), (150, 56))
        #self.btn_next = wx.Button(self.pnl, wx.ID_ANY, 'Export CSV', (x2, y2), (150, -1))


        self.text_static_depth = wx.StaticText(self.pnl, wx.ID_ANY, 'Depth (m):', (x3, y3))
        self.text_static_time = wx.StaticText(self.pnl, wx.ID_ANY, 'Time:', (x3, y4))


        self.text_ctrl_depth = wx.TextCtrl(self.pnl, wx.ID_ANY, "0.00", (x4, y1))
        self.text_ctrl_time = wx.TextCtrl(self.pnl, wx.ID_ANY, "HH:MM", (x4, y2))

        self.text_ctrl_date = wx.TextCtrl(self.pnl, wx.ID_ANY, "YYYY/MM/DD", (x6, y1))
        self.text_ctrl_location = wx.TextCtrl(self.pnl, wx.ID_ANY, "HMAS Penguin", (x6, y2))


        self.text_static_date = wx.StaticText(self.pnl, wx.ID_ANY, 'Date:', (x5, y3))

        self.text_static_location = wx.StaticText(self.pnl, wx.ID_ANY, 'Location:', (x5, y4))


        self.frame_main.Bind(wx.EVT_BUTTON, self.on_click_select_folder, self.btn_select_folder)

        self.frame_main.Bind(wx.EVT_BUTTON, self.on_click_next, self.btn_next)

        self.frame_main.Bind(wx.EVT_BUTTON, self.on_click_set_ref, self.btn_set_ref)

        self.frame_main.Bind(wx.EVT_BUTTON, self.on_click_select_image, self.btn_select_image)

        self.p0txt2 = wx.StaticText(self.pnl, wx.ID_ANY, '', (x1, 290), (300, -1))


        img = wx.Image(self.resized_dimensions)
        self.imageCtrl = wx.StaticBitmap(self.pnl, wx.ID_ANY,
                                         wx.Bitmap(img))

        self.imageCtrl.Bind(wx.EVT_LEFT_DOWN, self.on_click)

    def on_click_select_folder(self, evt):
        print('clicked')
        frame = wx.Frame(None, -1, 'win.py')
        frame.SetSize(0, 0, 200, 50)

        dlg = wx.DirDialog(frame, "Open a directory with supported files", "",
                           wx.DD_DEFAULT_STYLE | wx.DD_DIR_MUST_EXIST)
        if dlg.ShowModal() == wx.ID_OK:
            self.path = dlg.GetPath()
            self.dir = os.listdir(self.path)

            print('path:', self.path)

            img = cv2.imread(self.path + '\\' + self.dir[self.img_index])

            self.display_image(img)


        else:
            print('Invalid Selection')

        dlg.Destroy()

    def on_click_next(self, evt):
        self.img_index = self.img_index + 1

        img = cv2.imread(self.path + '\\' + self.dir[self.img_index])

        self.display_image(img)


    def on_click_set_ref(self, evt):
        self.ref_clicks = 0
        self.pixel_clicks = []
        self.btn_set_ref.SetForegroundColour((0, 128, 0))
        print('Set Reference Points!')
        # while self.ref_clicks < 4:
        #     self.ref_clicks = self.ref_clicks + 1
        #     print('ref_clicks', self.ref_clicks)
        #
        # self.ref_clicks = 0
        # print('Reference Set')

    def on_click_select_image(self, evt):

        print('clicked')
        frame = wx.Frame(None, -1, 'win.py')
        frame.SetSize(0, 0, 200, 50)

        dlg = wx.FileDialog(frame, "Select an image", wildcard="JPG files (*.jpg)|*.JPG",
                           style=wx.FD_OPEN | wx.FD_FILE_MUST_EXIST)
        if dlg.ShowModal() == wx.ID_OK:
            self.path = dlg.GetPath()

            print('path:', self.path)

            img = cv2.imread(self.path)

            self.display_image(img)


        else:
            print('Invalid Selection')

        dlg.Destroy()

    def on_click(self, evt):

        if self.ref_clicks < 3:
            self.pixel_clicks.append(evt.GetPosition())
            self.ref_clicks = self.ref_clicks + 1
            print(self.ref_clicks)
        else:
            self.btn_set_ref.SetForegroundColour((128, 0, 0))
            self.calculate_tide_manual(evt.GetPosition())

        if self.ref_clicks == 3:
            self.btn_set_ref.SetForegroundColour((128, 0, 0))
            self.calculate_regression()

        #print('position', evt.GetPosition())

    def calculate_regression(self):
        #Hardcoded for now...
        y1_m = 1.20
        y2_m = 1.50
        y3_m = 1.80
        print('self.pixel_clicks',self.pixel_clicks)

        y3_p = self.pixel_clicks[0][1]
        y2_p = self.pixel_clicks[1][1]
        y1_p = self.pixel_clicks[2][1]

        #quickly hardcoded for now...

        y1_p = 209
        y2_p = 170
        y3_p = 131

        # y = mx + b
        # First, calculate slope, m
        self.slope_m = (y3_m - y1_m)/(y3_p - y1_p)
        self.offset_b = y1_m - self.slope_m*y1_p



    def calculate_tide_manual(self, point):
        print('my point', point)
        y_p = point[1]

        self.depth = self.slope_m*y_p + self.offset_b
        print('depth', self.depth)
        self.proposed_depth = self.depth
        self.text_ctrl_depth = self.depth

        #depth =

    def display_image(self, img):

        W = img.shape[1]
        H = img.shape[0]

        if W > H:
            NewW = self.resized_dimensions[0]
            NewH = int(self.resized_dimensions[0] * H / W)
        else:
            NewH = self.resized_dimensions[0]
            NewW = int(self.resized_dimensions[0] * W / H)

        print('w/h', NewH, NewW)

        img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)

        img_resize = cv2.resize(img, (NewW, NewH))

        bitmap = wx.Bitmap.FromBuffer(NewW, NewH, img_resize)

        self.imageCtrl.SetBitmap(bitmap)

        self.pnl.Refresh()
