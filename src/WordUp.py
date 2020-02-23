#!/usr/bin/env python

import WordUpDev
import BoardWidget, CurrentWordWidget, Dialogs, Dictionary, Game, TopScoreManager, Utils
import Unlock
import datetime, gobject, pygtk, sys, time, webbrowser
pygtk.require('2.0')
import gtk, gtk.glade


class WordUp(gtk.glade.XML):

    def __init__(self):
        gtk.glade.XML.__init__(self, 'resources/glade/WordUp.glade', 'main_window')
        self.signal_autoconnect(self)
        self.main_window.connect('destroy', self.on_quit_activate)
        self.dictionary = Dictionary.Dictionary('resources/dictionaries/twl_split')
        self.top_score_manager = TopScoreManager.TopScoreManager()
        self.game = self.get_game()
        self.refresh_ui()
        timer = gobject.timeout_add(1000, self.update_time)

    def update_time(self):
        if self.game and self.main_window and self.main_window.has_toplevel_focus():
            game_time = str(self.game.current_game_time())
            self.game_time_label.set_text(game_time)
            
        return True
       
    def __getattr__(self, attr):
        return self.get_widget(attr)

    def get_game(self):
        game = Game.Game(self.dictionary)
        self.register_game_callbacks(game)
        return game

    def register_game_callbacks(self, game):
        game.board_column_change_callbacks.append(self.on_board_column_change)
        game.word_tiles_change_callbacks.append(self.on_word_tiles_change)
        game.word_added_callbacks.append(self.on_word_added)
        game.no_words_left_callbacks.append(self.on_no_words_left)

    def on_clear_button_clicked(self, button):
        self.game.pop_all_tiles()
        
    def on_undo_button_clicked(self, button):
        self.undo_letter()
        
    def on_apply_button_clicked(self, button):
        self.game.add_word()

    def on_main_window_key_press_event(self, window, event):
        if event.keyval == gtk.keysyms.BackSpace: self.undo_letter()

    def undo_letter(self):
        self.game.pop_tile()
        
    def on_tile_click(self, tile_widget):
        self.game.push_tile(tile_widget.col_idx)

    def on_board_column_change(self, col_idx, column_data):
        self.board_widget.refresh_column(col_idx, column_data)

    def on_word_tiles_change(self, word_tiles):    
        self.refresh_current_word_widget()
        self.refresh_word_score()
        self.refresh_button_states()
            
    def on_word_added(self, time, word, word_score, total_score):
        self.refresh_total_score()
        self.game_details.add_word(time, word, word_score)

    def on_no_words_left(self):
        GameOverDialog = Dialogs.GameOverDialog
        ret = GameOverDialog.show(self.main_window)
        if ret == GameOverDialog.RESPONSE_QUIT:       self.on_quit_activate()
        elif ret == GameOverDialog.RESPONSE_NEW_GAME: self.on_new_activate()

    def refresh_ui(self):    
        self.refresh_total_score()
        self.refresh_board()
        self.refresh_current_word_widget()
        self.refresh_word_score()
        self.refresh_button_states()
        self.refresh_game_details()
        self.game.check_words_left()
        
    def refresh_board(self):
        self.upsert_widget(BoardWidget.BoardWidget(self.game.board, self.on_tile_click),
                           self.board_hbox, 'board_widget')
            
    def refresh_current_word_widget(self):
        self.upsert_widget(CurrentWordWidget.CurrentWordWidget(self.game.current_word()),
                           self.current_word_frame, 'current_word_widget')
        
    def refresh_game_details(self):
        self.upsert_widget(Dialogs.GameDetailsDialog.GameDetails(self.game),
                           self.game_details_frame, 'game_details')

    def refresh_word_score(self):
        self.word_score_label.set_label(str(self.game.current_word_score()))

    def refresh_total_score(self):
        self.total_score_label.set_label(str(self.game.total_score))

    def refresh_button_states(self):
        self.clear_button.set_sensitive(len(self.game.current_word()) > 0)
        self.undo_button.set_sensitive(len(self.game.current_word()) > 0)
        self.apply_button.set_sensitive(self.dictionary.has_word(self.game.current_word()))

    def upsert_widget(self, new_widget, parent_widget, attr_name):
        old_widget = getattr(self, attr_name)
        if old_widget:
            Utils.replace_widget(old_widget, new_widget)
            old_widget.destroy()
        else:
            parent_widget.add(new_widget)
            new_widget.show_all()
        setattr(self, attr_name, new_widget)

    def on_game_details_pane_activate(self, action):
        if action.get_active(): self.game_details_frame.show()
        else:                   self.game_details_frame.hide()

    def on_about_activate(self, action):
        Dialogs.AboutDialog.show()

    def on_new_activate(self, action=None):
        if self.game.board.num_tiles <= 10:
            words_left = self.game.board.words_left(self.dictionary, max_num_words=500)
            if len(words_left) > 0:
                words_left.sort(lambda a, b: cmp(self.game.calc_word_score(b),
                                                 self.game.calc_word_score(a)))
                Dialogs.WordsLeftDialog.show(self.game, words_left, parent_window=self.main_window)
            
        self.check_if_top_score(self.game.total_score)
        if False and sys.platform == 'win32': self.nag()
        self.game = self.get_game()
        self.refresh_ui()

    def nag(self):
        response_register = 1
        
        dialog = gtk.MessageDialog(parent=self.main_window,
                                   flags=gtk.DIALOG_MODAL,
                                   type=gtk.MESSAGE_INFO,
                                   buttons=gtk.BUTTONS_CLOSE,
                                   message_format='Please register this software')
        dialog.set_title('Please Register')
        dialog.add_button('Register...', response_register)
        dialog.connect('key-press-event', lambda b, e: True)
        globals()['nag_wait_count'] = 6

        def timer_func():
            global nag_wait_count

            if nag_wait_count:
                dialog.format_secondary_text('Close button will be enabled in %s second(s)...'
                                             % nag_wait_count)
                Utils.freeze_size(dialog)
                nag_wait_count -= 1
                return True
            else:
                dialog.format_secondary_text('OK, go ahead and close this dialog.')
                dialog.set_response_sensitive(gtk.RESPONSE_CLOSE, True)
                
        dialog.set_response_sensitive(gtk.RESPONSE_CLOSE, False)
        timer_func()
        
        timer = gobject.timeout_add(1000, timer_func)
        response = dialog.run()
        gobject.source_remove(timer)
        dialog.destroy()
        dialog = None

        if response == response_register:
            seed = Unlock.get_seed()
            webbrowser.open('http://marc-abramowitz.com/word_up/register.php?seed=%s' % seed)

    def on_quit_activate(self, action=None):
        self.check_if_top_score(self.game.total_score)
        gtk.main_quit()

    def on_top_scores_activate(self, action):
        Dialogs.TopScoreDialog.show(self.top_score_manager.load_top_scores(),
                                    application=self,
                                    parent_window=self.main_window)

    def check_if_top_score(self, score):
        self.game.info.update(dict(end_time=datetime.datetime.now()))
        self.update_time()
        self.top_score_manager.check_if_top_score(score, self.game, application=self)
        

def main():
    if len(sys.argv) > 1 and sys.argv[1] == '-d':
        sys.argv.pop()
        WordUpDev.WordUpDev(sys.argv)
    else:
        WordUp()
    gtk.main()

if __name__ == '__main__': main()
