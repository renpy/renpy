#@PydevCodeAnalysisIgnore
"""Easy to use dialogs.

Message(msg) -- display a message and an OK button.
AskString(prompt, default) -- ask for a string, display OK and Cancel buttons.
AskPassword(prompt, default) -- like AskString(), but shows text as bullets.
AskYesNoCancel(question, default) -- display a question and Yes, No and Cancel buttons.
GetArgv(optionlist, commandlist) -- fill a sys.argv-like list using a dialog
AskFileForOpen(...) -- Ask the user for an existing file
AskFileForSave(...) -- Ask the user for an output file
AskFolder(...) -- Ask the user to select a folder
bar = Progress(label, maxvalue) -- Display a progress bar
bar.set(value) -- Set value
bar.inc( *amount ) -- increment value by amount (default=1)
bar.label( *newlabel ) -- get or set text label.

More documentation in each function.
This module uses DLOG resources 260 and on.
Based upon STDWIN dialogs with the same names and functions.
"""

from __future__ import division
from __future__ import print_function

import os

import ctypes
import ctypes.wintypes as wintypes

from EasyDialogsResources import resources


__all__ = ['Message', 'AskString', 'AskPassword', 'AskYesNoCancel',
    'GetArgv', 'AskFileForOpen', 'AskFileForSave', 'AskFolder',
    'ProgressBar']


# Load required Windows DLLs
comdlg32 = ctypes.windll.comdlg32
kernel32 = ctypes.windll.kernel32
ole32 = ctypes.windll.ole32
shell32 = ctypes.windll.shell32
user32 = ctypes.windll.user32


# Windows Constants
BFFM_INITIALIZED = 1
BFFM_SETOKTEXT = 1129
BFFM_SETSELECTIONA = 1126
BIF_EDITBOX = 16
BS_DEFPUSHBUTTON = 1
CB_ADDSTRING = 323
CB_GETCURSEL = 327
CB_SETCURSEL = 334
CDM_SETCONTROLTEXT = 1128
EM_GETLINECOUNT = 186
EM_GETMARGINS = 212
EM_POSFROMCHAR = 214
EM_SETSEL = 177
GWL_STYLE = -16
IDC_STATIC = -1
IDCANCEL = 2
IDNO = 7
IDOK = 1
IDYES = 6
MAX_PATH = 260
OFN_ALLOWMULTISELECT = 512
OFN_ENABLEHOOK = 32
OFN_ENABLESIZING = 8388608
OFN_ENABLETEMPLATEHANDLE = 128
OFN_EXPLORER = 524288
OFN_OVERWRITEPROMPT = 2
OPENFILENAME_SIZE_VERSION_400 = 76
PBM_GETPOS = 1032
PBM_SETMARQUEE = 1034
PBM_SETPOS = 1026
PBM_SETRANGE = 1025
PBM_SETRANGE32 = 1030
PBS_MARQUEE = 8
PM_REMOVE = 1
SW_HIDE = 0
SW_SHOW = 5
SW_SHOWNORMAL = 1
SWP_NOACTIVATE = 16
SWP_NOMOVE = 2
SWP_NOSIZE = 1
SWP_NOZORDER = 4
VER_PLATFORM_WIN32_NT = 2
WM_COMMAND = 273
WM_GETTEXT = 13
WM_GETTEXTLENGTH = 14
WM_INITDIALOG = 272
WM_NOTIFY = 78


# Windows function prototypes
BrowseCallbackProc = ctypes.WINFUNCTYPE(ctypes.c_int, wintypes.HWND, ctypes.c_uint, wintypes.LPARAM, wintypes.LPARAM)
DialogProc = ctypes.WINFUNCTYPE(ctypes.c_int, wintypes.HWND, ctypes.c_uint, wintypes.WPARAM, wintypes.LPARAM)
EnumChildProc = ctypes.WINFUNCTYPE(ctypes.c_int, wintypes.HWND, wintypes.LPARAM)
LPOFNHOOKPROC = ctypes.WINFUNCTYPE(ctypes.c_int, wintypes.HWND, ctypes.c_uint, wintypes.WPARAM, wintypes.LPARAM)


# Windows types
LPCTSTR = ctypes.c_char_p
LPTSTR = ctypes.c_char_p
LPVOID = ctypes.c_voidp
TCHAR = ctypes.c_char

class OSVERSIONINFO(ctypes.Structure):
    _fields_ = [
                ("dwOSVersionInfoSize", wintypes.DWORD),
                ("dwMajorVersion", wintypes.DWORD),
                ("dwMinorVersion", wintypes.DWORD),
                ("dwBuildNumber", wintypes.DWORD),
                ("dwPlatformId", wintypes.DWORD),
                ("szCSDVersion", TCHAR*128)
               ]
    def __init__(self):
        ctypes.Structure.__init__(self)
        self.dwOSVersionInfoSize = ctypes.sizeof(self)

