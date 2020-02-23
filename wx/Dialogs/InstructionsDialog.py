import wx

class InstructionsDialog(wx.Dialog):

    def __init__(self, parent):
        wx.Dialog.__init__(self, parent, -1, _("Word Up! Help"),
            style = wx.DEFAULT_DIALOG_STYLE)

    
