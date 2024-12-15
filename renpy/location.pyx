# Copyright 2004-2024 Tom Rothamel <pytom@bishoujo.us>
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

import sys
import cython

@cython.auto_pickle(False)
cdef class Location:

    # Despite what it looks like, these aren't slots. This just exists to convince reduce_ex to pickle this object
    # as if slots existed.
    __slots__ = [ "filename", "linenumber", "column" ]

    # The filename of the location.
    cdef public str filename

    # The line number of the location.
    cdef public int linenumber

    # The column number of the location.
    cdef public int column

    _types = """
        filename: str
        linenumber: int
        column: int
    """

    def __reduce_ex__(self, protocol):
        return object.__reduce_ex__(self, protocol)

    def __init__(self, filename, linenumber, column=0):
        self.filename = sys.intern(filename)
        self.linenumber = linenumber
        self.column = column