class OPENFILENAME(ctypes.Structure):
    _fields_ = [
                ("lStructSize", wintypes.DWORD),
                ("hwndOwner", wintypes.HWND),
                ("hInstance", LPCTSTR),
                ("lpstrFilter", LPCTSTR),
                ("lpstrCustomFilter", LPTSTR),
                ("nMaxCustFilter", wintypes.DWORD),
                ("nFilterIndex", wintypes.DWORD),
                ("lpstrFile", LPTSTR),
                ("nMaxFile", wintypes.DWORD),
                ("lpstrFileTitle", LPTSTR),
                ("nMaxFileTitle", wintypes.DWORD),
                ("lpstrInitialDir", LPCTSTR),
                ("lpstrTitle", LPCTSTR),
                ("flags", wintypes.DWORD),
                ("nFileOffset", wintypes.WORD),
                ("nFileExtension", wintypes.WORD),
                ("lpstrDefExt", LPCTSTR),
                ("lCustData", wintypes.LPARAM),
                ("lpfnHook", LPOFNHOOKPROC),
                ("lpTemplateName", LPCTSTR),
                ("pvReserved", LPVOID),
                ("dwReserved", wintypes.DWORD),
                ("FlagsEx", wintypes.DWORD)
               ]

    def __init__(self):
        ctypes.Structure.__init__(self)
        versionInfo = OSVERSIONINFO()
        kernel32.GetVersionExA(ctypes.byref(versionInfo))
        if versionInfo.dwPlatformId == VER_PLATFORM_WIN32_NT:
            if (versionInfo.dwMajorVersion, versionInfo.dwMinorVersion) == (4, 0):
                self.lStructSize = OPENFILENAME_SIZE_VERSION_400
            elif versionInfo.dwMajorVersion >= 5:
                self.lStructSize = ctypes.sizeof(OPENFILENAME)
            else:
                raise RuntimeError('Windows NT 4.0 or later is required.')
        else:
            self.lStructSize = ctypes.sizeof(OPENFILENAME) - 12

class BROWSEINFO(ctypes.Structure):
    _fields_ = [
                ("hwndOwner", wintypes.HWND),
                ("pidlRoot", LPVOID),
                ("pszDisplayName", LPTSTR),
                ("lpszTitle", LPCTSTR),
                ("ulFlags", ctypes.c_uint),
                ("lpfn", BrowseCallbackProc),
                ("lParam", wintypes.LPARAM),
                ("iImage", ctypes.c_int)
               ]


# Windows macro emulation
def HIWORD(x):
    return (x >> 16) & 0xffff

def LOWORD(x):
    return x & 0xffff

def MAKELONG(a, b):
    return (a & 0xffff) | ((b & 0xffff) << 16)

MAKELPARAM = MAKELONG


# Utilities
def CenterWindow(hwnd):
    desktopRect = GetWindowRect(user32.GetDesktopWindow())
    myRect = GetWindowRect(hwnd)
    x = width(desktopRect) // 2 - width(myRect) // 2
    y = height(desktopRect) // 2 - height(myRect) // 2
    user32.SetWindowPos(hwnd, 0,
                        desktopRect.left + x,
                        desktopRect.top + y,
                        0, 0,
                        SWP_NOACTIVATE | SWP_NOSIZE | SWP_NOZORDER
                       )

def EnumChildWindows(hwnd):
    childWindows = []
    def enumChildProc(hwnd, lParam):
        childWindows.append(hwnd)
        return True
    enumChildProc = EnumChildProc(enumChildProc)
    user32.EnumChildWindows(hwnd, enumChildProc, 0)
    return childWindows

def GetText(hwnd):
    length = user32.SendMessageA(hwnd, WM_GETTEXTLENGTH, 0, 0) + 1
    buffer = ctypes.c_char_p('\0' * length)
    user32.SendMessageA(hwnd, WM_GETTEXT, length, buffer)
    return buffer.value

def GetWindowRect(hwnd):
    rect = wintypes.RECT()
    user32.GetWindowRect(hwnd, ctypes.byref(rect))
    return rect

def width(rect):
    return rect.right-rect.left

def height(rect):
    return rect.bottom-rect.top


# Mac API emulation
def AutoSizeDialog(dialog, center=True):
    classNameBuffer = ctypes.c_buffer(1024)
    children = []
    editBoxes = []
    for child in EnumChildWindows(dialog):
        children.append(child)
        user32.GetClassNameA(child, classNameBuffer, 1024)
        if classNameBuffer.value.lower() == 'edit':
            editBoxes.append(child)

    editBoxes.sort(lambda x, y: cmp(GetWindowRect(x).top, GetWindowRect(y).top))

    for editBox in editBoxes:
        text = GetText(editBox)
        user32.SetWindowTextA(editBox, 'X\r\nX')
        if user32.SendMessageA(editBox, EM_GETLINECOUNT, 0, 0) < 2:
            user32.SetWindowTextA(editBox, text)
        else:
            lineHeight = HIWORD(user32.SendMessageA(editBox, EM_POSFROMCHAR, 3, 0)) - HIWORD(user32.SendMessageA(editBox, EM_POSFROMCHAR, 0, 0))
            user32.SetWindowTextA(editBox, text)
            newHeight = user32.SendMessageA(editBox, EM_GETLINECOUNT, 0, 0)*lineHeight + 2*LOWORD(user32.SendMessageA(editBox, EM_GETMARGINS, 0, 0))
            editBoxRect = GetWindowRect(editBox)
            oldHeight = height(editBoxRect)
            if newHeight != oldHeight:
                topLeft = wintypes.POINT(editBoxRect.left, editBoxRect.top)
                user32.ScreenToClient(dialog, ctypes.byref(topLeft))
                user32.MoveWindow(editBox, topLeft.x, topLeft.y, width(editBoxRect), newHeight, False)

                for child in children:
                    childRect = GetWindowRect(child)
                    if childRect.top >= editBoxRect.bottom:
                        topLeft = wintypes.POINT(childRect.left, childRect.top)
                        user32.ScreenToClient(dialog, ctypes.byref(topLeft))
                        user32.MoveWindow(child,
                                          topLeft.x, topLeft.y + newHeight - oldHeight,
                                          width(childRect), height(childRect),
                                          False
                                         )

                dRect = GetWindowRect(dialog)
                dRect.bottom += newHeight - oldHeight
                topLeft = wintypes.POINT(dRect.left, dRect.top)
                user32.MoveWindow(dialog, topLeft.x, topLeft.y, width(dRect), height(dRect), False)
                user32.InvalidateRect(dialog, None, True)

    if center:
        CenterWindow(dialog)


