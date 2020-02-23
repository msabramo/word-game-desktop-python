#!/usr/bin/env pythonw

import copy, sys, wx
import wx.lib.mixins.listctrl as listmix
from Dialogs.GameDetailsDialog import GameDetailsDialog


class TopScoreListCtrl(wx.ListCtrl):

    def __init__(self, parent, id=wx.ID_ANY, pos=wx.DefaultPosition,
                 size=wx.DefaultSize, style=0):
        wx.ListCtrl.__init__(self, parent, id, pos, size, style)
    

class TopScoreDialog(wx.Frame, listmix.ColumnSorterMixin):

    instance = None

    @classmethod
    def Display(cls, parent, topScores, *args, **kwargs):
        if cls.instance:
            cls.instance.Raise()
        else:
            cls.instance = cls(parent, topScores, *args, **kwargs)

    def __init__(self, parent, topScores, *args, **kwargs):
        wx.Frame.__init__(self, parent, *args, **kwargs)
        self.panel = wx.Panel(self)
        self.topScores = topScores
        vbox = wx.BoxSizer(wx.VERTICAL)
        self.panel.SetSizer(vbox)

        if sys.platform == 'darwin':
            wx.SystemOptions.SetOption("mac.listctrl.always_use_generic", False)
        
        self.list = wx.ListCtrl(self.panel, style=wx.LC_REPORT)
        self.PopulateList(topScores)

        self.buttonsHbox = wx.BoxSizer(wx.HORIZONTAL)
        self.viewGameDetailsButton = wx.Button(self.panel, wx.ID_ANY, 'View Game Details...')
        self.closeButton = wx.Button(self.panel, wx.ID_CLOSE)
        self.buttonsHbox.Add(self.viewGameDetailsButton)
        self.buttonsHbox.Add(self.closeButton, flag=wx.LEFT, border=12)
        
        def ShowGameDetailsDialog(event=None):
            row = self.list.GetFirstSelected()
            game = self.topScores[row][1]
            gameDetailsDialog = GameDetailsDialog(parent=self,
                                                  topWindow=parent,
                                                  game=game,
                                                  title='Game Details',
                                                  size=(300, 350))
        
        self.viewGameDetailsButton.Bind(wx.EVT_BUTTON, ShowGameDetailsDialog)
        self.list.Bind(wx.EVT_LEFT_DCLICK, ShowGameDetailsDialog)
        self.closeButton.Bind(wx.EVT_BUTTON, self.OnClose)
        self.closeButton.SetDefault()
        
        vbox.Add(self.list, 1, flag=wx.EXPAND|wx.ALL, border=20)
        vbox.Add(self.buttonsHbox, flag=wx.BOTTOM|wx.LEFT|wx.RIGHT|wx.ALIGN_RIGHT, border=20)

        vbox.Layout()
        self.Show(True)

    def GetListCtrl(self):
        return self.list
        
    def PopulateList(self, topScores):
        self.list.InsertColumn(0, "Rank", wx.LIST_FORMAT_RIGHT)
        self.list.InsertColumn(1, "Score", wx.LIST_FORMAT_RIGHT)
        self.list.InsertColumn(2, "Duration", wx.LIST_FORMAT_RIGHT)
        self.list.InsertColumn(3, "Name")
        self.list.InsertColumn(4, "Date")

        self.itemDataMap = {}

        for (score, game) in topScores:
            name = game.info['name']
            start_time = game.info['start_time'].replace(microsecond=0)
            end_time = game.info['end_time'].replace(microsecond=0)
            end_time_str = end_time.strftime('%Y-%m-%d %H:%M')
            duration_str = str(end_time - start_time)
            
            index = self.list.InsertItem(sys.maxint, '')
            item = (index + 1,
                    score,
                    duration_str,
                    name,
                    end_time_str)
            for columnIdx in range(0, 5):
                self.list.SetItem(index, columnIdx, str(item[columnIdx]))
            self.list.SetItemData(index, index)
            self.itemDataMap[index] = item

        listmix.ColumnSorterMixin.__init__(self, numColumns=5)

        self.list.SetColumnWidth(0, 50)
        self.list.SetColumnWidth(1, 60)
        self.list.SetColumnWidth(2, 70)
        self.list.SetColumnWidth(3, 80)
        self.list.SetColumnWidth(4, 150)

    def OnClose(self, event=None):
        self.Close()
        self.__class__.instance = None
