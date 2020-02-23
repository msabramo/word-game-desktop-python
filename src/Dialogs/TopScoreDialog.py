import GameDetailsDialog, gtk


def show(top_scores, application, parent_window):
    dialog_name = 'top_scores_dialog'
    glade_xml = gtk.glade.XML('resources/glade/WordUp.glade', dialog_name)
    dialog = glade_xml.get_widget(dialog_name)
    dialog.set_transient_for(parent_window)
    treeview = glade_xml.get_widget('top_scores_treeview')
    
    def on_double_click(treeview, path, treecolumn):
        view_details()
    
    def view_details(button=None):
        if treeview.get_cursor()[0]:
            row = treeview.get_cursor()[0][0]
            game = top_scores[row][1]
            GameDetailsDialog.show(game, application, parent_window=dialog)
        
    treeview.connect('row-activated', on_double_click)
    glade_xml.get_widget('top_scores_view_details_button').connect('clicked', view_details)
    glade_xml.get_widget('top_scores_close_button').connect('clicked', lambda w: dialog.destroy())
    populate_treeview(treeview, top_scores)
    dialog.show_all()


def populate_treeview(treeview, top_scores):
    model = gtk.TreeStore(int, int, str, str, str)
    for i, (score, game) in enumerate(top_scores):
        name = game.info['name']
        start_time = game.info['start_time'].replace(microsecond=0)
        end_time = game.info['end_time'].replace(microsecond=0)
        end_time_str = end_time.strftime('%Y-%m-%d %H:%M')
        duration_str = str(end_time - start_time)
        model.append(None, [i + 1, score, duration_str, name, end_time_str])
    treeview.set_model(model)
    
    for i, column_name in enumerate(('Rank', 'Score', 'Duration', 'Name', 'Date')):
        tvcolumn = gtk.TreeViewColumn(column_name, gtk.CellRendererText(), text=i)
        tvcolumn.set_sort_column_id(i)
        treeview.append_column(tvcolumn)
