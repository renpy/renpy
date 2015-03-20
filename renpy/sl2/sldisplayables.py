# Copyright 2004-2015 Tom Rothamel <pytom@bishoujo.us>
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

##############################################################################
# Definitions of screen language statements.

import renpy.display
import renpy.text.text

class ShowIf(renpy.display.layout.Container):
    """
    This is a displayable that wraps displayables that are
    underneath a showif statement.
    """

    def __init__(self, condition, replaces=None):
        super(ShowIf, self).__init__()

        self.condition = condition

        if replaces is None:
            if condition:
                self.pending_event = "appear"
            else:
                self.pending_event = None

            self.show_child = condition

        else:
            if self.condition and not replaces.condition:
                self.pending_event = "show"
            elif not self.condition and replaces.condition:
                self.pending_event = "hide"
            else:
                self.pending_event = replaces.pending_event

            self.show_child = replaces.show_child

    def per_interact(self):
        if self.pending_event:
            self.child.set_transform_event(self.pending_event)
            self.pending_event = None

    def render(self, width, height, st, at):

        if isinstance(self.child, renpy.display.motion.Transform):
            if self.condition or self.show_child:
                cr = renpy.display.render.render(self.child, width, height, st, at)
                self.show_child = self.condition or not self.child.hide_response
        else:
            if self.condition:
                cr = renpy.display.render.render(self.child, width, height, st, at)
                self.show_child = True
            else:
                self.show_child = False

        if self.show_child:
            cw, ch = cr.get_size()
            rv = renpy.display.render.Render(cw, ch)
            rv.blit(cr, (0, 0))
        else:
            rv = renpy.display.render.Render(0, 0)

        self.offsets = [ (0, 0) ]

        return rv

    def event(self, ev, x, y, st):
        if self.condition:
            return self.child.event(ev, x, y, st)
        else:
            return None

    def get_placement(self):
        return self.child.get_placement()


from renpy.sl2.slparser import Positional, Keyword, Style, PrefixStyle, add
from renpy.sl2.slparser import DisplayableParser, many

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
        "xoffset",
        "yoffset",
        "maximum",
        "xmaximum",
        "ymaximum",
        "area",
        "clipping",
        "xfill",
        "yfill",
        # no center, since it can conflict with the center transform.
        "xcenter",
        "ycenter",
        "xsize",
        "ysize",
        "xysize",
        "alt",
        "debug",
        ]

position_properties = [ Style(i) for i in position_property_names ]
text_position_properties = [ PrefixStyle("text_", i) for i in position_property_names ]
side_position_properties = [ PrefixStyle("side_", i) for i in position_property_names ]

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
        "rest_indent",
        "ruby_style",
        "slow_cps",
        "slow_cps_multiplier",
        "slow_abortable",
        "strikethrough",
        "text_align",
        "text_y_fudge",
        "underline",
        "minimum",
        "xminimum",
        "yminimum",
        ]

text_properties = [ Style(i) for i in text_property_names ]
text_text_properties = [ PrefixStyle("text_", i) for i in text_property_names ]

window_properties = [ Style(i) for i in [
        "background",
        "foreground",
        "left_margin",
        "right_margin",
        "bottom_margin",
        "top_margin",
        "xmargin",
        "ymargin",
        "left_padding",
        "right_padding",
        "top_padding",
        "bottom_padding",
        "xpadding",
        "ypadding",
        "size_group",
        "minimum",
        "xminimum",
        "yminimum",
        ] ]

button_properties = [ Style(i) for i in [
        "sound",
        "mouse",
        "focus_mask",
        "child",
        "keyboard_focus",
        ] ]

bar_properties = [ Style(i) for i in [
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
        "thumb",
        "thumb_shadow",
        "thumb_offset",
        "mouse",
        "unscrollable",
        "keyboard_focus",
        ] ]

box_properties = [ Style(i) for i in [
        "box_layout",
        "box_wrap",
        "box_reverse",
        "order_reverse",
        "spacing",
        "first_spacing",
        "fit_first",
        "minimum",
        "xminimum",
        "yminimum",
        ] ]

ui_properties = [
    Keyword("at"),
    Keyword("id"),
    Keyword("style"),
    Keyword("style_group"),
    Keyword("focus"),
    Keyword("default"),
    ]


DisplayableParser("null", renpy.display.layout.Null, "default", 0)
Keyword("width")
Keyword("height")
add(ui_properties)
add(position_properties)

DisplayableParser("text", renpy.text.text.Text, "text", 0, scope=True, replaces=True)
Positional("text")
Keyword("slow")
Keyword("slow_done")
Keyword("substitute")
Keyword("scope")
add(ui_properties)
add(position_properties)
add(text_properties)

