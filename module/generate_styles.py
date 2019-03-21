# Copyright 2004-2019 Tom Rothamel <pytom@bishoujo.us>
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

from __future__ import print_function, unicode_literals, division, absolute_import

str = unicode  # @ReservedAssignment

import collections
import os

try:
    from io import StringIO  # @UnusedImport
except:
    from StringIO import StringIO  # @Reimport

# Paths
BASE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(BASE)

import setuplib
module_gen = "module/" + setuplib.gen


def sorted_dict(**kwargs):
    """
    Constructs an ordered_dict from the keyword arguments in sorted order.
    """

    items = list(kwargs.items())
    return collections.OrderedDict(items)

################################################################################
# Prefixes
################################################################################


# A map from prefix name to Prefix object.
prefixes = collections.OrderedDict()


class Prefix(object):

    def __init__(self, index, name, priority, alts):

        # The index of where this prefix is stored in memory, or -1 if this
        # prefix isn't stored in memory.
        self.index = index

        # The name of this prefix.
        self.name = name

        # The priority of this prefix. When added at the same time, higher
        # priority prefixes take precendence over lower priority prefixes.
        #
        # We double the priority here so we have room for the special priority
        # stuff below.
        self.priority = priority * 2

        # A list of prefix indexes that should be updated when this prefix is
        # updated, including this prefix.
        if index >= 0:
            self.alts = [ self.index ]
            self.alt_names = [ self.name ]
        else:
            self.alts = [ ]
            self.alt_names = [ ]

        for i in alts:
            self.alts.append(prefixes[i].index)
            self.alt_names.append(i)

        prefixes[name] = self


# The number of priority levels we have. Double the number given below, due to the doubling above.
PRIORITY_LEVELS = 8

# The number of prefixes we have.
PREFIX_COUNT = 6

Prefix(5, 'selected_hover_', 3, [ ])
Prefix(4, 'selected_idle_', 3, [ ])
Prefix(3, 'selected_insensitive_', 3, [ ])
Prefix(-3, 'selected_', 2, [ "selected_hover_", "selected_idle_", "selected_insensitive_" ])
Prefix(2, 'hover_', 1, [ "selected_hover_" ])
Prefix(1, 'idle_', 1, [ "selected_idle_" ] )
Prefix(0, 'insensitive_', 1, [ "selected_insensitive_" ])
Prefix(-4, '', 0, [ "selected_hover_", "selected_idle_", "selected_insensitive_", "idle_", "hover_", "insensitive_" ] )

Prefix(-2, 'activate_', 0, [ ])
Prefix(-1, 'selected_activate_', 0, [ ])


# The images that are searched by a prefix.
PREFIX_SEARCH = {
    "idle_" : [ "idle_", "" ],
    "hover_" : [ "hover_", "" ],
    "insensitive_" : [ "insensitive_", "", "idle_" ],
    "selected_idle_" : [ "selected_idle_", "selected_", "", "idle_" ],
    "selected_hover_" : [ "selected_hover_", "hover_", "selected_", "" ],
    "selected_insensitive_" : [ "selected_insensitive_", "insensitive_", "selected_", "", "selected_idle_", "idle_" ],
    "" : [ "" ],
    }


################################################################################
# Style Properties
################################################################################

