import gtk


RESPONSE_NEW_GAME = 1
RESPONSE_QUIT = 2

        
class GameOverDialog(gtk.Dialog):

    def __init__(self, application):
	gtk.Dialog.__init__(
            self,
            title='Game Over',
            parent=application,
            flags=gtk.DIALOG_MODAL | gtk.DIALOG_DESTROY_WITH_PARENT,
            buttons=('New Game', RESPONSE_NEW_GAME,
                     gtk.STOCK_QUIT, RESPONSE_QUIT))
        
        for button in self.action_area.get_children():
            if button.get_label() == 'New Game':
                button.set_image(gtk.image_new_from_stock(gtk.STOCK_NEW, gtk.ICON_SIZE_BUTTON))
                
        self.set_size_request(250, -1)
        self.set_border_width(10)

        label = gtk.Label('Game over.\n\nThere are no words remaining.')

        self.vbox.set_spacing(10)
	self.vbox.pack_end(label, True, True, 0)


def show(application):
    dialog = GameOverDialog(application)
    dialog.show_all()
    ret = dialog.run()
    dialog.destroy()

    return ret
        
