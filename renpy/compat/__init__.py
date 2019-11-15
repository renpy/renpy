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

"""
This module is defined to allow us to program in Python 2 with a high degree
of compatibility with Python 3, and vice versa. It's intended to be invoked
with the following preamble::

    from __future__ import division, absolute_import, with_statement, print_function, unicode_literals
    from renpy.compat import *

Right now, it does the following things:

* Sets up aliases for Python 3 module moves, allowing the Python 3 names
  to be used in Python 2.

* Defines PY2 in the current context, to make Python 2 conditional.

* Replaces open with a function that mimics the Python 3 behavior, of
  opening files in a unicode-friendly mode by default.

* Redefines the text types, so that str is always the unicode type, and
  basestring is the list of string types available on the system.

* Changes the meaning of the .items(), .keys(), and .values() methods of
  dict to return views, rather than lists. (This is a fairly major change,
  and so is only available when with_statement and division are both
  imported.

* Aliases xrange to range on Python 2.
"""

from __future__ import division, absolute_import, with_statement, print_function, unicode_literals

import renpy
renpy.update_path()

import future.standard_library
import future.utils

################################################################################
# Alias the Python 3 standard library.

future.standard_library.install_aliases()

################################################################################
# Determine if this is Python2.

PY2 = future.utils.PY2

################################################################################
# Make open mimic Python 3.

from future.builtins import open

################################################################################
# Text types.

basestring = future.utils.string_types  # @ReservedAssignment
str = future.utils.text_type  # @ReservedAssignment

################################################################################
# Dictionary views.

# The try block solves a chicken-and-egg problem when dictviews is not
# compiled yet, as part of the Ren'Py build process.
try:
    if PY2:
        import renpy.compat.dictviews  # @UnresolvedImport
except ImportError:
    import sys
    print("Could not import renpy.compat.dictviews.", file=sys.stderr)

################################################################################
# Range.

range = xrange  # @ReservedAssignment

__all__ = [ "PY2", "open", "basestring", "str", "range" ]

if PY2:
    __all__ = [ bytes(i) for i in __all__ ]
