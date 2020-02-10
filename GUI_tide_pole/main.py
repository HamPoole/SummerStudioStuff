import os
import wx

import time
import cv2



class PhotoCtrl(wx.App):
    def __init__(self, redirect=False, filename=None):
        wx.App.__init__(self, redirect, filename)
        self.frame = wx.Frame(None, title='Auto Tidepole Reader')

        self.panel = wx.Panel(self.frame)
        self.PhotoMaxSize = 800

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
        img = wx.Image(800, 600)
        self.imageCtrl = wx.StaticBitmap(self.panel, wx.ID_ANY,
                                         wx.Bitmap(img))

        self.imageCtrl.Bind(wx.EVT_LEFT_DOWN, self.on_click)

        instructLbl = wx.StaticText(self.panel, label=instructions)
        self.photoTxt = wx.TextCtrl(self.panel, size=(200, -1))
        browseBtn = wx.Button(self.panel, label='Set Reference Height')
        browseBtn.Bind(wx.EVT_BUTTON, self.On_set_ref_height)

        browseDirBtn = wx.Button(self.panel, label='Get Tide Data')
        browseDirBtn.Bind(wx.EVT_BUTTON, self.onBrowseDir)

        nextBtn = wx.Button(self.panel, label='Next Image')
        nextBtn.Bind(wx.EVT_BUTTON, self.onNext)



        self.mainSizer = wx.BoxSizer(wx.VERTICAL)
        self.sizer = wx.BoxSizer(wx.HORIZONTAL)

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

    def On_set_ref_height(self, event):
        """
        Browse for file
        """
        wildcard = "JPEG files (*.jpg)|*.jpg"
        dialog = wx.FileDialog(None, "Choose a file",
                               wildcard=wildcard,
                               style=wx.FD_OPEN)
        if dialog.ShowModal() == wx.ID_OK:
            self.photoTxt.SetValue(dialog.GetPath())
        dialog.Destroy()
        self.onView()

        self.set_height = True



    def onNext(self, event):

        self.img_index = self.img_index + 1

        self.displayImage()



    def displayImage(self):

        img = cv2.imread(self.path + '\\' + self.dir[self.img_index])

        y, h = 0, int(img.shape[0]-img.shape[0]/4)
        x, w = int(img.shape[1]/5), int(img.shape[1] - img.shape[1]/3)

        crop_img = img[y:y + h, x:x + w]

        crop_img = cv2.cvtColor(crop_img, cv2.COLOR_BGR2RGB)



        print('shape:', img.shape)

        W = crop_img.shape[1]
        H = crop_img.shape[0]

        if W > H:
            NewW = self.PhotoMaxSize
            NewH = int(self.PhotoMaxSize * H / W)
        else:
            NewH = self.PhotoMaxSize
            NewW = int(self.PhotoMaxSize * W / H)

        print('w/h', NewH, NewW)

        img_resize = cv2.resize(crop_img, (NewW, NewH))


        bitmap = wx.Bitmap.FromBuffer(NewW, NewH, img_resize)

        self.imageCtrl.SetBitmap(bitmap)

        self.panel.Refresh()

    #
    # def set_ref_height(self):
    #
    #     pass


    def onBrowseDir(self, event):

        print('ok')

        frame = wx.Frame(None, -1, 'win.py')
        frame.SetSize(0, 0, 200, 50)

        dlg = wx.DirDialog(frame, "Open a dircetory with supportted files", "",
                    wx.DD_DEFAULT_STYLE | wx.DD_DIR_MUST_EXIST)
        if dlg.ShowModal() == wx.ID_OK:
            self.path = dlg.GetPath()
            self.dir = os.listdir(self.path)

            print('path:', self.path)
            print('dir:', self.dir)

            # self.images = self.load_images_folder(self.path)
            # self.updateDisplay(path)

        dlg.Destroy()

        self.displayImage()

    def onView(self):

        filepath = self.photoTxt.GetValue()
        img = wx.Image(filepath, wx.BITMAP_TYPE_ANY)

        img = cv2.rectangle(img, (2423,3), (2458,1216), (0,200,0), 1)
        # scale the image, preserving the aspect ratio
        W = img.GetWidth()
        H = img.GetHeight()
        if W > H:
            NewW = self.PhotoMaxSize
            NewH = self.PhotoMaxSize * H / W
        else:
            NewH = self.PhotoMaxSize
            NewW = self.PhotoMaxSize * W / H
        img = img.Scale(NewW, NewH)
        self.imageCtrl.SetBitmap(wx.Bitmap(img))
        self.panel.Refresh()


    def crop_img(self):


        filepath = self.photoTxt.GetValue()

        img = cv2.imread(filepath)

        y, h = 0, int(img.shape[0] - img.shape[0] / 4)
        x, w = int(img.shape[1] / 5), int(img.shape[1] - img.shape[1] / 3)

        crop_img = img[y:y + h, x:x + w]



        print('shape:', img.shape)

        W = crop_img.shape[1]
        H = crop_img.shape[0]

        if W > H:
            NewW = self.PhotoMaxSize
            NewH = int(self.PhotoMaxSize * H / W)
        else:
            NewH = self.PhotoMaxSize
            NewW = int(self.PhotoMaxSize * W / H)

        print('w/h', NewH, NewW)

        img_resize = cv2.resize(crop_img, (NewW, NewH))




        print('click 1&2', self.clicks[0], self.clicks[1])

        x, w = self.clicks[0][0], self.clicks[1][0]
        y, h = self.clicks[0][1], self.clicks[1][1]

        crop_img2 = img_resize[y:h, x:w]

        crop_img2 = cv2.cvtColor(crop_img2, cv2.COLOR_BGR2RGB)

        W = crop_img2.shape[1]
        H = crop_img2.shape[0]

        if W > H:
            NewW = self.PhotoMaxSize
            NewH = int(self.PhotoMaxSize * H / W)
        else:
            NewH = self.PhotoMaxSize
            NewW = int(self.PhotoMaxSize * W / H)


        img_resize = cv2.resize(crop_img2, (NewW, NewH))

        print(img_resize.shape, 'crop img_resize2')


        bitmap = wx.Bitmap.FromBuffer(NewW, NewH, img_resize)

        self.imageCtrl.SetBitmap(bitmap)

        self.panel.Refresh()

        self.clicks = []


        pass



if __name__ == '__main__':
    app = PhotoCtrl()
    app.MainLoop()