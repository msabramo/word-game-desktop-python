#!/usr/bin/env python

# Some of this script is from Pete Shinners pygame2exe script.
#(data copying and pygame icon changing) Special thanks to him!


# import modules
from distutils.core import setup
import sys, os, shutil
import py2exe


sys.path.append("../../wx")
sys.path.append("../../src")

#########################
### Variables to edit ###
#########################

script = "../../wx/WordUp.py"
dest_file = "WordUp"
dest_folder = "WordUp"
icon_file = "WordUp.ico"
extra_data = ["WordUp.ico",
              "../../wx/resources", 
              "../../game_data",
              "../../README",
              ]
extra_modules = [""]
dll_excludes = []    # excluded dlls ["w9xpopen.exe", "msvcr71.dll"]

# Stuff to show who made it, etc.
copyright = "Copyright (C) 2008, Marc Abramowitz"
author = "Marc Abramowitz"
company = "http://marc-abramowitz.com"
version = "1.1"

##################################################################
### Below if you edit variables, you could mess up the program ###
##################################################################


# Run the script if no commands are supplied 
if len(sys.argv) == 1:
    sys.argv.append("py2exe")
    sys.argv.append("-q")


# Use the pygame icon if there's no icon designated
if icon_file is '':
    path = os.path.split(pygame.__file__)[0]
    icon_file = '' + os.path.join(path, 'pygame.ico') 


# Copy extra data files
def installfile(name):
    dst = os.path.join(dest_folder)
    print 'copying', name, '->', dst
    if os.path.isdir(name):
        dst = os.path.join(dst, os.path.basename(name))
        if os.path.isdir(dst):
            shutil.rmtree(dst)
        print 'Doing shutil.copytree(name="%s", dst="%s")' % (name, dst)
        shutil.copytree(name, dst)
    elif os.path.isfile(name):
        shutil.copy(name, dst)
    else:
        print 'Warning, %s not found' % name
        

##############################
### Distutils setup script ###
##############################

# Set some variables for the exe
class Target:
    def __init__(self, **kw):
        self.__dict__.update(kw)
        self.description = "An addictive word game"
        self.version = version
        self.company_name = company
        self.author = author
        self.copyright = copyright
        self.name = "Word Up!"

# Set some more variables for the exe
target = Target(
    script = script,
    icon_resources = [(1, icon_file)],
    dest_base = dest_file,
    extra_modules = extra_modules
    )


# Run the setup script!
setup(
    options = {"py2exe": {
##                           "includes": "cairo, pango, pangocairo," + 
##                                       "atk, gobject, gtk.keysyms",
                          "includes": "wx",
                          "compressed": 1,
                          "optimize": 2,
                          #"bundle_files": 1,
                          "dll_excludes": dll_excludes,
                          "dist_dir": dest_folder}},
    #zipfile = None,
    windows = [target],
    )


# install extra data files
print '\n' # Just a space to make it look nicer :)
for d in extra_data:
    installfile(d)
