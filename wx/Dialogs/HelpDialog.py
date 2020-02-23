import webbrowser, wx, wx.html
from wx.lib.ClickableHtmlWindow import PyClickableHtmlWindow

_ = wx.GetTranslation


class HelpDialog(wx.Dialog):

    def __init__(self, parent, htmlFilename):
        wx.Dialog.__init__(self, parent, -1, _("Word Up! Help"), size=(-1, 550))
        panel = wx.Panel(self)
        
        htmlWindow = PyClickableHtmlWindow(panel, -1)
        htmlWindow.LoadFile(htmlFilename)

        okButton = wx.Button(panel, wx.ID_OK)
        okButton.SetDefault()
        self.Bind(wx.EVT_BUTTON, self.onOk, id=wx.ID_OK)

        vbox = wx.BoxSizer(wx.VERTICAL)
        vbox.Add(htmlWindow, 1, wx.EXPAND)
        vbox.Add(okButton, 0, wx.ALIGN_RIGHT|wx.ALL, 20)
        vbox.SetMinSize((300, 300))
        panel.SetSizer(vbox)
        vbox2 = wx.BoxSizer(wx.VERTICAL)
        vbox2.Add(panel, 1, wx.EXPAND)
        self.SetSizer(vbox2)
        
        self.CentreOnParent(wx.BOTH)

    def onOk(self, evt):
        self.Close()
