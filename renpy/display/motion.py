# Copyright 2004-2024 Tom Rothamel <pytom@bishoujo.us>
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

# This file contains displayables that move, zoom, rotate, or otherwise
# transform displayables. (As well as displayables that support them.)

from __future__ import division, absolute_import, with_statement, print_function, unicode_literals
from renpy.compat import PY2, basestring, bchr, bord, chr, open, pystr, range, round, str, tobytes, unicode # *


import math

import renpy
from renpy.display.render import render
from renpy.display.layout import Container

# Some imports are here to handle pickles of a moved class.
from renpy.display.transform import Transform, Proxy, TransformState, ATLTransform, null  # @UnusedImport


class Motion(Container):
    """
    This is used to move a child displayable around the screen. It
    works by supplying a time value to a user-supplied function,
    which is in turn expected to return a pair giving the x and y
    location of the upper-left-hand corner of the child, or a
    4-tuple giving that and the xanchor and yanchor of the child.

    The time value is a floating point number that ranges from 0 to
    1. If repeat is True, then the motion repeats every period
    sections. (Otherwise, it stops.) If bounce is true, the
    time value varies from 0 to 1 to 0 again.

    The function supplied needs to be pickleable, which means it needs
    to be defined as a name in an init block. It cannot be a lambda or
    anonymous inner function. If you can get away with using Pan or
    Move, use them instead.

    Please note that floats and ints are interpreted as for xpos and
    ypos, with floats being considered fractions of the screen.
    """

    def __init__(self, function, period, child=None, new_widget=None, old_widget=None, repeat=False, bounce=False, delay=None, anim_timebase=False, tag_start=None, time_warp=None, add_sizes=False, style='motion', **properties):
        """
        @param child: The child displayable.

        @param new_widget: If child is None, it is set to new_widget,
        so that we can speak the transition protocol.

        @param old_widget: Ignored, for compatibility with the transition protocol.

        @param function: A function that takes a floating point value and returns
        an xpos, ypos tuple.

        @param period: The amount of time it takes to go through one cycle, in seconds.

        @param repeat: Should we repeat after a period is up?

        @param bounce: Should we bounce?

        @param delay: How long this motion should take. If repeat is None, defaults to period.

        @param anim_timebase: If True, use the animation timebase rather than the shown timebase.

        @param time_warp: If not None, this is a function that takes a
        fraction of the period (between 0.0 and 1.0), and returns a
        new fraction of the period. Use this to warp time, applying
        acceleration and deceleration to motions.

        This can also be used as a transition. When used as a
        transition, the motion is applied to the new_widget for delay
        seconds.
        """

        if child is None:
            child = new_widget

        if delay is None and not repeat:
            delay = period

        super(Motion, self).__init__(style=style, **properties)

        if child is not None:
            self.add(child)

        self.function = function
        self.period = period
        self.repeat = repeat
        self.bounce = bounce
        self.delay = delay
        self.anim_timebase = anim_timebase
        self.time_warp = time_warp
        self.add_sizes = add_sizes

        self.position = None

    def update_position(self, t, sizes):

        if renpy.game.less_updates:
            if self.delay:
                t = self.delay
                if self.repeat:
                    t = t % self.period
            else:
                t = self.period
        elif self.delay and t >= self.delay:
            t = self.delay
            if self.repeat:
                t = t % self.period
        elif self.repeat:
            t = t % self.period
            renpy.display.render.redraw(self, 0)
        else:
            if t > self.period:
                t = self.period
            else:
                renpy.display.render.redraw(self, 0)

        if self.period > 0:
            t /= self.period
        else:
            t = 1

        if self.time_warp:
            t = self.time_warp(t)

        if self.bounce:
            t = t * 2
            if t > 1.0:
                t = 2.0 - t

        if self.add_sizes:
            res = self.function(t, sizes)
        else:
            res = self.function(t)

        res = tuple(res)

        if len(res) == 2:
            self.position = res + (self.style.xanchor or 0, self.style.yanchor or 0)
        else:
            self.position = res

    def get_placement(self):

        if self.position is None:
            if self.add_sizes:
                # Almost certainly gives the wrong placement, but there's nothing
                # we can do.
                return super(Motion, self).get_placement()
            else:
                self.update_position(0.0, None)

        return self.position + (self.style.xoffset, self.style.yoffset, self.style.subpixel)

    def render(self, width, height, st, at):

        if self.anim_timebase:
            t = at
        else:
            t = st

        child = render(self.child, width, height, st, at)
        cw, ch = child.get_size()

        self.update_position(t, (width, height, cw, ch))

        rv = renpy.display.render.Render(cw, ch)
        rv.blit(child, (0, 0))

        self.offsets = [ (0, 0) ]

        return rv


