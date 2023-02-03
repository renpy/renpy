# Copyright 2004-2023 Tom Rothamel <pytom@bishoujo.us>
#
# Permission is hereby granted, free of charge, to any person
# obtaining a copy of this software and associated documentation files
# (the "Software"), to deal in the Software without restriction,
# including without limitation the rights to use, copy, modify, merge,
# publish, distribute, sublicense, and/or sell copies of the Software,
# and to permit persons to whom the Software is furnished to do so,
# subject to the following conditions:
#
# The above copyright notice and this permission notice shall be
# included in all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND,
# EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF
# MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND
# NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE
# LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION
# OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION
# WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.

from __future__ import division, absolute_import, with_statement, print_function, unicode_literals

"""
This contains a wrapper for the tinyfiledialogs library. It's intended for use
in the launcher, and so may go away in some future Ren'Py version.
"""

cdef extern from "tinyfiledialogs/tinyfiledialogs.h":

    int tinyfd_notifyPopup(
        const char* aTitle,
        const char *aMessage,
        const char *aIconType)

    int tinyfd_messageBox(
        const char *aTitle,
        const char *aMessage,
        const char *aDialogType,
        const char *aIconType,
        int aDefaultButton)

    char * tinyfd_inputBox(
        const char *aTitle,
        const char *aMessage,
        const char *aDefaultInput)

    char * tinyfd_saveFileDialog(
        const char *aTitle,
        const char *aDefaultPathAndFile,
        int aNumOfFilterPatterns,
        const char *const * aFilterPatterns,
        const char *aSingleFilterDescription)

    char * tinyfd_openFileDialog(
        const char *aTitle,
        const char *aDefaultPathAndFile,
        int aNumOfFilterPatterns,
        const char *const * aFilterPatterns,
        const char *aSingleFilterDescription,
        int aAllowMultipleSelects)

    char * tinyfd_selectFolderDialog(
        const char *aTitle,
        const char *aDefaultPath)

    char * tinyfd_colorChooser(
        const char *aTitle,
        const char *aDefaultHexRGB,
        const unsigned char *aDefaultRGB,
        const unsigned char *aoResultRGB)

def encode(s):
    if s is None:
        return None
    else:
        return s.encode("utf-8")

cdef const char *cstr_or_null(s):
    if s is None:
        return NULL
    else:
        return s

encoded_filters = [ ]
cdef const char *encoded_filter_array[32]

cdef const char **filter_array(l):
    global encoded_filters
    encoded_filters = [ i.encode("utf-8") for i in l ]

    for i, b in enumerate(encoded_filters):
        encoded_filter_array[i] = b

    return encoded_filter_array

def notifyPopup(title, message, icon):
    """
    Causes a notification popup to be displayed.

    `title`
        The title of the popup. May be None for no title.

    `message`
        The message of the popup. May be None for no message, and may contain tab and newline
        characters.

    `icon`
        One of "info", "warning", or "error".
    """

    title = encode(title)
    message = encode(message)
    icon = encode(icon)

    return tinyfd_notifyPopup(cstr_or_null(title), cstr_or_null(message), icon.encode)

def messageBox(title, message, dialogtype, icon, defaultbutton):
    """
    Causes a message box to be displayed.

    `title`
        The title of the message box. May be None for no title.
    `message`
        The message of the message box. May be None for no message, and may contain tab and newline
        characters.
    `dialogtype`
        One of "ok", "okcancel", "yesno", or "yesnocancel".
    `icon`
        One of "info", "warning", "error", or "question".
    `defaultbutton`
        0 for no/cancel, 1 for ok/yes, 2 for no in "yesnocancel".

    Returns 0 for no/cancel, 1 for ok/yes, 2 for no in "yesnocancel".
    """

    title = encode(title)
    message = encode(message)
    dialogtype = encode(dialogtype)
    icon = encode(icon)


    return tinyfd_messageBox(cstr_or_null(title), cstr_or_null(message), dialogtype, icon, defaultbutton)


