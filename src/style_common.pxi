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

import renpy

from renpy.style cimport register_property_function, assign, assign_prefixed
from cpython.ref cimport PyObject

from renpy.styledata.styleutil import none_is_null, none_is_0, expand_focus_mask, expand_outlines, expand_anchor

cdef inline object index_0(object v):
    return v[0]

cdef inline object index_1(object v):
    return v[1]

cdef inline object index_2(object v):
    return v[2]

cdef inline object index_3(object v):
    return v[3]

cdef inline object index_2_or_0(object v):
    if len(v) >= 3:
        return v[2]
    else:
        return v[0]

cdef inline object index_3_or_1(object v):
    if len(v) >= 4:
        return v[3]
    else:
        return v[1]
