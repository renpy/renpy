# Copyright 2004-2021 Tom Rothamel <pytom@bishoujo.us>
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
from renpy.compat import *

from renpy import config
from renpy.python import RevertableObject

config.debug_equality = False

class DictEquality(RevertableObject):
    """
    Declares two objects equal if their types are the same, and
    their internal dictionaries are equal.
    """

    def __eq__(self, o):

        try:
            if self is o:
                return True

            if _type(self) is _type(o):
                return (self.__dict__ == o.__dict__)

            return False

        except:
            if config.debug_equality:
                raise

            return False

    def __ne__(self, o):
        return not (self == o)

class FieldEquality(RevertableObject):
    """
    Declares two objects equal if their types are the same, and
    the listed fields are equal.
    """

    # The lists of fields to use.
    equality_fields = [ ]
    identity_fields = [ ]

    def __eq__(self, o):

        try:

            if self is o:
                return True

            if _type(self) is not _type(o):
                return False

            for k in self.equality_fields:
                if self.__dict__[k] != o.__dict__[k]:
                    return False

            for k in self.identity_fields:
                if self.__dict__[k] is not o.__dict__[k]:
                    return False

            return True

        except:

            if config.debug_equality:
                raise

            return False

    def __ne__(self, o):
        return not (self == o)
