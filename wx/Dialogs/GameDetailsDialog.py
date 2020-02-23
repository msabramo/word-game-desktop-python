#!/usr/bin/env pythonw

import copy, sys, wx
import wx.lib.mixins.listctrl as listmix


class GameDetails(wx.ListCtrl, listmix.ColumnSorterMixin):

    def __init__(self, parent, game):
        if sys.platform == 'darwin':
            wx.SystemOptions.SetOption("mac.listctrl.always_use_generic", False)
        
        wx.ListCtrl.__init__(self, parent, style=wx.LC_REPORT)
        self.PopulateList(game)
        listmix.ColumnSorterMixin.__init__(self, numColumns=3)

        self.SortListItems(0, 0)
        self.Show()

    def GetListCtrl(self):
        """
        Needed by ColumnSorterMixin
        """
        
        return self

    def Clear(self):
        self.itemDataMap = {}
        self.itemIndexMap = {}
        self.DeleteAllItems()
        
    def PopulateList(self, game):
        self.InsertColumn(0, "Time", wx.LIST_FORMAT_RIGHT)
        self.InsertColumn(1, "Word")
        self.InsertColumn(2, "Score", wx.LIST_FORMAT_RIGHT)
        self.itemDataMap = {}
        self.itemIndexMap = {}

        for (word_tiles, time) in game.words:
            word = ''.join([tup[0] for tup in word_tiles])
            word_score = game.calc_word_score(word)
            self.AddWord(time, word, word_score)

        self.SetColumnWidth(0, 70)
        self.SetColumnWidth(1, 100)
        self.SetColumnWidth(2, 70)

    def AddWord(self, time, word, word_score):
        index = self.InsertItem(sys.maxint, '')
        item = (time, word, word_score)
        for columnIdx in range(0, 3):
            self.SetItem(index, columnIdx, str(item[columnIdx]))
        self.SetItemData(index, index)
        self.itemDataMap[len(self.itemDataMap)] = item
        if hasattr(self, '_col'): self.SortListItems()
        
    def OnGetItemText(self, item, col):
        index = self.itemIndexMap[item]
        s = self.itemDataMap[index][col]
        return s


class GameDetailsDialog(wx.Frame):

    def __init__(self, parent, topWindow,
                 game, title, size, *args, **kwargs):
        wx.Frame.__init__(self, parent=parent, title=title, size=size, *args, **kwargs)
        self.panel = wx.Panel(self)

        self.list = GameDetails(self.panel, game)
        vbox = wx.BoxSizer(wx.VERTICAL)
        vbox.Add(self.list, 1, flag=wx.EXPAND|wx.ALL, border=20)

        self.buttonsHbox = wx.BoxSizer(wx.HORIZONTAL)
        self.replayGameButton = wx.Button(self.panel, wx.ID_ANY, 'Replay Game...')
        self.closeButton = wx.Button(self.panel, wx.ID_CLOSE)
        self.buttonsHbox.Add(self.replayGameButton)
        self.buttonsHbox.Add(self.closeButton, flag=wx.LEFT, border=12)
        
        def OnReplayGame(button):
            topWindow.game = topWindow.get_game()
            topWindow.game.board = copy.deepcopy(game.orig_board)
            topWindow.board_widget.SetBoard(topWindow.game.board)
            topWindow.ClearWord()
            topWindow.RefreshWordScore()
            topWindow.RefreshTotalScore()
    
        self.replayGameButton.Bind(wx.EVT_BUTTON, OnReplayGame)
        self.closeButton.Bind(wx.EVT_BUTTON, self.OnClose)
        self.closeButton.SetDefault()
        
        vbox.Add(self.buttonsHbox, flag=wx.BOTTOM|wx.LEFT|wx.RIGHT|wx.ALIGN_RIGHT, border=20)

        self.panel.SetSizer(vbox)
        vbox.Layout()
        self.Show(True)
        
    def OnClose(self, event=None):
        self.Close()