class Interpolate(object):

    anchors = {
        'top' : 0.0,
        'center' : 0.5,
        'bottom' : 1.0,
        'left' : 0.0,
        'right' : 1.0,
        }

    def __init__(self, start, end):

        if len(start) != len(end):
            raise Exception("The start and end must have the same number of arguments.")

        self.start = [ self.anchors.get(i, i) for i in start ]
        self.end = [ self.anchors.get(i, i) for i in end ]

    def __call__(self, t, sizes=(None, None, None, None)):

        return renpy.atl.interpolate(t, tuple(self.start), tuple(self.end), renpy.atl.position_or_none)


def Pan(startpos, endpos, time, child=None, repeat=False, bounce=False,
        anim_timebase=False, style='motion', time_warp=None, **properties):
    """
    This is used to pan over a child displayable, which is almost
    always an image. It works by interpolating the placement of the
    upper-left corner of the screen, over time. It's only really
    suitable for use with images that are larger than the screen,
    and we don't do any cropping on the image.

    @param startpos: The initial coordinates of the upper-left
    corner of the screen, relative to the image.

    @param endpos: The coordinates of the upper-left corner of the
    screen, relative to the image, after time has elapsed.

    @param time: The time it takes to pan from startpos to endpos.

    @param child: The child displayable.

    @param repeat: True if we should repeat this forever.

    @param bounce: True if we should bounce from the start to the end
    to the start.

    @param anim_timebase: True if we use the animation timebase, False to use the
    displayable timebase.

    @param time_warp: If not None, this is a function that takes a
    fraction of the period (between 0.0 and 1.0), and returns a
    new fraction of the period. Use this to warp time, applying
    acceleration and deceleration to motions.

    This can be used as a transition. See Motion for details.
    """

    x0, y0 = startpos
    x1, y1 = endpos

    return Motion(Interpolate((-x0, -y0), (-x1, -y1)),
                  time,
                  child,
                  repeat=repeat,
                  bounce=bounce,
                  style=style,
                  anim_timebase=anim_timebase,
                  time_warp=time_warp,
                  **properties)


def Move(startpos, endpos, time, child=None, repeat=False, bounce=False,
         anim_timebase=False, style='motion', time_warp=None, **properties):
    """
    This is used to pan over a child displayable relative to
    the containing area. It works by interpolating the placement of the
    the child, over time.

    @param startpos: The initial coordinates of the child
    relative to the containing area.

    @param endpos: The coordinates of the child at the end of the
    move.

    @param time: The time it takes to move from startpos to endpos.

    @param child: The child displayable.

    @param repeat: True if we should repeat this forever.

    @param bounce: True if we should bounce from the start to the end
    to the start.

    @param anim_timebase: True if we use the animation timebase, False to use the
    displayable timebase.

    @param time_warp: If not None, this is a function that takes a
    fraction of the period (between 0.0 and 1.0), and returns a
    new fraction of the period. Use this to warp time, applying
    acceleration and deceleration to motions.

    This can be used as a transition. See Motion for details.
    """

    return Motion(Interpolate(startpos, endpos),
                  time,
                  child,
                  repeat=repeat,
                  bounce=bounce,
                  anim_timebase=anim_timebase,
                  style=style,
                  time_warp=time_warp,
                  **properties)


class Revolver(object):

    def __init__(self, start, end, child, around=(0.5, 0.5), cor=(0.5, 0.5), pos=None):
        self.start = start
        self.end = end
        self.around = around
        self.cor = cor
        self.pos = pos
        self.child = child

    def __call__(self, t, rect):
        absolute = renpy.display.core.absolute

        (w, h, cw, ch) = rect

        # Converts a float to an integer in the given range, passes
        # integers through unchanged.
        def fti(x, r):
            if x is None:
                x = 0

            return absolute.compute_raw(x, r)

        if self.pos is None:
            pos = self.child.get_placement()
        else:
            pos = self.pos

        xpos, ypos, xanchor, yanchor, _xoffset, _yoffset, _subpixel = pos

        xpos = fti(xpos, w)
        ypos = fti(ypos, h)
        xanchor = fti(xanchor, cw)
        yanchor = fti(yanchor, ch)

        xaround, yaround = self.around

        xaround = fti(xaround, w)
        yaround = fti(yaround, h)

        xcor, ycor = self.cor

        xcor = fti(xcor, cw)
        ycor = fti(ycor, ch)

        angle = self.start + (self.end - self.start) * t
        angle *= math.pi / 180

        # The center of rotation, relative to the xaround.
        x = xpos - xanchor + xcor - xaround
        y = ypos - yanchor + ycor - yaround

        # Rotate it.
        nx = x * math.cos(angle) - y * math.sin(angle)
        ny = x * math.sin(angle) + y * math.cos(angle)

        # Project it back.
        nx = nx - xcor + xaround
        ny = ny - ycor + yaround

        return (absolute(nx), absolute(ny), 0, 0)


