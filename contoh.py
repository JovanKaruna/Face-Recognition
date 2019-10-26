import wx


class myframe(wx.Frame):
    def __init__(self):
        "Constructor. No arguments"
        wx.Frame.__init__(self, None, size=(1000, 700))
        self.TitlePanel = wx.Panel(self, size=(350, 400))
        self.newPanel = wx.Panel(self, size=(300, 250))
        imgPanel = wx.Panel(self, size=(300, 250))
        modulePanel = wx.Panel(self, size=(350, 250))
        self.TCPanel = wx.Panel(self, size=(300, 250))
        ############################################
        self.TitlePanel.SetBackgroundColour("green")
        imgPanel.SetBackgroundColour("red")
        modulePanel.SetBackgroundColour("blue")
        self.TCPanel.SetBackgroundColour("yellow")
        self.newPanel.SetBackgroundColour("black")
        self.newPanel.Hide()
        ############################################
        self.myGridSizer = wx.GridBagSizer(1, 1)
        self.myGridSizer.Add(self.TitlePanel, pos=(0, 0), span=(4, 8), flag=wx.EXPAND)
        self.myGridSizer.Add(imgPanel, pos=(0, 10), span=(4, 8), flag=wx.ALL)
        self.myGridSizer.Add(modulePanel, pos=(10, 0), span=(1, 8), flag=wx.ALL)
        self.myGridSizer.Add(self.TCPanel, pos=(10, 10), span=(4, 8), flag=wx.ALL)
        #############################################
        self.text1 = wx.StaticText(self.TitlePanel, label="This is a test run", style=2, size=(350, -1))
        font = wx.Font(18, wx.DECORATIVE, wx.ITALIC, wx.BOLD, wx.NORMAL)
        self.text1.SetFont(font)
        #############################################
        self.SetSizer(self.myGridSizer)
        self.text1.Bind(wx.EVT_LEFT_DCLICK, self.hideMe)
        imgPanel.Bind(wx.EVT_LEFT_DCLICK, self.showMe)
        self.myGridSizer.SetEmptyCellSize((0, 0))

    def hideMe(self, event):
        self.TCPanel.Hide()
        self.myGridSizer.Add(self.newPanel, pos=(5, 10), span=(4, 8), flag=wx.ALL)
        self.newPanel.Show()
        self.Layout()

    def showMe(self, event):
        print("show!")
        self.newPanel.Hide()
        self.TCPanel.Show()
        self.Layout()


if __name__ == "__main__":
    app = wx.App()
    region = myframe()
    region.Show()
    app.MainLoop()