# Mac EasyDialogs emulation
def crlf2lf(text):
    if '\r\n' in text:
        text = '\n'.join(text.split('\r\n'))
    return text


def lf2crlf(text):
    if '\n' in text:
        text = '\r\n'.join(text.split('\n'))
    if len(text) > 253:
        text = text[:253] + '\205'
    return text


def Message(msg, id=260, ok=None):
    """Display a MESSAGE string.

    Return when the user clicks the OK button or presses Return.

    The MESSAGE string can be at most 255 characters long.
    """
    def DlgProc(hwnd, uMsg, wParam, lParam):
        if uMsg == WM_INITDIALOG:
            user32.SetWindowTextA(user32.GetDlgItem(hwnd, 1002), lf2crlf(msg))
            if ok:
                user32.SetWindowTextA(user32.GetDlgItem(hwnd, IDOK), ok)
            AutoSizeDialog(hwnd)
            return False
        if uMsg == WM_COMMAND and LOWORD(wParam) == IDOK:
            user32.EndDialog(hwnd, IDOK)
            return True
        if uMsg == WM_COMMAND and LOWORD(wParam) == IDCANCEL:
            user32.EndDialog(hwnd, IDCANCEL)
            return True
        else:
            return False

    # This next line is needed to prevent gc of the callback
    myDialogProc = DialogProc(DlgProc)
    return user32.DialogBoxIndirectParamA(0, resources[id], 0, myDialogProc, 0)


def AskString(prompt, default = '', id=261, ok=None, cancel=None):
    """Display a PROMPT string and a text entry field with a DEFAULT string.

    Return the contents of the text entry field when the user clicks the
    OK button or presses Return.
    Return None when the user clicks the Cancel button.

    If omitted, DEFAULT is empty.

    The PROMPT and DEFAULT strings, as well as the return value,
    can be at most 255 characters long.
    """
    result = [None]
    def DlgProc(hwnd, uMsg, wParam, lParam):
        if uMsg == WM_INITDIALOG:
            user32.SetWindowTextA(user32.GetDlgItem(hwnd, 1003), lf2crlf(prompt))
            user32.SetWindowTextA(user32.GetDlgItem(hwnd, 1004), lf2crlf(default))
            if ok:
                user32.SetWindowTextA(user32.GetDlgItem(hwnd, IDOK), ok)
            if cancel:
                user32.SetWindowTextA(user32.GetDlgItem(hwnd, IDCANCEL), cancel)
            AutoSizeDialog(hwnd)
            return False
        if uMsg == WM_COMMAND and LOWORD(wParam) == IDOK:
            result[0] = crlf2lf(GetText(user32.GetDlgItem(hwnd, 1004)))
            user32.EndDialog(hwnd, IDOK)
            return True
        if uMsg == WM_COMMAND and LOWORD(wParam) == IDCANCEL:
            user32.EndDialog(hwnd, IDCANCEL)
            return True
        else:
            return False

    # This next line is needed to prevent gc of the callback
    myDialogProc = DialogProc(DlgProc)
    user32.DialogBoxIndirectParamA(0, resources[id], 0, myDialogProc, 0)
    return result[0]


def AskPassword(prompt, default='', id=264, ok=None, cancel=None):
    """Display a PROMPT string and a text entry field with a DEFAULT string.
    The string is displayed as bullets only.

    Return the contents of the text entry field when the user clicks the
    OK button or presses Return.
    Return None when the user clicks the Cancel button.

    If omitted, DEFAULT is empty.

    The PROMPT and DEFAULT strings, as well as the return value,
    can be at most 255 characters long.
    """
    return AskString(prompt, default=default, id=id, ok=ok, cancel=cancel)


