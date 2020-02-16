import os
import wx

import time
import cv2



class PhotoCtrl(wx.App):

    def __init__(self, redirect=False, filename=None):
        wx.App.__init__(self, redirect, filename)

        self.frame = wx.Frame(self, None,
                          title='Radio Alignment Tool',
                          style=(wx.MINIMIZE_BOX
                                 | wx.MAXIMIZE_BOX
                                 | wx.SYSTEM_MENU
                                 | wx.CAPTION
                                 | wx.CLOSE_BOX
                                 | wx.CLIP_CHILDREN),
                          size=(800, 600))


        self.panel = wx.Panel(self.frame)
        #self.PhotoMaxSize = 800

        self.createWidgets()
        self.frame.Show()

        self.path = ''
        self.img_index = 1

        self.clicks = []
        self.set_height = False


    def load_images_folder(self, folder):
        images = []
        for filename in os.listdir(folder):
            img = cv2.imread(os.path.join(folder, filename), cv2.IMREAD_GRAYSCALE)
            if img is not None:
                images.append(img)
        return images

    def on_click(self, evt):

        self.clicks.append(evt.GetPosition())

        if len(self.clicks) == 2 and self.set_height:
            self.crop_img()


    def createWidgets(self):
        instructions = 'Select Tidepole Directory'
        img = wx.Image(600, 400)
        self.imageCtrl = wx.StaticBitmap(self.panel, wx.ID_ANY,
                                         wx.Bitmap(img))

#-----
        x1 = 20
        self.p0txt1 = wx.StaticText(self.panel, wx.ID_ANY, 'Serial ports:', (x1, 1000))
#----


        self.imageCtrl.Bind(wx.EVT_LEFT_DOWN, self.on_click)

        instructLbl = wx.StaticText(self.panel, label=instructions)

        self.photoTxt = wx.TextCtrl(self.panel, size=(200, -1))




        browseBtn = wx.Button(self.panel, label='Set Reference Height')
        #browseBtn.Bind(wx.EVT_BUTTON, self.On_set_ref_height)

        browseDirBtn = wx.Button(self.panel, label='Get Tide Data')
        #browseDirBtn.Bind(wx.EVT_BUTTON, self.onBrowseDir)

        nextBtn = wx.Button(self.panel, label='Next Image')
        #nextBtn.Bind(wx.EVT_BUTTON, self.onNext)



        self.mainSizer = wx.BoxSizer(wx.VERTICAL)
        self.sizer = wx.BoxSizer(wx.HORIZONTAL)
        self.sizer2 = wx.BoxSizer(wx.HORIZONTAL)

        self.mainSizer.Add(wx.StaticLine(self.panel, wx.ID_ANY),
                           0, wx.ALL | wx.EXPAND, 5)
        self.mainSizer.Add(instructLbl, 0, wx.ALL, 5)
        self.mainSizer.Add(self.imageCtrl, 0, wx.ALL, 5)
        self.sizer.Add(self.photoTxt, 0, wx.ALL, 5)

        self.sizer.Add(browseBtn, 0, wx.ALL, 5)

        self.sizer.Add(browseDirBtn, 0, wx.ALL, 5)

        self.sizer.Add(nextBtn, 0, wx.ALL, 5)


        self.mainSizer.Add(self.sizer, 0, wx.ALL, 5)

        self.panel.SetSizer(self.mainSizer)
        self.mainSizer.Fit(self.frame)
        self.panel.Layout()




if __name__ == '__main__':
    app = PhotoCtrl()
    app.MainLoop()