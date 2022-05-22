# Copyright 2004-2022 Tom Rothamel <pytom@bishoujo.us>
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

from __future__ import division, absolute_import, with_statement, print_function, unicode_literals
from renpy.compat import PY2, basestring, bchr, bord, chr, open, pystr, range, round, str, tobytes, unicode # *


import math

import pygame_sdl2 as pygame
import renpy


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

        if xadjustment is None:
            self.xadjustment = renpy.display.behavior.Adjustment(1, 0)
        else:
            self.xadjustment = xadjustment

        if yadjustment is None:
            self.yadjustment = renpy.display.behavior.Adjustment(1, 0)
        else:
            self.yadjustment = yadjustment

        if self.xadjustment.adjustable is None:
            self.xadjustment.adjustable = True

        if self.yadjustment.adjustable is None:
            self.yadjustment.adjustable = True

        self.set_adjustments = set_adjustments

        self.xoffset = offsets[0] if (offsets[0] is not None) else xinitial
        self.yoffset = offsets[1] if (offsets[1] is not None) else yinitial

        if isinstance(replaces, Viewport) and replaces.offsets:
            self.xadjustment.range = replaces.xadjustment.range
            self.xadjustment.value = replaces.xadjustment.value
            self.yadjustment.range = replaces.yadjustment.range
            self.yadjustment.value = replaces.yadjustment.value
            self.xoffset = replaces.xoffset
            self.yoffset = replaces.yoffset
            self.drag_position = replaces.drag_position
        else:
            self.drag_position = None # type: tuple[int, int]|None

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

        cw = int(math.ceil(cw))
        ch = int(math.ceil(ch))

        width = self.width
        height = self.height

        xminimum, yminimum = renpy.display.layout.xyminimums(self.style, width, height)

        if not self.style.xfill:
            width = min(cw, width)

        if not self.style.yfill:
            height = min(ch, height)

        width = max(width, xminimum)
        height = max(height, yminimum)

        if (not renpy.display.render.sizing) and self.set_adjustments:

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

        self.width = width
        self.height = height

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

    def check_edge_redraw(self, st, reset_st=True):
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
            if reset_st or self.edge_last_st is None:
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

            old_xvalue = self.xadjustment.value
            old_yvalue = self.yadjustment.value

            if renpy.display.behavior.map_event(ev, 'viewport_drag_end'):
                renpy.display.focus.set_grab(None)

                # Invoke rounding adjustment on viewport release
                xvalue = self.xadjustment.round_value(old_xvalue, release=True)
                self.xadjustment.change(xvalue)
                yvalue = self.yadjustment.round_value(old_yvalue, release=True)
                self.yadjustment.change(yvalue)
                raise renpy.display.core.IgnoreEvent()

            oldx, oldy = self.drag_position # type: ignore
            dx = x - oldx
            dy = y - oldy

            new_xvalue = self.xadjustment.round_value(old_xvalue - dx, release=False)
            if old_xvalue == new_xvalue:
                newx = oldx
            else:
                self.xadjustment.change(new_xvalue)
                newx = x

            new_yvalue = self.yadjustment.round_value(old_yvalue - dy, release=False)
            if old_yvalue == new_yvalue:
                newy = oldy
            else:
                self.yadjustment.change(new_yvalue)
                newy = y

            self.drag_position = (newx, newy) # W0201

        if not ((0 <= x < self.width) and (0 <= y <= self.height)):
            self.edge_xspeed = 0
            self.edge_yspeed = 0
            self.edge_last_st = None

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

            if renpy.display.behavior.map_event(ev, 'viewport_wheelup'):

                if change and (adjustment.value == 0):
                    return None

                rv = adjustment.change(adjustment.value - adjustment.step)
                if rv is not None:
                    return rv
                else:
                    raise renpy.display.core.IgnoreEvent()

            if renpy.display.behavior.map_event(ev, 'viewport_wheeldown'):

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
                self.check_edge_redraw(st, reset_st=False)
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
renpy.display.layout.Viewport = Viewport # type: ignore


class VPGrid(Viewport):

    __version__ = Viewport.__version__

    allow_underfull = None

    def __init__(self, cols=None, rows=None,
                 transpose=None,
                 style="vpgrid",
                 allow_underfull=None,
                 **properties):

        super(VPGrid, self).__init__(style=style, **properties)

        if (rows is None) and (cols is None):
            raise Exception("A VPGrid must be given the rows or cols property.")

        if (rows is not None) and (cols is None) and (transpose is None):
            transpose = True

        self.grid_cols = cols
        self.grid_rows = rows
        self.grid_transpose = transpose
        self.allow_underfull = allow_underfull

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
            cols = lc // rows # type: ignore
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

        left_margin = renpy.display.layout.scale(self.style.left_margin, width)
        right_margin = renpy.display.layout.scale(self.style.right_margin, width)
        top_margin = renpy.display.layout.scale(self.style.top_margin, height)
        bottom_margin = renpy.display.layout.scale(self.style.bottom_margin, height)

        rend = renpy.display.render.render(self.children[0], child_width, child_height, st, at)
        cw, ch = rend.get_size()

        tw = (cw + xspacing) * cols - xspacing + left_margin + right_margin
        th = (ch + yspacing) * rows - yspacing + top_margin + bottom_margin

        if self.style.xfill:
            tw = child_width
            cw = (tw - (cols - 1) * xspacing - left_margin - right_margin) // cols

        if self.style.yfill:
            th = child_height
            ch = (th - (rows - 1) * yspacing - top_margin - bottom_margin) // rows

        cxo, cyo, width, height = self.update_offsets(tw, th, st)
        cxo += left_margin
        cyo += top_margin

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

    def add(self, d):
        super(VPGrid, self).add(d)

        if None not in (self.grid_cols, self.grid_rows):
            if len(self.children) > (self.grid_cols * self.grid_rows):
                if not renpy.config.allow_unfull_vpgrids:
                    raise Exception("VPGrid overfull.")

    def per_interact(self):
        super(VPGrid, self).per_interact()

        exc = None
        delta = 0

        if None not in (self.grid_cols, self.grid_rows):
            delta = (self.grid_cols * self.grid_rows) - len(self.children)
            if delta > 0:
                exc = Exception("VPGrid not completely full.")

        else:
            given = self.grid_cols or self.grid_rows
            if given: # ignore the case where one is 0 - cannot be underfull
                delta = given - (len(self.children) % given)
                # the number of aditional children needed to complete
                # within [1, given], `given` being all right
                if delta < given:
                    exc = Exception("VPGrid not completely full, needs a multiple of {} children.".format(given))

        if exc is not None:
            allow_underfull = self.allow_underfull
            if allow_underfull is None:
                allow_underfull = renpy.config.allow_underfull_grids or renpy.config.allow_unfull_vpgrids

            if not renpy.config.developer:
                allow_underfull = True

            if not allow_underfull:
                raise exc

            for _ in range(delta):
                self.add(renpy.display.layout.Null())
