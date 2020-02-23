import copy, gtk


class GameDetails(gtk.VBox):

    def __init__(self, game):
        gtk.VBox.__init__(self)
        widget_name = 'treeview'
        glade_xml = gtk.glade.XML('resources/glade/WordUp.glade', widget_name)
        self.treeview = glade_xml.get_widget(widget_name)
        populate_treeview(self.treeview, game)
        self.add(self.treeview)

    def add_word(self, time, word, word_score):
        self.treeview.get_model().append(None, [time, word, word_score])


def show(game, application, parent_window):
    dialog_name = 'game_details_dialog'
    glade_xml = gtk.glade.XML('resources/glade/WordUp.glade', dialog_name)
    dialog = glade_xml.get_widget(dialog_name)
    dialog.set_transient_for(parent_window)

    if hasattr(game, 'info'):
        start_time = game.info['start_time'].replace(microsecond=0)
        end_time = game.info['end_time'].replace(microsecond=0)
        glade_xml.get_widget('name_data_label').set_text(game.info['name'])
        glade_xml.get_widget('start_time_data_label').set_text(start_time.ctime())
        glade_xml.get_widget('end_time_data_label').set_text(end_time.ctime())
        glade_xml.get_widget('duration_data_label').set_text(str(end_time - start_time))

    def replay_game(button):
        application.game.board = copy.deepcopy(game.orig_board)
        application.refresh_ui()
    
    glade_xml.get_widget('replay_game_button').connect('clicked', replay_game)
    glade_xml.get_widget('close_button').connect('clicked', lambda w: dialog.destroy())
    populate_treeview(glade_xml.get_widget('treeview'), game)


def populate_treeview(treeview, game):
    model = gtk.TreeStore(str, str, int)
    for word_tiles, time in game.words:
        word = ''.join([tup[0] for tup in word_tiles])
        model.append(None, [time, word, game.calc_word_score(word)])
    treeview.set_model(model)
    
    for i, column_name in enumerate(('Time', 'Word', 'Score')):
        tvcolumn = gtk.TreeViewColumn(column_name, gtk.CellRendererText(), text=i)
        tvcolumn.set_sort_column_id(i)
        tvcolumn.set_min_width(80)
        treeview.append_column(tvcolumn)
