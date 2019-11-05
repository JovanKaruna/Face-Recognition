import wx
import wx.lib.scrolledpanel
from pubsub import pub
import matcher

# Global Variables
title = "Face Recognition Algeo"
photos_shown = 20
photos_per_row = 2
total_rows = (photos_shown - 1) // photos_per_row + 1
app = wx.App()
screenSize = wx.DisplaySize()
screenWidth = screenSize[0]
screenHeight = screenSize[1]

# constants
PhotoMaxSize = screenHeight // 5
app.ExitMainLoop()
offset = 8
width = PhotoMaxSize * photos_per_row + offset * (photos_per_row + 1)
height = width * 2
imgpath = ""
image_database = "features.pck"
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
        # Add a panel so it looks the correct on all platforms
        self.panel = wx.Panel(self, wx.ID_ANY)
 
        ico = wx.Icon('icon.ico', wx.BITMAP_TYPE_ICO)
        self.SetIcon(ico)
    

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
        
        #Face
        faceLbl = wx.StaticText(self,-1, "FACE RECOGNITION", (100, 50), (300, -1), wx.ALIGN_CENTER)
        faceLbl.SetForegroundColour(wx.WHITE) # set text color
        font = wx.Font(17, wx.DECORATIVE, wx.NORMAL, wx.BOLD)
        faceLbl.SetFont(font)

        # instruction
        instructLbl = wx.StaticText(self,-1, "Drag and drop your image here", (100, 50), (300, -1), wx.ALIGN_CENTER)
        instructLbl.SetForegroundColour(wx.WHITE) # set text color
        font = wx.Font(9, wx.DECORATIVE, wx.NORMAL, wx.NORMAL)
        instructLbl.SetFont(font)

        # image slot and bind it with drag and drop function
        img = wx.Image(PhotoMaxSize * 2 - offset, PhotoMaxSize * 2 - offset)
        self.imageCtrl = wx.StaticBitmap(self, wx.ID_ANY, wx.Bitmap(img))
        filedroptarget = DropTarget(parent)
        self.imageCtrl.SetDropTarget(filedroptarget)

        # cosine button
        cosineBtn = wx.Button(self, label='with Cosine Method', size=(125,30))
        cosineBtn.Bind(wx.EVT_BUTTON, self.on_cosine)
        cosineBtn.SetBackgroundColour(wx.WHITE) 


        # euclidian button
        euclidianBtn = wx.Button(self, label='with Euclidean Method', size = (155,30))
        euclidianBtn.Bind(wx.EVT_BUTTON, self.on_euclidian)
        euclidianBtn.SetBackgroundColour(wx.WHITE)

        #Kelompok
        by = wx.StaticText(self,-1, "Product by:", (100, 50), (300, -1), wx.ALIGN_CENTER)
        by.SetForegroundColour(wx.WHITE) # set text color
        font = wx.Font(13, wx.DECORATIVE, wx.NORMAL, wx.BOLD)
        font.SetUnderlined(True)
        by.SetFont(font)

        by1 = wx.StaticText(self,-1, "Jovan Karuna Cahyadi / 13518024", (100, 50), (300, -1), wx.ALIGN_CENTER)
        by1.SetForegroundColour(wx.WHITE) # set text color
        font = wx.Font(10, wx.DECORATIVE, wx.NORMAL, wx.NORMAL)
        by1.SetFont(font)

        by2 = wx.StaticText(self,-1, "Jonathan Yudi Gunawan / 13518084", (100, 50), (300, -1), wx.ALIGN_CENTER)
        by2.SetForegroundColour(wx.WHITE) # set text color
        font = wx.Font(10, wx.DECORATIVE, wx.NORMAL, wx.NORMAL)
        by2.SetFont(font)

        by3 = wx.StaticText(self,-1, "William / 13518138", (100, 50), (300, -1), wx.ALIGN_CENTER)
        by3.SetForegroundColour(wx.WHITE) # set text color
        font = wx.Font(10, wx.DECORATIVE, wx.NORMAL, wx.NORMAL)
        by3.SetFont(font)

        #footer
        footer = wx.StaticText(self,-1, "© 2019 TimDariITB All Rights Reserved", (100, 50), (300, -1), wx.ALIGN_CENTER)
        footer.SetForegroundColour(wx.WHITE) # set text color
        font = wx.Font(7, wx.DECORATIVE, wx.NORMAL, wx.NORMAL)
        footer.SetFont(font)

        #line
        line = wx.StaticLine(self, wx.ID_ANY, size=(270, -1), style=wx.LI_HORIZONTAL)
        line2 = wx.StaticLine(self, wx.ID_ANY, size=(300, -1), style=wx.LI_HORIZONTAL)

        # arrange position
        self.mainSizer.Add(faceLbl, 0, wx.ALL, 7)
        self.mainSizer.Add(line,0,wx.ALL|wx.ALIGN_CENTER,0)
        self.mainSizer.Add(instructLbl, 0, wx.ALL, 3)
        self.mainSizer.Add(self.imageCtrl, 0, wx.ALL, 5)
        sizer = wx.BoxSizer(wx.HORIZONTAL)
        sizer.Add(cosineBtn, 0, wx.ALL|wx.ALIGN_CENTER, 5)
        sizer.Add(euclidianBtn, 0, wx.ALL|wx.ALIGN_CENTER, 5)
        self.mainSizer.Add(sizer, 0, wx.ALL, 10)
        self.mainSizer.Add(by,0,wx.ALL,8)
        self.mainSizer.Add(by1,0,wx.ALL,3)
        self.mainSizer.Add(by2,0,wx.ALL,3)
        self.mainSizer.Add(by3,0,wx.ALL,3)
        self.mainSizer.Add(line2,0,wx.ALL|wx.ALIGN_CENTER,15)
        self.mainSizer.Add(footer,0,wx.ALL,0)
        
        
        self.Colours()
        self.SetSizer(self.mainSizer)
        self.Layout()

    def Colours(self):
        self.SetBackgroundColour((35,35,35))
    
    def __del__(self):
        pass

    def on_cosine(self, event):
        self.match_img(event, method='cosine')

    def on_euclidian(self, event):
        self.match_img(event, method='euclidian')

    def match_img(self, event, method):
        self.Hide()

        # get matching images, then load it to second panel
        self.matches = matcher.get_match_img_path(imgpath, image_database, topn=photos_shown, method=method)
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
        instructLbl = wx.StaticText(self,-1, "Here's top " + str(photos_shown) + " images match!", (100, 50), (300, -1), wx.ALIGN_CENTER)
        instructLbl.SetForegroundColour(wx.WHITE) # set text color
        font = wx.Font(15, wx.DECORATIVE, wx.NORMAL, wx.NORMAL)
        instructLbl.SetFont(font)
        self.mainSizer.Add(instructLbl, 0, wx.ALL, 5)
        
        #line
        line = wx.StaticLine(self, wx.ID_ANY, size=(280, -1), style=wx.LI_HORIZONTAL)
        topline = wx.StaticLine(self, wx.ID_ANY, size=(280, -1), style=wx.LI_HORIZONTAL)
        self.mainSizer.Add(topline, 0, wx.ALL|wx.ALIGN_CENTER, 2)

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


        #footer
        footer = wx.StaticText(self,-1, "© 2019 TimDariITB All Rights Reserved", (100, 50), (300, -1), wx.ALIGN_CENTER)
        footer.SetForegroundColour(wx.WHITE) # set text color
        font = wx.Font(7, wx.DECORATIVE, wx.NORMAL, wx.NORMAL)
        footer.SetFont(font)

        # get other photo button
        otherBtn = wx.Button(self, label='Match other photo')
        otherBtn.Bind(wx.EVT_BUTTON, self.on_get_other_photo)
        otherBtn.SetBackgroundColour(wx.WHITE)
        self.mainSizer.Add(otherBtn, 0, wx.ALL|wx.ALIGN_CENTER, 5)
        self.mainSizer.Add(line,0,wx.ALL|wx.ALIGN_CENTER,5)
        self.mainSizer.Add(footer,0,wx.ALL,2)



        self.SetSizer(self.mainSizer)
        self.Colours()
        self.Layout()
    
    def Colours(self):
        self.SetBackgroundColour((35,35,35))

    def __del__(self):
        pass

    def on_get_other_photo(self, event):
        self.Hide()
        self.parent.drag_and_drop_panel.Show()

    def load_img(self, matches):
        for i in range(photos_shown):
            slot = self.imageMatch[i]
            match = matches[i]
            self.parent.on_view(match, slot)
