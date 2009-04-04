# Copyright 2004-2009 PyTom <pytom@bishoujo.us>
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

import time
import math

import pygame
from pygame.constants import *

import renpy
from renpy.display.render import render, IDENTITY, Matrix2D
from renpy.display.layout import Container


class Transform(Container):

    def __init__(self, child=None, function=None, alpha=1, rotate=None, zoom=1, xzoom=1, yzoom=1, **kwargs):

        # NOTE: When adding new parameters here, be sure they're
        # also used in called.
        
        self.kwargs = kwargs
        self.kwargs.setdefault('style', 'transform')
        
        super(Transform, self).__init__(**self.kwargs)

        self.function = function

        # Taken from the style by default.
        if child is not None:
            self.add(child)

        self.xpos = None
        self.ypos = None
        self.xanchor = None
        self.yanchor = None        

        # Taken from parameters.
        self.alpha = alpha
        self.rotate = rotate
        self.zoom = zoom
        self.xzoom = xzoom
        self.yzoom = yzoom

        # This is the matrix transforming our coordinates into child coordinates.
        self.forward = None

    def render(self, width, height, st, at):

        if self.function is not None:
            fr = self.function(self, st, at)

            if fr is not None:
                renpy.display.render.redraw(self, fr)
        
        cr = render(self.child, width, height, st, at)
        width, height = cr.get_size()

        forward = IDENTITY
        reverse = IDENTITY
        xo = yo = 0
        
        # Rotation first.
        if self.rotate is not None:

            cw = width
            ch = height
            
            width = height = math.hypot(cw, ch)
            angle = -self.rotate * math.pi / 180
        
            xdx = math.cos(angle)
            xdy = -math.sin(angle)
            ydx = -xdy 
            ydy = xdx 

            forward = Matrix2D(xdx, xdy, ydx, ydy)

            xdx = math.cos(-angle)
            xdy = -math.sin(-angle)
            ydx = -xdy 
            ydy = xdx 

            reverse = Matrix2D(xdx, xdy, ydx, ydy)

            xo, yo = reverse.transform(-cw / 2.0, -ch / 2.0)
            xo += width / 2.0
            yo += height / 2.0

        if self.zoom != 1 or self.xzoom != 1 or self.yzoom != None:
            xzoom = self.zoom * self.xzoom
            yzoom = self.zoom * self.yzoom

            forward = forward * Matrix2D(1.0 / xzoom, 0, 0, 1.0 / yzoom)
            reverse = Matrix2D(xzoom, 0, 0, yzoom) * reverse

            width *= xzoom
            height *= yzoom
            xo *= xzoom
            yo *= yzoom

        rv = renpy.display.render.Render(width, height)

        if forward is not IDENTITY:
            rv.forward = forward
            rv.reverse = reverse
            
        self.forward = forward

        rv.alpha = self.alpha
        
        rv.subpixel_blit(cr, (xo, yo), main=True)

        self.offsets = [ (xo, yo) ]
        
        return rv

    def event(self, ev, x, y, st):

        children = self.children
        offsets = self.offsets
        
        for i in xrange(len(self.children)-1, -1, -1):

            d = children[i]
            xo, yo = offsets[i]

            cx = x - xo
            cy = y - yo

            # Transform screen coordinates to child coordinates.
            cx, cy = self.forward.transform(cx, cy)
            
            rv = d.event(ev, cx, cy, st)    
            if rv is not None:
                return rv
                
        return None
            
    def __call__(self, child):
        return Transform(
            child=child,
            function=self.function,
            alpha=self.alpha,
            rotate=self.rotate,
            zoom=self.zoom,
            xzoom=self.xzoom,
            yzoom=self.yzoom,
            **self.kwargs)
        
    def get_placement(self):
        xpos = self.xpos
        if xpos is None:
            xpos = self.style.xpos

        ypos = self.ypos
        if ypos is None:
            ypos = self.style.ypos

        xanchor = self.xanchor
        if xanchor is None:
            xanchor = self.style.xanchor

        yanchor = self.yanchor
        if yanchor is None:
            yanchor = self.style.yanchor

        return xpos, ypos, xanchor, yanchor, self.style.xoffset, self.style.yoffset, self.style.subpixel

    def update(self):
        renpy.display.render.invalidate(self)


      

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
        

    def get_placement(self):

        if self.position is None:
            return super(Motion, self).get_placement()
        else:
            return self.position + (self.style.xoffset, self.style.yoffset, self.style.subpixel)
                
    def render(self, width, height, st, at):

        if self.anim_timebase:
            t = at
        else:
            t = st

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

        child = render(self.child, width, height, st, at)
        cw, ch = child.get_size()

        if self.add_sizes:
            res = self.function(t, (width, height, cw, ch))
        else:
            res = self.function(t)

        res = tuple(res)
            
        if len(res) == 2:
            self.position = res + (self.style.xanchor, self.style.yanchor)
        else:
            self.position = res

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

        def interp(a, b, c):

            if c is not None:
                if type(a) is float:
                    a = a * c
                if type(b) is float:
                    b = b * c
                            
            rv = a + t * (b - a)
            
            return renpy.display.core.absolute(rv)
            
        return [ interp(a, b, c) for a, b, c in zip(self.start, self.end, sizes) ]


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
                  add_sizes=True,
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
                  add_sizes=True,
                  **properties)


