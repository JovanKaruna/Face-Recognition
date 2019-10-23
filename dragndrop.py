import wx

from PIL import Image
from wx.lib.pubsub import pub
import os
import matcher
import time

PhotoMaxSize = 500


imgpath = ""


class DropTarget(wx.FileDropTarget):
    def __init__(self, widget):
        wx.FileDropTarget.__init__(self)
        self.widget = widget

    def OnDropFiles(self, x, y, filenames):
        print(x, y)
        global imgpath
        image = Image.open(filenames[0])
        imgpath = filenames[0]
        image.thumbnail((PhotoMaxSize, PhotoMaxSize))
        image.save('thumbnail.png')
        pub.sendMessage('dnd', filepath='thumbnail.png')
        return True


class PhotoCtrl(wx.App):
    filedroptarget = None

    def __init__(self, redirect=False, filename=None):
        wx.App.__init__(self, redirect, filename)
        self.frame = wx.Frame(None, title='Photo Control')

        self.panel = wx.Panel(self.frame)
        pub.subscribe(self.update_image_on_dnd, 'dnd')

        self.createWidgets()
        self.frame.Show()

    def createWidgets(self):
        instructions = 'Drag and drop your image here'
        img = wx.Image(PhotoMaxSize, PhotoMaxSize)
        self.imageCtrl = wx.StaticBitmap(self.panel, wx.ID_ANY,
                                         wx.Bitmap(img))
        self.filedroptarget = DropTarget(self)
        self.imageCtrl.SetDropTarget(self.filedroptarget)

        instructLbl = wx.StaticText(self.panel, label=instructions)
        self.photoTxt = wx.TextCtrl(self.panel, size=(200, -1))
        browseBtn = wx.Button(self.panel, label='Browse')
        browseBtn.Bind(wx.EVT_BUTTON, self.on_browse)

        self.mainSizer = wx.BoxSizer(wx.VERTICAL)
        self.sizer = wx.BoxSizer(wx.HORIZONTAL)

        self.mainSizer.Add(wx.StaticLine(self.panel, wx.ID_ANY),
                           0, wx.ALL | wx.EXPAND, 5)
        self.mainSizer.Add(instructLbl, 0, wx.ALL, 5)
        self.mainSizer.Add(self.imageCtrl, 0, wx.ALL, 5)
        self.sizer.Add(self.photoTxt, 0, wx.ALL, 5)
        self.sizer.Add(browseBtn, 0, wx.ALL, 5)
        self.mainSizer.Add(self.sizer, 0, wx.ALL, 5)

        self.panel.SetSizer(self.mainSizer)
        self.mainSizer.Fit(self.frame)

        self.panel.Layout()

    def on_browse(self, event):
        wildcard = "JPEG files (*.jpg)|*.jpg"
        dialog = wx.FileDialog(None, "Choose a file",
                               wildcard=wildcard,
                               style=wx.OPEN)
        if dialog.ShowModal() == wx.ID_OK:
            self.photoTxt.SetValue(dialog.GetPath())
        dialog.Destroy()
        self.on_view()

    def update_image_on_dnd(self, filepath):
        self.on_view(filepath=filepath)
        time.sleep(1)
        name = 'alexandra daddario'
        for match_img in matcher.get_match_img_path(imgpath, os.path.join(os.getcwd(), 'result/pins_' + name)):
            self.on_view(filepath=match_img)
            time.sleep(2)

    def on_view(self, filepath=None):
        match_img = wx.Image(filepath, wx.BITMAP_TYPE_ANY)
        # scale the image, preserving the aspect ratio
        W = match_img.GetWidth()
        H = match_img.GetHeight()
        if W > H:
            NewW = PhotoMaxSize
            NewH = PhotoMaxSize * H / W
        else:
            NewH = PhotoMaxSize
            NewW = PhotoMaxSize * W / H
        match_img = match_img.Scale(NewW, NewH)

        self.imageCtrl.SetBitmap(wx.Bitmap(match_img))
        self.panel.Refresh()


if __name__ == '__main__':
    app = PhotoCtrl()
    app.MainLoop()
