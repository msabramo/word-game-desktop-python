; !include WordFunc.nsh
; !include LogicLib.nsh

!include MUI2.nsh
!include nsDialogs.nsh
!include WinVer.nsh

Var StartMenuFolder

;--------------------------------

!define NAME "Word Up!"
!define VERSION "1.1"

; The name of the installer
Name "${NAME}"

; The file to write
OutFile "WordUp-${VERSION}-setup.exe"

; The default installation directory
InstallDir "$PROGRAMFILES\Word Up"

; Registry key to check for directory (so if you install again, it will 
; overwrite the old one automatically)
InstallDirRegKey HKLM "Software\${NAME}" "Install_Dir"

; Request application privileges for Windows Vista
RequestExecutionLevel admin

;--------------------------------

; Pages

# Page directory
# Page instfiles
# 
# UninstPage uninstConfirm
# UninstPage instfiles

var Dialog
Var Desktop_Shortcut_Checkbox
Var Desktop_Shortcut_Checkbox_State
Var Start_Menu_Shortcut_Checkbox
Var Start_Menu_Shortcut_Checkbox_State
Var Quick_Launch_Shortcut_Checkbox
Var Quick_Launch_Shortcut_Checkbox_State

;; IntOp $Desktop_Shortcut_Checkbox_State 1
;; IntOp $Start_Menu_Shortcut_Checkbox_State 1
;; IntOp $Quick_Launch_Shortcut_Checkbox_State 0

Function nsDialogsPage

	nsDialogs::Create /NOUNLOAD 1018
	Pop $Dialog

	${If} $Dialog == error
		Abort
	${EndIf}

	${NSD_CreateCheckbox} 0 0 100% 12u "Create &Desktop Shortcut"
	Pop $Desktop_Shortcut_Checkbox
	${NSD_SetState} $Desktop_Shortcut_Checkbox $Desktop_Shortcut_Checkbox_State

	${NSD_CreateCheckbox} 0 13u 100% 12u "Create &Start Menu Shortcut"
	Pop $Start_Menu_Shortcut_Checkbox
	${NSD_SetState} $Start_Menu_Shortcut_Checkbox $Start_Menu_Shortcut_Checkbox_State

	${NSD_CreateCheckbox} 0 26u 100% 12u "Create &Quick Launch Shortcut"
	Pop $Quick_Launch_Shortcut_Checkbox
	${NSD_SetState} $Quick_Launch_Shortcut_Checkbox $Quick_Launch_Shortcut_Checkbox_State

        nsDialogs::Show

FunctionEnd

Function nsDialogsPageLeave

	${NSD_GetState} $Desktop_Shortcut_Checkbox $Desktop_Shortcut_Checkbox_State
	${NSD_GetState} $Start_Menu_Shortcut_Checkbox $Start_Menu_Shortcut_Checkbox_State
	${NSD_GetState} $Quick_Launch_Shortcut_Checkbox $Quick_Launch_Shortcut_Checkbox_State

FunctionEnd

Function LockedListShow
  !insertmacro MUI_HEADER_TEXT `Quit running applications` `These running applications may prevent the program from installing properly.`
  ${If} ${AtLeastWinNt4}
    LockedList::AddModule /NOUNLOAD "$INSTDIR\MSVCR71.dll"
    LockedList::Dialog /AUTOCLOSE
    LockedList::Unload
  ${EndIf}
FunctionEnd

  !insertmacro MUI_PAGE_WELCOME

  Page Custom LockedListShow 