def Revolve(start, end, time, child, around=(0.5, 0.5), cor=(0.5, 0.5), pos=None, **properties):

    return Motion(Revolver(start, end, child, around=around, cor=cor, pos=pos),
                  time,
                  child,
                  add_sizes=True,
                  **properties)


def zoom_render(crend, x, y, w, h, zw, zh, bilinear):
    """
    This creates a render that zooms its child.

    `crend` - The render of the child.
    `x`, `y`, `w`, `h` - A rectangle inside the child.
    `zw`, `zh` - The size the rectangle is rendered to.
    `bilinear` - Should we be rendering in bilinear mode?
    """

    rv = renpy.display.render.Render(zw, zh)

    if zw == 0 or zh == 0 or w == 0 or h == 0:
        return rv

    rv.forward = renpy.display.matrix.Matrix2D(w / zw, 0, 0, h / zh)
    rv.reverse = renpy.display.matrix.Matrix2D(zw / w, 0, 0, zh / h)

    rv.xclipping = True
    rv.yclipping = True

    rv.blit(crend, rv.reverse.transform(-x, -y))

    return rv


class ZoomCommon(renpy.display.displayable.Displayable):

    def __init__(self,
                 time, child,
                 end_identity=False,
                 after_child=None,
                 time_warp=None,
                 bilinear=True,
                 opaque=True,
                 anim_timebase=False,
                 repeat=False,
                 style='motion',
                 **properties):
        """
        @param time: The amount of time it will take to
        interpolate from the start to the end rectange.

        @param child: The child displayable.

        @param after_child: If present, a second child
        widget. This displayable will be rendered after the zoom
        completes. Use this to snap to a sharp displayable after
        the zoom is done.

        @param time_warp: If not None, this is a function that takes a
        fraction of the period (between 0.0 and 1.0), and returns a
        new fraction of the period. Use this to warp time, applying
        acceleration and deceleration to motions.
        """

        super(ZoomCommon, self).__init__(style=style, **properties)

        child = renpy.easy.displayable(child)

        self.time = time
        self.child = child
        self.repeat = repeat

        if after_child:
            self.after_child = renpy.easy.displayable(after_child)
        else:
            if end_identity:
                self.after_child = child
            else:
                self.after_child = None

        self.time_warp = time_warp
        self.bilinear = bilinear
        self.opaque = opaque
        self.anim_timebase = anim_timebase

    def visit(self):
        return [ self.child, self.after_child ]

    def zoom_rectangle(self, done, width, height): # type: (ZoomCommon, float, float, float) -> tuple[int, int, int, int, int, int]
        raise Exception("Zoom rectangle not implemented.")

    def render(self, width, height, st, at):

        if self.anim_timebase:
            t = at
        else:
            t = st

        if self.time:
            done = min(t / self.time, 1.0)
        else:
            done = 1.0

        if self.repeat:
            done = done % 1.0

        if renpy.game.less_updates:
            done = 1.0

        self.done = done

        if self.after_child and done == 1.0:
            return renpy.display.render.render(self.after_child, width, height, st, at)

        if self.time_warp:
            done = self.time_warp(done)

        rend = renpy.display.render.render(self.child, width, height, st, at)

        rx, ry, rw, rh, zw, zh = self.zoom_rectangle(done, rend.width, rend.height)

        if rx < 0 or ry < 0 or rx + rw > rend.width or ry + rh > rend.height:
            raise Exception("Zoom rectangle %r falls outside of %dx%d parent surface." % ((rx, ry, rw, rh), rend.width, rend.height))

        rv = zoom_render(rend, rx, ry, rw, rh, zw, zh, self.bilinear)

        if self.done < 1.0:
            renpy.display.render.redraw(self, 0)

        return rv

    def event(self, ev, x, y, st):

        if not self.time:
            done = 1.0
        else:
            done = min(st / self.time, 1.0)

        if done == 1.0 and self.after_child:
            return self.after_child.event(ev, x, y, st)
        else:
            return None


class Zoom(ZoomCommon):

    def __init__(self, size, start, end, time, child, **properties):

        end_identity = (end == (0.0, 0.0) + size)

        super(Zoom, self).__init__(time, child, end_identity=end_identity, **properties)

        self.size = size
        self.start = start
        self.end = end

    def zoom_rectangle(self, done, width, height):

        rx, ry, rw, rh = [ (a + (b - a) * done) for a, b in zip(self.start, self.end) ] # type: ignore

        return rx, ry, rw, rh, self.size[0], self.size[1]


