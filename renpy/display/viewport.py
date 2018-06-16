# Copyright 2004-2018 Tom Rothamel <pytom@bishoujo.us>
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

# This file contains classes that handle layout of displayables on
# the screen.

from __future__ import print_function

import renpy.display
import pygame_sdl2 as pygame


def edgescroll_proportional(n):
    """
    An edgescroll function that causes the move speed to be proportional
    from the edge distance.
    """
    return n


class Viewport(renpy.display.layout.Container):

    __version__ = 5

    arrowkeys = False
    pagekeys = False

    def after_upgrade(self, version):
        if version < 1:
            self.xadjustment = renpy.display.behavior.Adjustment(1, 0)
            self.yadjustment = renpy.display.behavior.Adjustment(1, 0)
            self.set_adjustments = False
            self.mousewheel = False
            self.draggable = False
            self.width = 0
            self.height = 0

        if version < 2:
            self.drag_position = None

        if version < 3:
            self.edge_size = False
            self.edge_speed = False
            self.edge_function = None
            self.edge_xspeed = 0
            self.edge_yspeed = 0
            self.edge_last_st = None

        if version < 4:
            self.xadjustment_param = None
            self.yadjustment_param = None
            self.offsets_param = (None, None)
            self.set_adjustments_param = True
            self.xinitial_param = None
            self.yinitial_param = None

        if version < 5:
            self.focusable = self.draggable

    def __init__(self,
                 child=None,
                 child_size=(None, None),
                 offsets=(None, None),
                 xadjustment=None,
                 yadjustment=None,
                 set_adjustments=True,
                 mousewheel=False,
                 draggable=False,
                 edgescroll=None,
                 style='viewport',
                 xinitial=None,
                 yinitial=None,
                 replaces=None,
                 arrowkeys=False,
                 pagekeys=False,
                 **properties):

        super(Viewport, self).__init__(style=style, **properties)
        if child is not None:
            self.add(child)

        self.xadjustment_param = xadjustment
        self.yadjustment_param = yadjustment
        self.offsets_param = offsets
        self.set_adjustments_param = set_adjustments
        self.xinitial_param = xinitial
        self.yinitial_param = yinitial

        self._show()

        if isinstance(replaces, Viewport):
            self.xadjustment.range = replaces.xadjustment.range
            self.yadjustment.range = replaces.yadjustment.range
            self.xadjustment.value = replaces.xadjustment.value
            self.yadjustment.value = replaces.yadjustment.value
            self.xoffset = replaces.xoffset
            self.yoffset = replaces.yoffset
            self.drag_position = replaces.drag_position
        else:
            self.drag_position = None

        self.child_width, self.child_height = child_size

        self.mousewheel = mousewheel
        self.draggable = draggable
        self.arrowkeys = arrowkeys
        self.pagekeys = pagekeys

        # Layout participates in the focus system so drags get migrated.
        self.focusable = draggable or arrowkeys

        self.width = 0
        self.height = 0

        # The speed at which we scroll in the x and y directions, in pixels
        # per second.
        self.edge_xspeed = 0
        self.edge_yspeed = 0

        # The last time we edgescrolled.
        self.edge_last_st = None

        if edgescroll is not None:

            # The size of the edges that trigger scrolling.
            self.edge_size = edgescroll[0]

            # How far from the edge we can scroll.
            self.edge_speed = edgescroll[1]

            if len(edgescroll) >= 3:
                self.edge_function = edgescroll[2]
            else:
                self.edge_function = edgescroll_proportional

        else:
            self.edge_size = 0
            self.edge_speed = 0
            self.edge_function = edgescroll_proportional

    def _show(self):
        if self.xadjustment_param is None:
            self.xadjustment = renpy.display.behavior.Adjustment(1, 0)
        else:
            self.xadjustment = self.xadjustment_param

        if self.yadjustment_param is None:
            self.yadjustment = renpy.display.behavior.Adjustment(1, 0)
        else:
            self.yadjustment = self.yadjustment_param

        if self.xadjustment.adjustable is None:
            self.xadjustment.adjustable = True

        if self.yadjustment.adjustable is None:
            self.yadjustment.adjustable = True

        self.set_adjustments = self.set_adjustments_param

        offsets = self.offsets_param
        self.xoffset = offsets[0] if (offsets[0] is not None) else self.xinitial_param
        self.yoffset = offsets[1] if (offsets[1] is not None) else self.yinitial_param

    def per_interact(self):
        self.xadjustment.register(self)
        self.yadjustment.register(self)

    def update_offsets(self, cw, ch, st):
        """
        This is called by render once we know the width (`cw`) and height (`ch`)
        of all the children. It returns a pair of offsets that should be applied
        to all children.

        It also requires `st`, since hit handles edge scrolling.

        The returned offsets will be negative or zero.
        """

        width = self.width
        height = self.height

        if not self.style.xfill:
            width = min(cw, width)

        if not self.style.yfill:
            height = min(ch, height)

        width = max(width, self.style.xminimum)
        height = max(height, self.style.yminimum)

        if self.set_adjustments:

            xarange = max(cw - width, 0)

            if (self.xadjustment.range != xarange) or (self.xadjustment.page != width):
                self.xadjustment.range = xarange
                self.xadjustment.page = width
                self.xadjustment.update()

            yarange = max(ch - height, 0)

            if (self.yadjustment.range != yarange) or (self.yadjustment.page != height):
                self.yadjustment.range = yarange
                self.yadjustment.page = height
                self.yadjustment.update()

        if self.xoffset is not None:
            if isinstance(self.xoffset, int):
                value = self.xoffset
            else:
                value = max(cw - width, 0) * self.xoffset

            self.xadjustment.value = value

        if self.yoffset is not None:
            if isinstance(self.yoffset, int):
                value = self.yoffset
            else:
                value = max(ch - height, 0) * self.yoffset

            self.yadjustment.value = value

        if self.edge_size and (self.edge_last_st is not None) and (self.edge_xspeed or self.edge_yspeed):

            duration = max(st - self.edge_last_st, 0)
            self.xadjustment.change(self.xadjustment.value + duration * self.edge_xspeed)
            self.yadjustment.change(self.yadjustment.value + duration * self.edge_yspeed)

            self.check_edge_redraw(st)

        cxo = -int(self.xadjustment.value)
        cyo = -int(self.yadjustment.value)

        self._clipping = (cw > width) or (ch > height)

        return cxo, cyo, width, height

    def render(self, width, height, st, at):

        self.width = width
        self.height = height

        child_width = self.child_width or width
        child_height = self.child_height or height

        surf = renpy.display.render.render(self.child, child_width, child_height, st, at)

        cw, ch = surf.get_size()
        cxo, cyo, width, height = self.update_offsets(cw, ch, st)

        self.offsets = [ (cxo, cyo) ]

        rv = renpy.display.render.Render(width, height)
        rv.blit(surf, (cxo, cyo))

        rv = rv.subsurface((0, 0, width, height), focus=True)

        if self.draggable or self.arrowkeys:
            rv.add_focus(self, None, 0, 0, width, height)

        return rv

    def check_edge_redraw(self, st):
        redraw = False

        if (self.edge_xspeed > 0) and (self.xadjustment.value < self.xadjustment.range):
            redraw = True
        if (self.edge_xspeed < 0) and (self.xadjustment.value > 0):
            redraw = True

        if (self.edge_yspeed > 0) and (self.yadjustment.value < self.yadjustment.range):
            redraw = True
        if (self.edge_yspeed < 0) and (self.yadjustment.value > 0):
            redraw = True

        if redraw:
            renpy.display.render.redraw(self, 0)
            self.edge_last_st = st
        else:
            self.edge_last_st = None

    def event(self, ev, x, y, st):

        self.xoffset = None
        self.yoffset = None

        rv = super(Viewport, self).event(ev, x, y, st)

        if rv is not None:
            return rv

        if self.draggable and renpy.display.focus.get_grab() == self:

            oldx, oldy = self.drag_position
            dx = x - oldx
            dy = y - oldy

            self.xadjustment.change(self.xadjustment.value - dx)
            self.yadjustment.change(self.yadjustment.value - dy)

            self.drag_position = (x, y)  # W0201

            if renpy.display.behavior.map_event(ev, 'viewport_drag_end'):
                renpy.display.focus.set_grab(None)
                raise renpy.display.core.IgnoreEvent()

        if not ((0 <= x < self.width) and (0 <= y <= self.height)):
            self.edge_xspeed = 0
            self.edge_yspeed = 0

            inside = False

        else:

            inside = True

        if inside and self.mousewheel:

            if self.mousewheel == "horizontal-change":
                adjustment = self.xadjustment
                change = True
            elif self.mousewheel == "change":
                adjustment = self.yadjustment
                change = True
            elif self.mousewheel == "horizontal":
                adjustment = self.xadjustment
                change = False
            else:
                adjustment = self.yadjustment
                change = False

            if renpy.display.behavior.map_event(ev, 'viewport_up'):

                if change and (adjustment.value == 0):
                    return None

                rv = adjustment.change(adjustment.value - adjustment.step)
                if rv is not None:
                    return rv
                else:
                    raise renpy.display.core.IgnoreEvent()

            if renpy.display.behavior.map_event(ev, 'viewport_down'):

                if change and (adjustment.value == adjustment.range):
                    return None

                rv = adjustment.change(adjustment.value + adjustment.step)
                if rv is not None:
                    return rv
                else:
                    raise renpy.display.core.IgnoreEvent()

        if self.arrowkeys:

            if renpy.display.behavior.map_event(ev, 'viewport_leftarrow'):

                if self.xadjustment.value == 0:
                    return None

                rv = self.xadjustment.change(self.xadjustment.value - self.xadjustment.step)
                if rv is not None:
                    return rv
                else:
                    raise renpy.display.core.IgnoreEvent()

            if renpy.display.behavior.map_event(ev, 'viewport_rightarrow'):

                if self.xadjustment.value == self.xadjustment.range:
                    return None

                rv = self.xadjustment.change(self.xadjustment.value + self.xadjustment.step)
                if rv is not None:
                    return rv
                else:
                    raise renpy.display.core.IgnoreEvent()

            if renpy.display.behavior.map_event(ev, 'viewport_uparrow'):

                if self.yadjustment.value == 0:
                    return None

                rv = self.yadjustment.change(self.yadjustment.value - self.yadjustment.step)
                if rv is not None:
                    return rv
                else:
                    raise renpy.display.core.IgnoreEvent()

            if renpy.display.behavior.map_event(ev, 'viewport_downarrow'):

                if self.yadjustment.value == self.yadjustment.range:
                    return None

                rv = self.yadjustment.change(self.yadjustment.value + self.yadjustment.step)
                if rv is not None:
                    return rv
                else:
                    raise renpy.display.core.IgnoreEvent()

        if self.pagekeys:

            if renpy.display.behavior.map_event(ev, 'viewport_pageup'):

                rv = self.yadjustment.change(self.yadjustment.value - self.yadjustment.page)
                if rv is not None:
                    return rv
                else:
                    raise renpy.display.core.IgnoreEvent()

            if renpy.display.behavior.map_event(ev, 'viewport_pagedown'):

                rv = self.yadjustment.change(self.yadjustment.value + self.yadjustment.page)
                if rv is not None:
                    return rv
                else:
                    raise renpy.display.core.IgnoreEvent()

        if inside and self.draggable:

            if renpy.display.behavior.map_event(ev, 'viewport_drag_start'):

                focused = renpy.display.focus.get_focused()

                if (focused is None) or (focused is self):

                    self.drag_position = (x, y)
                    renpy.display.focus.set_grab(self)
                    raise renpy.display.core.IgnoreEvent()

        if inside and self.edge_size and ev.type in [ pygame.MOUSEMOTION, pygame.MOUSEBUTTONDOWN, pygame.MOUSEBUTTONUP ]:

            def speed(n, zero, one):
                """
                Given a position `n`, computes the speed. The speed is 0.0
                when `n` == `zero`, 1.0 when `n` == `one`, and linearly
                interpolated when between.

                Returns 0.0 when outside the bounds - in either direction.
                """

                n = 1.0 * (n - zero) / (one - zero)

                if n < 0.0:
                    return 0.0
                if n > 1.0:
                    return 0.0

                return n

            xspeed = speed(x, self.width - self.edge_size, self.width)
            xspeed -= speed(x, self.edge_size, 0)
            self.edge_xspeed = self.edge_speed * self.edge_function(xspeed)

            yspeed = speed(y, self.height - self.edge_size, self.height)
            yspeed -= speed(y, self.edge_size, 0)
            self.edge_yspeed = self.edge_speed * self.edge_function(yspeed)

            if xspeed or yspeed:
                self.check_edge_redraw(st)
            else:
                self.edge_last_st = None

        return None

    def set_xoffset(self, offset):
        self.xoffset = offset
        renpy.display.render.redraw(self, 0)

    def set_yoffset(self, offset):
        self.yoffset = offset
        renpy.display.render.redraw(self, 0)


