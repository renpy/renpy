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

##############################################################################
# Definitions of screen language statements.

from __future__ import division, absolute_import, with_statement, print_function, unicode_literals
from renpy.compat import *

import renpy.display
import renpy.text.text
import renpy.sl2

from renpy.sl2.slparser import Positional, Keyword, Style, PrefixStyle, add
from renpy.sl2.slparser import DisplayableParser, many

from renpy.sl2.slproperties import text_properties, box_properties, window_properties
from renpy.sl2.slproperties import bar_properties, button_properties
from renpy.sl2.slproperties import text_position_properties, text_text_properties
from renpy.sl2.slproperties import side_position_properties
from renpy.sl2.slproperties import scrollbar_bar_properties, scrollbar_position_properties
from renpy.sl2.slproperties import vscrollbar_bar_properties, vscrollbar_position_properties
from renpy.sl2.slproperties import viewport_position_properties, grid_properties


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
            rv.blit(cr, (0, 0), focus=self.condition)
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


DisplayableParser("null", renpy.display.layout.Null, "default", 0)
Keyword("width")
Keyword("height")

DisplayableParser("text", renpy.text.text.Text, "text", 0, scope=True, replaces=True)
Positional("text")
Keyword("slow")
Keyword("slow_done")
Keyword("substitute")
Keyword("scope")
add(text_properties)

DisplayableParser("hbox", renpy.display.layout.MultiBox, "hbox", many, default_keywords={ 'layout' : 'horizontal' })
add(box_properties)

DisplayableParser("vbox", renpy.display.layout.MultiBox, "vbox", many, default_keywords={ 'layout' : 'vertical' })
add(box_properties)

DisplayableParser("fixed", renpy.display.layout.MultiBox, "fixed", many, default_keywords={ 'layout' : 'fixed' })
add(box_properties)

DisplayableParser("grid", renpy.display.layout.Grid, "grid", many)
Positional("cols")
Positional("rows")
Keyword("transpose")
Keyword("allow_underfull")
add(grid_properties)

DisplayableParser("side", renpy.display.layout.Side, "side", many)
Positional("positions")
Style("spacing")

# Omit sizer, as we can always just put an xmaximum and ymaximum on an item.

for name in [ "window", "frame" ]:
    DisplayableParser(name, renpy.display.layout.Window, name, 1)
    add(window_properties)

DisplayableParser("key", renpy.ui._key, None, 0)
Positional("key")
Keyword("action")
Keyword("activate_sound")

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
Keyword("copypaste")
Keyword("prefix")
Keyword("suffix")
Keyword("changed")
Keyword("pixel_width")
Keyword("value")
Style("caret")
add(text_properties)

# Omit imagemap_compat for being too high level (and obsolete).

DisplayableParser("button", renpy.display.behavior.Button, "button", 1)
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
add(window_properties)
add(button_properties)

DisplayableParser("textbutton", renpy.ui._textbutton, "button", 0, scope=True)
Positional("label")
Keyword("action")
Keyword("clicked")
Keyword("hovered")
Keyword("unhovered")
Keyword("alternate")
Keyword("text_style")
Keyword("substitute")
Keyword("scope")
add(window_properties)
add(button_properties)
add(text_position_properties)
add(text_text_properties)

DisplayableParser("label", renpy.ui._label, "label", 0, scope=True)
Positional("label")
Keyword("text_style")
Keyword("substitute")
add(window_properties)
add(text_position_properties)
add(text_text_properties)


def sl2bar(context=None, **properties):
    range = 1 # @ReservedAssignment
    value = 0
    width = None
    height = None

    if "width" in properties:
        width = properties.pop("width")
    if "height" in properties:
        height = properties.pop("height")
    if "range" in properties:
        range = properties.pop("range") # @ReservedAssignment
    if "value" in properties:
        value = properties.pop("value")

    if "style" not in properties:
        if isinstance(value, renpy.ui.BarValue):
            style = renpy.ui.combine_style(context.style_prefix, value.get_style()[0])
            properties["style"] = style

    return renpy.display.behavior.Bar(range, value, width, height, vertical=False, **properties)


DisplayableParser("bar", sl2bar, None, 0, replaces=True, pass_context=True)
Keyword("adjustment")
Keyword("range")
Keyword("value")
Keyword("changed")
Keyword("hovered")
Keyword("unhovered")
add(bar_properties)


def sl2vbar(context=None, **properties):
    range = 1 # @ReservedAssignment
    value = 0
    width = None
    height = None

    if "width" in properties:
        width = properties.pop("width")
    if "height" in properties:
        height = properties.pop("height")
    if "range" in properties:
        range = properties.pop("range") # @ReservedAssignment
    if "value" in properties:
        value = properties.pop("value")

    if "style" not in properties:
        if isinstance(value, renpy.ui.BarValue):
            style = renpy.ui.combine_style(context.style_prefix, value.get_style()[1])
            properties["style"] = style

    return renpy.display.behavior.Bar(range, value, width, height, vertical=True, **properties)


DisplayableParser("vbar", sl2vbar, None, 0, replaces=True, pass_context=True)
Keyword("adjustment")
Keyword("range")
Keyword("value")
Keyword("changed")
Keyword("hovered")
Keyword("unhovered")
add(bar_properties)

