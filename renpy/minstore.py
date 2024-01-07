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

from __future__ import division, absolute_import, with_statement, print_function, unicode_literals
from renpy.compat import PY2, basestring, bchr, bord, chr, open, pystr, range, round, str, tobytes, unicode # *


xrange = range

unicode = str # @ReservedAssignment

python_list = _list = list
python_dict = _dict = dict
python_object = _object = object # type: ignore
python_set = _set = set

_type = type

from renpy.revertable import RevertableList as __renpy__list__
list = __renpy__list__ # @ReservedAssignment

from renpy.revertable import RevertableDict as __renpy__dict__
dict = __renpy__dict__ # @ReservedAssignment

from renpy.revertable import RevertableDefaultDict as __renpy_defaultdict__
defaultdict = __renpy_defaultdict__

from renpy.revertable import RevertableSet as __renpy__set__
set = __renpy__set__ # @ReservedAssignment
Set = __renpy__set__

from renpy.revertable import RevertableObject as object # @UnusedImport

from renpy.revertable import revertable_range as range # @UnusedImport
from renpy.revertable import revertable_sorted as sorted # @UnusedImport

from renpy.revertable import MultiRevertable

import renpy.ui as ui # @UnusedImport
from renpy.translation import translate_string as __ # @UnusedImport

from renpy.python import store_eval as eval

from renpy.display.core import absolute
from renpy.atl import position

import renpy
globals()["renpy"] = renpy.exports

_print = print


def print(*args, **kwargs):
    """
    :undocumented:

    This is a variant of the print function that forces a checkpoint
    at the start of the next statement, so that it can't be rolled past.
    """

    renpy.game.context().force_checkpoint = True # type: ignore
    _print(*args, **kwargs)


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

        define gui.about = _p("""
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

def input(*args, **kwargs):
    """
    :undocumented:
    """

    raise Exception("The Python input and raw_input functions do not work with Ren'Py. Please use the renpy.input function instead.")

raw_input = input


__all__ = [
    'PY2',
    'Set',
    '_',
    '__',
    '__renpy__dict__',
    '__renpy__list__',
    '__renpy__set__',
    '_dict',
    '_list',
    '_object',
    '_p',
    '_print',
    '_set',
    '_type',
    'absolute',
    'basestring',
    'bchr',
    'bord',
    'dict',
    'eval',
    'input',
    'list',
    'object',
    'open',
    'position',
    'print',
    'python_dict',
    'python_list',
    'python_object',
    'python_set',
    'range',
    'raw_input',
    'set',
    'sorted',
    'str',
    'tobytes',
    'ui',
    'unicode',
]

if PY2:
    __all__ = [ bytes(i) for i in __all__ ] # type: ignore