class Revolver(object):

    def __init__(self, start, end, child, around=(0.5, 0.5), cor=(0.5, 0.5), pos=None):
        self.start = start
        self.end = end
        self.around = around
        self.cor = cor
        self.pos = pos
        self.child = child
        
    def __call__(self, t, (w, h, cw, ch)):

        # Converts a float to an integer in the given range, passes
        # integers through unchanged.
        def fti(x, r):
            if x is None:
                x = 0

            if isinstance(x, float):
                return int(x * r)
            else:
                return x
        
        if self.pos is None:
            pos = self.child.get_placement()
        else:
            pos = self.pos
            
        xpos, ypos, xanchor, yanchor, xoffset, yoffset, subpixel = pos

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

        return (renpy.display.core.absolute(nx), renpy.display.core.absolute(ny), 0, 0)


def Revolve(start, end, time, child, around=(0.5, 0.5), cor=(0.5, 0.5), pos=None, **properties):

    return Motion(Revolver(start, end, child, around=around, cor=cor, pos=pos),
                  time,
                  child,
                  add_sizes=True,
                  **properties)

class Zoom(renpy.display.core.Displayable):
    """
    This displayable causes a zoom to take place, using image
    scaling. The render of this displayable is always of the supplied
    size. The child displayable is rendered, and a rectangle is
    cropped out of it. This rectangle is interpolated between the
    start and end rectangles. The rectangle is then scaled to the
    supplied size. The zoom will take time seconds, after which it
    will show the end rectangle, unless an after_child is
    given.

    The algorithm used for scaling does not perform any
    interpolation or other smoothing.
    """



    def __init__(self, size, start, end, time, child,
                 after_child=None, time_warp=None,
                 bilinear=True, opaque=True,
                 anim_timebase=False,
                 repeat=False,
                 style='motion',
                 **properties):
        """
        @param size: The size that the rectangle is scaled to, a
        (width, height) tuple.

        @param start: The start rectangle, an (xoffset, yoffset,
        width, height) tuple.

        @param end: The end rectangle, an (xoffset, yoffset,
        width, height) tuple.

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

        super(Zoom, self).__init__(style=style, **properties)

        child = renpy.easy.displayable(child)

        self.size = size
        self.start = start
        self.end = end
        self.time = time
        self.done = 0.0
        self.child = child
        self.repeat = repeat
        
        if after_child:
            self.after_child = renpy.easy.displayable(after_child)
        else:
            if self.end == 1.0:
                self.after_child = child
            else:
                self.after_child = None
        
        self.time_warp = time_warp
        self.bilinear = bilinear and renpy.display.module.can_bilinear_scale
        self.opaque = opaque
        self.anim_timebase = anim_timebase
        

    def visit(self):
        return [ self.child, self.after_child ]

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
        surf = rend.pygame_surface()

        rect = tuple([ (1.0 - done) * a + done * b for a, b in zip(self.start, self.end) ])

        # Check for inclusion, report an error otherwise.
        rx, ry, rw, rh = rect

        if rx < 0 or ry < 0 or rx + rw > rend.width or ry + rh > rend.height:
            raise Exception("Zoom rectangle %r falls outside of %dx%d parent surface." % (rect, rend.width, rend.height))

        rv = zoom_core(rend, surf, rect, self.size[0], self.size[1], self.bilinear, self.opaque)

        if self.done < 1.0:
            renpy.display.render.redraw(self, 0)

        return rv

    def event(self, ev, x, y, st):
        if self.done == 1.0:
            return self.child.event(ev, x, y, st)
        else:
            return None


def zoom_core(rend, surf, rect, neww, newh, bilinear, opaque):


    if bilinear and opaque:

        def draw(dest, x, y, surf=surf, rect=rect, neww=neww, newh=newh):

            # Find the part of dest we must draw to. Realize x and y
            # are negative or 0.

            sx, sy, sw, sh = rect
            dw, dh = dest.get_size()

            subw = min(neww + x, dw)
            subh = min(newh + y, dh)

            if subw <= 0 or subh <= 0:
                return

            dest = dest.subsurface((0, 0, subw, subh))

            renpy.display.module.bilinear_scale(surf, dest,
                                                sx, sy, sw, sh,
                                                -x, -y, neww, newh)
            
        rv = renpy.display.render.Render(neww, newh, draw_func=draw, opaque=True)
        

    else:
        
        if bilinear:
            sx, sy, sw, sh = rect

            scalesurf = pygame.Surface((neww, newh), surf.get_flags(), surf)

            renpy.display.module.bilinear_scale(surf, scalesurf,
                                                sx, sy, sw, sh,
                                                0, 0, neww, newh)
        else:

            renpy.display.render.blit_lock.acquire()
            scalesurf = pygame.transform.scale(surf.subsurface(rect), (neww, newh))
            renpy.display.render.blit_lock.release()
            
        renpy.display.render.mutated_surface(scalesurf)

        rv = renpy.display.render.Render(neww, newh)
        rv.blit(scalesurf, (0, 0))
        
    rv.depends_on(rend)
    return rv


class FactorZoom(renpy.display.core.Displayable):

    def __init__(self, start, end, time, child,
                 after_child=None, time_warp=None,
                 bilinear=True, opaque=True,
                 anim_timebase=False,
                 repeat=False,
                 style='motion',
                 **properties):

        super(FactorZoom, self).__init__(style=style, **properties)

        child = renpy.easy.displayable(child)

        self.start = start
        self.end = end
        self.time = time
        self.child = child 
        self.repeat = repeat
        
        if after_child:
            self.after_child = renpy.easy.displayable(after_child)
        else:
            if self.end == 1.0:
                self.after_child = child
            else:
                self.after_child = None
        
        self.time_warp = time_warp
        self.bilinear = bilinear and renpy.display.module.can_bilinear_scale
        self.opaque = opaque
        self.done = 0.0
        self.anim_timebase = anim_timebase
        
    def visit(self):
        return [ self.child, self.after_child ]

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
        surf = rend.pygame_surface()

        factor = self.start * (1.0 - done) + self.end * done

        oldw, oldh = surf.get_size()
        neww = int(oldw * factor)
        newh = int(oldh * factor)

        rv = zoom_core(rend, surf, (0, 0, oldw, oldh), neww, newh, self.bilinear, self.opaque)
        
        if self.done < 1.0:
            renpy.display.render.redraw(self, 0)
            
        return rv

    def event(self, ev, x, y, st):
        if self.done == 1.0 and self.after_child:
            return self.after_child.event(ev, x, y, st)
        else:
            return None

class SizeZoom(renpy.display.core.Displayable):

    def __init__(self, start, end, time, child,
                 after_child=None, time_warp=None,
                 bilinear=True, opaque=True,
                 anim_timebase=False,
                 repeat=False,
                 style='motion',
                 **properties):

        super(SizeZoom, self).__init__(style=style, **properties)

        child = renpy.easy.displayable(child)

        self.start = start
        self.end = end
        self.time = time        
        self.child = child 
        self.repeat = repeat
        
        if after_child:
            self.after_child = renpy.easy.displayable(after_child)
        else:
            if self.end == (1.0, 1.0):
                self.after_child = child
            else:
                self.after_child = None
        
        self.time_warp = time_warp
        self.bilinear = bilinear and renpy.display.module.can_bilinear_scale
        self.opaque = opaque
        self.done = 0.0
        self.anim_timebase = anim_timebase
        
    def visit(self):
        return [ self.child, self.after_child ]

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
        surf = rend.pygame_surface()

        sx, sy = self.start
        ex, ey = self.end

        neww = int(sx + (ex - sx) * done)
        newh = int(sy + (ey - sy) * done)
        oldw, oldh = surf.get_size()

        rv = zoom_core(rend, surf, (0, 0, oldw, oldh), neww, newh, self.bilinear, self.opaque)
        
        if self.done < 1.0:
            renpy.display.render.redraw(self, 0)

        return rv

    def event(self, ev, x, y, st):
        if self.done == 1.0 and self.after_child:
            return self.after_child.event(ev, x, y, st)
        else:
            return None

class RotoZoom(renpy.display.core.Displayable):

    def __init__(self,
                 rot_start, rot_end, rot_delay,
                 zoom_start, zoom_end, zoom_delay,
                 child,
                 rot_repeat=False, zoom_repeat=False,
                 rot_bounce=False, zoom_bounce=False,
                 rot_anim_timebase=False, zoom_anim_timebase=False,
                 rot_time_warp=None, zoom_time_warp=None,
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
        
    def render(self, w, h, st, at):

        if not renpy.display.module.can_transform:
            rv = renpy.display.render.Render(1, 1)
            return rv
        
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
            
        if rot_time <= 1.0 or zoom_time <= 1.0:
            renpy.display.render.redraw(self, 0)

        rot_time = min(rot_time, 1.0)
        zoom_time = min(zoom_time, 1.0)
        
        if self.rot_time_warp:
            rot_time = self.rot_time_warp(rot_time)

        if self.zoom_time_warp:
            zoom_time = self.zoom_time_warp(zoom_time)

            
        angle = self.rot_start + (1.0 * self.rot_end - self.rot_start) * rot_time
        zoom = self.zoom_start + (1.0 * self.zoom_end - self.zoom_start) * zoom_time
        angle = -angle * math.pi / 180

        zoom = max(zoom, 0.001) 
        
        child_rend = renpy.display.render.render(self.child, w, h, st, at)
        surf = child_rend.pygame_surface(True)

        cw, ch = child_rend.get_size()

        # Figure out the size of the target.
        dw = math.hypot(cw, ch) * zoom
        dh = dw

        # We shrink the size by one, since we can't access these pixels.
        # cw -= 1
        # ch -= 1

         # Figure out the various components of the rotation.

        xdx = math.cos(angle) / zoom
        xdy = -math.sin(angle) / zoom
        ydx = -xdy # math.sin(angle) / zoom
        ydy = xdx # math.cos(angle) / zoom

        def draw(dest, xo, yo):

            target = dest
                                            
            dulcx = -dw / 2.0 - xo
            dulcy = -dh / 2.0 - yo

            culcx = cw / 2.0 + xdx * dulcx + xdy * dulcy
            culcy = ch / 2.0 + ydx * dulcx + ydy * dulcy

            renpy.display.module.transform(surf, target,
                                           culcx, culcy,
                                           xdx, ydx, xdy, ydy)

        rv = renpy.display.render.Render(dw, dh, draw_func=draw, opaque=self.opaque)
        rv.depends_on(child_rend)
        return rv

# For compatibility with old games.
renpy.display.layout.Transform = Transform
renpy.display.layout.RotoZoom = RotoZoom
renpy.display.layout.SizeZoom = SizeZoom
renpy.display.layout.FactorZoom = FactorZoom
renpy.display.layout.Zoom = Zoom
renpy.display.layout.Revolver = Revolver
renpy.display.layout.Motion = Motion
renpy.display.layout.Interpolate = Interpolate

# Leave these functions around - they might have been pickled somewhere.
renpy.display.layout.Revolve = Revolve # function
renpy.display.layout.Move = Move # function
renpy.display.layout.Pan = Pan # function