def inputBox(title, message, defaultinput=""):
    """
    Displays an inputbox, to prompt for textual input.

    `title`
        The title of the input box. May be None for no title.

    `message`
        The message of the input box. May be none of no message, does not understand
        tab and newline.

    `defaultinput`
        The default input string. If None, a password input is used.

    Returns the input string, or None if the user cancelled the dialog.
    """

    title = encode(title)
    message = encode(message)
    defaultinput = encode(defaultinput)

    cdef char *rv

    rv = tinyfd_inputBox(cstr_or_null(title), cstr_or_null(message), cstr_or_null(defaultinput))

    if rv == NULL:
        return None
    else:
        return rv.decode("utf-8")

def saveFileDialog(title, defaultPathAndFile, filters, singleFilterDescription):
    """
    Displays a save file dialog.

    `title`
        The title of the dialog. May be None for no title.
    `defaultPathAndFile`
        The default path and file name. May be None for no default.
    `filters`
        A list of file filters. Each filter is a list of strings. The first
        string is a description of the filter. The other strings are file
        extensions.
    `singleFilterDescription`
        A description of the single file filter. May be None for no single file filter.

    Returns the path and file name of the selected file, or None if the user cancelled the dialog.
    """

    title = encode(title)
    defaultPathAndFile = encode(defaultPathAndFile)
    singleFilterDescription = encode(singleFilterDescription)

    cdef char *rv

    rv = tinyfd_saveFileDialog(cstr_or_null(title), cstr_or_null(defaultPathAndFile), len(filters), filter_array(filters), cstr_or_null(singleFilterDescription))

    if rv == NULL:
        return None
    else:
        return rv.decode("utf-8")

def openFileDialog(title, defaultPathAndFile, filters, singleFilterDescription, allowMultipleSelects=False):
    """
    Displays a save file dialog.

    `title`
        The title of the dialog. May be None for no title.
    `defaultPathAndFile`
        The default path and file name. May be None for no default.
    `filters`
        A list of file filters. Each filter is a list of strings. The first
        string is a description of the filter. The other strings are file
        extensions.
    `singleFilterDescription`
        A description of the single file filter. May be None for no single file filter.
    `allowMultipleSelects`
        True for allowing multiple file selections.

    Returns a list of the paths and file names of the selected files, or None if the user cancelled the dialog.
    """

    title = encode(title)
    defaultPathAndFile = encode(defaultPathAndFile)
    singleFilterDescription = encode(singleFilterDescription)

    cdef char *rv

    rv = tinyfd_openFileDialog(cstr_or_null(title), cstr_or_null(defaultPathAndFile), len(filters), filter_array(filters), cstr_or_null(singleFilterDescription), allowMultipleSelects)

    if rv == NULL:
        return None
    else:
        return rv.decode("utf-8")

def selectFolderDialog(title, defaultPath):
    """
    Displays a select folder dialog.

    `title`
        The title of the dialog. May be None for no title.
    `defaultPath`
        The default path. May be None for no default.

    Returns None on cancel, otherwise the path of the selected directory.
    """

    title = encode(title)
    defaultPath = encode(defaultPath)

    cdef char *rv

    rv = tinyfd_selectFolderDialog(cstr_or_null(title), cstr_or_null(defaultPath))

    if rv == NULL:
        return None
    else:
        return rv.decode("utf-8")

def colorChooser(title, initialColor=None):
    """
    Displays a color chooser dialog.

    `title`
        The title of the dialog. May be None for no title.
    `initialColor`
        The initial color, a string in the form "#ff0000". May be None for no initial color.

    Returns the selected color, or None if the user cancelled the dialog.
    """

    title = encode(title)
    initialColor = encode(initialColor)

    cdef char *rv
    cdef unsigned char rgb[3]
    rgb[0] = 0
    rgb[1] = 0
    rgb[2] = 0

    rv = tinyfd_colorChooser(cstr_or_null(title), cstr_or_null(initialColor), rgb, rgb)

    if rv == NULL:
        return None
    else:
        return rv.decode("utf-8")
