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

from __future__ import print_function


cdef inline int letterlike(Py_UNICODE c):
    if u'a' <= c <= u'z':
        return 1

    if u'A' <= c <= u'Z':
        return 1

    if u'0' <= c <= u'9':
        return 1

    if u'_' == c:
        return 1

    return 0


def match_logical_word(unicode s, int pos):

    cdef int start = pos
    cdef int len_s = len(s)
    cdef Py_UNICODE c = s[pos]

    if c == u' ':

        pos += 1

        while pos < len_s:
            if not (s[pos] == u' '):
                break

            pos += 1

    elif letterlike(c):

        pos += 1

        while pos < len_s:
            if not letterlike(s[pos]):
                break

            pos += 1

    else:

        pos += 1

    word = s[start:pos]

    if (pos - start) >= 3 and (word[0] == u'_') and (word[1] == u'_'):
        magic = True
    else:
        magic = False


    return s[start:pos], magic, pos
