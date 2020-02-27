#!/usr/bin/env pythonw

import datetime
import os
import sys
import webbrowser
import wx, wx.adv, wx.html, wx.lib.buttons

import Board, BoardWidget, Dictionary, Game, Utils, TopScoreManager
from Dialogs.AboutDialog import AboutDialog
from Dialogs.HelpDialog import HelpDialog
from Dialogs.TopScoreDialog import TopScoreDialog
from Dialogs.WordsLeftDialog import WordsLeftDialog
from Dialogs.GameDetailsDialog import GameDetails

from Version import VERSION, FREE_EDITION

ID_SHOW_TOP_SCORES = 100
ID_TOGGLE_GAME_DETAILS = 200
ID_TOGGLE_SOUNDS_ENABLED = 201
ID_WORD_UP_HELP = 300
ID_WORD_UP_CREDITS = 301

soundsEnabled = True
tileClickSound = None
wordAddedSound = None


class MainWindow(wx.Frame):
        
    def __init__(self, parent, id, title):
        self.VERSION = VERSION
        self.FREE_EDITION = FREE_EDITION
        wx.Frame.__init__(self, parent, wx.ID_ANY, title)
        try:
            os.chdir(os.path.dirname(sys.argv[0]))
        except:
            pass
        if sys.platform == 'win32':
            self.SetIcon(wx.Icon('resources/images/WordUp.ico', wx.BITMAP_TYPE_ICO))
        self.CreateMenu()
        self.InitGame()
        
        self.panel = wx.Panel(self)
        self.hbox = wx.BoxSizer(wx.HORIZONTAL)
        self.vbox = wx.BoxSizer(wx.VERTICAL)
        self.hbox.Add(self.vbox)
        self.gameDetails = GameDetails(self.panel, self.game)
        self.hbox.Add(self.gameDetails, 1, wx.EXPAND)
        self.hbox.SetItemMinSize(self.gameDetails, (270, 50))

        self.gameInfo = self.GameInfo(parent=self.panel, sizer=self.vbox)
        self.wordPanel = self.WordPanel(parent=self.panel, sizer=self.vbox)
        self.buttons = self.Buttons(parent=self.panel, sizer=self.vbox)
        self.board_widget = self.Board(parent=self.panel, sizer=self.vbox)
        # iPhoneButton = wx.Button(parent=self.panel,
        #                          label='Get Word Up! for iPhone/iPod Touch...')
        # iPhoneButton.Bind(wx.EVT_BUTTON,
        #                   lambda event: webbrowser.open(
        #     'http://phobos.apple.com/WebObjects/MZStore.woa/wa/viewSoftware?id=290594543&mt=8'))
        # self.vbox.Add(iPhoneButton, flag=wx.BOTTOM|wx.LEFT, border=20)
        self.vbox.Layout()

        def focus(e):
            applyButtonEnabled = self.buttons.applyButton.IsEnabled()
            self.buttons.applyButton.Enable(enable=True)
            self.buttons.applyButton.SetFocus()
            self.buttons.applyButton.Enable(enable=applyButtonEnabled)

        self.gameDetails.Bind(wx.EVT_SET_FOCUS, focus)
        
        self.buttons.applyButton.SetFocus()
        self.RefreshButtonStates()
        self.panel.SetSizer(self.hbox)
        self.panel.SetAutoLayout(True)
        self.hbox.Fit(self)
        self.Centre()
        self.Show(True)

    def CreateMenu(self):
        openEnabled = False
        
        menuBar = wx.MenuBar()

        gameMenu = wx.Menu()
        if sys.platform == 'win32':
            gameMenu.Append(wx.ID_NEW, '&New...\tCtrl+N')
        else:
            gameMenu.Append(wx.ID_NEW)

        gameMenu.AppendSeparator()
        
        if openEnabled:
            gameMenu.Append(wx.ID_OPEN, '&Open...\tCtrl+O')
            gameMenu.AppendSeparator()
        
        if sys.platform == 'win32':
            gameMenu.Append(wx.ID_EXIT, 'E&xit\tAlt+F4', 'Terminate the program')
        else:
            gameMenu.Append(wx.ID_EXIT)
            
        menuBar.Append(gameMenu, "&Game")
        
        optionsMenu = wx.Menu()
        toggleSoundsEnabled = optionsMenu.AppendCheckItem(
            ID_TOGGLE_SOUNDS_ENABLED,
            '&Sounds Enabled\tCtrl+S',
            'Toggle game sounds')
        optionsMenu.Check(ID_TOGGLE_SOUNDS_ENABLED, True)
        menuBar.Append(optionsMenu, '&Options')
        
        viewMenu = wx.Menu()
        if FREE_EDITION:
            topScoresMenuItem = viewMenu.Append(
                ID_SHOW_TOP_SCORES,
                '&Top Scores only available in premium edition',
                'Show the top scores window')
            topScoresMenuItem.Enable(False)
        else:
            topScoresMenuItem = viewMenu.Append(
                ID_SHOW_TOP_SCORES,
                '&Top Scores...\tCtrl+T',
                'Show the top scores window')
        toggleGameDetailsMenuItem = viewMenu.AppendCheckItem(
            ID_TOGGLE_GAME_DETAILS,
            'Game &Details\tCtrl+D',
            'Toggle the Game Details pane')
        viewMenu.Check(ID_TOGGLE_GAME_DETAILS, True)
        menuBar.Append(viewMenu, '&View')
        
        helpMenu = wx.Menu()
        helpMenu.Append(ID_WORD_UP_HELP, '&Word Up! Help...')
        helpMenu.Append(ID_WORD_UP_CREDITS, '&Credits...')
        if sys.platform == 'win32':
            helpMenu.AppendSeparator()
        helpMenu.Append(wx.ID_ABOUT, "&About Word Up!...",
                        "More information About this program")
        menuBar.Append(helpMenu, '&Help')

        self.SetMenuBar(menuBar)
        
        self.Bind(wx.EVT_MENU, self.OnClose, id=wx.ID_EXIT)
        self.Bind(wx.EVT_MENU, self.OnNewGame, id=wx.ID_NEW)
        if openEnabled:
            self.Bind(wx.EVT_MENU, self.OnOpenGame, id=wx.ID_OPEN)
        self.Bind(wx.EVT_MENU, self.ShowTopScoreDialog, id=ID_SHOW_TOP_SCORES)
        self.Bind(wx.EVT_MENU, self.ToggleGameDetails, id=ID_TOGGLE_GAME_DETAILS)
        self.Bind(wx.EVT_MENU, self.ToggleSoundsEnabled, id=ID_TOGGLE_SOUNDS_ENABLED)
        self.Bind(wx.EVT_MENU, self.OnAbout, id=wx.ID_ABOUT)
        self.Bind(wx.EVT_MENU, self.OnHelp, id=ID_WORD_UP_HELP)
        self.Bind(wx.EVT_MENU, self.OnCredits, id=ID_WORD_UP_CREDITS)
        self.Bind(wx.EVT_CLOSE, self.OnCloseEvent)

    def ToggleSoundsEnabled(self, event=None):
        global soundsEnabled
        
        soundsEnabled = not soundsEnabled

    def ToggleGameDetails(self, event=None):
        self.gameDetails.Show(not self.gameDetails.IsShown())
        self.hbox.Fit(self)

    def OnAbout(self, event=None):
        aboutDialog = AboutDialog(self)
        aboutDialog.ShowModal()

    def OnHelp(self, event=None):
        helpDialog = HelpDialog(self, 'resources/html/help.html')
        helpDialog.ShowModal()

    def OnCredits(self, event=None):
        helpDialog = HelpDialog(self, 'resources/html/credits.html')
        helpDialog.ShowModal()

    def OnClose(self, event=None):
        self.check_if_top_score(self.game.total_score)
        self.Close()

    def OnCloseEvent(self, event=None):
        self.Destroy()
        sys.exit(0)

    def GetDataDir(self):
        return wx.StandardPaths.Get().GetUserDataDir()
        
    def InitGame(self, event=None):
        self.dictionary = Dictionary.Dictionary('resources/dictionaries/twl_split')
        self.top_score_manager = TopScoreManager.TopScoreManager()
        data_dir = self.GetDataDir()
        if not os.path.exists(data_dir):
            try:
                os.makedirs(data_dir)
            except Exception as e:
                sys.stderr.write('Could not create data directory: %s\n' % data_dir)
                data_dir = None
        self.top_score_manager.set_data_dir(data_dir)
        self.game = self.get_game()

    def OnNewGame(self, event=None):
        if self.game.board.num_tiles <= 10:
            words_left = self.game.board.words_left(self.dictionary, max_num_words=500)
            if len(words_left) > 0:
                words_left.sort(lambda a, b: cmp(self.game.calc_word_score(b),
                                                 self.game.calc_word_score(a)))
                WordsLeftDialog(self, self.game, words_left)
            
        if FREE_EDITION:
            dialog = wx.MessageDialog(self, 'This is the free edition of Word Up!\n\nIf you were using the premium edition, then you would not see this dialog and the program would also keep track of your top scores and the words used for those games. Would you like to visit the Word Up! upgrade page?', 'Please upgrade...',
                                      wx.YES_NO | wx.YES_DEFAULT | wx.ICON_INFORMATION)
            evt = dialog.ShowModal()
            if evt == wx.ID_YES:
                webbrowser.open('http://marc-abramowitz.com/word_up/upgrade.php')
            dialog.Destroy()
        else:
            self.check_if_top_score(self.game.total_score)

        self.Freeze()    
        self.game = self.get_game()
        self.board_widget.SetBoard(self.game.board)
        self.ClearWord()
        self.RefreshWordScore()
        self.RefreshTotalScore()
        self.Thaw()

    def OnOpenGame(self, action):
        wildcard = 'All files (*)|*|Word Up! files (*.wordup)|*.wordup|Text files (*.txt)|*.txt'
        fileDialog = wx.FileDialog(self,
                                   message='Choose a file',
                                   defaultDir=os.getcwd() + '/game_data',
                                   defaultFile='', 
                                   wildcard=wildcard,
                                   style=wx.OPEN)
        if fileDialog.ShowModal() == wx.ID_OK:
            self.check_if_top_score(self.game.total_score)

            filename = fileDialog.GetPath()

            try:
                self.game = Game.Game.load(filename)
                self.game.dictionary = self.dictionary
                self.register_game_callbacks(self.game)
            except:
                game = self.get_game()
                game.board.load_from_file(filename)
                self.game = game
            finally:
                self.board_widget.SetBoard(self.game.board)
                self.ClearWord()
                self.RefreshWordScore()
                self.RefreshTotalScore()
                words_left = self.game.board.words_left(self.dictionary, max_num_words=500)
                print('words_left = %s' % words_left)

    def GameInfo(self, parent, sizer):
        wordScoreLabel   = wx.StaticText(parent, wx.ID_ANY, 'Word Score:')
        wordScore        = wx.StaticText(parent, wx.ID_ANY, '0')
        totalScoreLabel  = wx.StaticText(parent, wx.ID_ANY, 'Total Score:')
        totalScore       = wx.StaticText(parent, wx.ID_ANY, '0')
