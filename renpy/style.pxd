#@PydevCodeAnalysisIgnore
from cpython.ref cimport PyObject, Py_XINCREF, Py_XDECREF

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

cdef inline void assign(int index, PyObject **cache, int *cache_priorities, int priority, PyObject *value):
    """
    Assigns `value` to `index` in `cache`, if it has a higher (or equal) priority than the value
    that is currently in that slot.
    """

    if priority < cache_priorities[index]:
        return

    Py_XDECREF(cache[index])
    Py_XINCREF(value)

    cache[index] = value
    cache_priorities[index] = priority

cdef void register_property_function(name, property_function function)

cdef class StyleCore:

    ############################################################## Public Fields

    # The name of this style, a tuple of strings.
    cdef public object name

    # The parent of this style, a tuple of strings.
    cdef public object parent

    # A list of dictionaries mapping properties to values. The later items
    # in this list override eariler ones.
    cdef public list properties

    # The style prefix that accesses to unprefixed styles will use.
    cdef public object prefix

    # The help for the style object.
    cdef public object help

    ############################################################# Private Fields

    # True if this style has been built, False otherwise.
    cdef bint built

    # References to the down and left parents, or None if we do nothave one.
    #
    # The down parent uses inheritance, while the left parent uses less style
    # indexing. For example, if style.mybutton inherits from style.button, and
    # self is style.mybutton['Quit']
    #
    # self.down_parent is style.button['Quit']
    # self.left_parent is style.mybutton
    cdef StyleCore down_parent
    cdef StyleCore left_parent

    # This is a map from prefixed style property to its value, or NULL if
    # the prefixed style property is not defined by this style.
    #
    # Each prefix and style property are given an index, using the formula
    # (prefix_index * STYLE_PROPERTY_COUNT) + style_property_index
    cdef PyObject **cache

    # The offset in the cache corresponding to self.prefix.
    cdef int offset

    #################################################################### Methods

    cpdef _get(StyleCore self, int)