#  !insertmacro MUI_PAGE_LICENSE "${NSISDIR}\Docs\Modern UI\License.txt"
#  !insertmacro MUI_PAGE_COMPONENTS
  !insertmacro MUI_PAGE_DIRECTORY

  ; Start Menu Folder Configuration
  !define MUI_STARTMENUPAGE_REGISTRY_ROOT "HKCU"
  !define MUI_STARTMENUPAGE_REGISTRY_KEY "Software\${NAME}"
  !define MUI_STARTMENUPAGE_REGISTRY_VALUENAME "Start Menu Folder"

  !insertmacro MUI_PAGE_STARTMENU "Application" $StartMenuFolder

  Page custom nsDialogsPage nsDialogsPageLeave nsDialogsPage

  !insertmacro MUI_PAGE_INSTFILES

    !define MUI_FINISHPAGE_TEXT_LARGE
    !define MUI_FINISHPAGE_TEXT '${NAME} has been installed. If Run \
${NAME} is checked below, then it will run when you click \
Finish. $\r$\n$\r$\n\
In the future, you may run the program at \
Start Menu\Programs\$StartMenuFolder\${NAME}'

    # !define MUI_FINISHPAGE_RUN_NOTCHECKED
    !define MUI_FINISHPAGE_RUN $INSTDIR\WordUp.exe
    # !define MUI_FINISHPAGE_SHOWREADME_NOTCHECKED
    # !define MUI_FINISHPAGE_SHOWREADME $INSTDIR\README.txt
    !define MUI_FINISHPAGE_LINK "Click here to visit the ${NAME} web site."
    !define MUI_FINISHPAGE_LINK_LOCATION "http://marc-abramowitz.com/word_up"
  !insertmacro MUI_PAGE_FINISH

  !insertmacro MUI_UNPAGE_WELCOME
  !insertmacro MUI_UNPAGE_CONFIRM
  !insertmacro MUI_UNPAGE_INSTFILES
  !insertmacro MUI_UNPAGE_FINISH

 !insertmacro MUI_LANGUAGE "English"
 
;--------------------------------

; The stuff to install
Section "Install"

  ; Set output path to the installation directory.
  SetOutPath $INSTDIR
  
  ; Put file there
  File /r "WordUp\*.*"

  ; Write the uninstall keys for Windows
  WriteRegStr HKLM "Software\Microsoft\Windows\CurrentVersion\Uninstall\${NAME}" "DisplayName" "${NAME} ${VERSION}"
  WriteRegStr HKLM "Software\Microsoft\Windows\CurrentVersion\Uninstall\${NAME}" "UninstallString" '"$INSTDIR\uninstall.exe"'
  WriteRegDWORD HKLM "Software\Microsoft\Windows\CurrentVersion\Uninstall\${NAME}" "NoModify" 1
  WriteRegDWORD HKLM "Software\Microsoft\Windows\CurrentVersion\Uninstall\${NAME}" "NoRepair" 1
  WriteUninstaller "uninstall.exe"

  !insertmacro MUI_STARTMENU_WRITE_BEGIN Application

      CreateDirectory "$SMPROGRAMS\$StartMenuFolder"
      CreateShortCut "$SMPROGRAMS\$StartMenuFolder\${NAME}.lnk" "$INSTDIR\WordUp.exe" "" "" "" SW_SHOWNORMAL "" "An addictive word game"
      CreateShortCut "$SMPROGRAMS\$StartMenuFolder\Uninstall.lnk" "$INSTDIR\Uninstall.exe"

      ${If} $Desktop_Shortcut_Checkbox_State == 1
          CreateShortCut "$DESKTOP\${NAME}.lnk" "$INSTDIR\WordUp.exe" "" "" "" SW_SHOWNORMAL "" "An addictive word game"
      ${EndIf}
      ${If} $Start_Menu_Shortcut_Checkbox_State == 1
          CreateShortCut "$STARTMENU\${NAME}.lnk" "$INSTDIR\WordUp.exe" "" "" "" SW_SHOWNORMAL "" "An addictive word game"
      ${EndIf}
      ${If} $Quick_Launch_Shortcut_Checkbox_State == 1
          CreateShortCut "$QUICKLAUNCH\${NAME}.lnk" "$INSTDIR\WordUp.exe" "" "" "" SW_SHOWNORMAL "" "An addictive word game"
      ${EndIf}

  !insertmacro MUI_STARTMENU_WRITE_END
  
SectionEnd ; end the section

;--------------------------------

; Uninstaller

Section "Uninstall"
  
  ; Remove registry keys
  DeleteRegKey HKLM "Software\Microsoft\Windows\CurrentVersion\Uninstall\${NAME}"
  DeleteRegKey HKLM "Software\${NAME}"

  !insertmacro MUI_STARTMENU_GETFOLDER Application $StartMenuFolder

  ; Remove directories used
  RMDir /r "$SMPROGRAMS\$StartMenuFolder"
  Delete "$DESKTOP\${NAME}.lnk"
  Delete "$STARTMENU\${NAME}.lnk"
  Delete "$QUICKLAUNCH\${NAME}.lnk"
  RMDir /r "$INSTDIR"

SectionEnd