# All the style properties we know about. This is a dict, that maps each style
# to a function that is called when it is set, or None if no such function
# is needed.
style_properties = sorted_dict(
    activate_sound=None,
    adjust_spacing=None,
    aft_bar='none_is_null',
    aft_gutter=None,
    alt=None,
    altruby_style=None,
    antialias=None,
    vertical=None,
    background='renpy.easy.displayable_or_none',
    bar_invert=None,
    bar_resizing=None,
    unscrollable=None,
    bar_vertical=None,
    black_color='renpy.easy.color',
    bold=None,
    bottom_margin=None,
    bottom_padding=None,
    box_layout=None,
    box_reverse=None,
    box_wrap=None,
    box_wrap_spacing=None,
    caret='renpy.easy.displayable_or_none',
    child='renpy.easy.displayable_or_none',
    clipping=None,
    color='renpy.easy.color',
    debug=None,
    drop_shadow=None,
    drop_shadow_color='renpy.easy.color',
    first_indent=None,
    first_spacing=None,
    fit_first=None,
    focus_mask='expand_focus_mask',
    focus_rect=None,
    font=None,
    fore_bar='none_is_null',
    fore_gutter=None,
    foreground='renpy.easy.displayable_or_none',
    hinting=None,
    hover_sound=None,
    hyperlink_functions=None,
    italic=None,
    justify=None,
    kerning=None,
    key_events=None,
    keyboard_focus=None,
    language=None,
    layout=None,
    line_leading=None,
    left_margin=None,
    line_overlap_split=None,
    left_padding=None,
    line_spacing=None,
    mouse=None,
    min_width=None,
    newline_indent=None,
    order_reverse=None,
    outlines='expand_outlines',
    outline_scaling=None,
    rest_indent=None,
    right_margin=None,
    right_padding=None,
    ruby_style=None,
    size=None,
    size_group=None,
    slow_abortable=None,
    slow_cps=None,
    slow_cps_multiplier=None,
    spacing=None,
    strikethrough=None,
    subtitle_width=None,
    subpixel=None,
    text_y_fudge=None,
    text_align=None,
    thumb='none_is_null',
    thumb_offset=None,
    thumb_shadow='none_is_null',
    time_policy=None,
    top_margin=None,
    top_padding=None,
    underline=None,
    xanchor='expand_anchor',
    xfill=None,
    xfit=None,
    xmaximum=None,
    xminimum=None,
    xoffset=None,
    xpos=None,
    xspacing=None,
    yanchor='expand_anchor',
    yfill=None,
    yfit=None,
    ymaximum=None,
    yminimum=None,
    yoffset=None,
    ypos=None,
    yspacing=None,
    )

# Properties that take displayables that should be given the right set
# of prefixes.
displayable_properties = {
    "background",
    "foreground",
    "child",
    "fore_bar",
    "aft_bar",
    "thumb",
    "thumb_shadow",
    }


# A map from a style property to its index in the order of style_properties.
style_property_index = collections.OrderedDict()
for i, name in enumerate(style_properties):
    style_property_index[name] = i

style_property_count = len(style_properties)

# print("{} properties * {} prefixes = {} cache entries".format(
#     style_property_count, PREFIX_COUNT, style_property_count * PREFIX_COUNT))


# Special priority properties - these take a +1 compared to others. Generally,
# these would be listed in the tuples in synthetic_properies, below.
property_priority = sorted_dict(
    left_margin=1,
    top_margin=1,
    right_margin=1,
    bottom_margin=1,
    xpos=1,
    xanchor=1,
    ypos=1,
    yanchor=1,
    left_padding=1,
    top_padding=1,
    right_padding=1,
    bottom_padding=1,
    xoffset=1,
    yoffset=1,
    xminimum=1,
    yminimum=1,
    xmaximum=1,
    ymaximum=1,
    xfill=1,
    yfill=1,
)