def AskYesNoCancel(question, default=0, yes=None, no=None, cancel=None, id=262):
    """Display a QUESTION string which can be answered with Yes or No.

    Return 1 when the user clicks the Yes button.
    Return 0 when the user clicks the No button.
    Return -1 when the user clicks the Cancel button.

    When the user presses Return, the DEFAULT value is returned.
    If omitted, this is 0 (No).

    The QUESTION string can be at most 255 characters.
    """
    def DlgProc(hwnd, uMsg, wParam, lParam):
        if uMsg == WM_INITDIALOG:
            user32.SetWindowTextA(user32.GetDlgItem(hwnd, 1005), lf2crlf(question))

            if yes is not None:
                button = user32.GetDlgItem(hwnd, IDYES)
                if yes == '':
                    user32.ShowWindow(button, False)
                else:
                    user32.SetWindowTextA(button, yes)
            if no is not None:
                button = user32.GetDlgItem(hwnd, IDNO)
                if no == '':
                    user32.ShowWindow(button, False)
                else:
                    user32.SetWindowTextA(button, no)
            if cancel is not None:
                button = user32.GetDlgItem(hwnd, IDCANCEL)
                if cancel == '':
                    user32.ShowWindow(button, False)
                else:
                    user32.SetWindowTextA(button, cancel)

            button = None
            if default == 1:
                button = user32.GetDlgItem(hwnd, IDYES)
            elif default == 0:
                button = user32.GetDlgItem(hwnd, IDNO)
            elif default == -1:
                button = user32.GetDlgItem(hwnd, IDCANCEL)
            if button:
                style = user32.GetWindowLongA(button, GWL_STYLE)
                user32.SetWindowLongA(button, GWL_STYLE, style | BS_DEFPUSHBUTTON)
                user32.SetFocus(button)

            AutoSizeDialog(hwnd)
            return False
        if uMsg == WM_COMMAND and LOWORD(wParam) == IDYES:
            user32.EndDialog(hwnd, 1)
            return True
        elif uMsg == WM_COMMAND and LOWORD(wParam) == IDNO:
            user32.EndDialog(hwnd, 0)
            return True
        elif uMsg == WM_COMMAND and LOWORD(wParam) == IDCANCEL:
            user32.EndDialog(hwnd, -1)
            return True
        else:
            return False

    # This next line is needed to prevent gc of the callback
    myDialogProc = DialogProc(DlgProc)
    return user32.DialogBoxIndirectParamA(0, resources[id], 0, myDialogProc, 0)


class ProgressBar:
    def __init__(self, title="Working...", maxval=0, label="", id=263):
        self._label = lf2crlf(label)
        def DlgProc(hwnd, uMsg, wParam, lParam):
            if uMsg == WM_INITDIALOG:
                user32.SetWindowTextA(hwnd, title)
                user32.SetWindowTextA(user32.GetDlgItem(hwnd, 1002), DlgProc.label)
            if uMsg == WM_COMMAND and LOWORD(wParam) == IDOK:
                user32.EndDialog(hwnd, IDOK)
                return True
            if uMsg == WM_COMMAND and LOWORD(wParam) == IDCANCEL:
                user32.EndDialog(hwnd, IDCANCEL)
                return True
            else:
                return False

        # Why a function attribute? Originally nested scopes
        # were used to get at self._label. This caused a cyclic reference
        # and since ProgressBar has a __del__ method (which closes the
        # window) it would never be collected (and hence the window
        # wouldn't close). Think of label as being like self. When this
        # function it used it will be used as a bound method where the
        # label is the object.
        DlgProc.label = self._label

        # This next line is needed to prevent gc of the callback
        self.wrappedDlgProc = DialogProc(DlgProc)
        self.hwnd = user32.CreateDialogIndirectParamA(0, resources[id], 0, self.wrappedDlgProc, 0)

        AutoSizeDialog(self.hwnd)
        user32.ShowWindow(self.hwnd, SW_SHOWNORMAL)
        self.set(0, maxval)

    def __del__(self):
        user32.DestroyWindow(self.hwnd)

    def title(self, newstr=""):
        """title(text) - Set title of progress window"""
        user32.SetWindowTextA(self.hwnd, newstr)
        self._pump()

    def label( self, *newstr ):
        """label(text) - Set text in progress box"""
        if newstr:
            self._label = lf2crlf(newstr[0])
        user32.SetWindowTextA(user32.GetDlgItem(self.hwnd, 1002), self._label)
        AutoSizeDialog(self.hwnd, center=False)
        self._pump()


    def _pump(self):
        msg = wintypes.MSG()
        while user32.PeekMessageA(ctypes.byref(msg), 0, 0, 0, PM_REMOVE):
            if not user32.IsDialogMessage(self.hwnd, ctypes.byref(msg)):
                user32.TranslateMessage(ctypes.byref(msg))
                user32.DispatchMessageA(ctypes.byref(msg))

        if not user32.IsWindowVisible(self.hwnd):
            raise KeyboardInterrupt


    def _update(self, value):
        maxval = self.maxval
        progbar = user32.GetDlgItem(self.hwnd, 1003)
        if maxval == 0:     # an indeterminate bar
            # make the bar grow and wrap around in case Marquee bars aren't supported
            pass
            pos = user32.SendMessageA(progbar, PBM_GETPOS, 0, 0)
            user32.SendMessageA(progbar, PBM_SETRANGE, 0, MAKELPARAM(0, 10))
            user32.SendMessageA(progbar, PBM_SETPOS, (pos+1) % 10, 0)
        else:               # a determinate bar
            if maxval > 32767:
                value = int(value/(maxval/32767.0))
                maxval = 32767
            maxval = int(maxval)
            value = int(value)
            if maxval > 65535:
                user32.SendMessageA(progbar, PBM_SETRANGE32, 0, maxval)
            else:
                user32.SendMessageA(progbar, PBM_SETRANGE, 0, MAKELPARAM(0, maxval))
            user32.SendMessageA(progbar, PBM_SETPOS, value, 0)  # set the bar length
        self._pump()


    def set(self, value, max=None):
        """set(value) - Set progress bar position"""
        if max != None:
            self.maxval = max
            bar = user32.GetDlgItem(self.hwnd, 1003)
            if max <= 0:    # indeterminate bar
                self.maxval = 0
                style = user32.GetWindowLongA(bar, GWL_STYLE)
                if not (style & PBS_MARQUEE):
                    user32.SetWindowLongA(bar, GWL_STYLE, style | PBS_MARQUEE)
                    user32.SendMessageA(bar, PBM_SETMARQUEE, 1, 10)
            else:           # determinate bar
                user32.SendMessageA(bar, PBM_SETMARQUEE, 0, 0)
                style = user32.GetWindowLongA(bar, GWL_STYLE)
                if style & PBS_MARQUEE:
                    user32.SetWindowLongA(bar, GWL_STYLE, style - PBS_MARQUEE)
        if value < 0:
            value = 0
        elif value > self.maxval:
            value = self.maxval
        self.curval = value
        self._update(value)

    def inc(self, n=1):
        """inc(amt) - Increment progress bar position"""
        self.set(self.curval + n)


