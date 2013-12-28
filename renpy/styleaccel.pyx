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


################################################################################
# Style Management
################################################################################


# A map from style name (a tuple) to the style object with that name.
styles = { }

cpdef get_style(name):
    """
    Gets the style with `name`, which must be a string.

    If the style doesn't exist, and it contains an underscore in it, creates
    a new style that has as a parent the part after the first underscore, if
    a parent with that name exists.
    """

    nametuple = (name,)

    rv = styles.get(nametuple, None)
    if rv is not None:
        return rv

    _start, _mid, end = name.partition("_")

    if not end:
        raise Exception("Style %r does not exist." % name)

    try:
        parent = get_style(end)
    except:
        raise Exception("Style %r does not exist." % name)

    rv = Style(parent, name=nametuple)
    styles[nametuple] = rv
    return rv

cpdef get_full_style(name):
    """
    Gets the style with `name`, which must be a tuple.
    """

    rv = styles.get(name, None)
    if rv is not None:
        return rv

    rv = get_style(name[0])

    for i in name[1:]:
        rv = name[i]

    return rv


class StyleManager(object):
    """
    The object exported as style in the store.
    """

    def __setattr__(self, name, value):

        if not isinstance(value, StyleCore):
            raise Exception("Value is not a style.")

        name = (name,)
        value.name = name
        styles[name] = value

    __setitem__ = setattr

    def __getattr__(self, name):
        return get_style(name)

    __getitem__ = getattr

    def create(self, name, parent, description=None):
        """
        Deprecated way of creating styles.
        """

        s = Style(parent,help=description)
        self[name] = s

    def rebuild(self):
        renpy.style.rebuild()

    def exists(self, name):
        """
        Returns `true` if name is a style.
        """

        return (name in styles) or ((name,) in styles)

    def get(self, name):
        """
        Gets a style, which may be a name or a tuple.
        """

        if isinstance(name, tuple):
            return get_full_style(name)
        else:
            return get_style(name)


################################################################################
# Style Class
################################################################################

cdef class StyleCore:

    def __init__(self, parent, properties=None, name=None, help=None):
        self.prefix = "insensitive_"
        self.offset = INSENSITIVE_PREFIX

        if properties:
            self.properties.append(properties)

        self.properties = [ ]

        if isinstance(parent, StyleCore):
            self.parent = parent.name
        elif isinstance(parent, tuple):
            self.parent = parent
        elif parent is None:
            self.parent = parent
        else:
            self.parent = (parent,)

        self.name = name

        self.help = help

    def __dealloc__(self):

        if self.cache != NULL:
            free(self.cache)

    def __repr__(self):
        return "<{} parent={}>".format(self.name, self.parent)

    def __getitem__(self, name):
        tname = self.name + (name,)

        rv = styles.get(tname, None)
        if rv is not None:
            return rv

        if self.parent is not None:
            parent = self.parent + (name,)
        else:
            parent = None

        rv = Style(parent, name=tname)
        styles[tname] = rv
        return rv

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

    # Find our parents.
    if s.parent is not None:
        s.down_parent = get_full_style(s.parent)
        build_style(s.down_parent)

    if s.name is not None and len(s.name) > 1:
        s.left_parent = get_full_style(s.name[:-1])
        build_style(s.left_parent)

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

def build_styles():
    """
    Builds or rebuilds all styles.
    """

    for s in styles.values():
        unbuild_style(s)

    for s in styles.values():
        build_style(s)

cpdef unbuild_style(StyleCore s):

    if not s.built:
        return

    if s.cache != NULL:
        free(s.cache)
        s.cache = NULL

    s.left_parent = None
    s.down_parent = None

    s.built = False
