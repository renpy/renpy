tiny file dialogs ( cross-platform C C++ ) v3.8.8 [Apr 22, 2021] zlib licence
 _________
/         \   Tray-popup InputBox PasswordBox MessageBox Notification Beep
|tiny file|   ColorPicker OpenFileDialog SaveFileDialog SelectFolderDialog
| dialogs |   ASCII UTF-8 (and also MBCS & UTF-16 for windows)
\____  ___/   Native dialog library for WINDOWS MAC OSX GTK+ QT CONSOLE
     \|       SSH support via automatic switch to console mode or X forwarding

C89/C18 & C++98/C++20 compliant: tested with C & C++ compilers
VisualStudio MinGW GCC Clang TinyCC OpenWatcom-v2 BorlandC SunCC ZapCC
on Windows Mac Linux Bsd Solaris Minix Raspbian Flatpak
using Gnome Kde Mate Enlightenment Cinnamon Budgie Unity Lxde Lxqt Xfce
      WindowMaker IceWm Cde Jds OpenBox Awesome Jwm Xdm Cwm

Bindings for LUA and C# dll, Haskell, Fortran. Included in LWJGL(java), Rust, Allegrobasic

                   http://tinyfiledialogs.sourceforge.net
         git clone http://git.code.sf.net/p/tinyfiledialogs/code tinyfd
 ____________________________________________________________________________
|  ________________________________________________________________________  |
| |  ____________________________________________________________________  | |
| | | If you like tinyfiledialogs, please upvote my stackoverflow answer | | |
| | |                https://stackoverflow.com/a/47651444                | | |
| | |____________________________________________________________________| | |
| |________________________________________________________________________| |
|____________________________________________________________________________|
     _____________________________________________________________________
    |                                                                     |
    | my email address is at the top of the header file tinyfiledialogs.h |
    |_____________________________________________________________________|
 ________________________________________________________________________________
|  ____________________________________________________________________________  |
| |                                                                            | |
| | on windows:                                                                | |
| |  - for UTF-16, use the wchar_t functions at the bottom of the header file  | |
| |  - _wfopen() requires wchar_t                                              | |
| |                                                                            | |
| |  - in tinyfiledialogs, char is UTF-8 by default (since v3.6)               | |
| |  - but fopen() expects MBCS (not UTF-8)                                    | |
| |  - if you want char to be MBCS: set tinyfd_winUtf8 = 0                     | |
| |                                                                            | |
| |  - alternatively, tinyfiledialogs provides                                 | |
| |                        functions to convert between UTF-8, UTF-16 and MBCS | |
| |____________________________________________________________________________| |
|________________________________________________________________________________|

void tinyfd_beep();

int tinyfd_notifyPopup(
    char const * aTitle , // NULL or ""
    char const * aMessage , // NULL or "" may contain \n \t
    char const * aIconType ); // "info" "warning" "error"

int tinyfd_messageBox(
    char const * aTitle , // NULL or ""
    char const * aMessage , // NULL or "" may contain \n \t
    char const * aDialogType , // "ok" "okcancel" "yesno" "yesnocancel"
    char const * aIconType , // "info" "warning" "error" "question"
    int aDefaultButton );
        // 0 for cancel/no , 1 for ok/yes , 2 for no in yesnocancel

char const * tinyfd_inputBox(
    char const * aTitle , // NULL or ""
    char const * aMessage , // NULL or "" (\n and \t have no effect)
    char const * aDefaultInput ); // NULL for a passwordBox, "" for an inputbox
        // returns NULL on cancel

char const * tinyfd_saveFileDialog(
    char const * aTitle , // NULL or ""
    char const * aDefaultPathAndFile , // NULL or ""
    int aNumOfFilterPatterns , // 0 (1 in the following example)
    char const * const * aFilterPatterns , // NULL or char const * lFilterPatterns[1]={"*.txt"};
    char const * aSingleFilterDescription ); // NULL or "text files"
        // returns NULL on cancel

char const * tinyfd_openFileDialog(
    char const * aTitle , // NULL or ""
    char const * aDefaultPathAndFile , // NULL or ""
    int aNumOfFilterPatterns , // 0 (2 in the following example)
    char const * const * aFilterPatterns , // NULL or char const * lFilterPatterns[2]={"*.png","*.jpg"};
    char const * aSingleFilterDescription , // NULL or "image files"
    int aAllowMultipleSelects ); // 0
        // in case of multiple files, the separator is |
        // returns NULL on cancel

