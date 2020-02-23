import sys, webbrowser, wx


class WordsLeftDialog(wx.Frame):

    def __init__(self, parent, game, words_left, *args, **kwargs):
        wx.Frame.__init__(self, parent=parent,
                          title='Words Left',
                          size=(355, 295),
                          *args, **kwargs)
        self.panel = wx.Panel(self)

        if sys.platform == 'darwin':
            wx.SystemOptions.SetOptionInt("mac.listctrl.always_use_generic", False)

        staticText = wx.StaticText(self.panel, wx.ID_ANY,
                                   'You ended the game.\n\n' +
                                   'Here are some words that were remaining:')
        self.list = wx.ListCtrl(self.panel, style=wx.LC_REPORT|wx.LC_SINGLE_SEL)

        vbox = wx.BoxSizer(wx.VERTICAL)
        vbox.Add(staticText, 0, flag=wx.TOP|wx.LEFT|wx.RIGHT, border=20)
        vbox.Add(self.list, 1, flag=wx.EXPAND|wx.ALL, border=20)

        self.PopulateList(game, words_left)

        self.buttonsHbox = wx.BoxSizer(wx.HORIZONTAL)
        self.lookupWordButton = wx.Button(self.panel, wx.ID_ANY, 'Lookup word...')
        self.closeButton = wx.Button(self.panel, wx.ID_CLOSE)
        self.buttonsHbox.Add(self.lookupWordButton)
        self.buttonsHbox.Add(self.closeButton, flag=wx.LEFT, border=12)
        
        def OnLookupWord(button):
            row = self.list.GetFirstSelected()
            word = words_left[row]
            webbrowser.open('http://www.m-w.com/dictionary/%s' % word)
        
        self.lookupWordButton.Bind(wx.EVT_BUTTON, OnLookupWord)
        self.closeButton.Bind(wx.EVT_BUTTON, self.OnClose)
        self.closeButton.SetDefault()
        
        vbox.Add(self.buttonsHbox, flag=wx.BOTTOM|wx.LEFT|wx.RIGHT|wx.ALIGN_RIGHT, border=20)

        self.panel.SetSizer(vbox)
        vbox.Layout()
##         vbox.Fit(self)
        self.Show(True)

    def PopulateList(self, game, words_left):
        self.list.InsertColumn(0, "Word")
        self.list.InsertColumn(1, "Score", wx.LIST_FORMAT_RIGHT)

        for row, word in enumerate(words_left):
            score = game.calc_word_score(word)
            index = self.list.InsertStringItem(sys.maxint, word)
            self.list.SetStringItem(row, 0, word)
            self.list.SetStringItem(row, 1, str(score))

        self.list.SetColumnWidth(0, 80)
        self.list.SetColumnWidth(1, 70)

    def OnClose(self, event=None):
        self.Close()
        
        """
        dialog_name = 'words_left_dialog'
        glade_xml = gtk.glade.XML('resources/glade/WordUp.glade', dialog_name)
        dialog = glade_xml.get_widget(dialog_name)
        dialog.set_transient_for(parent_window)
        treeview = glade_xml.get_widget('words_left_treeview')
        
        def lookup_word(button):
            row = treeview.get_cursor()[0][0]
            word = words_left[row]
            webbrowser.open('http://www.m-w.com/dictionary/%s' % word)
            
        glade_xml.get_widget('words_left_lookup_word_button').connect('clicked', lookup_word)
        glade_xml.get_widget('words_left_close_button').connect('clicked', lambda w: dialog.destroy())
        populate_treeview(treeview, game, words_left)
        dialog.run()
        dialog.destroy()
        """
