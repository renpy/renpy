# Copyright 2004-2018 Tom Rothamel <pytom@bishoujo.us>
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

python_list = _list = list
python_dict = _dict = dict
python_object = _object = object
python_set = _set = set

_type = type

from renpy.python import RevertableList as __renpy__list__
list = __renpy__list__  # @ReservedAssignment

from renpy.python import RevertableDict as __renpy__dict__
dict = __renpy__dict__  # @ReservedAssignment

from renpy.python import RevertableSet as __renpy__set__
set = __renpy__set__  # @ReservedAssignment
Set = __renpy__set__

from renpy.python import RevertableObject as object  # @UnusedImport

from renpy.python import revertable_range as range  # @UnusedImport
from renpy.python import revertable_sorted as sorted  # @UnusedImport

import renpy.ui as ui  # @UnusedImport
import renpy.exports as renpy  # @Reimport @UnusedImport
from renpy.translation import translate_string as __  # @UnusedImport


def _(s):
    """
    :undocumented: Documented directly in the .rst.

    Flags a string as translatable, and returns it immediately. The string
    will be translated when displayed by the text displayable.
    """

    return s


def _p(s):
    '''
    :doc: underscore_p
    :name: _p

    Reformats a string and flags it as translatable. The string will be
    translated when displayed by the text displayable. This is intended
    to define multi-line for use in strings, of the form::

        define config.about = _p("""
            These two lines will be combined together
            to form a long line.

            This line will be separate.
            """)

    The reformatting is done by breaking the text up into lines,
    removing whitespace from the start and end of each line. Blank lines
    are removed at the end. When there is a blank line, a blank line is
    inserted to separate paragraphs. The {p} tag breaks a line, but
    doesn't add a blank one.

    This can be used in a string translation, using the construct::

        old "These two lines will be combined together to form a long line.\\n\\nThis line will be separate."
        new _p("""
            These two lines will be combined together
            to form a long line. Bork bork bork.

            This line will be separate. Bork bork bork.
            """)
    '''

    import re

    lines = [ i.strip() for i in s.split("\n") ]

    if lines and not lines[0]:
        lines.pop(0)

    if lines and not lines[-1]:
        lines.pop()

    rv = ""
    para = [ ]

    for l in lines:
        if not l:
            rv += " ".join(para) + "\n\n"
            para = [ ]
        elif re.search(r'\{p[^}]*\}$', l):
            para.append(l)
            rv += " ".join(para)
            para = [ ]
        else:
            para.append(l)

    rv += " ".join(para)
    return rv
