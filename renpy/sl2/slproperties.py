# Copyright 2004-2023 Tom Rothamel <pytom@bishoujo.us>
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

from __future__ import division, absolute_import, with_statement, print_function, unicode_literals
from renpy.compat import PY2, basestring, bchr, bord, chr, open, pystr, range, round, str, tobytes, unicode # *



from renpy.sl2.slparser import Keyword, Style, PrefixStyle

position_property_names = [
    "anchor",
    "xanchor",
    "yanchor",
    "pos",
    "xpos",
    "ypos",
    "align",
    "xalign",
    "yalign",
    "offset",
    "xoffset",
    "yoffset",
    "maximum",
    "xmaximum",
    "ymaximum",
    "minimum",
    "xminimum",
    "yminimum",
    "area",
    "clipping",
    "xfill",
    "yfill",
    "xcenter",
    "ycenter",
    "xycenter",
    # not center, since it can conflict with the center transform.
    "xsize",
    "ysize",
    "xysize",
    # not size, which is a text style property
    "alt",
    "debug",
    ]

position_properties = [ Style(i) for i in position_property_names ] + [ Keyword("tooltip") ] # type: ignore
text_position_properties = [ PrefixStyle("text_", i) for i in position_property_names ] # type: ignore
side_position_properties = [ PrefixStyle("side_", i) for i in position_property_names ] + [ Keyword("tooltip") ] # type: ignore
viewport_position_properties = [ PrefixStyle("viewport_", i) for i in position_property_names ] # type: ignore
scrollbar_position_properties = [ PrefixStyle("scrollbar_", i) for i in position_property_names ] + [ Keyword("tooltip") ] # type: ignore
vscrollbar_position_properties = [ PrefixStyle("vscrollbar_", i) for i in position_property_names ] + [ Keyword("tooltip") ] # type: ignore

text_property_names = [
    "antialias",
    "vertical",
    "black_color",
    "bold",
    "color",
    "drop_shadow",
    "drop_shadow_color",
    "first_indent",
    "font",
    "size",
    "hyperlink_functions",
    "italic",
    "justify",
    "kerning",
    "language",
    "layout",
    "line_leading",
    "line_spacing",
    "minwidth",
    "min_width",
    "newline_indent",
    "outlines",
    "outline_scaling",
    "rest_indent",
    "ruby_style",
    "slow_cps",
    "slow_cps_multiplier",
    "slow_abortable",
    "strikethrough",
    "textalign",
    "text_align",
    "text_y_fudge",
    "underline",
    "hinting",
    "adjust_spacing",
    "mipmap",
    ]

text_properties = [ Style(i) for i in text_property_names ]
text_text_properties = [ PrefixStyle("text_", i) for i in text_property_names ]

margin_properties = [ Style(i) for i in [
    "left_margin",
    "right_margin",
    "bottom_margin",
    "top_margin",
    "xmargin",
    "ymargin",
    "margin",
    ] ]

padding_properties = [ Style(i) for i in [
    "left_padding",
    "right_padding",
    "top_padding",
    "bottom_padding",
    "xpadding",
    "ypadding",
    "padding",
    ] ]

window_properties = [ Style(i) for i in [
    "background",
    "foreground",
    "size_group",
    "modal",
    ] ] + margin_properties + padding_properties

button_properties = [ Style(i) for i in [
    "sound",
    "mouse",
    "focus_mask",
    "child",
    "keyboard_focus",
    "key_events",
    ] ] + [
        Keyword("action"),
        Keyword("clicked"),
        Keyword("hovered"),
        Keyword("unhovered"),
        Keyword("alternate"),
        Keyword("selected"),
        Keyword("sensitive"),
        Keyword("keysym"),
        Keyword("alternate_keysym"),
    ] # type: ignore

bar_property_names = [
    "bar_vertical",
    "bar_invert",
    "bar_resizing",
    "left_gutter",
    "right_gutter",
    "top_gutter",
    "bottom_gutter",
    "left_bar",
    "right_bar",
    "top_bar",
    "bottom_bar",
    "base_bar",
    "thumb",
    "thumb_shadow",
    "thumb_offset",
    "mouse",
    "unscrollable",
    "keyboard_focus",
    ]

bar_properties = [ Style(i) for i in bar_property_names ]
scrollbar_bar_properties = [ PrefixStyle("scrollbar_", i) for i in bar_property_names ]
vscrollbar_bar_properties = [ PrefixStyle("vscrollbar_", i) for i in bar_property_names ]

box_property_names = [
    "box_layout",
    "box_wrap",
    "box_wrap_spacing",
    "box_reverse",
    "order_reverse",
    "spacing",
    "first_spacing",
    "fit_first",
    "xfit",
    "yfit",
]

box_properties = [ Style(i) for i in box_property_names ]

grid_properties = [ Style(i) for i in [
    "spacing",
    "xspacing",
    "yspacing",
    ] ] + margin_properties

ui_properties = [
    Keyword("at"),
    Keyword("id"),
    Keyword("style"),
    Keyword("style_group"),
    Keyword("style_prefix"),
    Keyword("style_suffix"),
    Keyword("focus"),
    Keyword("default"),
    Keyword("default_focus"),
    ]

property_groups = {
    "bar" : bar_properties,
    "box" : box_properties,
    "button" : button_properties,
    "position" : position_properties,
    "text" : text_properties,
    "window" : window_properties,
    "ui" : ui_properties,
    "grid" : grid_properties,
    }