def AskFileForOpen(
        message=None,
        typeList=None,
        # From here on the order is not documented
        version=None,
        defaultLocation=None,
        dialogOptionFlags=None,
        location=None,
        clientName=None,
        windowTitle=None,
        actionButtonLabel=None,
        cancelButtonLabel=None,
        preferenceKey=None,
        popupExtension=None,
        eventProc=None,
        previewProc=None,
        filterProc=None,
        wanted=None,
        multiple=None,
        # the following are for implementation use only
        defaultfn='',
        defaultext=None,
        fn=comdlg32.GetOpenFileNameA):
    """Display a dialog asking the user for a file to open.

    wanted is the return type wanted: FSSpec, FSRef, unicode or string (default)
    the other arguments can be looked up in Apple's Navigation Services documentation

    Windows differences:

    typeList is used for the same purpose, but file type handling is different
    between Windows and Mac, so the form of this argument is different. In an
    attempt to remain as similar as possible, a list of extensions can be
    supplied (e.g., ['*', 'txt', 'bat']). A more complete form is also
    allowed: [('All Files (*.*)', '*.*'), ('C Files (*.c, *.h)', '*.c;*.h')].
    The first item in each tuple is the text description presented to the
    user. The second item in each tuple is a semi-colon seperated list of
    standard Windows wildcard patterns that will match files described in the
    text description.

    The folowing parameters are ignored on Windows:
    clientName, dialogOptionFlags, eventProc, filterProc, popupExtension,
    preferenceKey, previewProc, version, wanted
    """

    ofn = OPENFILENAME()
    filename = defaultfn + '\0'*1024
    ofn.lpstrFile = filename
    ofn.nMaxFile = len(filename)
    ofn.flags = OFN_ENABLEHOOK | OFN_EXPLORER | OFN_ENABLESIZING | OFN_OVERWRITEPROMPT
    if multiple:
        ofn.flags |= OFN_ALLOWMULTISELECT
    ofn.lpstrTitle = windowTitle
    ofn.lpstrInitialDir = defaultLocation

    if typeList and filter(None, typeList):
        lpstrFilter = ''
        for typeSpec in typeList:
            try:
                lpstrFilter += '*.'+typeSpec+'\0*.'+typeSpec+'\0'
                if defaultext and not ofn.lpstrDefExt:
                    ofn.lpstrDefExt = typeSpec
            except TypeError:
                lpstrFilter += '%s\0%s\0' % typeSpec
                if defaultext and not ofn.lpstrDefExt:
                    ext = os.path.splitext(typeSpec[1])[1].lstrip('.')
                    if ext != '*':
                        ofn.lpstrDefExt = ext
        ofn.lpstrFilter = lpstrFilter + '\0'
    else:
        ofn.lpstrFilter = 'All Files (*.*)\0*.*\0\0'

    if message:
        ofn.flags |= OFN_ENABLETEMPLATEHANDLE
        ofn.hInstance = resources[270]

    hookProcInitDone = []
    def hookProc(hdlg, uiMsg, wParam, lParam):
        if uiMsg == WM_INITDIALOG:
            dialog = user32.GetParent(hdlg)
            if message:
                handle = user32.FindWindowExA(hdlg, 0, 0, 0)
                user32.SetWindowTextA(handle, message)
            if actionButtonLabel:
                user32.SendMessageA(dialog, CDM_SETCONTROLTEXT, IDOK, actionButtonLabel)
            if cancelButtonLabel:
                user32.SendMessageA(dialog, CDM_SETCONTROLTEXT, IDCANCEL, cancelButtonLabel)
        elif uiMsg == WM_NOTIFY:
            if not hookProcInitDone:
                hookProcInitDone.append(True)
                dialog = user32.GetParent(hdlg)
                desktop = user32.GetDesktopWindow()
                if message:
                    clientRect = wintypes.RECT()
                    user32.GetClientRect(dialog, ctypes.byref(clientRect))
                    dlgRect = wintypes.RECT()
                    user32.GetWindowRect(hdlg, ctypes.byref(dlgRect))
                    user32.SetWindowPos(hdlg, 0,
                                      0, 0,
                                      width(clientRect), height(dlgRect),
                                      SWP_NOMOVE | SWP_NOZORDER)
                    handle = user32.GetDlgItem(hdlg, IDC_STATIC)
                    user32.SetWindowPos(handle, 0,
                                      0, 0,
                                      width(clientRect), height(dlgRect),
                                      SWP_NOMOVE | SWP_NOZORDER)
                if location:
                    x, y = location
                    desktopRect = wintypes.RECT()
                    user32.GetWindowRect(desktop, ctypes.byref(desktopRect))
                    user32.SetWindowPos(dialog, 0,
                                      desktopRect.left + x,
                                      desktopRect.top + y, 0, 0,
                                      SWP_NOACTIVATE | SWP_NOSIZE | SWP_NOZORDER)
                else: # center
                    CenterWindow(dialog)
        return 0

    ofn.lpfnHook = LPOFNHOOKPROC(hookProc)

    if fn(ctypes.byref(ofn)):
        filenames = filter(None, filename.split('\0'))
        if len(filenames) > 1:
            dir, filenames = filenames[0], filenames[1:]
            return map(lambda fn: os.path.join(dir, fn), filenames)
        elif multiple:
            return filenames
        else:
            return filenames[0]
    else:
        return None