# A list of synthetic style properties, where each property is expanded into
# multiple style properties. Each property are mapped into a list of tuples,
# with each consisting of:
#
# * The name of the style to assign.
# * A string giving the name of a functon to call to get the value to assign, a constant
#   numeric value, or None to not change the argument.
synthetic_properties = sorted_dict(

    margin=[
        ('left_margin', 'index_0'),
        ('top_margin', 'index_1'),
        ('right_margin', 'index_2_or_0'),
        ('bottom_margin', 'index_3_or_1'),
        ],

    xmargin=[
        ('left_margin', None),
        ('right_margin', None)
        ],

    ymargin=[
        ('top_margin', None),
        ('bottom_margin', None),
        ],

    xalign=[
        ('xpos', None),
        ('xanchor', None),
        ],

    yalign=[
        ('ypos', None),
        ('yanchor', None),
        ],

    padding=[
        ('left_padding', 'index_0'),
        ('top_padding', 'index_1'),
        ('right_padding', 'index_2_or_0'),
        ('bottom_padding', 'index_3_or_1'),
        ],

    xpadding=[
        ('left_padding', None),
        ('right_padding', None),
        ],

    ypadding=[
        ('top_padding', None),
        ('bottom_padding', None),
        ],

    minwidth=[ ('min_width', None) ],
    textalign=[ ('text_align', None) ],
    slow_speed=[ ('slow_cps', None) ],
    enable_hover=[ ],

    left_gutter=[ ('fore_gutter', None) ],
    right_gutter=[ ('aft_gutter', None) ],
    top_gutter=[ ('fore_gutter', None) ],
    bottom_gutter=[ ('aft_gutter', None) ],

    left_bar=[ ('fore_bar', None) ],
    right_bar=[ ('aft_bar', None) ],
    top_bar=[ ('fore_bar', None) ],
    bottom_bar=[ ('aft_bar', None) ],

    base_bar=[
        ('fore_bar', None),
        ('aft_bar', None),
        ],

    box_spacing=[ ( 'spacing', None ) ],
    box_first_spacing=[ ( 'first_spacing', None) ],

    pos=[
        ('xpos', 'index_0'),
        ('ypos', 'index_1'),
        ],

    anchor=[
        ('xanchor', 'index_0'),
        ('yanchor', 'index_1'),
        ],

    offset=[
        ('xoffset', 'index_0'),
        ('yoffset', 'index_1'),
        ],

    align=[
        ('xpos', 'index_0'),
        ('ypos', 'index_1'),
        ('xanchor', 'index_0'),
        ('yanchor', 'index_1'),
        ],

    maximum=[
        ('xmaximum', 'index_0'),
        ('ymaximum', 'index_1'),
        ],

    minimum=[
        ('xminimum', 'index_0'),
        ('yminimum', 'index_1'),
        ],

    xsize=[
        ('xminimum', None),
        ('xmaximum', None),
        ],

    ysize=[
        ('yminimum', None),
        ('ymaximum', None),
        ],

    xysize=[
        ('xminimum', 'index_0'),
        ('xmaximum', 'index_0'),
        ('yminimum', 'index_1'),
        ('ymaximum', 'index_1'),
        ],

    area=[
        ('xpos', 'index_0'),
        ('ypos', 'index_1'),
        ('xanchor', 0),
        ('yanchor', 0),
        ('xfill', True),
        ('yfill', True),
        ('xmaximum', 'index_2'),
        ('ymaximum', 'index_3'),
        ('xminimum', 'index_2'),
        ('yminimum', 'index_3'),
        ],

    xcenter=[
        ('xpos', None),
        ('xanchor', 0.5),
        ],

    ycenter=[
        ('ypos', None),
        ('yanchor', 0.5),
        ],
    )

all_properties = collections.OrderedDict()

for k, v in style_properties.items():
    all_properties[k] = [ (k, None) ]

all_properties.update(synthetic_properties)

################################################################################
# Code Generation
################################################################################


class CodeGen(object):
    """
    Utility class for code generation.

    `filename`
        The name of the file we code-generate into.
    `spew`
        If true, spew the generated code to stdout.
    """

    def __init__(self, filename, spew=False):
        self.filename = os.path.join(ROOT, filename)
        self.f = StringIO()
        self.depth = 0
        self.spew = spew

    def close(self):

        text = self.f.getvalue()

        if os.path.exists(self.filename):
            with open(self.filename, "rb") as f:
                old = f.read()

            if old == text:
                return

        with open(self.filename, "wb") as f:
            f.write(text)

    def write(self, s, *args, **kwargs):
        out = "    " * self.depth
        out += s.format(*args, **kwargs)
        out = out.rstrip()

        if self.spew:
            print(out)

        out += "\n"
        self.f.write(out)

    def indent(self):
        self.depth += 1

    def dedent(self):
        self.depth -= 1


def generate_constants():
    """
    This generates code that defines the property functions.
    """

    g = CodeGen(module_gen + "/styleconstants.pxi")

    g.write("DEF PRIORITY_LEVELS = {}", PRIORITY_LEVELS)
    g.write("DEF PREFIX_COUNT = {}", PREFIX_COUNT)
    g.write("DEF STYLE_PROPERTY_COUNT = {}", style_property_count)

    for p in prefixes.values():
        if p.index < 0:
            continue

        g.write("DEF {}PREFIX = {}", p.name.upper(), p.index * style_property_count)

    for k in style_properties:
        g.write("DEF {}_INDEX = {}", k.upper(), style_property_index[k])

    g.close()


