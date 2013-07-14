# Copyright 2004-2013 Tom Rothamel <pytom@bishoujo.us>
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

import collections
import renpy.display

# A list of roles we know about.
roles = [ 'selected_', '' ]

# A list of style prefixes we care about, including no prefix.
prefixes = [ 'hover_', 'idle_', 'insensitive_', 'activate_', ]

# A map from prefix to priority and alternates.
prefix_subs = { }

# These allow quick access to important properties.
prop_xpos = None
prop_ypos = None
prop_xanchor = None
prop_yanchor = None
prop_xoffset = None
prop_yoffset = None
prop_subpixel = None


def register_prefix(prefix, prio, addprefixes=[]):

    for r in roles:
        if r and prefix.startswith(r):
            alts1 = [ r ]
            break
    else:
        alts1 = roles

    for p in prefixes:
        if prefix.endswith(p):
            alts2 = [ p ]
            break
    else:
        alts2 = prefixes

    alts2 += addprefixes

    alts = [ a1 + a2 for a1 in alts1 for a2 in alts2 ]

    prefix_subs[prefix] = prio, alts


register_prefix('selected_activate_', 6)
register_prefix('selected_hover_', 5, [ 'activate_' ])
register_prefix('selected_idle_', 5)
register_prefix('selected_insensitive_', 5)
register_prefix('selected_', 4)
register_prefix('activate_', 3)
register_prefix('hover_', 2, [ 'activate_' ])
register_prefix('idle_', 2)
register_prefix('insensitive_', 2)
register_prefix('', 1)

# A function that turns None into an instance of Null()
def none_is_null(d):
    if d is None:
        return renpy.display.layout.Null()
    else:
        return renpy.easy.displayable(d)

# This expands the outlines list.
def expand_outlines(l):
    rv = [ ]

    for i in l:
        if len(i) == 2:
            rv.append((i[0], renpy.easy.color(i[1]), 0, 0))
        else:
            rv.append((i[0], renpy.easy.color(i[1]), i[2], i[3]))

    return rv

