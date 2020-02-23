DITTO 				= /usr/bin/ditto
PYTHON 				= /usr/local/bin/python
HDIUTIL 			= /usr/bin/hdiutil
MKDIR 				= /bin/mkdir
MV					= /bin/mv
LN					= /bin/ln

PRODUCT 			= Word\ Up!
VERSION 			= 1.1
PRODUCTVERSION 		= $(PRODUCT)-$(VERSION)
APP_BUNDLE 			= dist/$(PRODUCT).app
APP_BUNDLE_i386 	= dist/$(PRODUCT)-i386.app
FOLDER 				= dist/$(PRODUCTVERSION)-folder
FOLDER_i386 		= dist/$(PRODUCTVERSION)-i386-folder
DMG 				= dist/$(PRODUCTVERSION).dmg
DMG_i386 			= dist/$(PRODUCTVERSION)-i386.dmg

all: $(DMG_i386) $(DMG)

$(DMG): $(FOLDER)
	$(HDIUTIL) create -srcfolder "$<" -format UDBZ "$@"

$(FOLDER): $(APP_BUNDLE)
	$(MKDIR) "$@"
	$(MV) $(APP_BUNDLE) $(FOLDER)
	$(LN) -s /Applications $(FOLDER)

$(DMG_i386): $(FOLDER_i386)
	$(HDIUTIL) create -srcfolder "$<" -format UDBZ "$@"

$(FOLDER_i386): $(APP_BUNDLE_i386)
	$(MKDIR) "$@"
	$(MV) $(APP_BUNDLE_i386) $(FOLDER_i386)
	$(LN) -s /Applications $(FOLDER_i386)

$(APP_BUNDLE_i386): $(APP_BUNDLE)
	$(DITTO) --rsrc --arch i386 "$<" "$@"

$(APP_BUNDLE): py2app_setup.py
	$(PYTHON) "$<" py2app

clean:
	$(RM) -r build dist

