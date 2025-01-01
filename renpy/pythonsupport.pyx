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

cdef union UCS4:
    Py_UCS4 u
    unsigned char c[4]

def hash_fnv1a(unicode s):
    """
    FNV-1a hash function.

    This computes a stable 32-bit hash of the unicode string (s).
    """

    cdef unsigned int rv = 0x811c9dc5
    cdef UCS4 codepoint

    for codepoint.u in s:
        rv ^= codepoint.c[0]
        rv *= 0x01000193

        rv ^= codepoint.c[1]
        rv *= 0x01000193

        rv ^= codepoint.c[2]
        rv *= 0x01000193

        rv ^= codepoint.c[3]
        rv *= 0x01000193

    return rv
