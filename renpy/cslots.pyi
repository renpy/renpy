# Copyright 2004-2025 Tom Rothamel <pytom@bishoujo.us>
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

class Object:

    linenumber: int
    "If known, the line number of the object in the source file."

    col_offset: int
    "If known, the column offset of the object in the source file."

    _cslot_count: int
    "The number of slots in this class and all of its parents."

    def _compress(self) -> None:
        """
        Compresses the slots of this object.
        """

    def _decompress(self) -> None:
        """
        Decompresses the slots of this object.
        """

    def _kill(self) -> None:
        """
        This 'kills' the object, by removing all references from it to other objects,
        and setting all slots to the default, breaking reference cycles.
        """


class Slot[T]:

    number: int
    "A number assigned to this slot."

    default_value: T
    "The default value of this slot."

    intern: bool
    "If true, the value of this slot should be interned."

    def __init__(self, default_value: T|None=None, intern: bool=False) -> None:
        """
        A slot that stores a value in a CObject.

        `default_value`
            The default value of this slot.

        `intern`
            If true, this slot is a string that should be interned before being assigned
            to the cslot.
        """

    def __get__(self, instance : Object, owner: type) -> T:
        """
        Gets the value of a slot.
        """

    def __set__(self, instance : Object, value: T) -> None:
        """
        Sets the value of a slot.
        """


class IntegerSlot:

    number: int
    "A number assigned to this slot."

    default_value: int
    "The default value of this slot."

    def __init__(self, default_value: int = 0,) -> None:
        """
        A slot that stores a value in a CObject.

        `default_value`
            The default value of this slot.

        """

    def __get__(self, instance : Object, owner: type) -> int:
        """
        Gets the value of a slot.
        """

    def __set__(self, instance : Object, value: int) -> None:
        """
        Sets the value of a slot.
        """
