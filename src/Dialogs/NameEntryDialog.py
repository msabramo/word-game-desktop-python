import gtk


class NameEntryDialog(gtk.MessageDialog):

    def __init__(self, parent_window, score, idx):
	gtk.MessageDialog.__init__(
            self,
            parent=parent_window,
            flags=gtk.DIALOG_MODAL | gtk.DIALOG_DESTROY_WITH_PARENT,
            type=gtk.MESSAGE_QUESTION,
            buttons=gtk.BUTTONS_OK_CANCEL)
        self.set_title('Top Score!')
	self.set_markup('You scored %d which is top score #%d!' % (score, idx + 1))
	self.format_secondary_markup('Please enter your name for the top score list.')
        
	# Allow the user to press enter to do ok
        def responseToDialog(entry, dialog, response):
            dialog.response(response)

	self.entry = gtk.Entry()
	self.entry.connect("activate", responseToDialog, self, gtk.RESPONSE_OK)
        self.entry.show()
        
  	self.vbox.pack_end(self.entry, True, True, 0)
        
        
def show(application, score, idx):
    dialog = NameEntryDialog(application.main_window, score, idx)
    response = dialog.run()
    
    if response == gtk.RESPONSE_OK: text = dialog.entry.get_text()
    else:                           text = None
        
    dialog.destroy()
        
    return text
        
