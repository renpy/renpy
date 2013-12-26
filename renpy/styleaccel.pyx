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

    def __init__(self, **properties):
        self.properties = [ ]
        self.prefix = "insensitive_"
        self.offset = INSENSITIVE_PREFIX

    def __dealloc__(self):

        if self.cache != NULL:
            free(self.cache)

    def setattr(self, property, value): # @ReservedAssignment
        self.properties.append({ property : value })

    def delattr(self, property): # @ReservedAssignment
        for d in self.properties:
            if property in d:
                del d[property]

    def set_prefix(self, prefix):
        """
        Sets the style_prefix to `prefix`.
        """

        if prefix == self.prefix:
            return

        self.prefix = prefix

        if prefix == "insensitive_":
            self.offset = INSENSITIVE_PREFIX
        elif prefix == "idle_":
            self.offset = IDLE_PREFIX
        elif prefix == "hover_":
            self.offset = HOVER_PREFIX
        elif prefix == "selected_insensitive_":
            self.offset = SELECTED_INSENSITIVE_PREFIX
        elif prefix == "selected_idle_":
            self.offset = SELECTED_IDLE_PREFIX
        elif prefix == "selected_hover_":
            self.offset = SELECTED_HOVER_PREFIX

    cpdef _get(StyleCore self, int index):
        """
        Retrieves the property at `index` from this style or its parents.
        """

        index += self.offset

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
