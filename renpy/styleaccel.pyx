from cpython.ref cimport PyObject
from libc.string cimport memset
from libc.stdlib cimport calloc, free

import renpy

include "styleconstants.pxi"

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
ctypedef int (*property_function)(PyObject **cache, int *cache_priorities, int priority, object value) except -1

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

    if priority < cache_priorities[index]:
        return

    cache[index] = value
    cache_priorities[index] = priority


# Utility functions used by the various property functions:

def none_is_null(o):
    if o is None:
        return renpy.display.layout.Null()
    else:
        return renpy.easy.displayable(o)

def expand_outlines(list l):
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


cdef class StyleCore:

    # True if this style has been built, False otherwise.
    cdef bint built

    # A list of dictionaries mapping properties to
    cdef public list properties

    # This is a map from prefixed style property to its value, or NULL if
    # the prefixed style property is not defined by this style.
    #
    # Each prefix and style property are given an index, using the formula
    # (prefix_index * STYLE_PROPERTY_COUNT) + style_property_index
    #
    # Note: We cheat the reference counting on this cache. Since we know
    # that every object has a positive reference count because it's in properties,
    # we don't increment the reference count while it's in the cache.
    cdef PyObject **cache

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

include "styleproperties.pxi"

cpdef get(StyleCore s, int index):
    """
    Retrieves the property at `index` from `s` and its parents.
    """

    if not s.built:
        build_style(s)

    cdef PyObject *o

    o = s.cache[index]

    if o == NULL:
        return None

    return <object> o


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
