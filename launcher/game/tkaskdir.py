#!/usr/bin/env python

# Copyright 2004-2021 Tom Rothamel <pytom@bishoujo.us>
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

# This is used on Linux and Mac to prompt the user for the projects
# directory.

import sys


# Gtk generally has better support than TKinter on various Linux distributions
def gtk_select_directory(title):
    dialog = Gtk.FileChooserNative(title=title,
                                   action=Gtk.FileChooserAction.SELECT_FOLDER)

    dialog.run()

    return dialog.get_filename()


# Fall back to TKinter if Gtk isn't available
def tk_select_directory(initialdir, title):
    root = Tk()
    root.withdraw()

    return askdirectory(initialdir=initialdir, parent=root, title=title)


try:
    import gi
    gi.require_version('Gtk', '3.0')
    from gi.repository import Gtk

    def select_directory(title):
        result = gtk_select_directory(title)

        return result if result else ''

except:
# Python3 and Python2-style imports.
    try:
        from tkinter import Tk
        from tkinter.filedialog import askdirectory
    except ImportError:
        from Tkinter import Tk
        from tkFileDialog import askdirectory

    def select_directory(title):
        return tk_select_directory(title, sys.argv[1])

if __name__ == '__main__':
    directory = select_directory('Select Ren\'Py Projects Directory')

    sys.stdout.write(directory)
