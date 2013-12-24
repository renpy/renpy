# Code for generating the includes used by renpy.styleaccel.

import collections

################################################################################
# Prefixes
################################################################################

# A map from prefix name to Prefix object.
prefixes = { }

class Prefix(object):
    def __init__(self, index, name, priority, alts):

        # The index of where this prefix is stored in memory, or -1 if this
        # prefix isn't stored in memory.
        self.index = index

        # The name of this prefix.
        self.name = name

        # The priority of this prefix. When added at the same time, higher
        # priority prefixes take precendence over lower priority prefixes.
        self.priority = priority

        # A list of prefix indexes that should be updated when this prefix is
        # updated, including this prefix.
        if index >= 0:
            self.alts = [ self.index ]
        else:
            self.alts = [ ]

        for i in alts:
            self.alts.append(prefixes[i].index)

        prefixes[name] = self

# The number of priority levels we have.
PRIORITY_LEVELS = 4

Prefix(5, 'selected_hover_', 3, [ ])
Prefix(4, 'selected_idle_', 3, [ ])
Prefix(3, 'selected_insensitive_', 3, [ ])
Prefix(-1, 'selected_', 2, [ "selected_hover_", "selected_idle_", "selected_insensitive_" ])
Prefix(2, 'hover_', 1, [ "selected_hover_" ])
Prefix(1, 'idle_', 1, [ "selected_idle_" ] )
Prefix(0, 'insensitive_', 1, [ "selected_insensitive_" ])
Prefix(-1, '', 0, [ "selected_hover_", "selected_idle_", "selected_insensitive_", "idle_", "hover_", "insensitive_" ] )


################################################################################
# Style Properties
################################################################################

# All the style properties we know about. This is a dict, that maps each style
# to a function that is called when it is set, or None if no such function
# is needed.
style_properties = collections.OrderedDict(
    aft_bar = 'none_is_null',
    aft_gutter = None,
    antialias = None,
    vertical = None,
    background = 'renpy.easy.displayable_or_none',
    bar_invert = None,
    bar_resizing = None,
    unscrollable = None,
    bar_vertical = None,
    black_color = 'renpy.easy.color',
    bold = None,
    bottom_margin = None,
    bottom_padding = None,
    box_layout = None,
    box_reverse = None,
    box_wrap = None,
    caret = 'renpy.easy.displayable_or_none',
    child = 'renpy.easy.displayable_or_none',
    clipping = None,
    color = 'renpy.easy.color',
    drop_shadow = None,
    drop_shadow_color = 'renpy.easy.color',
    first_indent = None,
    first_spacing = None,
    fit_first = None,
    focus_mask = None,
    focus_rect = None,
    font = None,
    fore_bar = 'none_is_null',
    fore_gutter = None,
    foreground = 'renpy.easy.displayable_or_none',
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
    outlines = 'expand_outlines',
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
    thumb = 'none_is_null',
    thumb_offset = None,
    thumb_shadow = 'none_is_null',
    time_policy = None,
    top_margin = None,
    top_padding = None,
    underline = None,
    xanchor = 'expand_anchor',
    xfill = None,
    xmaximum = None,
    xminimum = None,
    xoffset = None,
    xpos = None,
    yanchor = 'expand_anchor',
    yfill = None,
    ymaximum = None,
    yminimum = None,
    yoffset = None,
    ypos = None,
    hyperlink_functions=None,
    line_overlap_split=None,
    )

# A list of synthetic style properties, where each property is expanded into
# multiple style properties. Each property are mapped into a list of tuples,
# with each consisting of:
#
# * The name of the style to assign.
# * A string giving the name of a functon to call to get the value to assign, a constant
#   numeric value, or None to not change the argument.
synthetic_properties = collections.OrderedDict(
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
    left_bar = [ ('fore_bar', 'none_is_null') ],
    right_bar = [ ('aft_bar', 'none_is_null') ],
    top_bar = [ ('fore_bar', 'none_is_null') ],
    bottom_bar = [ ('aft_bar', 'none_is_null') ],
    box_spacing = [ ( 'spacing', None ) ],
    box_first_spacing = [ ( 'first_spacing', None) ],

    pos = [
        ('xpos', 'index_0'),
        ('ypos', 'index_1'),
        ],

    anchor = [
        ('xanchor', 'index_0'),
        ('yanchor', 'index_1'),
        ],

    # Conflicts w/ a variable used in the Style implementation.
    # offset = [
    #     ('xoffset', index_0),
    #     ('yoffset', index_1),
    #     ],

    align = [
        ('xpos', 'index_0'),
        ('ypos', 'index_1'),
        ('xanchor', 'index_0'),
        ('yanchor', 'index_1'),
        ],

    maximum = [
        ('xmaximum', 'index_0'),
        ('ymaximum', 'index_1'),
        ],

    minimum = [
        ('xminimum', 'index_0'),
        ('yminimum', 'index_1'),
        ],

    area = [
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

    xcenter = [
        ('xpos', None),
        ('xanchor', 0.5),
        ],

    ycenter = [
        ('ypos', None),
        ('yanchor', 0.5),
        ],

    )




def generate(force=False):

    # TODO: If nothing is out of date, do not generate styles.

    pass

if __name__ == "__main__":
    generate(force=True)