DisplayableParser("hbox", renpy.display.layout.MultiBox, "hbox", many, default_keywords={ 'layout' : 'horizontal' })
add(ui_properties)
add(position_properties)
add(box_properties)

DisplayableParser("vbox", renpy.display.layout.MultiBox, "vbox", many, default_keywords={ 'layout' : 'vertical' })
add(ui_properties)
add(position_properties)
add(box_properties)

DisplayableParser("fixed", renpy.display.layout.MultiBox, "fixed", many, default_keywords={ 'layout' : 'fixed' })
add(ui_properties)
add(position_properties)
add(box_properties)

DisplayableParser("grid", renpy.display.layout.Grid, "grid", many)
Positional("cols")
Positional("rows")
Keyword("transpose")
Style("spacing")
add(ui_properties)
add(position_properties)

DisplayableParser("side", renpy.display.layout.Side, "side", many)
Positional("positions")
Style("spacing")
add(ui_properties)
add(position_properties)

# Omit sizer, as we can always just put an xmaximum and ymaximum on an item.

for name in [ "window", "frame" ]:
    DisplayableParser(name, renpy.display.layout.Window, name, 1)
    add(ui_properties)
    add(position_properties)
    add(window_properties)

DisplayableParser("key", renpy.ui._key, None, 0)
Positional("key")
Keyword("action")

DisplayableParser("timer", renpy.display.behavior.Timer, "default", 0, replaces=True)
Positional("delay")
Keyword("action")
Keyword("repeat")

# Omit behaviors.
# Omit menu as being too high-level.

DisplayableParser("input", renpy.display.behavior.Input, "input", 0, replaces=True)
Keyword("default")
Keyword("length")
Keyword("allow")
Keyword("exclude")
Keyword("prefix")
Keyword("suffix")
Keyword("changed")
Keyword("pixel_width")
add(ui_properties)
add(position_properties)
add(text_properties)

DisplayableParser("image", renpy.display.im.image, "default", 0)
Positional("im")

# Omit imagemap_compat for being too high level (and obsolete).

DisplayableParser("button", renpy.display.behavior.Button, "button", 1)
Keyword("action")
Keyword("clicked")
Keyword("hovered")
Keyword("unhovered")
Keyword("alternate")
add(ui_properties)
add(position_properties)
add(window_properties)
add(button_properties)

DisplayableParser("imagebutton", renpy.ui._imagebutton, "image_button", 0)
Keyword("auto")
Keyword("idle")
Keyword("hover")
Keyword("insensitive")
Keyword("selected_idle")
Keyword("selected_hover")
Keyword("selected_insensitive")
Keyword("action")
Keyword("clicked")
Keyword("hovered")
Keyword("unhovered")
Keyword("alternate")
Keyword("image_style")
add(ui_properties)
add(position_properties)
add(window_properties)
add(button_properties)

DisplayableParser("textbutton", renpy.ui._textbutton, 0, scope=True)
Positional("label")
Keyword("action")
Keyword("clicked")
Keyword("hovered")
Keyword("unhovered")
Keyword("alternate")
Keyword("text_style")
Keyword("substitute")
Keyword("scope")
add(ui_properties)
add(position_properties)
add(window_properties)
add(button_properties)
add(text_position_properties)
add(text_text_properties)

DisplayableParser("label", renpy.ui._label, "label", 0, scope=True)
Positional("label")
Keyword("text_style")
add(ui_properties)
add(position_properties)
add(window_properties)
add(text_position_properties)
add(text_text_properties)

def sl2bar(context=None, **properties):
    range = 1 #@ReservedAssignment
    value = 0
    width = None
    height = None

    if "width" in properties:
        width = properties.pop("width")
    if "height" in properties:
        height  = properties.pop("height")
    if "range" in properties:
        range = properties.pop("range") #@ReservedAssignment
    if "value" in properties:
        value = properties.pop("value")

    if "style" not in properties:
        if isinstance(value, renpy.ui.BarValue):
            style = context.style_prefix + value.get_style()[0]
            properties["style"] = style

    return renpy.display.behavior.Bar(range, value, width, height, vertical=False, **properties)

DisplayableParser("bar", sl2bar, None, 0, replaces=True, pass_context=True)
Keyword("adjustment")
Keyword("range")
Keyword("value")
Keyword("changed")
Keyword("hovered")
Keyword("unhovered")
add(ui_properties)
add(position_properties)
add(bar_properties)