def AskFileForSave(
        message=None,
        savedFileName=None,
        # From here on the order is not documented
        version=None,
        defaultLocation=None,
        dialogOptionFlags=None,
        location=None,
        clientName=None,
        windowTitle=None,
        actionButtonLabel=None,
        cancelButtonLabel=None,
        preferenceKey=None,
        popupExtension=None,
        eventProc=None,
        fileType=None,
        fileCreator=None,
        wanted=None,
        multiple=None):
    """Display a dialog asking the user for a filename to save to.

    wanted is the return type wanted: FSSpec, FSRef, unicode or string (default)
    the other arguments can be looked up in Apple's Navigation Services documentation

    Windows differences:

    fileType is used for the same purpose, but file type handling is different
    between Windows and Mac, so the form of this argument is different. In an
    attempt to remain as similar as possible, an extensions can be supplied
    (e.g., 'txt'). A more complete form is also	allowed:
    ('Text Files (*.txt)', '*.txt'). The first item in the tuple is the text
    description presented to the user. The second item in the tuple is a
    standard Windows wildcard pattern that will match files described in the
    text description.

    The folowing parameters are ignored on Windows:
    clientName, dialogOptionFlags, eventProc, fileCreator, filterProc,
    multiple, popupExtension, preferenceKey, previewProc, version, wanted
    """
    return AskFileForOpen(
                        message=message, typeList=[fileType], version=version,
                        defaultLocation=defaultLocation,
                        dialogOptionFlags=dialogOptionFlags, location=location,
                        clientName=clientName, windowTitle=windowTitle,
                        actionButtonLabel=actionButtonLabel,
                        cancelButtonLabel=cancelButtonLabel,
                        preferenceKey=preferenceKey,
                        popupExtension=popupExtension, eventProc=eventProc,
                        wanted=wanted, multiple=multiple,
                        defaultfn=savedFileName or '',
                        defaultext=True,
                        fn=comdlg32.GetSaveFileNameA)


def AskFolder(
        message=None,
        # From here on the order is not documented
        version=None,
        defaultLocation=None,
        dialogOptionFlags=None,
        location=None,
        clientName=None,
        windowTitle=None,
        actionButtonLabel=None,
        cancelButtonLabel=None,
        preferenceKey=None,
        popupExtension=None,
        eventProc=None,
        filterProc=None,
        wanted=None,
        multiple=None):
    """Display a dialog asking the user for select a folder.

    wanted is the return type wanted: FSSpec, FSRef, unicode or string (default)
    the other arguments can be looked up in Apple's Navigation Services documentation

    Windows differences:

    The folowing parameters are ignored on Windows:
    clientName, dialogOptionFlags, eventProc, filterProc,
    multiple, popupExtension, preferenceKey, version, wanted
    """


    def BrowseCallback(hwnd, uMsg, lParam, lpData):
        if uMsg == BFFM_INITIALIZED:
            if actionButtonLabel:
                label = unicode(actionButtonLabel, errors='replace')
                user32.SendMessageW(hwnd, BFFM_SETOKTEXT, 0, label)
            if cancelButtonLabel:
                cancelButton = user32.GetDlgItem(hwnd, IDCANCEL)
                if cancelButton:
                    user32.SetWindowTextA(cancelButton, cancelButtonLabel)
            if windowTitle:
                user32.SetWindowTextA(hwnd, windowTitle)
            if defaultLocation:
                user32.SendMessageW(hwnd, BFFM_SETSELECTIONA, 1, defaultLocation.replace('/', '\\'))
            if location:
                x, y = location
                desktopRect = wintypes.RECT()
                user32.GetWindowRect(0, ctypes.byref(desktopRect))
                user32.SetWindowPos(hwnd, 0,
                                  desktopRect.left + x,
                                  desktopRect.top + y, 0, 0,
                                  SWP_NOACTIVATE | SWP_NOSIZE | SWP_NOZORDER)
            else:
                CenterWindow(hwnd)
        return 0

    # This next line is needed to prevent gc of the callback
    callback = BrowseCallbackProc(BrowseCallback)

    browseInfo = BROWSEINFO()
    browseInfo.pszDisplayName = ctypes.c_char_p('\0' * (MAX_PATH+1))
    browseInfo.lpszTitle = message
    browseInfo.lpfn = callback
    #~ browseInfo.ulFlags = BIF_EDITBOX

    # BIF_NEWDIALOGSTYLE is not used because it only works with apartment
    # threading. Using this style with COINIT_MULTITHREADED can cause problems.
    pidl = shell32.SHBrowseForFolder(ctypes.byref(browseInfo))
    if not pidl:
        result = None
    else:
        path = ctypes.c_char_p('\0' * (MAX_PATH+1))
        shell32.SHGetPathFromIDList(pidl, path)
        ole32.CoTaskMemFree(pidl)
        result = path.value
    return result


