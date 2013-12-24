from cpython.ref cimport PyObject, Py_INCREF, Py_DECREF

import renpy

################################################################################
# Property Functions
################################################################################

# A property function. The property function is responsible for taking a
# style property, expanding it as necessary, and assigning it to the
# appropriate place(s) in the properties array of the style object.
#
# cache
#     An array of objects representing the values of properties present on
#     the style object. (We will update this cache.)
# cache_priorities
#     An array of priority values the properties were last assigned at. (We
#     update this.)
# priority
#     An offset that is applied to the priority of the property.
# value
#     The value of the style property.
ctypedef void (*property_function)(PyObject **cache, int *cache_priorities, int priority, object value)

# A class that wraps a pointer to a property function.
cdef class PropertyFunctionWrapper:
    cdef property_function function

# A dictionary that maps the name of a property function into a
# PropertyFunctionWrapper.
cdef dict property_functions = { }

cdef void register_property_function(name, property_function function):
    """
    Registers `function` to be the property function called for the
    property `name`.
    """

    cdef PropertyFunctionWrapper pfw

    pfw = PropertyFunctionWrapper()
    pfw.function = function
    property_functions[name] = pfw


cdef inline void assign(int index, PyObject **cache, int *cache_priorities, int priority, PyObject *value):
    """
    Assigns `value` to `index` in `cache`, if it has a higher (or equal) priority than the value
    that is currently in that slot.
    """

    pass

# Utility functions used by the various property functions:

cdef object none_is_null(object o):
    if o is None:
        return renpy.display.layout.Null()
    else:
        return renpy.easy.displayable(o)

cdef object expand_outlines(list l):
    rv = [ ]

    for i in l:
        if len(i) == 2:
            rv.append((i[0], renpy.easy.color(i[1]), 0, 0))
        else:
            rv.append((i[0], renpy.easy.color(i[1]), i[2], i[3]))

    return rv

cdef object expand_anchor(object v):
    # TODO: Properly expand the anchor, perhaps optionally.
    return v

cdef inline object index_0(object v):
    return v[0]

cdef inline object index_1(object v):
    return v[1]

cdef inline object index_2(object v):
    return v[2]

cdef inline object index_3(object v):
    return v[3]

include "stylepropertyfunctions.pxi"
