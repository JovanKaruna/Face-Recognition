import wx
import wx.lib.scrolledpanel
from pubsub import pub
import os
import matcher

# Global Variables
title = "Face Recognition Algeo"
photos_shown = 20
photos_per_row = 2
total_rows = (photos_shown - 1) // photos_per_row + 1

# constants
PhotoMaxSize = 280
offset = 8
width = PhotoMaxSize * photos_per_row + offset * (photos_per_row + 1)
height = width * 1.5
imgpath = ""
name = 'alexandra daddario'
appSize = wx.Size(width, height)


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
        self.on_view(filepath=filepath, images_slot=self.drag_and_drop_panel.imageCtrl, resize_to=PhotoMaxSize * 2 - offset)

    def on_view(self, filepath, images_slot, resize_to=PhotoMaxSize):
        match_img = wx.Image(filepath, wx.BITMAP_TYPE_ANY)

        # scale the image, preserving the aspect ratio
        W = match_img.GetWidth()
        H = match_img.GetHeight()
        if W > H:
            NewW = resize_to
            NewH = resize_to * H / W
        else:
            NewH = resize_to
            NewW = resize_to * W / H
        match_img = match_img.Scale(NewW, NewH)
        images_slot.SetBitmap(wx.Bitmap(match_img))
        self.Refresh()


class panel_one (wx.Panel):
    matches = []

    def __init__(self, parent):
        # setup panel
        wx.Panel.__init__(self, parent, id=wx.ID_ANY, pos=wx.DefaultPosition, size=appSize, style=wx.TAB_TRAVERSAL)
        self.mainSizer = wx.BoxSizer(wx.VERTICAL)

        # instruction
        instructions = 'Drag and drop your image here'
        instructLbl = wx.StaticText(self, label=instructions)

        # image slot and bind it with drag and drop function
        img = wx.Image(PhotoMaxSize * 2 - offset, PhotoMaxSize * 2 - offset)
        self.imageCtrl = wx.StaticBitmap(self, wx.ID_ANY, wx.Bitmap(img))
        filedroptarget = DropTarget(parent)
        self.imageCtrl.SetDropTarget(filedroptarget)

        # cosine button
        cosineBtn = wx.Button(self, label='with Cosine Method')
        cosineBtn.Bind(wx.EVT_BUTTON, self.on_cosine)

        # euclidian button
        euclidianBtn = wx.Button(self, label='with Euclidian Method')
        euclidianBtn.Bind(wx.EVT_BUTTON, self.on_euclidian)

        # arrange position
        self.mainSizer.Add(instructLbl, 0, wx.ALL, 5)
        self.mainSizer.Add(self.imageCtrl, 0, wx.ALL, 5)
        sizer = wx.BoxSizer(wx.HORIZONTAL)
        sizer.Add(cosineBtn, 0, wx.ALL, 5)
        sizer.Add(euclidianBtn, 0, wx.ALL, 5)
        self.mainSizer.Add(sizer, 0, wx.ALL, 5)

        self.SetSizer(self.mainSizer)
        self.Layout()

    def __del__(self):
        pass

    def on_cosine(self, event):
        self.match_img(event, method='cosine')

    def on_euclidian(self, event):
        self.match_img(event, method='euclidian')

    def match_img(self, event, method):
        self.Hide()

        # get matching images, then load it to second panel
        self.matches = matcher.get_match_img_path(imgpath, os.path.join(os.getcwd(), 'result/pins_' + name), topn=photos_shown, method=method)
        self.parent.show_img_panel.load_img(self.matches)
        self.parent.show_img_panel.Show()
        self.Layout()


class panel_two (wx.lib.scrolledpanel.ScrolledPanel):
    def __init__(self, parent):
        # setup scrolling panel
        wx.Panel.__init__(self, parent, id=wx.ID_ANY, size=appSize, style=wx.TAB_TRAVERSAL)
        self.SetupScrolling()
        self.mainSizer = wx.BoxSizer(wx.VERTICAL)

        # title
        instructLbl = wx.StaticText(self, label="Here's top " + str(photos_shown) + " images match!")
        self.mainSizer.Add(instructLbl, 0, wx.ALL, 5)

        # image slot * photos_shown
        self.imageMatch = []
        for i in range(photos_shown):
            img = wx.Image(PhotoMaxSize, PhotoMaxSize)
            self.imageMatch.append(wx.StaticBitmap(self, wx.ID_ANY, wx.Bitmap(img)))

        for i in range(total_rows):
            sizer = wx.BoxSizer(wx.HORIZONTAL)
            for j in range(photos_per_row):
                if len(parent.drag_and_drop_panel.matches) != 0:
                    filepath = parent.drag_and_drop_panel.matches[i * photos_per_row + j]
                    parent.on_view(filepath, self.imageMatch[i * photos_per_row + j])
                if i * photos_per_row + j < photos_shown:
                    sizer.Add(self.imageMatch[i * photos_per_row + j], 0, wx.ALL, 5)
            self.mainSizer.Add(sizer, 0, wx.ALL, 5)

        # get other photo button
        otherBtn = wx.Button(self, label='Match other photo')
        otherBtn.Bind(wx.EVT_BUTTON, self.on_get_other_photo)
        self.mainSizer.Add(otherBtn, 0, wx.ALL, 5)

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
        for i in range(photos_shown):
            slot = self.imageMatch[i]
            match = matches[i]
            self.parent.on_view(match, slot)