def sl2vbar(context=None, **properties):
    range = 1 #@ReservedAssignment
    value = 0
    width = None
    height = None

    if "width" in properties:
        width = properties.pop("width")
    if "height" in properties:
        height  = properties.pop("height")
    if "range" in properties:
        range = properties.pop("range") #@ReservedAssignment
    if "value" in properties:
        value = properties.pop("value")

    if "style" not in properties:
        if isinstance(value, renpy.ui.BarValue):
            style = context.style_prefix + value.get_style()[1]
            properties["style"] = style

    return renpy.display.behavior.Bar(range, value, width, height, vertical=True, **properties)

DisplayableParser("vbar", sl2vbar, None, 0, replaces=True, pass_context=True)
Keyword("adjustment")
Keyword("range")
Keyword("value")
Keyword("changed")
Keyword("hovered")
Keyword("unhovered")
add(ui_properties)
add(position_properties)
add(bar_properties)



# Omit autobar. (behavior)

def sl2viewport(**kwargs):
    """
    This converts the output of renpy.ui.viewport into something that
    sl.displayable can use.
    """

    d = renpy.ui.detached()
    vp = renpy.ui.viewport(**kwargs)

    renpy.ui.stack.pop()

    rv = d.child
    rv._main = vp
    rv._composite_parts = list(rv.children)

    return rv

DisplayableParser("viewport", sl2viewport, "viewport", 1, replaces=True)
Keyword("child_size")
Keyword("mousewheel")
Keyword("draggable")
Keyword("edgescroll")
Keyword("xadjustment")
Keyword("yadjustment")
Keyword("xinitial")
Keyword("yinitial")
Keyword("scrollbars")
Style("xminimum")
Style("yminimum")
PrefixStyle("side_", "spacing")
add(ui_properties)
add(position_properties)
add(side_position_properties)

DisplayableParser("imagemap", renpy.ui._imagemap, "imagemap", many, imagemap=True)
Keyword("ground")
Keyword("hover")
Keyword("insensitive")
Keyword("idle")
Keyword("selected_hover")
Keyword("selected_idle")
Keyword("selected_insensitive")
Keyword("auto")
Keyword("alpha")
Keyword("cache")
add(ui_properties)
add(position_properties)

DisplayableParser("hotspot", renpy.ui._hotspot, "hotspot", 1, hotspot=True)
Positional("spot")
Keyword("action")
Keyword("alternate")
Keyword("clicked")
Keyword("hovered")
Keyword("unhovered")
add(ui_properties)
add(position_properties)
add(window_properties)
add(button_properties)

DisplayableParser("hotbar", renpy.ui._hotbar, "hotbar", 0, replaces=True, hotspot=True)
Positional("spot")
Keyword("adjustment")
Keyword("range")
Keyword("value")
add(ui_properties)
add(position_properties)
add(bar_properties)


DisplayableParser("transform", renpy.display.motion.Transform, "transform", 1)
Keyword("at")
Keyword("id")
for i in renpy.atl.PROPERTIES:
    Style(i)

def sl2add(d, replaces=None, **kwargs):
    d = renpy.easy.displayable(d)
    d = d.parameterize('displayable', [ ])

    rv = d

    Transform = renpy.display.motion.Transform

    if kwargs:
        rv = Transform(child=d, **kwargs)

    if isinstance(rv, Transform):
        rv.take_state(replaces)
        rv.take_execution_state(replaces)

    return rv

DisplayableParser("add", sl2add, None, 0, replaces=True)
Positional("im")
Keyword("at")
Keyword("id")
for i in renpy.atl.PROPERTIES:
    Style(i)

DisplayableParser("drag", renpy.display.dragdrop.Drag, "drag", 1, replaces=True)
Keyword("drag_name")
Keyword("draggable")
Keyword("droppable")
Keyword("drag_raise")
Keyword("dragged")
Keyword("dropped")
Keyword("drag_handle")
Keyword("drag_joined")
Keyword("drag_offscreen")
Keyword("clicked")
Keyword("hovered")
Keyword("unhovered")
Keyword("focus_mask")
Style("child")
add(ui_properties)
add(position_properties)

DisplayableParser("draggroup", renpy.display.dragdrop.DragGroup, None, many, replaces=True)
add(ui_properties)
add(position_properties)

DisplayableParser("mousearea", renpy.display.behavior.MouseArea, 0, replaces=True)
Keyword("hovered")
Keyword("unhovered")
Style("focus_mask")
add(ui_properties)
add(position_properties)

DisplayableParser("on", renpy.display.behavior.OnEvent, None, 0)
Positional("event")
Keyword("action")