ARGV_ID=265
ARGV_ITEM_OK=1
ARGV_ITEM_CANCEL=2
ARGV_OPTION_GROUP=3
ARGV_OPTION_EXPLAIN=4
ARGV_OPTION_VALUE=5
ARGV_OPTION_ADD=6
ARGV_COMMAND_GROUP=7
ARGV_COMMAND_EXPLAIN=8
ARGV_COMMAND_ADD=9
ARGV_ADD_OLDFILE=10
ARGV_ADD_NEWFILE=11
ARGV_ADD_FOLDER=12
ARGV_CMDLINE_GROUP=13
ARGV_CMDLINE_DATA=14

def _setmenu(control, items):
    for item in items:
        if type(item) == type(()):
            label = item[0]
        else:
            label = item
        if label[-1] == '=' or label[-1] == ':':
            label = label[:-1]
        user32.SendMessageA(control, CB_ADDSTRING, 0, label)
    user32.SendMessageA(control, CB_SETCURSEL, 0, 0)

def _selectoption(d, optionlist, idx):
    if idx < 0 or idx >= len(optionlist):
        user32.MessageBeep(-1)
        return
    option = optionlist[idx]
    if type(option) == type(()):
        if len(option) == 4:
            help = option[2]
        elif len(option) > 1:
            help = option[-1]
        else:
            help = ''
    else:
        help = ''
    h = user32.GetDlgItem(d, ARGV_OPTION_EXPLAIN)
    if help and len(help) > 250:
        help = help[:250] + '...'
    user32.SetWindowTextA(h, help)
    hasvalue = 0
    if type(option) == type(()):
        label = option[0]
    else:
        label = option
    if label[-1] == '=' or label[-1] == ':':
        hasvalue = 1
    h = user32.GetDlgItem(d, ARGV_OPTION_VALUE)
    user32.SetWindowTextA(h, '')
    if hasvalue:
        user32.ShowWindow(h, SW_SHOW)
        #~ d.SelectDialogItemText(ARGV_OPTION_VALUE, 0, 0)
    else:
        user32.ShowWindow(h, SW_HIDE)

def GetArgv(optionlist=None, commandlist=None, addoldfile=1, addnewfile=1, addfolder=1, id=ARGV_ID):
    commandLineContents = []
    def DlgProc(hwnd, uMsg, wParam, lParam):
        if uMsg == WM_INITDIALOG:
            if optionlist:
                _setmenu(user32.GetDlgItem(hwnd, ARGV_OPTION_GROUP), optionlist)
                _selectoption(hwnd, optionlist, 0)
            else:
                for id in (30, ARGV_OPTION_GROUP, ARGV_OPTION_VALUE, ARGV_OPTION_ADD):
                    user32.EnableWindow(user32.GetDlgItem(hwnd, id), False)
            if commandlist:
                _setmenu(user32.GetDlgItem(hwnd, ARGV_COMMAND_GROUP), commandlist)
                if type(commandlist[0]) == type(()) and len(commandlist[0]) > 1:
                    help = commandlist[0][-1]
                    h = user32.GetDlgItem(hwnd, ARGV_COMMAND_EXPLAIN)
                    user32.SetWindowTextA(h, help)
            else:
                for id in (70, ARGV_COMMAND_GROUP, ARGV_COMMAND_ADD):
                    user32.EnableWindow(user32.GetDlgItem(hwnd, id), False)
            if not addoldfile:
                user32.EnableWindow(user32.GetDlgItem(hwnd, ARGV_ADD_OLDFILE), False)
            if not addnewfile:
                user32.EnableWindow(user32.GetDlgItem(hwnd, ARGV_ADD_NEWFILE), False)
            if not addfolder:
                user32.EnableWindow(user32.GetDlgItem(hwnd, ARGV_ADD_FOLDER), False)
            CenterWindow(hwnd)
            return False
        elif uMsg == WM_COMMAND and LOWORD(wParam) == IDOK:
            h = user32.GetDlgItem(hwnd, ARGV_CMDLINE_DATA)
            commandLineContents.append(GetText(h))
            user32.EndDialog(hwnd, IDOK)
            return True
        elif uMsg == WM_COMMAND and LOWORD(wParam) == IDCANCEL:
            user32.EndDialog(hwnd, IDCANCEL)
            return True

        if uMsg == WM_COMMAND:
            stringstoadd = []
            n = LOWORD(wParam)
            if n == ARGV_OPTION_GROUP:
                idx = user32.SendMessageA(lParam, CB_GETCURSEL, 0, 0)
                _selectoption(hwnd, optionlist, idx)
                return True
            elif n == ARGV_OPTION_ADD:
                idx = user32.SendMessageA(user32.GetDlgItem(hwnd, ARGV_OPTION_GROUP), CB_GETCURSEL, 0, 0)
                if 0 <= idx < len(optionlist):
                    option = optionlist[idx]
                    if type(option) == type(()):
                        option = option[0]
                    if option[-1] == '=' or option[-1] == ':':
                        option = option[:-1]
                        h = user32.GetDlgItem(hwnd, ARGV_OPTION_VALUE)
                        value = GetText(h)
                    else:
                        value = ''
                    if len(option) == 1:
                        stringtoadd = '-' + option
                    else:
                        stringtoadd = '--' + option
                    stringstoadd[:] = [stringtoadd]
                    if value:
                        stringstoadd.append(value)
                else:
                    user32.MessageBeep(-1)
            elif n == ARGV_COMMAND_GROUP:
                idx = user32.SendMessageA(lParam, CB_GETCURSEL, 0, 0)
                if 0 <= idx < len(commandlist) and type(commandlist[idx]) == type(()) and \
                        len(commandlist[idx]) > 1:
                    help = commandlist[idx][-1]
                    h = user32.GetDlgItem(hwnd, ARGV_COMMAND_EXPLAIN)
                    user32.SetWindowTextA(h, help)
            elif n == ARGV_COMMAND_ADD:
                idx = user32.SendMessageA(user32.GetDlgItem(hwnd, ARGV_COMMAND_GROUP), CB_GETCURSEL, 0, 0)
                if 0 <= idx < len(commandlist):
                    command = commandlist[idx]
                    if type(command) == type(()):
                        command = command[0]
                    stringstoadd = [command]
                else:
                    user32.MessageBeep(-1)
            elif n == ARGV_ADD_OLDFILE:
                pathname = AskFileForOpen()
                if pathname:
                    stringstoadd = [pathname]
            elif n == ARGV_ADD_NEWFILE:
                pathname = AskFileForSave()
                if pathname:
                    stringstoadd = [pathname]
            elif n == ARGV_ADD_FOLDER:
                pathname = AskFolder()
                if pathname:
                    stringstoadd = [pathname]

            for stringtoadd in stringstoadd:
                if '"' in stringtoadd or "'" in stringtoadd or " " in stringtoadd:
                    stringtoadd = repr(stringtoadd)
                h = user32.GetDlgItem(hwnd, ARGV_CMDLINE_DATA)
                oldstr = GetText(h)
                if oldstr and oldstr[-1] != ' ':
                    oldstr = oldstr + ' '
                oldstr = oldstr + stringtoadd
                if oldstr[-1] != ' ':
                    oldstr = oldstr + ' '
                user32.SetWindowTextA(h, oldstr)
                user32.SendMessageA(user32.GetDlgItem(hwnd, ARGV_CMDLINE_DATA), EM_SETSEL, 0, -1)

        return False

    # This next line is needed to prevent gc of the callback
    myDialogProc = DialogProc(DlgProc)
    if IDOK == user32.DialogBoxIndirectParamA(0, resources[id], 0, myDialogProc, 0):
        oldstr = commandLineContents[0]
        tmplist = oldstr.split()
        newlist = []
        while tmplist:
            item = tmplist[0]
            del tmplist[0]
            if item[0] == '"':
                while item[-1] != '"':
                    if not tmplist:
                        raise RuntimeError("Unterminated quoted argument")
                    item = item + ' ' + tmplist[0]
                    del tmplist[0]
                item = item[1:-1]
            if item[0] == "'":
                while item[-1] != "'":
                    if not tmplist:
                        raise RuntimeError("Unterminated quoted argument")
                    item = item + ' ' + tmplist[0]
                    del tmplist[0]
                item = item[1:-1]
            newlist.append(item)
        return newlist
    else:
        raise SystemExit