# Names for anchors.
anchors = dict(
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
        return anchors.get(v, v)
    except:
        # This fixes some bugs in very old Ren'Pys.

        for n in anchors:
            o = getattr(renpy.store, n, None)
            if o is None:
                continue

            if v is o:
                return anchors[n]

        raise



# A map of properties that we know about. The properties may take a
# function that is called to convert the argument to something more
# useful.
style_properties = dict(
    aft_bar = none_is_null,
    aft_gutter = None,
    antialias = None,
    vertical = None,
    background = renpy.easy.displayable_or_none,
    bar_invert = None,
    bar_resizing = None,
    unscrollable = None,
    bar_vertical = None,
    black_color = renpy.easy.color,
    bold = None,
    bottom_margin = None,
    bottom_padding = None,
    box_layout = None,
    box_reverse = None,
    box_wrap = None,
    caret = renpy.easy.displayable_or_none,
    child = renpy.easy.displayable_or_none,
    clipping = None,
    color = renpy.easy.color,
    drop_shadow = None,
    drop_shadow_color = renpy.easy.color,
    first_indent = None,
    first_spacing = None,
    fit_first = None,
    focus_mask = None,
    focus_rect = None,
    font = None,
    fore_bar = none_is_null,
    fore_gutter = None,
    foreground = renpy.easy.displayable_or_none,
    sound = None,
    italic = None,
    justify = None,
    kerning = None,
    language = None,
    layout = None,
    line_leading = None,
    left_margin = None,
    left_padding = None,
    line_spacing = None,
    mouse = None,
    min_width = None,
    newline_indent = None,
    order_reverse = None,
    outlines = expand_outlines,
    rest_indent = None,
    right_margin = None,
    right_padding = None,
    ruby_style = None,
    size = None,
    size_group = None,
    slow_abortable = None,
    slow_cps = None,
    slow_cps_multiplier = None,
    spacing = None,
    strikethrough = None,
    subtitle_width = None,
    subpixel = None,
    text_y_fudge = None,
    text_align = None,
    thumb = none_is_null,
    thumb_offset = None,
    thumb_shadow = none_is_null,
    time_policy = None,
    top_margin = None,
    top_padding = None,
    underline = None,
    xanchor = expand_anchor,
    xfill = None,
    xmaximum = None,
    xminimum = None,
    xoffset = None,
    xpos = None,
    yanchor = expand_anchor,
    yfill = None,
    ymaximum = None,
    yminimum = None,
    yoffset = None,
    ypos = None,
    hyperlink_functions=None,
    line_overlap_split=None,
    )


def index_0(a):
    return a[0]
def index_1(a):
    return a[1]
def index_2(a):
    return a[2]
def index_3(a):
    return a[3]
def always_true(a):
    return True
def always_0(a):
    return 0
def always_half(a):
    return 0.5

substitutes = dict(
    xmargin = [
        ('left_margin', None),
        ('right_margin', None)
        ],

    ymargin = [
        ('top_margin', None),
        ('bottom_margin', None),
        ],

    xalign = [
        ('xpos', None),
        ('xanchor', None),
        ],

    yalign = [
        ('ypos', None),
        ('yanchor', None),
        ],

    xpadding = [
        ('left_padding', None),
        ('right_padding', None),
        ],

    ypadding = [
        ('top_padding', None),
        ('bottom_padding', None),
        ],

    minwidth = [ ('min_width', None) ],
    textalign = [ ('text_align', None) ],
    slow_speed = [ ('slow_cps', None) ],
    enable_hover = [ ],
    left_gutter = [ ('fore_gutter', None) ],
    right_gutter = [ ('aft_gutter', None) ],
    top_gutter = [ ('fore_gutter', None) ],
    bottom_gutter = [ ('aft_gutter', None) ],
    left_bar = [ ('fore_bar', none_is_null) ],
    right_bar = [ ('aft_bar', none_is_null) ],
    top_bar = [ ('fore_bar', none_is_null) ],
    bottom_bar = [ ('aft_bar', none_is_null) ],
    box_spacing = [ ( 'spacing', None ) ],
    box_first_spacing = [ ( 'first_spacing', None) ],

    pos = [
        ('xpos', index_0),
        ('ypos', index_1),
        ],

    anchor = [
        ('xanchor', index_0),
        ('yanchor', index_1),
        ],

    # Conflicts w/ a variable used in the Style implementation.
    # offset = [
    #     ('xoffset', index_0),
    #     ('yoffset', index_1),
    #     ],

    align = [
        ('xpos', index_0),
        ('ypos', index_1),
        ('xanchor', index_0),
        ('yanchor', index_1),
        ],

    maximum = [
        ('xmaximum', index_0),
        ('ymaximum', index_1),
        ],

    minimum = [
        ('xminimum', index_0),
        ('yminimum', index_1),
        ],

    area = [
        ('xpos', index_0),
        ('ypos', index_1),
        ('xanchor', always_0),
        ('yanchor', always_0),
        ('xfill', always_true),
        ('yfill', always_true),
        ('xmaximum', index_2),
        ('ymaximum', index_3),
        ('xminimum', index_2),
        ('yminimum', index_3),
        ],

    xcenter = [
        ('xpos', None),
        ('xanchor', always_half),
        ],

    ycenter = [
        ('ypos', None),
        ('yanchor', always_half),
        ],

    )

# Map from property to number.
property_number = { }

# Map from prefix to offset.
prefix_offset = { }

# Map from prefix_property to a list of priorities, offset numbers, and functions.
expansions = { }

# The total number of property numbers out there.
property_numbers = 0

# This is a function, to prevent namespace pollution. It's called
# once at module load time.
def init():

    global property_numbers

    # Figure out a map from style property name to an (arbitrary,
    # session-specific) style property number.
    for i, p in enumerate(style_properties):
        property_number[p] = i

    # Figure out a map from style prefix to style property number offset.
    property_numbers = 0
    for r in roles:
        for p in prefixes:
            prefix_offset[r + p] = property_numbers
            property_numbers += len(style_properties)

    # Figure out the mappings from prefixed properties to expansions of
    # those properties.
    for prefix, (prio, alts) in prefix_subs.iteritems():

        for prop, propn in property_number.iteritems():
            func = style_properties[prop]
            expansions[prefix + prop] = [ (prio, propn + prefix_offset[a], func) for a in alts ]


    # Expand out substitutes.
    for prefix, (prio, alts) in prefix_subs.iteritems():

        for virtual_prop, replacements in substitutes.iteritems():
            expansions[prefix + virtual_prop] = [ ]

            for real_prop, function in replacements:
                propn = property_number[real_prop]

                for a in alts:
                    expansions[prefix + virtual_prop].append((prio, propn + prefix_offset[a], function))

    # Cache mappings for position properties.
    for i in ('xpos', 'xanchor', 'xoffset', 'ypos', 'yanchor', 'yoffset', 'subpixel'):
        globals()["prop_" + i] = property_number[i]


init()

# A map from a style name to the style associated with that name.
style_map = { }

# A map from a the first part of a style name to a dict giving the
# second part of the style name.
style_parts = collections.defaultdict(dict)

# A map from style to style help.
style_help = { }

# True if we have expanded all of the style caches, False otherwise.
styles_built = False

# A list of styles that are pending expansion.
styles_pending = [ ]

def reset():
    """
    This resets all of the data structures associated with style
    management.
    """

    global style_map
    global style_parts
    global styles_built
    global styles_pending
    global style_help

    style_map = { }
    style_help = { }
    style_parts = collections.defaultdict(dict)
    styles_built = False
    styles_pending = [ ]

class StyleManager(object):
    """
    This is the singleton object that is exported into the store
    as style.
    """

    def __getattr__(self, name):
        global styles_built

        try:
            return style_map[name]
        except:
            pass

        # Automatically create styles, maybe.
        if "_" in name:

            rest = name

            while "_" in rest:
                _first, rest = rest.split("_", 1)

                if rest in style_map:

                    s = Style(rest)
                    self.__setattr__(name, s, False)

                    return s

            raise Exception("The style %s does not exist, and couldn't be auto-created because %s doesn't exist, either." % (name, rest))

        raise Exception('The style %s does not exist.' % name)

    def __setattr__(self, name, value, check_built=True):

        if check_built and styles_built:
            raise Exception("Cannot assign to style outside of the init phase.")

        if isinstance(value, Style):
            if value.name is None:
                value.name = (name, )

            style_map[name] = value
            style_parts[name][()] = value
        else:
            object.__setattr__(self, name, value)

    def create(self, name, parent, description=None):
        """
        Creates a new style.

        @param name: The name of the new style, as a string.

        @param parent: The parent of the new style, as a string. This
        is either 'default' or something more specific.

        @param description: A description of the style, for
        documentation purposes.
        """

        s = Style(parent, { }, heavy=True, help=description)
        setattr(self, name, s)

    def rebuild(self):
        renpy.style.rebuild()

    def exists(self, name):
        """
        This determines if the named style exists.
        """

        return name in style_map

    def get(self, name):

        if not isinstance(name, tuple):
            name = (name, )

        s = style_map

        for i in name:
            s = s[i]

        return s

def expand_properties(properties):

    rv = [ ]

    for prop, val in properties.iteritems():

        oldfunc = None

        try:
            e = expansions[prop]
        except KeyError:
            raise Exception("Style property %s is unknown." % prop)

        for prio, propn, func in e:

            if func:
                if oldfunc is not func:
                    oldfunc = func
                    newval = func(val)
            else:
                newval = val

            rv.append((prio, propn, newval))

    # Places things in priority order... so more important properties
    # come last.
    rv.sort()
    return rv


# This builds the style.
def build_style(style):

    if style.cache is not None:
        return

    updates = [ ]

    if style.parent is not None:

        name = style.parent

        # The left base is the style that shares the most indexes with
        # style.parent, while being one of the parents of style.parent.
        left_base = None

        while True:
            first = name[0]
            rest = name[1:]

            # The down bases inherit from the parents of the unindexd
            # style, but don't have as many components.

            if rest:
                down_base = [ style_map[first] ]
            else:
                down_base = [ ]

            while first:

                left_base = style_parts[first].get(rest, None)

                if left_base:
                    break

                try:
                    ss = style_map[first]
                except KeyError:
                    ss = getattr(renpy.game.style, first)

                down_base.insert(0, ss)
                first = ss.parent and ss.parent[0]

            if left_base:
                break

            name = name[:-1]

        for ss in down_base:
            if ss.updates:

                if ss.cache is None:
                    build_style(ss)

                updates.extend(ss.updates)

            for j in rest:

                if ss.indexed is None:
                    break

                ss = ss.indexed.get(j, None)

                if ss is None:
                    break

                if ss.cache is None:
                    build_style(ss)

                updates.extend(ss.updates)

        if left_base.cache is None:
            build_style(left_base)

        cache = left_base.cache

    else:
        cache = [ None ] * property_numbers

    # Now, factor in the style that we're indexed off of.
    if style.name is not None and len(style.name) > 1:

        ss = style_map[style.name[0]]

        if ss.cache is None:
            build_style(ss)

        updates.extend(ss.updates)

        for i in style.name[1:-1]:
            if (ss.indexed is None) or (i not in ss.indexed):
                break

            ss = ss.indexed[i]

            if ss.cache is None:
                build_style(ss)

            updates.extend(ss.updates)

    style.updates = my_updates = [ ]

    for p in style.properties:
        my_updates.extend(expand_properties(p))

    if updates or my_updates:
        cache = cache[:]
        for _prio, propn, val in updates:
            cache[propn] = val
        for _prio, propn, val in my_updates:
            cache[propn] = val

    style.cache = cache


# This builds all pending styles, recursing to ensure that they are built
# in the right order.
def build_styles(early=False):
    """
    Builds all pending styles.

    `early`
        If true, builds the pending styles, but leaves the pending queue
        around, so the styles will be rebuilt later. If false, stops
        using the pending queue - style changes will be processed
        immediately.
    """

    global styles_pending
    global styles_built

    for s in styles_pending:
        build_style(s)

    if not early:
        styles_pending = None
        styles_built = True


def rebuild():
    global styles_pending
    global styles_built

    if renpy.game.context().init_phase:
        return

    if styles_pending is None:
        styles_pending = [ ]

    styles_pending += [ j for i in style_parts.values() for j in i.values() ]
    styles_built = False

    for i in styles_pending:
        i.cache = None

    build_styles()


def backup():
    rv = { }

    for first, parts in style_parts.iteritems():
        for rest, v in parts.iteritems():
            rv[first, rest] = (v.parent, v.properties[:])

    return rv


def restore(o):
    global styles_built
    global styles_pending

    styles_pending = [ ]
    styles_built = False

    for (first, rest), (parent, properties) in o.iteritems():
        style_parts[first][rest].set_parent(parent)
        style_parts[first][rest].properties = properties[:]
        styles_pending.append(style_parts[first][rest])


def style_metaclass(name, bases, attrs):

    for k in expansions:
        def setter_a(self, v,  k=k):
            self.setattr(k, v)

        def deleter_a(self, k=k):
            self.delattr(k)

        def getter_a(self, k=k):
            return self.getattr(k)

        attrs[k] = property(getter_a, setter_a, deleter_a)


    for k, number in property_number.iteritems():
        def getter_b(self, number=number):
            return self.cache[self.offset + number]

        def setter_b(self, v,  k=k):
            self.setattr(k, v)

        def deleter_b(self, k=k):
            self.delattr(k)

        attrs[k] = property(getter_b, setter_b, deleter_b)

    return type(name, bases, attrs)


# This class is used for heavyweight and lightweight styles. (Heavyweight
# styles have a cache, lightweight styles do not.)
class Style(object):

    __metaclass__ = style_metaclass
    __slots__ = [
        'cache',
        'properties',
        'offset',
        'prefix',
        'updates',
        'name',
        'parent',
        'indexed',
        ]

    def __getstate__(self):

        rv = dict()

        for i in self.__slots__:
            rv[i] = getattr(self, i)

        del rv["cache"]
        del rv["offset"]
        del rv["updates"]

        return rv

    def __setstate__(self, state):

        state.pop("heavy", None)
        state.pop("help", None)

        for k, v in state.iteritems():
            setattr(self, k, v)

        self.cache = None
        self.updates = None
        self.offset = prefix_offset[self.prefix]

        build_style(self)

    def set_parent(self, parent):

        if parent:
            if isinstance(parent, basestring):
                parent = ( parent, )
            if isinstance(parent, Style):
                parent = parent.name # E1103

                if parent is None:
                    raise Exception("The parent of a style must be a named style.")

        self.parent = parent


    def __init__(self, parent, properties=None, heavy=True, name=None, help=None): #@ReservedAssignment

        self.prefix = 'insensitive_'
        self.offset = prefix_offset['insensitive_']

        if name is None or isinstance(name, tuple):
            self.name = name
        else:
            self.name = ( name, )

        self.parent = None
        self.set_parent(parent)

        self.indexed = None
        self.cache = None
        self.updates = None
        self.properties = [ ]

        if help is not None:
            style_help[self] = help

        if properties:
            self.properties.append(properties)

        if heavy:
            if styles_built:
                build_style(self)
            else:
                styles_pending.append(self)

    def set_prefix(self, prefix):
        self.prefix = prefix
        self.offset = prefix_offset[prefix]

    def setattr(self, name, value): #@ReservedAssignment
        self.properties.append({ name : value })

    def delattr(self, name): #@ReservedAssignment

        for p in self.properties:
            if name in p:
                del p[name]

    def getattr(self, name): #@ReservedAssignment
        return self.cache[expansions[name][0][1]]

    def clear(self):
        if styles_built:
            raise Exception("Cannot clear a style after styles have been built.")
        else:
            self.properties = [ ]

    def take(self, other):

        self.properties = other.properties[:]

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

    def __getitem__(self, index):

        if self.indexed is None:
            self.indexed = { }

        if index in self.indexed:
            return self.indexed[index]

        name = self.name + (index,)

        s = Style(self.parent + (index,), name=name, heavy=not styles_built)

        if not styles_built:
            self.indexed[index] = s
            style_parts[name[0]][name[1:]] = s

        return s

    # This is here to accelerate Displayable.get_placement.
    def get_placement(self):
        o = self.offset
        c = self.cache
        return (
            c[o + prop_xpos],
            c[o + prop_ypos],
            c[o + prop_xanchor],
            c[o + prop_yanchor],
            c[o + prop_xoffset],
            c[o + prop_yoffset],
            c[o + prop_subpixel],
            )


def write_text(filename):

    def style_name(name):
        rv = name[0]
        for i in name[1:]:
            rv += "[%r]" % i

        return rv


    f = file(filename, "w")

    styles = style_map.items()
    styles.sort()

    for _name, sty in styles:

        if not isinstance(sty, Style):
            continue

        print >>f, style_name(sty.name),

        if sty.parent:
            print >>f, "inherits from", style_name(sty.parent)
        else:
            print >>f

        if not sty.cache:
            continue

        inherited = [ True ] * property_numbers

        for p in sty.properties:
            for _prio, propn, _newval in expand_properties(p):
                inherited[propn] = False

        props = [ (prefix + prop, sty.cache[prefixn + propn], inherited[prefixn + propn])
                  for prefix, prefixn in prefix_offset.iteritems()
                  for prop, propn in property_number.iteritems() ]

        props.sort()

        for prop, value, inherit in props:

            if inherit:
                inherit = "(inherited)"
            else:
                inherit = ""

            print >>f, "   ", prop, "=", repr(value), inherit

        print >>f

    f.close()


def style_hierarchy():
    rv = [ ]
    children = { } # Map from parent to list of children.

    for v in style_map.values():

        if v.parent is not None:
            parent = style_map
            for i in v.parent:
                parent = parent[i]
        else:
            parent = None

        children.setdefault(parent, [ ]).append(v)

    def recurse(p, depth):
        for s in sorted(children.get(p, []), key=lambda i : i.name):
            if s in style_help:
                rv.append((depth, "style." + s.name[0], style_help[s]))
            recurse(s, depth + 1)

    recurse(None, 0)

    return rv

