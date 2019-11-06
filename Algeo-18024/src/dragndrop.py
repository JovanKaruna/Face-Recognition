import wx
import gui_panel


class PhotoCtrl(gui_panel.MainFrame):
    def __init__(self, parent):
        gui_panel.MainFrame.__init__(self, parent)

        self.drag_and_drop_panel = Panel1(self)
        self.show_img_panel = Panel2(self)
        self.show_img_panel.Hide()

        bSizer1 = wx.BoxSizer(wx.VERTICAL)
        bSizer1.Add(self.drag_and_drop_panel)
        self.SetSizer(bSizer1)


class Panel1(gui_panel.panel_one):
    def __init__(self, parent):
        gui_panel.panel_one.__init__(self, parent)
        self.parent = parent


class Panel2(gui_panel.panel_two):
    def __init__(self, parent):
        gui_panel.panel_two.__init__(self, parent)
        self.parent = parent


def main():
    app = wx.App()
    window = PhotoCtrl(None)
    window.Show()
    app.MainLoop()


if __name__ == '__main__':
    main()
