# Copyright 2004-2020 Tom Rothamel <pytom@bishoujo.us>
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

from __future__ import print_function, unicode_literals

from cpython.ref cimport PyObject, Py_XDECREF
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

    start, _mid, end = name.partition("_")

    if not end:
        raise Exception("Style %r does not exist." % name)

    # Deal with inheritance of styles beginning with _ a bit specially,
    # so _foo_bar inherits from _bar, not bar.
    if not start:
        _start, _mid, end = name[1:].partition("_")

        if not end:
            raise Exception("Style %r does not exist." % name)

        end = "_" + end

    try:
        parent = get_style(end)
    except:
        raise Exception("Style %r does not exist." % name)

    rv = Style(parent, name=nametuple)
    styles[nametuple] = rv
    return rv

cpdef get_or_create_style(name):
    """
    Like get_style, but if the style doesn't exist, its hierarchy is created,
    eventually inheriting from default.
    """

    nametuple = (name,)

    rv = styles.get(nametuple, None)
    if rv is not None:
        return rv

    start, _mid, end = name.partition("_")

    # We need both sides of the _, as we don't want to have
    # _foo auto-inherit from foo.
    if not start or not end:
        rv = Style("default", name=nametuple)
        styles[nametuple] = rv
        return rv

    parent = get_or_create_style(end)

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
        rv = rv[i]

    return rv


cpdef get_tuple_name(s):
    """
    Gets the tuple name of a style, where `s` may be a tuple, Style, or string.

    If `s` is None, returns None.
    """

    if isinstance(s, StyleCore):
        return s.name
    elif isinstance(s, tuple):
        return s
    elif s is None:
        return s
    else:
        return (s,)


def get_text_style(style, default):
    """
    If style exists, returns `style` + "_text". Otherwise, returns `default`.
    For indexed styles, the above is applied first, and then indexing is applied.
    """

    if style is None:
        style = default

    style = get_tuple_name(style)

    start = style[0]
    rest = style[1:]

    rv = get_full_style((start + "_text",))

    for i in rest:
        rv = rv[i]

    return rv


class StyleManager(object):
    """
    The object exported as style in the store.
    """

    def __setattr__(self, name, value):

        if not isinstance(value, StyleCore):

            if getattr(value, "_is_style_compat", False):
                self.__dict__[name] = value
                return

            raise Exception("Value is not a style.")

        cdef StyleCore style = value

        name = (name,)

        if style.name is None:
            style.name = name

        styles[name] = value

    __setitem__ = __setattr__

    def __getattr__(self, name):
        return get_style(name)

    __getitem__ = __getattr__

    def create(self, name, parent, description=None):
        """
        Deprecated way of creating styles.
        """

        s = Style(parent, help=description)
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

def style_name_to_string(name):

    if name is None:
        return "anonymous style"

    rv = "style " + name[0]

    for i in name[1:]:
        rv += "['{}']".format(i)

    return rv

