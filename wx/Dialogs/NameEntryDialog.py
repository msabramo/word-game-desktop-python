import wx


def show(application, score, idx):
    dialog = wx.TextEntryDialog(application,
                                'You scored %d which is top score #%d!\n\n' % (score, idx + 1) +
                                'Please enter your name for the top score list.',
                                'Top Score!')
    dialog.ShowModal()
    dialog.Destroy()
        
    return dialog.GetValue()
        
