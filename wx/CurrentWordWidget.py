from TileWidget import TileWidget
import Utils, gtk


class CurrentWordWidget(gtk.Table):

    def __init__(self, letters, columns=12):
        gtk.Table.__init__(self, columns=columns, rows=1, homogeneous=True)

        for i, letter in enumerate(letters):
            self.add_tile(i, TileWidget(letter, sensitive=False))

        self.set_border_width(0)
        self.set_size_request(-1, TileWidget.height)
        Utils.freeze_size(self)
        
    def add_tile(self, col_idx, tile_widget):
        self.attach(tile_widget, col_idx, col_idx + 1, 0, 1)