cdef class StyleCore:

    def __init__(self, parent, properties=None, name=None, help=None, heavy=True):
        """
        `parent`
            The parent of this style. One of:

            * A Style object.
            * A string giving the name of a style.
            * A tuple giving the name of an indexed style.
            * None, to indicate there is no parent.

        `properties`
            A map from style property to its value.

        `name`
            If given, a tuple that will be the name of this style.

        `help`
            Help information for this style.

        `heavy`
            Ignored, but retained for compatibility.
        """

        self.prefix = "insensitive_"
        self.prefix_offset = INSENSITIVE_PREFIX

        self.properties = [ ]

        if properties:
            if not type(properties) is dict:
                properties = dict(properties)

            self.properties.append(properties)

        if properties and ("insensitive_child" in properties):
            if properties["insensitive_child"] is False:
                import traceback
                traceback.print_stack()

        self.parent = get_tuple_name(parent)
        self.name = name
        self.help = help

    def copy(self):
        cdef StyleCore rv

        rv = Style(self.parent)
        rv.properties = list(self.properties)
        return rv

    def __richcmp__(self, o, int op):
        if self is o:
            eq = True
        elif type(self) != type(o):
            eq = False
        elif self.parent != o.parent:
            eq = False
        elif self.name != o.name:
            eq = False
        elif self.properties != o.properties:
            eq = False
        else:
            eq = True

        if op == 2: # ==
            return eq
        elif op == 3: # !=
            return not eq
        else:
            return NotImplemented

    def __dealloc__(self):
        unbuild_style(self)

    def __getstate__(self):

        rv = dict(
            properties=self.properties,
            prefix=self.prefix,
            name=self.name,
            parent=self.parent)

        return rv

    def __setstate__(self, state):

        self.properties = state["properties"]
        self.name = state["name"]
        self.set_parent(state["parent"])
        self.set_prefix(state["prefix"])

    def __repr__(self):
        if self.parent:
            return "<{} is {} @ {}>".format(style_name_to_string(self.name), style_name_to_string(self.parent), hex(id(self)))
        else:
            return "<{} @ {}>".format(style_name_to_string(self.name), hex(id(self)))

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

    def __setattr__(self, name, value):
        if name not in prefixed_all_properties:
            raise Exception("Style property {} is not known.".format(name))
        self.properties.append({ name : value })

    def __delattr__(self, name):
        self.delattr(name)

    def set_parent(self, parent):
        self.parent = get_tuple_name(parent)

    def clear(self):
        self.properties = [ ]

    def take(self, other):
        """
        Takes the style properties from `other`, which may be a style name
        string or a style object.
        """

        if not isinstance(other, StyleCore):
            other = get_style(other)

        self.properties = copy_properties(other.properties)

    def setdefault(self, **properties):
        """
        This sets the default value of the given properties, if no more
        explicit values have been set.
        """

        for p in self.properties:
            for k in p:
                if k in properties:
                    del properties[k]

        if properties:
            self.properties.append(properties)

    def add_properties(self, properties):
        """
        Adds the properties (which must be a dict) to this style.
        """

        self.properties.append(dict(properties))

    def set_prefix(self, prefix):
        """
        Sets the style_prefix to `prefix`.
        """

        if prefix == self.prefix:
            return

        self.prefix = prefix

        if prefix == "insensitive_":
            self.prefix_offset = INSENSITIVE_PREFIX
        elif prefix == "idle_":
            self.prefix_offset = IDLE_PREFIX
        elif prefix == "hover_":
            self.prefix_offset = HOVER_PREFIX
        elif prefix == "selected_insensitive_":
            self.prefix_offset = SELECTED_INSENSITIVE_PREFIX
        elif prefix == "selected_idle_":
            self.prefix_offset = SELECTED_IDLE_PREFIX
        elif prefix == "selected_hover_":
            self.prefix_offset = SELECTED_HOVER_PREFIX

    def get_offset(self):
        return self.prefix_offset

    def get_placement(self):
        """
        Returns a tuple giving the placement of the object.
        """
        return (
            self._get(XPOS_INDEX),
            self._get(YPOS_INDEX),
            self._get(XANCHOR_INDEX),
            self._get(YANCHOR_INDEX),
            self._get(XOFFSET_INDEX),
            self._get(YOFFSET_INDEX),
            self._get(SUBPIXEL_INDEX),
            )

    cpdef _get(StyleCore self, int index):
        """
        Retrieves the property at `index` from this style or its parents.
        """

        cdef PyObject *o

        # The current style object we're looking at.
        cdef StyleCore s

        # The style object we'll backtrack to when s has no down-parent.
        cdef StyleCore left

        # A limit to the number of styles we'll consider.
        cdef int limit

        index += self.prefix_offset

        if not self.built:
            build_style(self)

        s = self
        left = None
        limit = 100

        while limit > 0:

            # If we have the style, return it.
            if s.cache != NULL:
                o = s.cache[index]
                if o != NULL:
                    return <object> o

            # If there is no left-parent, and we have one, store it.
            if left is None and s.left_parent is not None:
                left = s.left_parent

            s = s.down_parent

            # If no down-parent, try left.
            if s is None:
                s = left
                left = None

            # If no down-parent or left-parent, default to None.
            if s is None:
                return None

            limit -= 1

        raise Exception("{} is too complex. Check for loops in style inheritance.".format(self))


    cpdef _get_unoffset(self, int index):
        return self._get(index - self.prefix_offset)


    def _visit_window(self, pd):
        """
        Predicts properties for a window.

        `pd`
            The function that should be called to predict a displayable.
        """

        for i in [ INSENSITIVE_PREFIX, IDLE_PREFIX, HOVER_PREFIX, SELECTED_INSENSITIVE_PREFIX, SELECTED_IDLE_PREFIX, SELECTED_HOVER_PREFIX ]:
            for j in [ BACKGROUND_INDEX, CHILD_INDEX, FOREGROUND_INDEX ]:
                v = self._get_unoffset(i + j)
                if v is not None:
                    pd(v)

    def _visit_bar(self, pd):
        """
        Predicts properties for a window.

        `pd`
            The function that should be called to predict a displayable.
        """

        for i in [ INSENSITIVE_PREFIX, IDLE_PREFIX, HOVER_PREFIX, SELECTED_INSENSITIVE_PREFIX, SELECTED_IDLE_PREFIX, SELECTED_HOVER_PREFIX ]:
            for j in [ FORE_BAR_INDEX, AFT_BAR_INDEX, THUMB_INDEX, THUMB_SHADOW_INDEX ]:
                v = self._get_unoffset(i + j)
                if v is not None:
                    pd(v)

    def _visit_frame(self, pd):
        """
        Predicts properties for a Frame.

        `pd`
            The function that should be called to predict a displayable.
        """

        for i in [ INSENSITIVE_PREFIX, IDLE_PREFIX, HOVER_PREFIX, SELECTED_INSENSITIVE_PREFIX, SELECTED_IDLE_PREFIX, SELECTED_HOVER_PREFIX ]:
            for j in [ CHILD_INDEX ]:
                v = self._get_unoffset(i + j)
                if v is not None:
                    pd(v)

    def inspect(StyleCore self):
        """
        Inspects this style.

        Returns a list of (name, properties) pairs for each style, with only
        properties that affect the final result being in the properties
        list. Properties is a map from property name to value.
        """

        cdef StyleCore s
        cdef StyleCore left

        init_inspect()

        if not self.built:
            build_style(self)

        rv = [ ]

        # Affected properties that we've seen already.
        seen_properties = set()

        def inspect_one(s):

            my_properties = { }

            for pdict in reversed(s.properties):

                propnames = list(pdict)
                propnames.sort(key=lambda pn : priority.get(pn, 100))
                propnames.reverse()

                for propname in propnames:
                    prop_affects = affects.get(propname, [ ])

                    for a in prop_affects:
                        if a not in seen_properties:
                            break
                    else:
                        continue

                    for a in prop_affects:
                        seen_properties.add(a)

                    my_properties[propname] = pdict[propname]

            rv.append((s.name, my_properties))

        s = self
        left = None

        while True:

            inspect_one(s)

            # If there is no left-parent, and we have one, store it.
            if left is None and s.left_parent is not None:
                left = s.left_parent

            s = s.down_parent

            # If no down-parent, try left.
            if s is None:
                s = left
                left = None

            # If no down-parent or left-parent, default to None.
            if s is None:
                break

        return rv


