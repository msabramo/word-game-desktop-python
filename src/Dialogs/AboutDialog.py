import gtk, webbrowser


class AboutDialog(gtk.AboutDialog):

    def set_comments_markup(self, markup):
        comments_label = self.get_children()[0].get_children()[0].get_children()[2]
        comments_label.set_markup('GTK+ version: %s (%s)\n' % (gtk.gtk_version, gtk.__file__) +
                                  'PyGTK version: %d.%d.%d\n\n' % gtk.pygtk_version +
                                  markup)
        comments_label.set_justify(gtk.JUSTIFY_LEFT)
        comments_label.set_size_request(400, -1)


def show():
    about_dialog = AboutDialog()
    about_dialog.set_name('')
    about_dialog.set_version('0.1')
    about_dialog.set_logo(gtk.gdk.pixbuf_new_from_file('resources/images/WordUp.png'))
    about_dialog.set_authors(['Marc Abramowitz'])
    about_dialog.set_website('http://marc-abramowitz.com/word_up')
    try: about_dialog.set_comments_markup(file('README').read())
    except IOError: print('Failed to load README')
    about_dialog.show_all()
    about_dialog.run()
    about_dialog.destroy()


def on_url(dialog, link):
    webbrowser.open(link)


gtk.about_dialog_set_url_hook(on_url)


