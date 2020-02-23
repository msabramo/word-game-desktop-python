import gtk, Utils


class TileWidget(gtk.Button):

    lightwood_pixbuf = gtk.gdk.pixbuf_new_from_file('resources/images/lightwood.jpg')
    lightwood_pixmap, _ = lightwood_pixbuf.render_pixmap_and_mask()
    gray = gtk.gdk.color_parse('#444444')
    black = gtk.gdk.color_parse('black')
    width = height = -1

    @classmethod
    def set_size(cls):
        """
        This classmethod sets the width and height for all
        subsequently created TileWidgets. It determines the width and
        height by creating a temporary TileWidget for 'Q' (the widest
        tile) and querying its size.
        
        Call this classmethod before any TileWidgets are created.
        """
        
        q_tile_widget = cls('Q')
        q_tile_widget.show_all()
        cls.width, cls.height = q_tile_widget.size_request()
        q_tile_widget.destroy()

    def __init__(self, letter, on_click=None, sensitive=True):
        gtk.Button.__init__(self)
        self.label = gtk.Label()
        self.add(self.label)
        self.set_sensitive(sensitive)
        self.set_size_request(self.__class__.width, self.__class__.height)
        self.set_label(letter, Utils.num_points_for_letter(letter))
        self.set_background_image(self.lightwood_pixmap)
        self.label.modify_fg(self.state, self.black)
        if on_click: self.connect('clicked', on_click)

    def set_label(self, letter, num_points):
        letter_font_size = 20
        number_font_size = 12
        if num_points > 9: number_font_size = 10
        self.label.set_markup(
            '<span font_desc="%d">%s</span>' % (letter_font_size, letter) +
            '<sub><span font_desc="%d">%d</span></sub>' % (number_font_size, num_points))

    def set_background_image(self, pixmap):
        style = self.get_style().copy()
        style.bg_pixmap[self.state] = pixmap
        self.set_style(style)
        
    def gray_out(self):
        self.set_sensitive(False)
        self.label.modify_fg(self.state, self.gray)


TileWidget.set_size()
