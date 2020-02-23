from TileWidget import TileWidget
import Utils, gtk


class BoardWidget(gtk.HBox):

    def __init__(self, board, on_tile_click):
        gtk.HBox.__init__(self, homogeneous=True)
        self.on_tile_click = on_tile_click

        for col_idx, column_data in enumerate(board.cols):
            self.refresh_column(col_idx, column_data)
                
        self.show_all()
        Utils.freeze_size(self)

    def refresh_column(self, col_idx, column_data):
        column_widget = gtk.Table(columns=1, rows=7, homogeneous=True)

        for row_idx, letter in enumerate(column_data):
            if letter and letter.isalpha():
                tile_widget = TileWidget(letter, on_click=self.on_tile_click)
                if row_idx == 0: tile_widget.col_idx = col_idx
                else: tile_widget.gray_out()
                column_widget.attach(tile_widget, 0, 1, row_idx, row_idx + 1)

        self.set_column_widget(col_idx, column_widget)
            
    def set_column_widget(self, col_idx, column_widget):
        children = self.get_children()
        if col_idx < len(children):
            Utils.replace_widget(children[col_idx], column_widget)
        else:
            self.add(column_widget)
            