# This will be replaced when renpy.styledata.import_style_functions is called.
Style = StyleCore

from renpy.styledata.stylesets import all_properties, prefix_priority, prefix_alts, property_priority

# The set of all prefixed properties we know about.
prefixed_all_properties = {
    prefix + propname
    for prefix in prefix_priority
    for propname in all_properties
    }

################################################################################
# Building
################################################################################

cpdef build_style(StyleCore s):
    cdef int cache_priorities[PREFIX_COUNT * STYLE_PROPERTY_COUNT]
    cdef dict d
    cdef PropertyFunctionWrapper pfw

    if s.built:
        return

    if s.building and s.name:
        raise Exception("{} is part of a loop of recursive styles (is one of its own parents).".format(style_name_to_string(s.name)))

    s.building = True

    try:

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

        memset(cache_priorities, 0, sizeof(int) * PREFIX_COUNT * STYLE_PROPERTY_COUNT)

        s.cache = <PyObject **> calloc(PREFIX_COUNT * STYLE_PROPERTY_COUNT, sizeof(PyObject *))

        priority = 1

        for d in s.properties:
            for k, v in d.items():

                pfw = property_functions.get(k, None)

                if pfw is None:
                    continue

                try:
                    pfw.function(s.cache, cache_priorities, priority, v)
                except:
                    renpy.game.exception_info = "While processing the {} property of {}:".format(k, style_name_to_string(s.name))
                    raise

            priority += PRIORITY_LEVELS

        s.built = True

    finally:
        s.building = False

cpdef unbuild_style(StyleCore s):
    cdef int i

    if not s.built:
        return

    if s.cache != NULL:

        for 0 <= i < PREFIX_COUNT * STYLE_PROPERTY_COUNT:
            Py_XDECREF(s.cache[i])

        free(s.cache)
        s.cache = NULL

    s.left_parent = None
    s.down_parent = None

    s.built = False
    s.building = False

################################################################################
# Inspect support
################################################################################

# A map from prefixed property to priority.
priority = None

# A map from prefixed property to the prefixed properties it affects.
affects = None

def init_inspect():

    global priority
    global affects

    if priority is not None:
        return

    priority = { }
    affects = { }

    for prefixname, pri in prefix_priority.items():
        for propname, proplist in all_properties.items():
            priority[prefixname + propname] = pri + property_priority.get(propname, 0)
            affects[prefixname + propname] = [ a + i for a in prefix_alts[prefixname] for i in proplist ]


################################################################################
# Other functions
################################################################################

def reset():
    """
    Reset the style system.
    """

    styles.clear()


def build_styles():
    """
    Builds or rebuilds all styles.
    """
    for i in renpy.config.build_styles_callbacks:
        i()

    for s in list(styles.values()):
        unbuild_style(s)

    for s in list(styles.values()):
        build_style(s)

def rebuild(prepare_screens=True):
    """
    Rebuilds all styles.
    """

    build_styles()

    renpy.display.screen.prepared = False

    if not renpy.game.context().init_phase:
        renpy.display.screen.prepare_screens()

    renpy.exports.restart_interaction()

def copy_properties(p):
    """
    Makes a copy of the properties dict p.
    """

    return [ dict(i) for i in p ]

def backup():
    """
    Returns an opaque object that backs up the current styles.
    """

    rv = { }

    for k, v in styles.items():
        rv[k] = (v.parent, copy_properties(v.properties))

    return rv

def restore(o):
    """
    Restores a style backup.
    """

    cdef StyleCore s

    keys = list(styles.keys())

    for i in keys:
        if i not in o:
            del styles[i]


    for k, v in o.items():

        s = get_or_create_style(k[0])

        for i in k[1:]:
            s = s[i]

        parent, properties = v

        s.clear()
        s.set_parent(parent)
        s.properties = copy_properties(properties)

