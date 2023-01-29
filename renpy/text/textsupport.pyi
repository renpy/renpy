# Copyright 2004-2022 Tom Rothamel <pytom@bishoujo.us>
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

from __future__ import annotations


TEXT = 1
TAG = 2
PARAGRAPH = 3
DISPLAYABLE = 4


def language_tailor(chars: str, cls: str) -> None:
    """
    :doc: other

    This can be used to override the line breaking class of a unicode
    character. For
    example, the linebreaking class of a character can be set to ID to
    treat it as an ideograph, which allows breaks before and after that
    character.

    `chars`
        A string containing each of the characters to tailor.

    `cls`
        A string giving a character class. This should be one of the classes defined in Table
        1 of `UAX #14: Unicode Line Breaking Algorithm <http://www.unicode.org/reports/tr14/tr14-30.html>`_.
    """