# Omit autobar. (behavior)


def sl2viewport(context=None, **kwargs):
    """
    This converts the output of renpy.ui.viewport into something that
    sl.displayable can use.
    """

    d = renpy.ui.detached()

    if context is not None:
        renpy.ui.stack[-1].style_prefix = context.style_prefix

    vp = renpy.ui.viewport(**kwargs)

    renpy.ui.stack.pop()

    rv = d.child

    if vp is not rv:
        rv._main = vp

    rv._composite_parts = list(rv.children)

    return rv


def sl2vpgrid(context=None, **kwargs):
    """
    This converts the output of renpy.ui.viewport into something that
    sl.displayable can use.
    """

    d = renpy.ui.detached()

    if context is not None:
        renpy.ui.stack[-1].style_prefix = context.style_prefix

    vp = renpy.ui.vpgrid(**kwargs)

    renpy.ui.stack.pop()

    rv = d.child

    if vp is not rv:
        rv._main = vp

    rv._composite_parts = list(rv.children)

    return rv


DisplayableParser("viewport", sl2viewport, "viewport", 1, replaces=True, pass_context=True)
Keyword("child_size")
Keyword("mousewheel")
Keyword("arrowkeys")
Keyword("pagekeys")
Keyword("draggable")
Keyword("edgescroll")
Keyword("xadjustment")
Keyword("yadjustment")
Keyword("xinitial")
Keyword("yinitial")
Keyword("scrollbars")
Keyword("spacing")
Keyword("transpose")
Style("xminimum")
Style("yminimum")
PrefixStyle("side_", "spacing")
add(side_position_properties)
add(scrollbar_position_properties)
add(vscrollbar_position_properties)
add(scrollbar_bar_properties)
add(vscrollbar_bar_properties)
add(viewport_position_properties)

DisplayableParser("vpgrid", sl2vpgrid, "vpgrid", many, replaces=True, pass_context=True)
Keyword("rows")
Keyword("cols")
Keyword("child_size")
Keyword("mousewheel")
Keyword("arrowkeys")
Keyword("pagekeys")
Keyword("draggable")
Keyword("edgescroll")
Keyword("xadjustment")
Keyword("yadjustment")
Keyword("xinitial")
Keyword("yinitial")
Keyword("scrollbars")
Keyword("spacing")
Keyword("transpose")
Style("spacing")
Style("xminimum")
Style("yminimum")
PrefixStyle("side_", "spacing")
add(side_position_properties)
add(scrollbar_position_properties)
add(vscrollbar_position_properties)
add(scrollbar_bar_properties)
add(vscrollbar_bar_properties)
add(viewport_position_properties)
add(grid_properties)

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

DisplayableParser("hotspot", renpy.ui._hotspot, "hotspot", 1, hotspot=True)
Positional("spot")
add(window_properties)
add(button_properties)

DisplayableParser("hotbar", renpy.ui._hotbar, "hotbar", 0, replaces=True, hotspot=True)
Positional("spot")
Keyword("adjustment")
Keyword("range")
Keyword("value")
add(bar_properties)

DisplayableParser("transform", renpy.display.motion.Transform, "transform", 1, default_properties=False)
Keyword("at")
Keyword("id")
for i in renpy.atl.PROPERTIES:
    Style(i)


def sl2add(d, replaces=None, scope=None, **kwargs):

    if d is None:
        return renpy.sl2.slast.NO_DISPLAYABLE

    d = renpy.easy.displayable(d, scope=scope)

    if d._duplicatable:
        d = d._duplicate(None)
        d._unique()

    rv = d

    Transform = renpy.display.motion.Transform

    if (replaces is not None) and isinstance(rv, Transform):
        rv.take_state(replaces)
        rv.take_execution_state(replaces)

    if kwargs:
        rv = Transform(child=d, **kwargs)
        rv._main = d

    return rv


for name in [ "add", "image" ]:
    DisplayableParser(name, sl2add, None, 0, replaces=True, default_properties=False, scope=True)
    Positional("im")
    Keyword("at")
    Keyword("id")
    for i in renpy.atl.PROPERTIES:
        Style(i)

DisplayableParser("drag", renpy.display.dragdrop.Drag, "drag", 1, replaces=True)
Keyword("activated")
Keyword("drag_name")
Keyword("draggable")
Keyword("droppable")
Keyword("drag_raise")
Keyword("dragged")
Keyword("dropped")
Keyword("drop_allowable")
Keyword("drag_handle")
Keyword("drag_joined")
Keyword("drag_offscreen")
Keyword("clicked")
Keyword("hovered")
Keyword("unhovered")
Keyword("focus_mask")
Keyword("mouse_drop")
Keyword("alternate")
Style("child")

DisplayableParser("draggroup", renpy.display.dragdrop.DragGroup, None, many, replaces=True)
Keyword("min_overlap")

DisplayableParser("mousearea", renpy.display.behavior.MouseArea, None, 0, replaces=True)
Keyword("hovered")
Keyword("unhovered")
Style("focus_mask")

DisplayableParser("on", renpy.display.behavior.OnEvent, None, 0)
Positional("event")
Keyword("action")

# Ensure that Parsers are no longer added automatically.
renpy.sl2.slparser.parser = None
