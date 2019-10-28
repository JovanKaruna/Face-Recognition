import wx
from pubsub import pub
import os
import matcher


PhotoMaxSize = 300
photos_per_row = 3
imgpath = ""
name = 'alexandra daddario'
title = "Face Recognition Algeo"
appSize = wx.Size(970, 770)
photos_shown = 6


class DropTarget(wx.FileDropTarget):
    def __init__(self, widget):
        wx.FileDropTarget.__init__(self)
        self.widget = widget

    def OnDropFiles(self, x, y, filenames):
        global imgpath
        imgpath = filenames[0]
        pub.sendMessage('dnd', filepath=imgpath)
        return True


class MainFrame(wx.Frame):
    def __init__(self, parent):
        wx.Frame.__init__(self, parent, id=wx.ID_ANY, title=title, size=appSize, style=wx.DEFAULT_FRAME_STYLE | wx.TAB_TRAVERSAL)
        pub.subscribe(self.update_image_on_dnd, 'dnd')

    def update_image_on_dnd(self, filepath):
        self.on_view(filepath=filepath, images_slot=self.drag_and_drop_panel.imageCtrl)

    def on_view(self, filepath, images_slot):
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
        images_slot.SetBitmap(wx.Bitmap(match_img))
        self.Refresh()


class panel_one (wx.Panel):
    matches = []

    def __init__(self, parent):
        wx.Panel.__init__(self, parent, id=wx.ID_ANY, pos=wx.DefaultPosition, size=appSize, style=wx.TAB_TRAVERSAL)
        self.mainSizer = wx.BoxSizer(wx.VERTICAL)

        instructions = 'Drag and drop your image here'
        img = wx.Image(PhotoMaxSize, PhotoMaxSize)
        self.imageCtrl = wx.StaticBitmap(self, wx.ID_ANY, wx.Bitmap(img))
        filedroptarget = DropTarget(parent)
        self.imageCtrl.SetDropTarget(filedroptarget)

        instructLbl = wx.StaticText(self, label=instructions)
        photoTxt = wx.TextCtrl(self, size=(200, -1))
        browseBtn = wx.Button(self, label='Match')
        browseBtn.Bind(wx.EVT_BUTTON, self.on_match)

        self.mainSizer.Add(instructLbl, 0, wx.ALL, 5)
        self.mainSizer.Add(self.imageCtrl, 0, wx.ALL, 5)

        sizer = wx.BoxSizer(wx.HORIZONTAL)
        sizer.Add(photoTxt, 0, wx.ALL, 5)
        sizer.Add(browseBtn, 0, wx.ALL, 5)

        self.mainSizer.Add(sizer, 0, wx.ALL, 5)
        self.SetSizer(self.mainSizer)
        self.Layout()

    def __del__(self):
        pass

    def on_match(self, event):
        self.Hide()
        self.matches = matcher.get_match_img_path(imgpath, os.path.join(os.getcwd(), 'result/pins_' + name), topn=photos_shown)
        self.parent.show_img_panel.load_img(self.matches)
        self.parent.show_img_panel.Show()
        self.Layout()


class panel_two (wx.Panel):
    def __init__(self, parent):
        wx.Panel.__init__(self, parent, id=wx.ID_ANY, size=appSize, style=wx.TAB_TRAVERSAL)
        self.mainSizer = wx.BoxSizer(wx.VERTICAL)

        instructLbl = wx.StaticText(self, label="Here's top 6 images match!")
        self.mainSizer.Add(instructLbl, 0, wx.ALL, 5)

        self.imageMatch = []
        for i in range(photos_shown):
            img = wx.Image(PhotoMaxSize, PhotoMaxSize)
            self.imageMatch.append(wx.StaticBitmap(self, wx.ID_ANY, wx.Bitmap(img)))

        for i in range(len(self.imageMatch) // photos_per_row):
            sizer = wx.BoxSizer(wx.HORIZONTAL)
            for j in range(photos_per_row):
                if len(parent.drag_and_drop_panel.matches) > (i * photos_per_row + j):
                    filepath = parent.drag_and_drop_panel.matches[i * photos_per_row + j]
                    parent.on_view(filepath, self.imageMatch[i * photos_per_row + j])
                sizer.Add(self.imageMatch[i * photos_per_row + j], 0, wx.ALL, 5)
            self.mainSizer.Add(sizer, 0, wx.ALL, 5)

        browseBtn = wx.Button(self, label='Match other photo')
        browseBtn.Bind(wx.EVT_BUTTON, self.on_get_other_photo)
        self.mainSizer.Add(browseBtn, 0, wx.ALL, 5)

        self.SetSizer(self.mainSizer)
        self.Layout()

    def __del__(self):
        pass

    def on_get_other_photo(self, event):
        self.Hide()
        self.parent.drag_and_drop_panel.Show()
        global imgpath
        imgpath = ""

    def load_img(self, matches):
        for i in range(len(self.imageMatch)):
            slot = self.imageMatch[i]
            match = matches[i]
            self.parent.on_view(match, slot)
