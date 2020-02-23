from setuptools import setup
import py2app

import sys
sys.path.append("../../wx")
sys.path.append("../../src")

setup(
    name = 'Word Up!',
    description = 'Addictive word game',
    version = '0.3',
    app = ['../../wx/WordUp.py'],
    options = {
                  'py2app': {
                      'packages':'encodings',
                      'includes': 'wx',
                      'iconfile': 'W.icns',
                      'optimize': '2',
                  },
              },
    data_files=[
                   #'WordUp.glade',
                   'W.icns',
                   '../../README',
                   '../../wx/resources',
               ]
)