# For compatibility with old saves.
renpy.display.layout.Viewport = Viewport


class VPGrid(Viewport):

    __version__ = Viewport.__version__

    def __init__(self, cols=None, rows=None, transpose=None, style="vpgrid", **properties):

        super(VPGrid, self).__init__(style=style, **properties)

        if (rows is None) and (cols is None):
            raise Exception("A VPGrid must be given the rows or cols property.")

        if (rows is not None) and (cols is None) and (transpose is None):
            transpose = True

        self.grid_cols = cols
        self.grid_rows = rows
        self.grid_transpose = transpose

    def render(self, width, height, st, at):

        self.width = width
        self.height = height

        child_width = self.child_width or width
        child_height = self.child_height or height

        if not self.children:
            self.offsets = [ ]
            return renpy.display.render.Render(0, 0)

        # The number of children.
        lc = len(self.children)

        # Figure out the number of columns and rows.
        cols = self.grid_cols
        rows = self.grid_rows

        if cols is None:
            cols = lc // rows
            if rows * cols < lc:
                cols += 1

        if rows is None:
            rows = lc // cols
            if rows * cols < lc:
                rows += 1

        # Determine the total size.
        xspacing = self.style.xspacing
        yspacing = self.style.yspacing

        if xspacing is None:
            xspacing = self.style.spacing
        if yspacing is None:
            yspacing = self.style.spacing

        rend = renpy.display.render.render(self.children[0], child_width, child_height, st, at)
        cw, ch = rend.get_size()

        tw = (cw + xspacing) * cols - xspacing
        th = (ch + yspacing) * rows - yspacing

        if self.style.xfill:
            tw = child_width
            cw = (tw - (cols - 1) * xspacing) / cols

        if self.style.yfill:
            th = child_height
            ch = (th - (rows - 1) * yspacing) / rows

        cxo, cyo, width, height = self.update_offsets(tw, th, st)

        self.offsets = [ ]

        # Render everything.
        rv = renpy.display.render.Render(width, height)

        for index, c in enumerate(self.children):

            if self.grid_transpose:
                x = index // rows
                y = index % rows
            else:
                x = index % cols
                y = index // cols

            x = x * (cw + xspacing) + cxo
            y = y * (ch + yspacing) + cyo

            if x + cw < 0:
                self.offsets.append((x, y))
                continue

            if y + ch < 0:
                self.offsets.append((x, y))
                continue

            if x >= width:
                self.offsets.append((x, y))
                continue

            if y >= height:
                self.offsets.append((x, y))
                continue

            surf = renpy.display.render.render(c, cw, ch, st, at)
            pos = c.place(rv, x, y, cw, ch, surf)

            self.offsets.append(pos)

        rv = rv.subsurface((0, 0, width, height), focus=True)

        if self.draggable or self.arrowkeys:
            rv.add_focus(self, None, 0, 0, width, height)

        return rv