def test():
    import time

    class empty: pass
    Carbon = empty()
    Carbon.File = empty()
    Carbon.File.FSSpec = None
    Carbon.File.FSRef = None
    MacOS = empty()

    Message("Testing EasyDialogs.")
    optionlist = (('v', 'Verbose'), ('verbose', 'Verbose as long option'),
                ('flags=', 'Valued option'), ('f:', 'Short valued option'))
    commandlist = (('start', 'Start something'), ('stop', 'Stop something'))
    argv = GetArgv(optionlist=optionlist, commandlist=commandlist, addoldfile=0)
    Message("Command line: %s"%' '.join(argv))
    for i in range(len(argv)):
        print(('arg[%d] = %r' % (i, argv[i])))
    ok = AskYesNoCancel("Do you want to proceed?")
    ok = AskYesNoCancel("Do you want to identify?", yes="Identify", no="No")
    if ok > 0:
        s = AskString("Enter your first name", "Joe")
        s2 = AskPassword("Okay %s, tell us your nickname"%s, s, cancel="None")
        if not s2:
            Message("%s has no secret nickname"%s)
        else:
            Message("Hello everybody!!\nThe secret nickname of %s is %s!!!"%(s, s2))
    else:
        s = 'Anonymous'
    rv = AskFileForOpen(message="Gimme a file, %s"%s, wanted=Carbon.File.FSSpec)
    Message("rv: %s"%rv)
    rv = AskFileForSave(wanted=Carbon.File.FSRef, savedFileName="%s.txt"%s)
    Message("rv: %s"%rv) # was: Message("rv.as_pathname: %s"%rv.as_pathname())
    rv = AskFolder()
    Message("Folder name: %s"%rv)
    text = ( "Working Hard...", "Hardly Working..." ,
            "So far, so good!", "Keep on truckin'" )
    bar = ProgressBar("Progress, progress...", 0, label="Ramping up...")
    try:
        if hasattr(MacOS, 'SchedParams'):
            appsw = MacOS.SchedParams(1, 0)
        for i in xrange(20):
            bar.inc()
            time.sleep(0.05)
        bar.set(0,100)
        for i in xrange(100):
            bar.set(i)
            time.sleep(0.05)
            if i % 10 == 0:
                bar.label(text[(i//10) % 4])
        bar.label("Done.")
        time.sleep(1.0)     # give'em a chance to see "Done."
    finally:
        del bar
        if hasattr(MacOS, 'SchedParams'):
            MacOS.SchedParams(*appsw)

if __name__ == '__main__':
    try:
        test()
    except KeyboardInterrupt:
        Message("Operation Canceled.")
