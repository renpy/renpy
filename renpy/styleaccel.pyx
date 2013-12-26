from cpython.ref cimport PyObject
from libc.string cimport memset
from libc.stdlib cimport calloc, free

import renpy

include "styleconstants.pxi"

################################################################################
# Property Functions
################################################################################

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


cdef class StyleCore:
#
#     # True if this style has been built, False otherwise.
#     cdef bint built
#
#     # A list of dictionaries mapping properties to
#     cdef public list properties
#
#     # This is a map from prefixed style property to its value, or NULL if
#     # the prefixed style property is not defined by this style.
#     #
#     # Each prefix and style property are given an index, using the formula
#     # (prefix_index * STYLE_PROPERTY_COUNT) + style_property_index
#     #
#     # Note: We cheat the reference counting on this cache. Since we know
#     # that every object has a positive reference count because it's in properties,
#     # we don't increment the reference count while it's in the cache.
#     cdef PyObject **cache

    def __init__(self, **properties):
        self.properties = [ ]

    def __dealloc__(self):

        if self.cache != NULL:
            free(self.cache)

    def setattr(self, property, value): # @ReservedAssignment
        self.properties.append({ property : value })

    def delattr(self, property): # @ReservedAssignment
        for d in self.properties:
            if property in d:
                del d[property]

    cpdef _get(StyleCore self, int index):
        """
        Retrieves the property at `index` from this style or its parents.
        """

        if not self.built:
            build_style(self)

        cdef PyObject *o

        o = self.cache[index]

        if o == NULL:
            return None

        return <object> o

from renpy.styleclass import Style

cpdef build_style(StyleCore s):

    if s.built:
        return

    s.built = True

    # Build the properties cache.
    if not s.properties:
        s.cache = NULL
        return

    cdef int cache_priorities[PREFIX_COUNT * STYLE_PROPERTY_COUNT]
    cdef dict d
    cdef PropertyFunctionWrapper pfw

    memset(cache_priorities, 0, sizeof(int) * PREFIX_COUNT * STYLE_PROPERTY_COUNT)

    s.cache = <PyObject **> calloc(PREFIX_COUNT * STYLE_PROPERTY_COUNT, sizeof(PyObject *))

    priority = 1

    for d in s.properties:
        for k, v in d.items():
            pfw = property_functions.get(k, None)

            if pfw is None:
                print "Warning:", k,
                continue

            pfw.function(s.cache, cache_priorities, priority, v)

        priority += PRIORITY_LEVELS

cpdef unbuild_style(StyleCore s):

    if not s.built:
        return

    if s.cache != NULL:
        free(s.cache)
        s.cache = NULL

    s.built = False
