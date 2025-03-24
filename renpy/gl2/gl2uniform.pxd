#cython: profile=False
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

from renpy.uguu.gl cimport *
from renpy.gl2.gl2draw cimport GL2DrawingContext
from renpy.gl2.gl2model cimport GL2Model

cdef class Getter:
    """
    Subclasses of this class are responsioble for getting uniform data.
    """

    cdef str uniform_name
    "The name of the uniform."

    cdef object get(self, GL2DrawingContext context, GL2Model model)


cdef class Setter:
    """
    Subclasses of this class are responsible for setting unforms of a
    given type.
    """

    cdef str uniform_name
    "The name of the uniform."

    cdef str uniform_type
    "The type of the uniform."

    cdef GLint location
    "The location the uniform is stored in."

    cdef Getter getter
    "The getter that's used to get the data for this uniform."

    cdef object set(self, GL2DrawingContext context, value)
