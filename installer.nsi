;;; Comments beginning with ";;;" are commentary added by PyTom to 
;;; try to help you understand this file.
;;;
;;; This installer expects that you will have supplied LICENSE.txt 
;;; and README.txt files in the root directory of your game.
;;;
;;; To use this, place it in the root directory of your game, 
;;; right-click on it, and choose "Compile NSIS script..."

;;; First up, change the settings below to match your game.

;;; The exe used to run your game.
!define EXE "moonlight.exe"

;;; The exe containing the installer. This will be created in the directory
;;; above the root directory containing your game. 
!define INSTALLER_EXE "moonlight-1.0ni.exe"

;;; The name and version.
!define PRODUCT_NAME "Moonlight Walks"
!define PRODUCT_VERSION "1.0"

;;; The following settings are only shown to the user in Add/Remove programs
;;; but you'll still want to use them.

!define PRODUCT_WEB_SITE "http://www.bishoujo.us/moonlight/"
!define PRODUCT_PUBLISHER "American Bishoujo"

;;; Ignore this next block of stuff. It's mostly boilerplate.
!include "MUI.nsh"
!define MUI_ABORTWARNING

;;; Change this to change the compression scheme.
SetCompressor lzma

;;; You can change these to customize the bitmaps and icons used for
;;; your installer and uninstaller. Bitmaps should be 150x57.

; !define MUI_HEADERIMAGE
; !define MUI_HEADERIMAGE_BITMAP "${NSISDIR}\Contrib\Graphics\Header\nsis.bmp"
; !define MUI_HEADERIMAGE_UNBITMAP "${NSISDIR}\Contrib\Graphics\Header\nsis.bmp"
!define MUI_ICON "${NSISDIR}\Contrib\Graphics\Icons\modern-install.ico"
!define MUI_UNICON "${NSISDIR}\Contrib\Graphics\Icons\modern-uninstall.ico"


;;; This is the sequencing of the pages that does the actual installation.
;;; you can comment pages out, if you want to.

; Welcome page
!insertmacro MUI_PAGE_WELCOME

; License page
!insertmacro MUI_PAGE_LICENSE "LICENSE.txt"

; Directory page
!insertmacro MUI_PAGE_DIRECTORY
; Instfiles page
!insertmacro MUI_PAGE_INSTFILES
; Finish page
!define MUI_FINISHPAGE_SHOWREADME "$INSTDIR\README.txt"
!insertmacro MUI_PAGE_FINISH

; Uninstaller pages
!insertmacro MUI_UNPAGE_INSTFILES

;;; Okay, that's it for the commentary. You're on your own from here...
;;; but you probably won't need to touch anything below this point.

; Various other defines.
!define PRODUCT_UNINST_KEY "Software\Microsoft\Windows\CurrentVersion\Uninstall\${PRODUCT_NAME}"
!define PRODUCT_UNINST_ROOT_KEY "HKLM"

; Language files
!insertmacro MUI_LANGUAGE "English"

; Reserve files
!insertmacro MUI_RESERVEFILE_INSTALLOPTIONS


Name "${PRODUCT_NAME} ${PRODUCT_VERSION}"
OutFile "..\${INSTALLER_EXE}"
InstallDir "$PROGRAMFILES\${PRODUCT_NAME}"

Section "!${PRODUCT_NAME}" SEC01
  SetOutPath "$INSTDIR"
  SetOverwrite ifnewer

  File /r /x renpy /x *.py /x *.pyw /x installer.nsi /x persistent *.*
  CreateDirectory "$SMPROGRAMS\${PRODUCT_NAME}"
  CreateShortCut "$SMPROGRAMS\${PRODUCT_NAME}\${PRODUCT_NAME}.lnk" "$INSTDIR\${EXE}"
  CreateShortCut "$DESKTOP\${PRODUCT_NAME}.lnk" "$INSTDIR\${EXE}"
SectionEnd

Section -AdditionalIcons
  CreateShortCut "$SMPROGRAMS\${PRODUCT_NAME}\Uninstall.lnk" "$INSTDIR\uninst.exe"
  CreateShortCut "$SMPROGRAMS\${PRODUCT_NAME}\README.lnk" "$INSTDIR\README.txt"
SectionEnd

Section -Post
  WriteUninstaller "$INSTDIR\uninst.exe"
  WriteRegStr ${PRODUCT_UNINST_ROOT_KEY} "${PRODUCT_UNINST_KEY}" "DisplayName" "$(^Name)"
  WriteRegStr ${PRODUCT_UNINST_ROOT_KEY} "${PRODUCT_UNINST_KEY}" "UninstallString" "$INSTDIR\uninst.exe"
  WriteRegStr ${PRODUCT_UNINST_ROOT_KEY} "${PRODUCT_UNINST_KEY}" "DisplayIcon" "$INSTDIR\${EXE}"
  WriteRegStr ${PRODUCT_UNINST_ROOT_KEY} "${PRODUCT_UNINST_KEY}" "DisplayVersion" "${PRODUCT_VERSION}"
  WriteRegStr ${PRODUCT_UNINST_ROOT_KEY} "${PRODUCT_UNINST_KEY}" "URLInfoAbout" "${PRODUCT_WEB_SITE}"
  WriteRegStr ${PRODUCT_UNINST_ROOT_KEY} "${PRODUCT_UNINST_KEY}" "Publisher" "${PRODUCT_PUBLISHER}"
SectionEnd


Function un.onUninstSuccess
  HideWindow
  MessageBox MB_ICONINFORMATION|MB_OK "$(^Name) was successfully removed from your computer."
FunctionEnd

Function un.onInit
  MessageBox MB_ICONQUESTION|MB_YESNO|MB_DEFBUTTON2 "Are you sure you want to completely remove $(^Name) and all of its components?" IDYES +2
  Abort
FunctionEnd

Section Uninstall

  Delete "$SMPROGRAMS\${PRODUCT_NAME}\README.lnk"
  Delete "$SMPROGRAMS\${PRODUCT_NAME}\Uninstall.lnk"
  Delete "$DESKTOP\${PRODUCT_NAME}.lnk"
  Delete "$SMPROGRAMS\${PRODUCT_NAME}\${PRODUCT_NAME}.lnk"

  RMDir "$SMPROGRAMS\${PRODUCT_NAME}"
  RMDir /r "$INSTDIR"

  DeleteRegKey ${PRODUCT_UNINST_ROOT_KEY} "${PRODUCT_UNINST_KEY}"
  SetAutoClose true
SectionEnd


