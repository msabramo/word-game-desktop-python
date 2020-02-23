import sys, wx, wx.html, wx.lib.wxpTag, wx.lib.hyperlink as hl

_ = wx.GetTranslation


class AboutDialog(wx.Dialog):

    def __init__(self, parent):
        wx.Dialog.__init__(self, parent, -1, _("About Word Up!"),
            style = wx.DEFAULT_DIALOG_STYLE)

        version = parent.VERSION

        title = wx.StaticText(self, -1, "Word Up!") 
        title.SetFont(wx.Font(18, wx.DEFAULT, wx.NORMAL, wx.BOLD))
        
        sz = wx.BoxSizer(wx.VERTICAL)
        sz.Add((15, 15))
        sz.Add(title, 0, wx.ALIGN_CENTRE|wx.ALL, 5)
        sz.Add(wx.StaticText(self, -1, "Version %s" % version),
               0, wx.ALIGN_CENTRE|wx.ALL, 5)

        sz.Add(hl.HyperLinkCtrl(self, -1, "Marc Abramowitz",
                                URL="http://marc-abramowitz.com/"),
               0, wx.ALIGN_CENTRE|wx.ALL, 5)
        sz.Add(hl.HyperLinkCtrl(self, -1, "Word Up! Web",
                                URL="http://marc-abramowitz.com/word_up"),
               0, wx.ALIGN_CENTRE|wx.ALL, 5)
        if parent.FREE_EDITION:
            sz.Add(hl.HyperLinkCtrl(self, -1, "Buy Word Up! Premium Edition",
                                    URL="http://marc-abramowitz.com/word_up/upgrade.php"),
               0, wx.ALIGN_CENTRE|wx.ALL, 5)

        sz.Add((15, 15))
        sz.Add(wx.StaticLine(self, -1, style = wx.LI_HORIZONTAL),
               0, wx.ALIGN_CENTRE|wx.ALL|wx.EXPAND, 5)
        sz.Add((5, 5))

        okButton = wx.Button(self, wx.ID_OK)
        okButton.SetDefault()
        sz.Add(okButton, 0, wx.ALIGN_RIGHT|wx.RIGHT|wx.BOTTOM, 20)
        self.Bind(wx.EVT_BUTTON, self.onOk, id = wx.ID_OK)

        self.SetSizer(sz)
        self.SetAutoLayout(True)
        sz.SetMinSize((300, -1))
        sz.Fit(self)
        self.CentreOnParent(wx.BOTH)

    def onOk(self, evt):
        self.Close()
