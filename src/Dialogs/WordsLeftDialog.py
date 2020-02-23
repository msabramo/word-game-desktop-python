import gtk, webbrowser


def show(game, words_left, parent_window):
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


def populate_treeview(treeview, game, words_left):
    model = gtk.TreeStore(str, int)
    for word in words_left:
        score = game.calc_word_score(word)
        model.append(None, [word, score])
    treeview.set_model(model)
    
    for i, column_name in enumerate(('Word', 'Score')):
        tvcolumn = gtk.TreeViewColumn(column_name, gtk.CellRendererText(), text=i)
        tvcolumn.set_sort_column_id(i)
        tvcolumn.set_min_width(120)
        treeview.append_column(tvcolumn)
