from distutils.core import setup
import py2exe
import sys
sys.path.append('../../wx')
sys.path.append('../../src')

setup(
    name = 'Word Up!',
    description = 'Addictive word game',
    version = '1.1',

    windows = [
                  {
                      'script': '../../wx/WordUp.py',
                      'icon_resources': [(1, "WordUp.ico")],
                  }
              ],

    options = {
                  'py2exe': {
                      'packages':'encodings',
                      'includes': 'wx, Board',
                      #'includes': 'cairo, pango, pangocairo, atk, gobject, gtk.keysyms',
                  }
              },

    data_files=[
                   #'WordUp.glade',
                   'README.txt',
                   '../../resources'
               ]
)