class FactorZoom(ZoomCommon):

    def __init__(self, start, end, time, child, **properties):

        end_identity = (end == 1.0)

        super(FactorZoom, self).__init__(time, child, end_identity=end_identity, **properties)

        self.start = start
        self.end = end

    def zoom_rectangle(self, done, width, height):

        factor = self.start + (self.end - self.start) * done

        return 0, 0, width, height, factor * width, factor * height


class SizeZoom(ZoomCommon):

    def __init__(self, start, end, time, child, **properties):

        end_identity = False

        super(SizeZoom, self).__init__(time, child, end_identity=end_identity, **properties)

        self.start = start
        self.end = end

    def zoom_rectangle(self, done, width, height):

        sw, sh = self.start
        ew, eh = self.end

        zw = sw + (ew - sw) * done
        zh = sh + (eh - sh) * done

        return 0, 0, width, height, zw, zh


class RotoZoom(renpy.display.displayable.Displayable):

    transform = None

    def __init__(self,
                 rot_start,
                 rot_end,
                 rot_delay,
                 zoom_start,
                 zoom_end,
                 zoom_delay,
                 child,
                 rot_repeat=False,
                 zoom_repeat=False,
                 rot_bounce=False,
                 zoom_bounce=False,
                 rot_anim_timebase=False,
                 zoom_anim_timebase=False,
                 rot_time_warp=None,
                 zoom_time_warp=None,
                 opaque=False,
                 style='motion',
                 **properties):

        super(RotoZoom, self).__init__(style=style, **properties)

        self.rot_start = rot_start
        self.rot_end = rot_end
        self.rot_delay = rot_delay

        self.zoom_start = zoom_start
        self.zoom_end = zoom_end
        self.zoom_delay = zoom_delay

        self.child = renpy.easy.displayable(child)

        self.rot_repeat = rot_repeat
        self.zoom_repeat = zoom_repeat

        self.rot_bounce = rot_bounce
        self.zoom_bounce = zoom_bounce

        self.rot_anim_timebase = rot_anim_timebase
        self.zoom_anim_timebase = zoom_anim_timebase

        self.rot_time_warp = rot_time_warp
        self.zoom_time_warp = zoom_time_warp

        self.opaque = opaque

    def visit(self):
        return [ self.child ]

    def render(self, width, height, st, at):

        if self.rot_anim_timebase:
            rot_time = at
        else:
            rot_time = st

        if self.zoom_anim_timebase:
            zoom_time = at
        else:
            zoom_time = st

        if self.rot_delay == 0:
            rot_time = 1.0
        else:
            rot_time /= self.rot_delay

        if self.zoom_delay == 0:
            zoom_time = 1.0
        else:
            zoom_time /= self.zoom_delay

        if self.rot_repeat:
            rot_time %= 1.0

        if self.zoom_repeat:
            zoom_time %= 1.0

        if self.rot_bounce:
            rot_time *= 2
            rot_time = min(rot_time, 2.0 - rot_time)

        if self.zoom_bounce:
            zoom_time *= 2
            zoom_time = min(zoom_time, 2.0 - zoom_time)

        if renpy.game.less_updates:
            rot_time = 1.0
            zoom_time = 1.0

        rot_time = min(rot_time, 1.0)
        zoom_time = min(zoom_time, 1.0)

        if self.rot_time_warp:
            rot_time = self.rot_time_warp(rot_time)

        if self.zoom_time_warp:
            zoom_time = self.zoom_time_warp(zoom_time)

        angle = self.rot_start + (1.0 * self.rot_end - self.rot_start) * rot_time
        zoom = self.zoom_start + (1.0 * self.zoom_end - self.zoom_start) * zoom_time
        # angle = -angle * math.pi / 180

        zoom = max(zoom, 0.001)

        if self.transform is None:
            self.transform = Transform(self.child)

        self.transform.rotate = angle # type: ignore
        self.transform.zoom = zoom # type: ignore

        rv = renpy.display.render.render(self.transform, width, height, st, at)

        if rot_time <= 1.0 or zoom_time <= 1.0:
            renpy.display.render.redraw(self.transform, 0)

        return rv


# For compatibility with old games.
renpy.display.layout.Transform = Transform # type: ignore
renpy.display.layout.RotoZoom = RotoZoom # type: ignore
renpy.display.layout.SizeZoom = SizeZoom # type: ignore
renpy.display.layout.FactorZoom = FactorZoom # type: ignore
renpy.display.layout.Zoom = Zoom # type: ignore
renpy.display.layout.Revolver = Revolver # type: ignore
renpy.display.layout.Motion = Motion # type: ignore
renpy.display.layout.Interpolate = Interpolate  # type: ignore

# Leave these functions around - they might have been pickled somewhere.
renpy.display.layout.Revolve = Revolve  # type: ignore
renpy.display.layout.Move = Move  # type: ignore
renpy.display.layout.Pan = Pan  # type: ignore
