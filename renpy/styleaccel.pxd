from cpython.ref cimport PyObject

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

    cache[index] = value
    cache_priorities[index] = priority

cdef void register_property_function(name, property_function function)

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

    cpdef _get(StyleCore self, int)
