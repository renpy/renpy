from style cimport register_property_function, StyleCore, assign
from cpython.ref cimport PyObject

# Utility functions used by the various property functions:

import renpy

def none_is_null(o):
    if o is None:
        return renpy.display.layout.Null()
    else:
        return renpy.easy.displayable(o)

def expand_outlines(l):
    rv = [ ]

    for i in l:
        if len(i) == 2:
            rv.append((i[0], renpy.easy.color(i[1]), 0, 0))
        else:
            rv.append((i[0], renpy.easy.color(i[1]), i[2], i[3]))

    return rv

# Names for anchors.
ANCHORS = dict(
    left=0.0,
    right=1.0,
    center=0.5,
    top=0.0,
    bottom=1.0,
    )

def expand_anchor(v):
    """
    Turns an anchor into a number.
    """

    try:
        return ANCHORS.get(v, v)
    except:
        # This fixes some bugs in very old Ren'Pys.

        for n in ANCHORS:
            o = getattr(renpy.store, n, None)
            if o is None:
                continue

            if v is o:
                return ANCHORS[n]

        raise

cdef inline object index_0(object v):
    return v[0]

cdef inline object index_1(object v):
    return v[1]

cdef inline object index_2(object v):
    return v[2]

cdef inline object index_3(object v):
    return v[3]

include "stylepropertyfunctions.pxi"
include "styleproperties.pxi"
include "stylesets.pxi"
