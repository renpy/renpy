# Copyright 2004-2014 Tom Rothamel <pytom@bishoujo.us>
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

from renpy.python import RevertableList as __renpy__list__
list = __renpy__list__ #@ReservedAssignment

from renpy.python import RevertableDict as __renpy__dict__
dict = __renpy__dict__ #@ReservedAssignment

from renpy.python import RevertableSet as set
Set = set

from renpy.python import RevertableObject as object #@UnusedImport

from renpy.python import revertable_range as range #@UnusedImport
from renpy.python import revertable_sorted as sorted #@UnusedImport

import renpy.ui as ui #@UnusedImport
import renpy.exports as renpy #@Reimport @UnusedImport
from renpy.translation import translate_string as __ # @UnusedImport

def _(s):
    """
    :undocumented: Documented directly in the .rst.

    Flags a string as translatable, and returns it immediately. The string
    will be translated when text displays it.
    """

    return s

