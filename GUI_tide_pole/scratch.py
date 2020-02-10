img = wx.Image(self.path + '\\' + self.dir[self.img_index], wx.BITMAP_TYPE_ANY)

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


def onViewDir(self):
    print('hi')

    img = cv2.imread(self.path + '\\' + self.dir[self.img_index])

    img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)

    color = (0, 255, 0)
    line_width = 5
    radius = 300
    point = (500, 500)
    cv2.circle(img, point, radius, color, line_width)

    print('shape:', img.shape)

    W = img.shape[1]
    H = img.shape[0]

    if W > H:
        NewW = self.PhotoMaxSize
        NewH = int(self.PhotoMaxSize * H / W)
    else:
        NewH = self.PhotoMaxSize
        NewW = int(self.PhotoMaxSize * W / H)

    print('w/h', NewH, NewW)

    img_resize = cv2.resize(img, (NewW, NewH))

    bitmap = wx.Bitmap.FromBuffer(NewW, NewH, img_resize)

    self.imageCtrl.SetBitmap(bitmap)

    self.panel.Refresh()
