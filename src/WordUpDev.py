#!/usr/bin/env python

import Game, WordUp, sys, os.path, pygtk
pygtk.require('2.0')
import gtk


def dump_board(board, out=sys.stdout):
    for row_idx in range(0, board.num_rows):
        for col_idx in range(0, board.num_cols):
            try:               tile = board.cols[col_idx][row_idx]
            except IndexError: tile = ' '
            out.write('%s ' % tile)
        out.write('\n')


class WordUpDev(WordUp.WordUp):

    def __init__(self, argv):
        WordUp.WordUp.__init__(self)
        if len(argv) > 1:
            self.game.board.load_from_file(sys.argv[1])
            self.refresh_ui()
            print(self.game.board.words_left(self.dictionary, max_num_words=20))
        self.open.connect('activate', self.on_open_activate)
        self.open.show()
        self.save.connect('activate', self.on_save_activate)
        self.save.show()

    def on_open_activate(self, action):
        filename = self.get_file_from_dialog('filechooserdialog_open')
        if not filename: return
        
        self.check_if_top_score(self.game.total_score)

        try:
            self.game = Game.Game.load(filename)
            self.game.dictionary = self.dictionary
            self.register_game_callbacks(self.game)
        except:
            game = self.get_game()
            game.board.load_from_file(filename)
            self.game = game
        finally:
##             print(self.game.board.words_left(self.dictionary, max_num_words=20))
            self.refresh_ui()

    def on_save_activate(self, action):
        filename = self.get_file_from_dialog('filechooserdialog_save')
        if not filename: return

        self.game.save(filename)

    def get_file_from_dialog(self, dialog_name):
        result = None
        glade_xml = gtk.glade.XML('resources/glade/WordUp.glade', dialog_name)
        dialog = glade_xml.get_widget(dialog_name)
        dialog.set_current_folder(os.path.abspath('game_data'))
        if dialog.run() == gtk.RESPONSE_OK: result = dialog.get_filename()
        dialog.destroy()
        return result

    def on_new_activate(self, action=None):
        WordUp.WordUp.on_new_activate(self, action)
        

def main():
    WordUpDev(sys.argv)
    gtk.main()

if __name__ == '__main__':
    main()
