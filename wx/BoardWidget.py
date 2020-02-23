import wx
import datetime

tileBitmaps = {}

def getBitmapForLetter(letter):
    global tileBitmaps
    
    if not tileBitmaps.get(letter):
        tileBitmaps[letter] = wx.Bitmap('resources/images/tiles/%s.png' % letter)

    return tileBitmaps[letter]


class BoardWidget(wx.BoxSizer):

    def __init__(self, parent, board, onClick=None):
        wx.BoxSizer.__init__(self, wx.HORIZONTAL)
        self.parent = parent
        self.board = board
        self.onClick = onClick
        self.buttons = [0 for i in range(84)]

        for colIdx, col in enumerate(board.cols):
            columnVbox = self.GetColumnVbox(colIdx, col)
            self.Add(columnVbox)

    def SetBoard(self, board):
        self.board = board
##         print 'refreshing boardwidget...'
##         start_time = datetime.datetime.now()
        self.Refresh()
##         end_time = datetime.datetime.now()
##         print 'refreshed boardwidget (%s).' % (end_time - start_time)

    def GetColumnVbox(self, colIdx, col):    
        vbox = wx.BoxSizer(wx.VERTICAL)
        vbox.AddSpacer(50)

        for rowIdx, letter in enumerate(col):
            if not letter or not letter.isalpha(): break
            newTile = self.GetNewTile(letter, colIdx, rowIdx, enabled=(rowIdx == 0))
            vbox.Add(newTile)

        return vbox
        
    def OnButtonPush(self, e):
        if self.onClick: self.onClick(e.GetEventObject().colIdx)

    def Refresh(self):
        for colIdx in range(0, 12):
            self.RefreshColumn(colIdx)

        self.Layout()

    def RefreshColumn(self, colIdx):
        columnVbox = self.GetChildren()[colIdx].GetSizer()
        columnVbox.Clear(deleteWindows=True)
        
        self.Remove(colIdx)
        self.Insert(colIdx,  self.GetColumnVbox(colIdx, self.board.cols[colIdx]))

    def GetTopTile(self, columnVbox):
        if 1 < len(columnVbox.GetChildren()):
            return columnVbox.GetItem(1).GetWindow()  # 1 b/c 0 is spacer
        else:
            return None

    def GetNewTile(self, letter, colIdx, rowIdx, enabled):
        button = wx.lib.buttons.GenBitmapButton(
            parent=self.parent,
            bitmap=getBitmapForLetter(letter),
            size=(50, 56))
        button.colIdx = colIdx
        button.Bind(wx.EVT_BUTTON, self.OnButtonPush)
        button.Enable(enabled)
        return button
    
    def AddLetterToColumn(self, letter, colIdx):
        columnVbox = self.GetChildren()[colIdx].GetSizer()
        
        oldTopTile = self.GetTopTile(columnVbox)
        if oldTopTile: oldTopTile.Enable(False)

        rowIdx = 7 - len(columnVbox.GetChildren())
        newTile = self.GetNewTile(letter, colIdx, rowIdx, enabled=True)
        columnVbox.Insert(1, newTile)
        columnVbox.Layout()

    def RemoveLetterFromColumn(self, letter, colIdx):
        columnVbox = self.GetChildren()[colIdx].GetSizer()

        self.GetTopTile(columnVbox).Hide()
        columnVbox.Remove(1)

        newTopTile = self.GetTopTile(columnVbox)
        if newTopTile: newTopTile.Enable(True)
        columnVbox.Layout()
