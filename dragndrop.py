import wx
from PIL import Image
from wx.lib.pubsub import pub
import os
import matcher

PhotoMaxSize = 300
photos_per_row = 3
imgpath = ""
name = 'alexandra daddario'


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
    def __init__(self, redirect=False, filename=None):
        wx.App.__init__(self, redirect, filename)
        self.frame = wx.Frame(None, title='Face Recognition Algeo', size=(1000, 1000))
        self.frame.mainSizer = wx.BoxSizer(wx.VERTICAL)

        self.frame.drag_and_drop_panel = wx.Panel(self.frame)
        pub.subscribe(self.update_image_on_dnd, 'dnd')
        self.createWidgets()

        self.frame.show_img_panel = wx.Panel(self.frame)
        self.createResultWidget()
        self.frame.show_img_panel.Hide()
        self.frame.mainSizer.Fit(self.frame)

        self.frame.Show()

    def createWidgets(self):
        self.frame.drag_and_drop_panel.SetSizer(self.frame.mainSizer)

        instructions = 'Drag and drop your image here'
        img = wx.Image(PhotoMaxSize, PhotoMaxSize)
        self.imageCtrl = wx.StaticBitmap(self.frame.drag_and_drop_panel, wx.ID_ANY,
                                         wx.Bitmap(img))
        self.filedroptarget = DropTarget(self)
        self.imageCtrl.SetDropTarget(self.filedroptarget)

        instructLbl = wx.StaticText(self.frame.drag_and_drop_panel, label=instructions)
        self.photoTxt = wx.TextCtrl(self.frame.drag_and_drop_panel, size=(200, -1))
        browseBtn = wx.Button(self.frame.drag_and_drop_panel, label='Match')
        browseBtn.Bind(wx.EVT_BUTTON, self.on_match)

        self.frame.mainSizer.Add(instructLbl, 0, wx.ALL, 5)
        self.frame.mainSizer.Add(self.imageCtrl, 0, wx.ALL, 5)

        self.frame.sizer = wx.BoxSizer(wx.HORIZONTAL)
        self.frame.sizer.Add(self.photoTxt, 0, wx.ALL, 5)
        self.frame.sizer.Add(browseBtn, 0, wx.ALL, 5)

        self.frame.mainSizer.Add(self.frame.sizer, 0, wx.ALL, 5)

    def createResultWidget(self):
        self.frame.show_img_panel.SetSizer(self.frame.mainSizer)

        instructLbl = wx.StaticText(self.frame.show_img_panel, label="Here's top 6 images match!")
        self.frame.mainSizer.Add(instructLbl, 0, wx.ALL, 5)

        self.imageMatch = []
        for i in range(6):
            img = wx.Image(PhotoMaxSize, PhotoMaxSize)
            self.imageMatch.append(wx.StaticBitmap(self.frame.show_img_panel, wx.ID_ANY,
                                                   wx.Bitmap(img)))
        for i in range(len(self.imageMatch) // photos_per_row):
            self.frame.sizer = wx.BoxSizer(wx.HORIZONTAL)
            self.frame.sizer.Add(self.imageMatch[i * photos_per_row + 0], 0, wx.ALL, 5)
            self.frame.sizer.Add(self.imageMatch[i * photos_per_row + 1], 0, wx.ALL, 5)
            self.frame.sizer.Add(self.imageMatch[i * photos_per_row + 2], 0, wx.ALL, 5)
            self.frame.mainSizer.Add(self.frame.sizer, 0, wx.ALL, 5)

        browseBtn = wx.Button(self.frame.show_img_panel, label='Match other photo')
        browseBtn.Bind(wx.EVT_BUTTON, self.on_get_other_photo)
        self.frame.mainSizer.Add(browseBtn, 0, wx.ALL, 5)

    def on_match(self, event):
        self.matches = matcher.get_match_img_path(imgpath, os.path.join(os.getcwd(), 'result/pins_' + name))
        self.frame.drag_and_drop_panel.Hide()
        self.frame.mainSizer.Replace(self.frame.show_img_panel, self.frame.show_img_panel)
        self.frame.show_img_panel.Show()
        self.frame.Layout()

    def on_get_other_photo(self, event):
        self.frame.show_img_panel.Hide()
        self.frame.drag_and_drop_panel.Show()
        self.frame.mainSizer.Replace(self.frame.show_img_panel, self.frame.drag_and_drop_panel)
        self.frame.Layout()
        global imgpath
        imgpath = ""

    def update_image_on_dnd(self, filepath):
        self.on_view(filepath=filepath, images_slot=self.imageCtrl)
        self.frame.drag_and_drop_panel.Refresh()

    def on_view(self, filepath, images_slot):
        match_img = wx.Image(filepath, wx.BITMAP_TYPE_ANY)
        print(filepath)
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
        images_slot.SetBitmap(wx.Bitmap(match_img))


if __name__ == '__main__':
    app = PhotoCtrl()
    app.MainLoop()
