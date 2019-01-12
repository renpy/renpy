#!/usr/bin/env python

# Copyright 2004-2019 Tom Rothamel <pytom@bishoujo.us>
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

# Python3 and Python2-style imports.
try:
    from tkinter import Tk
    from tkinter.filedialog import askdirectory
except ImportError:
    from Tkinter import Tk
    from tkFileDialog import askdirectory

# Binary mode stdout for python3.
try:
    sys.stdout = sys.stdout.buffer
except:
    pass

# Create the TK canvas.

if __name__ == "__main__":
    root = Tk()
    root.withdraw()

    result = askdirectory(initialdir=sys.argv[1], parent=root, title="Select Ren'Py Projects Directory")

    if result == ():
        result = ""

    sys.stdout.write(result.encode("utf8"))