def generate_property_function(g, prefix, propname, properties):

    name = prefix.name + propname

    g.write("cdef int {name}_property(PyObject **cache, int *cache_priorities, int priority, object value) except -1:", name=name)
    g.indent()

    g.write("priority += {}", prefix.priority + property_priority.get(propname, 0))

    for stylepropname, func in properties:
        value = "value"

        g.write("")

        if isinstance(func, str):
            g.write("v = {func}({value})", func=func, value=value)
            value = "v"
        elif func is not None:
            g.write("v = {}", func)
            value = "v"

        propfunc = style_properties[stylepropname]

        if propfunc is not None:
            g.write("v = {propfunc}({value})", propfunc=propfunc, value=value)
            value = "v"

        for alt, alt_name in zip(prefix.alts, prefix.alt_names):

            if stylepropname in displayable_properties:
                g.write("assign_prefixed({}, cache, cache_priorities, priority, {}, '{}') # {}{}",
                        alt * len(style_properties) + style_property_index[stylepropname],
                        value, alt_name, alt_name, stylepropname)
            else:
                g.write("assign({}, cache, cache_priorities, priority, <PyObject *> {}) # {}{}",
                        alt * len(style_properties) + style_property_index[stylepropname],
                        value, alt_name, stylepropname)

    g.write("return 0")
    g.dedent()

    g.write("")
    g.write('register_property_function("{}", {}_property)', name, name)
    g.write("")

    pass


def generate_property_functions():
    """
    This generates code that defines the property functions.
    """

    for prefix in sorted(prefixes.values(), key=lambda p : p.index):
        g = CodeGen(module_gen + "/style_{}functions.pyx".format(prefix.name))

        g.write('include "style_common.pxi"')
        g.write('')

        for propname, proplist in all_properties.items():
            generate_property_function(g, prefix, propname, proplist)

        g.close()


def generate_property(g, propname):
    """
    This generates the code for a single property on the style object.
    """

    g.write("property {}:", propname)
    g.indent()

    # __get__
    g.write("def __get__(self):")
    g.indent()
    g.write("return self._get({})", style_property_index[propname])
    g.dedent()

    # __set__
    g.write("def __set__(self, value):")
    g.indent()
    g.write("self.properties.append({{ '{}' : value }})", propname)
    g.dedent()

    # __del__
    g.write("def __del__(self):")
    g.indent()
    g.write("self.delattr('{}')", propname)
    g.dedent()

    g.dedent()
    g.write("")


def generate_properties():

    g = CodeGen(module_gen + "/styleclass.pxi")

    g.write("cdef class Style(StyleCore):")
    g.write("")

    g.indent()

    for propname in style_properties:
        generate_property(g, propname)

    g.dedent()
    g.close()


def generate_sets():
    """
    Generates code for sets of properties.
    """

    ap = collections.OrderedDict()

    for k, v in all_properties.items():
        ap[k] = [ i[0] for i in v ]

    prefix_priority = collections.OrderedDict()
    prefix_alts = collections.OrderedDict()

    for p in prefixes.values():
        prefix_priority[p.name] = p.priority
        prefix_alts[p.name] = p.alt_names

    g = CodeGen(module_gen + "/stylesets.pxi")

    g.write("# This file is generated by generate_styles.py.")
    g.write("")
    g.write('exec """\\')
    g.write("all_properties = {}", ap)
    g.write("prefix_priority = {}", prefix_priority)
    g.write("prefix_alts = {}", prefix_alts)
    g.write("prefix_search = {}", PREFIX_SEARCH)
    g.write("property_priority = {}", property_priority)
    g.write('"""')
    g.close()


def generate():
    generate_constants()
    generate_property_functions()
    generate_properties()
    generate_sets()


if __name__ == "__main__":
    generate()