char const * tinyfd_selectFolderDialog(
    char const * aTitle , // NULL or ""
    char const * aDefaultPath ); // NULL or ""
        // returns NULL on cancel

char const * tinyfd_colorChooser(
    char const * aTitle , // NULL or ""
    char const * aDefaultHexRGB , // NULL or "#FF0000”
    unsigned char const aDefaultRGB[3] , // unsigned char lDefaultRGB[3] = { 0 , 128 , 255 };
    unsigned char aoResultRGB[3] ); // unsigned char lResultRGB[3];
        // returns the hexcolor as a string "#FF0000"
        // aoResultRGB also contains the result
        // aDefaultRGB is used only if aDefaultHexRGB is NULL
        // aDefaultRGB and aoResultRGB can be the same array
        // returns NULL on cancel
 ___________________________________________________________________________________
|  _______________________________________________________________________________  |
| |                                                                               | |
| | wchar_t UTF-16 (windows only) prototypes are at the bottom of the header file | |
| |_______________________________________________________________________________| |
|___________________________________________________________________________________|

- This is not for ios nor android (it works in termux though).
- The files can be renamed with extension ".cpp" as the code is 100% compatible C C++
  (just comment out << extern "C" >> in the header file)
- Windows is fully supported from XP to 10 (maybe even older versions)
- C# & LUA via dll, see files in the folder EXTRAS
- OSX supported from 10.4 to latest (maybe even older versions)
- Do not use " and ' as the dialogs will be display with a warning
  instead of the title, message, etc...
- There's one file filter only, it may contain several patterns.
- If no filter description is provided,
  the list of patterns will become the description.
- On windows link against Comdlg32.lib and Ole32.lib
  (on windows the no linking claim is a lie)
- On unix: it tries command line calls, so no such need (NO LINKING).
- On unix you need one of the following:
  applescript, kdialog, zenity, matedialog, shellementary, qarma, yad,
  python (2 or 3)/tkinter/python-dbus (optional), Xdialog
  or curses dialogs (opens terminal if running without console).
- One of those is already included on most (if not all) desktops.
- In the absence of those it will use gdialog, gxmessage or whiptail
  with a textinputbox.
- If nothing is found, it switches to basic console input,
  it opens a console if needed (requires xterm + bash).
- for curses dialogs you must set tinyfd_allowCursesDialogs=1
- You can query the type of dialog that will be used (pass "tinyfd_query" as aTitle)
- String memory is preallocated statically for all the returned values.
- File and path names are tested before return, they should be valid.
- tinyfd_forceConsole=1; at run time, forces dialogs into console mode.
- On windows, console mode only make sense for console applications.
- On windows, console mode is not implemented for wchar_T UTF-16.
- Mutiple selects are not possible in console mode.
- The package dialog must be installed to run in curses dialogs in console mode.
  It is already installed on most unix systems.
- On osx, the package dialog can be installed via
  http://macappstore.org/dialog or http://macports.org
- On windows, for curses dialogs console mode,
  dialog.exe should be copied somewhere on your executable path.
  It can be found at the bottom of the following page:
  http://andrear.altervista.org/home/cdialog.php
  _________________________________________________________________
 |                                                                 |
 | The project provides an Hello World example:                    |
 |   if a console is missing, it will use graphic dialogs          |
 |   if a graphical display is absent, it will use console dialogs |
 |_________________________________________________________________|

OSX :
$ clang -o hello.app hello.c tinyfiledialogs.c
( or gcc )

UNIX :
$ gcc -o hello hello.c tinyfiledialogs.c
( or clang tcc owcc cc CC )

Windows :
  MinGW needs gcc >= v4.9 otherwise some headers are incomplete
  > gcc -o hello.exe hello.c tinyfiledialogs.c -LC:/mingw/lib -lcomdlg32 -lole32

  TinyCC needs >= v0.9.27 (+ tweaks - contact me) otherwise some headers are missing
  > tcc -o hello.exe hello.c tinyfiledialogs.c ^
      -isystem C:\tcc\winapi-full-for-0.9.27\include\winapi ^
      -lcomdlg32 -lole32 -luser32 -lshell32

  Borland C: > bcc32c -o hello.exe hello.c tinyfiledialogs.c
  OpenWatcom v2: create a character-mode executable project.

  VisualStudio :
    Create a console application project,
    it links against comdlg32.lib & ole32.lib.

  VisualStudio command line :
> cl hello.c tinyfiledialogs.c comdlg32.lib ole32.lib user32.lib shell32.lib /W4
