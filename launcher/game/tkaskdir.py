#!/usr/bin/env python

# Copyright 2004-2012 Tom Rothamel <pytom@bishoujo.us>
# See LICENSE.txt for license details.

# This is used on Linux and Mac to prompt the user for the projects 
# directory.

import sys

# Python3 and Python2-style imports.
try:
    from tkinter import Tk
    from tkinter.filedialog import askdirectory
except ImportError:
    from Tkinter import Tk
    from tkFileDialog import askdirectory

# Create the TK canvas.

if __name__ == "__main__":   
    root = Tk()
    root.withdraw()

    result = askdirectory(initialdir=sys.argv[1], parent=root, title="Select Ren'Py Projects Directory")
    sys.stdout.write(result)