##         gameTimeLabel    = wx.StaticText(parent, wx.ID_ANY, 'Game Time:')
##         gameTime         = wx.StaticText(parent, wx.ID_ANY, '0:00')
        
        gameInfoHbox = wx.BoxSizer(wx.HORIZONTAL)
        gameInfoHbox.Layout()
        
        for w in (wordScoreLabel, wordScore, totalScoreLabel, totalScore):
            gameInfoHbox.Add(w, 1, wx.ALIGN_CENTER|wx.LEFT|wx.RIGHT|wx.EXPAND, border=20)
        
        sizer.Add(gameInfoHbox, 1,
                  flag=wx.TOP|wx.LEFT|wx.RIGHT|wx.ALIGN_CENTER|wx.EXPAND, border=20)
        sizer.Layout()
        
        return Utils.Bunch(wordScore=wordScore,
                           totalScore=totalScore,
##                            gameTime=gameTime
                           )

    def WordPanel(self, parent, sizer):
        wordPanelTilesHbox = wx.BoxSizer(wx.HORIZONTAL)
        wordPanel = wx.Panel(parent, style=wx.SUNKEN_BORDER)
        wordPanel.SetMinSize((400, 60))
        wordPanel.SetSizer(wordPanelTilesHbox)
        wordPanel.SetBackgroundColour('#cccccc')
        wordPanelHbox = wx.BoxSizer(wx.HORIZONTAL)
        wordPanelHbox.Add(wordPanel, 1, flag=wx.EXPAND)
        wordPanelHbox.Fit(wordPanel)
        sizer.Add(wordPanelHbox,
                  flag=wx.EXPAND|wx.TOP|wx.LEFT|wx.RIGHT,
                  border=20)
        wordPanel.hbox = wordPanelHbox
        wordPanel.tilesHbox = wordPanelTilesHbox
        return wordPanel

    def Buttons(self, parent, sizer):
        buttonsHbox = wx.BoxSizer(wx.HORIZONTAL)
        clearButton = wx.Button(parent, wx.ID_CLEAR)
        clearButton.Bind(wx.EVT_BUTTON, self.OnClearButtonClicked)
        undoButton = wx.Button(parent, wx.ID_UNDO)
        undoButton.Bind(wx.EVT_BUTTON, self.OnUndoButtonClicked)
        applyButton = wx.Button(parent, wx.ID_APPLY)
        applyButton.Bind(wx.EVT_BUTTON, self.OnApplyButtonClicked)
        applyButton.SetDefault()
        buttonsHbox.Add(clearButton,
                        flag=wx.ALIGN_CENTER|wx.LEFT, border=20)
        buttonsHbox.Add(undoButton,
                        flag=wx.ALIGN_CENTER|wx.LEFT|wx.RIGHT, border=12)
        buttonsHbox.Add(applyButton,
                        flag=wx.ALIGN_CENTER|wx.RIGHT, border=20)
        sizer.Add(buttonsHbox, flag=wx.ALIGN_CENTER|wx.TOP, border=10)
        return Utils.Bunch(clearButton=clearButton,
                           undoButton=undoButton,
                           applyButton=applyButton)

    def Board(self, parent, sizer):
        board_widget = BoardWidget.BoardWidget(parent=parent,
                                               board=self.game.board,
                                               onClick=self.OnTileClicked)
        boardHbox = wx.BoxSizer(wx.HORIZONTAL)
        boardHbox.Add(board_widget, flag=wx.LEFT|wx.RIGHT|wx.BOTTOM, border=20)
        sizer.Add(boardHbox)
        sizer.Layout()
        board_widget.hbox = boardHbox
        return board_widget
        
    def OnTileClicked(self, colIdx):
        self.Freeze()
        self.game.push_tile(colIdx)
        self.Thaw()
        if soundsEnabled: tileClickSound.Play()

    def OnUndoButtonClicked(self, event):    
        self.Freeze()
        self.game.pop_tile()
        self.Thaw()
        if soundsEnabled: tileClickSound.Play()

    def OnClearButtonClicked(self, button):
        self.Freeze()
        self.game.pop_all_tiles()
        self.Thaw()
        if soundsEnabled: tileClickSound.Play()
        
    def OnApplyButtonClicked(self, button):
        self.Freeze()
        self.game.add_word()
        self.Thaw()

    def OnBoardColumnChange(self, columnIdx, columnData, letter_added, letter_removed):
        if letter_added:
            self.board_widget.AddLetterToColumn(letter_added, columnIdx)
        if letter_removed:
            self.board_widget.RemoveLetterFromColumn(letter_removed, columnIdx)

    def OnWordTileAdded(self, letter):
        wordTilesHbox = self.wordPanel.tilesHbox
        bitmap = BoardWidget.getBitmapForLetter(letter)
        button = wx.lib.buttons.GenBitmapButton(
            parent=self.wordPanel,
            bitmap=bitmap,
            size=(50, 56))
        wordTilesHbox.Add(button)
        wordTilesHbox.Layout()
        self.RefreshButtonStates()
        self.RefreshWordScore()

    def OnWordTilesRemoved(self, num):
        wordTilesHbox = self.wordPanel.tilesHbox
        numChildren = len(wordTilesHbox.GetChildren())
        for i in range(0, num):
            wordTilesHbox.Hide(numChildren - i - 1)
            wordTilesHbox.Remove(numChildren - i - 1)
        
        wordTilesHbox.Layout()
        self.RefreshButtonStates()
        self.RefreshWordScore()
        
    def OnWordAdded(self, time, word, word_score, total_score):
        self.RefreshTotalScore()
        self.gameDetails.AddWord(time, word, word_score)
        if soundsEnabled: wordAddedSound.Play()

    def OnNoWordsLeft(self):
        dialog = wx.MessageDialog(self, 'There are no words left.', 'Game Over!',
                                  wx.OK | wx.ICON_INFORMATION)
        dialog.ShowModal()
        dialog.Destroy()
        self.OnNewGame()

    def ClearWord(self):
        wordTilesHbox = self.wordPanel.tilesHbox
        self.OnWordTilesRemoved(len(wordTilesHbox.GetChildren()))

    def RefreshWordScore(self):
        self.gameInfo.wordScore.SetLabel(str(self.game.current_word_score()))
        
    def RefreshTotalScore(self):
        self.gameInfo.totalScore.SetLabel(str(self.game.total_score))

    def RefreshButtonStates(self):
        current_word = self.game.current_word()
        current_word_len = len(current_word)
        buttons = self.buttons
        buttons.clearButton.Enable(current_word_len > 0)
        buttons.undoButton.Enable(current_word_len > 0)
        buttons.applyButton.Enable(self.dictionary.has_word(current_word))
        if buttons.applyButton.IsEnabled():
            buttons.applyButton.SetFocus()

    def ShowTopScoreDialog(self, event=None):
        topScores = self.top_score_manager.load_top_scores()
        topScoreDialog = TopScoreDialog.Display(parent=self,
                                                topScores=topScores,
                                                title='Top Scores',
                                                size=(480, 350))
        
    def get_game(self):
        if hasattr(self, 'gameDetails') and self.gameDetails:
            self.gameDetails.Clear()
        game = Game.Game(self.dictionary)
        self.register_game_callbacks(game)
        return game

    def register_game_callbacks(self, game):
        game.board_column_change_callbacks.append(self.OnBoardColumnChange)
        game.word_tile_added_callbacks.append(self.OnWordTileAdded)
        game.word_tiles_removed_callbacks.append(self.OnWordTilesRemoved)
        game.word_added_callbacks.append(self.OnWordAdded)
        game.no_words_left_callbacks.append(self.OnNoWordsLeft)

    def check_if_top_score(self, score):
        self.game.info.update(dict(end_time=datetime.datetime.now()))
##         self.update_time()
        self.top_score_manager.check_if_top_score(score, self.game, application=self)
        

app = wx.App()
tileClickSound = wx.adv.Sound('resources/sounds/Click03.wav')
wordAddedSound = wx.adv.Sound('resources/sounds/Click02.wav')
app.SetAppName('Word Up!')
frame = MainWindow(None, wx.ID_ANY, "Word Up!")
app.MainLoop()
