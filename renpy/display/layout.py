# Copyright 2004-2008 PyTom <pytom@bishoujo.us>
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

import pygame
from pygame.constants import *

import renpy
from renpy.display.render import render
import time
import math

def scale(num, base):
    """
    If num is a float, multiplies it by base and returns that. Otherwise,
    returns num unchanged.
    """

    if isinstance(num, float):
        return num * base
    else:
        return num

class Null(renpy.display.core.Displayable):
    """
    This is a displayable that doesn't actually display anything. It's
    useful, I guess, when you need to wrap something with a behavior,
    but don't want to actually have anything there.
    """

    def __init__(self, width=0, height=0, style='default', **properties):
        super(Null, self).__init__(style=style, **properties)
        self.width = width
        self.height = height

    def render(self, width, height, st, at):
        rv = renpy.display.render.Render(self.width, self.height)

        if self.focusable:
            rv.add_focus(self, None, None, None, None, None)

        return rv


class Container(renpy.display.core.Displayable):
    """
    This is the base class for containers that can have one or more
    children.

    @ivar children: A list giving the children that have been added to
    this container, in the order that they were added in.

    @ivar child: The last child added to this container. This is also
    used to access the sole child in containers that can only hold
    one child.

    @ivar offsets: A list giving offsets for each of our children.
    It's expected that render will set this up each time it is called.

    @ivar sizes: A list giving sizes for each of our children. It's
    also expected that render will set this each time it is called.

    """

    def __init__(self, *args, **properties):

        self.children = []
        self.child = None
        self.offsets = []

        for i in args:
            self.add(i)

        super(Container, self).__init__(**properties)

    def set_style_prefix(self, prefix):
        super(Container, self).set_style_prefix(prefix)

        for i in self.children:
            i.set_style_prefix(prefix)

            
    def add(self, child):
        """
        Adds a child to this container.
        """

        if child is None:
            return

        self.children.append(child)
        self.offsets.append((0, 0))
        self.child = child

    def render(self, width, height, st, at):

        rv = render(self.child, width, height, st, at)
        self.children = [ self.child ]
        self.offsets = [ (0, 0) ]
        self.sizes = [ rv.get_size() ]

        return rv

    def event(self, ev, x, y, st):

        children = self.children
        offsets = self.offsets
        
        for i in xrange(len(self.children)-1, -1, -1):
            d = children[i]
            xo, yo = offsets[i]

            rv = d.event(ev, x - xo, y - yo, st)    
            if rv is not None:
                return rv
                
        return None

    def child_at_point(self, x, y):
        """
        Returns the index of the child of this widge that is being
        rendered at the given coordinates. Return None if the
        coordinates are not in any child widget.
        """

        for i, ((xo, yo), (w, h)) in enumerate(zip(self.offsets, self.sizes)):
            xrel = x - xo
            yrel = y - yo

            if xrel < 0 or yrel < 0:
                continue

            if xrel >= w or yrel >= h:
                continue

            return i

        return None

    def visit(self):
        return self.children
    
    

def LiveComposite(size, *args, **properties):
    """
    This is similar to im.Composite, but can be used with displayables
    instead of images. This allows it to be used to composite, for
    example, an animation on top of the image.

    This is less efficient then im.Composite, as it needs to draw all
    of the displayables on the screen. On the other hand, it allows
    displayables to change while they are on the screen, which is
    necessary for animation.
    
    This takes a variable number of arguments. The first argument is
    size, which must be a tuple giving the width and height of the
    composited widgets, for layout purposes.

    It then takes an even number of further arguments. (For an odd
    number of total arguments.) The second and other even numbered
    arguments contain position tuples, while the third and further
    odd-numbered arguments give displayables. A position argument
    gives the position of the displayable immediately following it,
    with the position expressed as a tuple giving an offset from the
    upper-left corner of the LiveComposite.  The displayables are
    drawn in bottom-to-top order, with the last being closest to the
    user.
    """

    properties.setdefault('style', 'image_placement')

    width, height = size

    rv = Fixed(xmaximum=width, ymaximum=height, **properties)

    if len(args) % 2 != 0:
        raise Exception("LiveComposite requires an odd number of arguments.")

    for pos, widget in zip(args[0::2], args[1::2]):
        xpos, ypos = pos
        rv.add(Position(renpy.easy.displayable(widget),
                        xpos=xpos, xanchor=0, ypos=ypos, yanchor=0))

    return rv

class Position(Container):
    """
    Controls the placement of a displayable on the screen, using
    supplied position properties. This is the non-curried form of
    Position, which should be used when the user has directly created
    the displayable that will be shown on the screen.
    """

    def __init__(self, child, style='image_placement', **properties):
        """
        @param child: The child that is being laid out.

        @param style: The base style of this position.

        @param properties: Position properties that control where the
        child of this widget is placed.
        """

        super(Position, self).__init__(style=style, **properties)
        self.add(child)

    def render(self, width, height, st, at):

        surf = render(self.child, width, height, st, at)
        cw, ch = surf.get_size()

        self.offsets = [ (0, 0) ]
        self.sizes = [ (cw, ch) ]

        rv = renpy.display.render.Render(surf.width, surf.height)
        rv.blit(surf, (0, 0))
        
        return rv

    def get_placement(self):
    
        xpos, ypos, xanchor, yanchor, xoffset, yoffset = self.child.get_placement()
            
        if self.style.xpos is not None:
            xpos = self.style.xpos

        if self.style.ypos is not None:
            ypos = self.style.ypos

        if self.style.xanchor is not None:
            xanchor = self.style.xanchor

        if self.style.yanchor is not None:
            yanchor = self.style.yanchor

        return xpos, ypos, xanchor, yanchor, xoffset, yoffset

    
class Grid(Container):
    """
    A grid is a widget that evenly allocates space to its children.
    The child widgets should not be greedy, but should instead be
    widgets that only use part of the space available to them.
    """

    def __init__(self, cols, rows, padding=None,
                 transpose=False,
                 style='default', **properties):
        """
        @param cols: The number of columns in this widget.

        @params rows: The number of rows in this widget.

        @params transpose: True if the grid should be transposed.
        """

        if padding is not None:
            properties.setdefault('spacing', padding)
        
        super(Grid, self).__init__(style=style, **properties)

        self.cols = cols
        self.rows = rows

        self.transpose = transpose

    def render(self, width, height, st, at):

        # For convenience and speed.
        padding = self.style.spacing
        cols = self.cols
        rows = self.rows

        if len(self.children) != cols * rows:
            raise Exception("Grid not completely full.")

        # If necessary, transpose the grid (kinda hacky, but it works here.)
        if self.transpose:
            self.transpose = False

            old_children = self.children[:]
            
            for y in range(0, rows):
                for x in range(0, cols):
                    self.children[x + y * cols] = old_children[ y + x * rows ]

            
        # Now, start the actual rendering.

        renwidth = width
        renheight = height

        if self.style.xfill:
            renwidth = (width - (cols - 1) * padding) / cols
        if self.style.yfill:
            renheight = (height - (rows - 1) * padding) / rows
        
        renders = [ render(i, renwidth, renheight, st, at) for i in self.children ]
        self.sizes = [ i.get_size() for i in renders ]

        cwidth = 0
        cheight = 0

        for w, h in self.sizes:
            cwidth = max(cwidth, w)
            cheight = max(cheight, h)

        if self.style.xfill:
            cwidth = renwidth

        if self.style.yfill:
            cheight = renheight

        width = cwidth * cols + padding * (cols - 1)
        height = cheight * rows + padding * (rows - 1)

        rv = renpy.display.render.Render(width, height)

        self.offsets = [ ]
            
        for y in range(0, rows):
            for x in range(0, cols):

                child = self.children[ x + y * cols ]
                surf = renders[x + y * cols]

                xpos = x * (cwidth + padding)
                ypos = y * (cheight + padding)

                offset = child.place(rv, xpos, ypos, cwidth, cheight, surf)
                self.offsets.append(offset)

        return rv

class MultiBox(Container):

    layer_name = None
    first = True
    
    def __init__(self, spacing=None, layout=None, style='default', **properties):

        if spacing is not None:
            properties['spacing'] = spacing

        super(MultiBox, self).__init__(style=style, **properties)

        self.default_layout = layout
        
        self.start_times = [ ]
        self.anim_times = [ ]

        # A map from layer name to the widget corresponding to
        # that layer.
        self.layers = None

        # The scene list for this widget.
        self.scene_list = None
        
        
    def add(self, widget, start_time=None, anim_time=None):
        super(MultiBox, self).add(widget)
        self.start_times.append(start_time)
        self.anim_times.append(anim_time)

    def append_scene_list(self, l):
        for tag, zo, start, anim, d in l:
            self.add(d, start, anim)

        if self.scene_list is None:
            self.scene_list = [ ]
            
        self.scene_list.extend(l)
        
    def render(self, width, height, st, at):

        t = renpy.game.interface.frame_time

        if self.first:
        
            it = renpy.game.interface.interact_time

            self.start_times = [ i or it for i in self.start_times ]
            self.anim_times = [ i or it for i in self.anim_times ]

            self.first = False
            
            layout = self.style.box_layout

            if layout is None:
                layout = self.default_layout

            self.layout = layout

        else:
            layout = self.layout

                
        if layout == "fixed":

            self.offsets = [ ]
            self.sizes = [ ]
            
            rv = renpy.display.render.Render(width, height, layer_name=self.layer_name)

        
            for child, start, anim in zip(self.children, self.start_times, self.anim_times):

                cst = t - start
                cat = t - anim

                surf = render(child, width, height, cst, cat)

                if surf:
                    self.sizes.append(surf.get_size())
                    offset = child.place(rv, 0, 0, width, height, surf)
                    self.offsets.append(offset)
                else:
                    self.sizes.append((0, 0))
                    self.offsets.append((0, 0))

            return rv
                    
        if layout == "horizontal":

            spacing = self.style.spacing
            first_spacing = self.style.first_spacing

            if first_spacing is None:
                first_spacing = spacing

            spacings = [ first_spacing ] + [ spacing ] * (len(self.children) - 1)

            self.offsets = [ ]
            self.sizes = [ ]

            surfaces = [ ]
            xoffsets = [ ]

            remwidth = width
            xo = 0

            myheight = 0

            padding = 0

            for i, padding, start, anim in zip(self.children, spacings, self.start_times, self.anim_times):

                xoffsets.append(xo)
                surf = render(i, remwidth, height, t - start, t - anim)

                sw, sh = surf.get_size()

                remwidth -= sw
                remwidth -= padding

                xo += sw + padding

                myheight = max(sh, myheight)

                surfaces.append(surf)
                self.sizes.append((sw, sh))


            if self.style.yfill:
                myheight = height

            if not self.style.xfill:
                width = xo - padding
                bonus = 0
            else:
                bonus = (remwidth + padding) / len(xoffsets)
                xoffsets = [ xo + i * bonus for i, xo in enumerate(xoffsets) ]
                
                
            rv = renpy.display.render.Render(width, myheight)

            for surf, child, xo in zip(surfaces, self.children, xoffsets):
                sw, sh = surf.get_size()

                offset = child.place(rv, xo, 0, sw + bonus, myheight, surf)
                self.offsets.append(offset)

            return rv
        
        elif layout == "vertical":

            spacing = self.style.spacing
            first_spacing = self.style.first_spacing

            if first_spacing is None:
                first_spacing = spacing

            spacings = [ first_spacing ] + [ spacing ] * (len(self.children) - 1)
    
            self.offsets = [ ]
            self.sizes = [ ]

            surfaces = [ ]
            yoffsets = [ ]

            remheight = height
            yo = 0

            mywidth = 0

            padding = 0

            for i, padding, start, anim in zip(self.children, spacings, self.start_times, self.anim_times):

                yoffsets.append(yo)

                surf = render(i, width, remheight, t - start, t - anim)

                sw, sh = surf.get_size()

                remheight -= sh
                remheight -= padding

                yo += sh + padding

                mywidth = max(sw, mywidth)

                surfaces.append(surf)
                self.sizes.append((sw, sh))

            if self.style.xfill:
                mywidth = width

            if not self.style.yfill:
                height = yo - padding
                bonus = 0
            else:
                bonus = (remheight + padding) / len(yoffsets)
                yoffsets = [ yo + i * bonus for i, yo in enumerate(yoffsets) ]
                
            rv = renpy.display.render.Render(mywidth, height)

            for surf, child, yo in zip(surfaces, self.children, yoffsets):

                sw, sh = surf.get_size()

                offset = child.place(rv, 0, yo, mywidth, sh + bonus, surf)

                self.offsets.append(offset)

            return rv

        
    def event(self, ev, x, y, st):
        children_offsets = zip(self.children, self.offsets, self.start_times)
        children_offsets.reverse()

        for i, (xo, yo), t in children_offsets: 

            if t is None:
                cst = 0
            else:
                cst = renpy.game.interface.event_time - t

            rv = i.event(ev, x - xo, y - yo, cst)    
            if rv is not None:
                return rv
                
        return None

def Fixed(**properties):
    return MultiBox(layout='fixed', **properties)

class SizeGroup(renpy.object.Object):

    def __init__(self):
        self.members = [ ]
        self._width = None
        self.computing_width = False
        
    def width(self, width, height, st, at):
        if self._width is not None:
            return self._width

        if self.computing_width:
            return 0

        self.computing_width = True
        
        maxwidth = 0

        for i in self.members:
            rend = renpy.display.render.render(i, width, height, st, at)
            maxwidth = max(rend.width, maxwidth)
            rend.kill()
            
        self._width = maxwidth
        self.computing_width = False

        return maxwidth
        

size_groups = dict()
    
class Window(Container):
    """
    A window is a container that holds a single Displayable in it. A window
    is responsable for displaying the displayable on top of a background.

    Margin is space that is left empty by the window, and does not
    have the background displayed in it. Padding is space that is
    filled with the background, but does not contain the widget in it.

    If fill in a dimension is True, then the window expands to the
    maximum size possible in that dimension, and the child is place at
    the left or top of the space. Otherwise, the window will shrink to
    fit the child, but on no account will the size of child area +
    2*padding shrink below the minimum.    
    """
    
    def __init__(self, child, style='window', **properties):

        super(Window, self).__init__(style=style, **properties)
        self.add(child)

    def visit(self):
        return [ self.style.background ] + self.children

    def get_child(self):
        return self.style.child or self.child

    def per_interact(self):
        size_group = self.style.size_group

        if size_group:
            group = size_groups.get(size_group, None)
            if group is None:
                group = size_groups[size_group] = SizeGroup()

            group.members.append(self)

                
    def render(self, width, height, st, at):

        # save some typing.
        style = self.style

        xminimum = scale(style.xminimum, width)
        yminimum = scale(style.yminimum, height)

        size_group = self.style.size_group
        if size_group:
            xminimum = max(xminimum, size_groups[size_group].width(width, height, st, at))
        
        left_margin = scale(style.left_margin, width)
        left_padding = scale(style.left_padding, width)

        right_margin = scale(style.right_margin, width)
        right_padding = scale(style.right_padding, width)

        top_margin = scale(style.top_margin, height)
        top_padding = scale(style.top_padding, height)

        bottom_margin = scale(style.bottom_margin, height)
        bottom_padding = scale(style.bottom_padding, height)

        # c for combined.
        cxmargin = left_margin + right_margin
        cymargin = top_margin + bottom_margin

        cxpadding = left_padding + right_padding
        cypadding = top_padding + bottom_padding

        child = self.get_child()
        
        # Render the child.
        surf = render(child,
                      width  - cxmargin - cxpadding,
                      height - cymargin - cypadding,
                      st, at)

        sw, sh = surf.get_size()

        # If we don't fill, shrink our size to fit.

        if not style.xfill:
            width = max(cxmargin + cxpadding + sw, xminimum)

        if not style.yfill:
            height = max(cymargin + cypadding + sh, yminimum)

        rv = renpy.display.render.Render(width, height)

        # Draw the background. The background should render at exactly the
        # requested size. (That is, be a Frame or a Solid).
        if style.background:
            bw = width  - cxmargin
            bh = height - cymargin

            back = render(style.background, bw, bh, st, at)

            style.background.place(rv, left_margin, top_margin, bw, bh, back, main=False)

        offsets = child.place(rv,
                              left_margin + left_padding, 
                              top_margin + top_padding,
                              width  - cxmargin - cxpadding,
                              height - cymargin - cypadding,
                              surf)

        # Draw the foreground. The background should render at exactly the
        # requested size. (That is, be a Frame or a Solid).
        if style.foreground:
            bw = width  - cxmargin
            bh = height - cymargin

            back = render(style.foreground, bw, bh, st, at)

            style.foreground.place(rv, left_margin, top_margin, bw, bh, back, main=False)

        self.offsets = [ offsets ]
        self.sizes = [ (sw, sh) ]

        self.window_size = width, height

        return rv


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

    def __init__(self, function, period, child=None, new_widget=None, old_widget=None, repeat=False, bounce=False, delay=None, anim_timebase=False, tag_start=None, time_warp=None, add_sizes=False, style='default', **properties):
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

        child = renpy.easy.displayable(child)

        if child is None:
            child = new_widget

        if delay is None and not repeat:
            delay = period

        super(Motion, self).__init__(style=style, **properties)

        self.child = child 
        self.children = [ child ]
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
            return self.position + (self.style.xoffset, self.style.yoffset)
                
    def render(self, width, height, st, at):

        if self.anim_timebase:
            t = at
        else:
            t = st


        if self.delay and t >= self.delay:
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
                
        t /= self.period

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

        self.sizes = [ child.get_size() ]
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

            if c is not None and isinstance(a, float):
                a = int(a * c)

            if c is not None and isinstance(b, float):
                b = int(b * c)
            
            rv = (1.0 - t) * a + t * b
            
            if isinstance(a, int) and isinstance(b, int):
                return int(rv)
            else:
                return rv

        return [ interp(a, b, c) for a, b, c in zip(self.start, self.end, sizes) ]


def Pan(startpos, endpos, time, child=None, repeat=False, bounce=False,
        anim_timebase=False, style='default', time_warp=None, **properties):
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
         anim_timebase=False, style='default', time_warp=None, **properties):
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
            
        xpos, ypos, xanchor, yanchor, xoffset, yoffset = pos

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

        return (int(nx), int(ny), 0, 0)


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

        super(Zoom, self).__init__(**properties)

        child = renpy.easy.displayable(child)

        self.size = size
        self.start = start
        self.end = end
        self.time = time
        self.child = child            
        self.done = 0.0
        
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


    def visit(self):
        return [ self.child, self.after_child ]

    def render(self, width, height, st, at):

        if self.time:
            done = min(st / self.time, 1.0)
        else:
            done = 1.0

        self.done = done

        if self.after_child and done == 1.0:
            self.child = self.after_child
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

        if done < 1.0:
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

            scalesurf = pygame.Surface((neww, newh), 0, surf)
            renpy.display.module.bilinear_scale(surf, scalesurf,
                                                sx, sy, sw, sh,
                                                0, 0, neww, newh)
        else:
            scalesurf = pygame.transform.scale(surf, (neww, newh))

        renpy.display.render.mutated_surface(scalesurf)

        rv = renpy.display.render.Render(neww, newh)
        rv.blit(scalesurf, (0, 0))
        
    rv.depends_on(rend)
    return rv


class FactorZoom(renpy.display.core.Displayable):

    def __init__(self, start, end, time, child,
                 after_child=None, time_warp=None,
                 bilinear=True, opaque=True,
                 **properties):
        """
        @param start: The start scaling factor.

        @param end: The end scaling factor.

        @param time: The amount of time it will take to
        from the start to the end scaling factors.

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

        super(FactorZoom, self).__init__(**properties)

        child = renpy.easy.displayable(child)

        self.start = start
        self.end = end
        self.time = time
        self.child = child                    
        
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
        
    def visit(self):
        return [ self.child, self.after_child ]

    def render(self, width, height, st, at):

        if self.time:
            done = min(st / self.time, 1.0)
        else:
            done = 1.0

        self.done = done
            
        if self.after_child and done == 1.0:
            self.child = self.after_child
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
        
        if done < 1.0:
            renpy.display.render.redraw(self, 0)

        self.done = done
            
        return rv

    def event(self, ev, x, y, st):
        if self.done == 1.0:
            return self.child.event(ev, x, y, st)
        else:
            return None


        
def dynamic_displayable_compat(st, at, expr):
    child = renpy.python.py_eval(expr)
    return child, None

class DynamicDisplayable(renpy.display.core.Displayable):

    nosave = [ 'child' ]

    def after_setstate(self):
        self.child = None

    def __init__(self, function, *args, **kwargs):
        super(DynamicDisplayable, self).__init__()
        self.child = None

        if isinstance(function, basestring):
            args = ( function, )
            kwargs = { }
            function = dynamic_displayable_compat

        self.predict_function = kwargs.pop("_predict_function", None)            
        self.function = function
        self.args = args
        self.kwargs = kwargs

    def visit(self):
        return [ ]

    def per_interact(self):
        renpy.display.render.redraw(self, 0)
        
    def render(self, w, h, st, at):

        child, redraw = self.function(st, at, *self.args, **self.kwargs)
        child = renpy.easy.displayable(child)

        self.child = child
        child.visit_all(lambda c : c.per_interact())

        if redraw is not None:
            renpy.display.render.redraw(self, redraw)
        
        return renpy.display.render.render(self.child, w, h, st, at)

    def predict_one(self, callback):

        if not self.predict_function:
            return
        
        for i in self.predict_function(*self.args, **self.kwargs):
            if i is not None:
                i.predict(callback)
        
    def get_placement(self):
        return self.child.get_placement()

    def event(self, ev, x, y, st):
        if self.child:
            return self.child.event(ev, x, y, st)

# This chooses the first member of switch that's being shown on the
# given layer.
def condition_switch_pick(switch):
    for cond, d in switch:
        if cond is None or renpy.python.py_eval(cond):
            return d

    raise Exception("Switch could not choose a displayable.")

def condition_switch_show(st, at, switch):
    return condition_switch_pick(switch), None

def condition_switch_predict(switch):

    if renpy.game.lint:
        return [ d for cond, d in switch ]

    return [ condition_switch_pick(switch) ]

def ConditionSwitch(*args, **kwargs):

    kwargs.setdefault('style', 'default')
    
    switch = [ ]
    
    if len(args) % 2 != 0:
        raise Exception('ConditionSwitch takes an even number of arguments')

    for cond, d in zip(args[0::2], args[1::2]):

        d = renpy.easy.displayable(d)
        switch.append((cond, d))

    rv = DynamicDisplayable(condition_switch_show,
                            switch,
                            _predict_function=condition_switch_predict)
                              
    return Position(rv, **kwargs)

    
def ShowingSwitch(*args, **kwargs):

    layer = kwargs.pop('layer', 'master')

    
    if len(args) % 2 != 0:
        raise Exception('ConditionSwitch takes an even number of arguments')

    condargs = [ ]

    
    for name, d in zip(args[0::2], args[1::2]):
        if name is not None:
            if not isinstance(name, tuple):        
                name = tuple(name.split())
            cond = "renpy.showing(%r, layer=%r)" % (name, layer)
        else:
            cond = None 
            
 
        condargs.append(cond)
        condargs.append(d)

    return ConditionSwitch(*condargs, **kwargs)
    
    
    

        
class IgnoresEvents(renpy.display.core.Displayable):

    def __init__(self, child):
        super(IgnoresEvents, self).__init__(style='default')
        self.child = renpy.easy.displayable(child)
    
    def visit(self):
        return [ self.child ]

    def render(self, w, h, st, at):
        cr = renpy.display.render.render(self.child, w, h, st, at)
        cw, ch = cr.get_size()

        rv = renpy.display.render.Render(cw, ch)
        rv.blit(cr, (0, 0))
        rv.focuses = [ ]

        return rv

    def get_placement(self):
        return self.child.get_placement()

    # Ignores events.
    def event(self, ev, x, y, st):
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
                 opaque=True,
                 **properties):

        super(RotoZoom, self).__init__(**properties)

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

        self.opaque = False

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

        rot_time /= self.rot_delay
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

        if rot_time <= 1.0 or zoom_time <= 1.0:
            renpy.display.render.redraw(self, 0)

        rot_time = min(rot_time, 1.0)
        zoom_time = min(zoom_time, 1.0)
            
        if self.rot_time_warp:
            rot_time = self.rot_time_warp(rot_time)

        if self.zoom_time_warp:
            zoom_time = self.zoom_time_warp(zoom_time)

        angle = self.rot_start + (self.rot_end - self.rot_start) * rot_time
        zoom = self.zoom_start + (self.zoom_end - self.zoom_start) * zoom_time
        angle = -angle * math.pi / 180

        zoom = max(zoom, 0.001) 
        
        child_rend = renpy.display.render.render(self.child, w, h, st, at)
        surf = child_rend.pygame_surface(True)

        cw, ch = child_rend.get_size()

        # We shrink the size by one, since we can't access these pixels.
        cw -= 1
        ch -= 1

        # Figure out the size of the target.
        dw = math.hypot(cw, ch) * zoom
        dh = dw
        
        # Figure out the various components of the rotation.
        xdx = math.cos(angle) / zoom
        xdy = - math.sin(angle) / zoom
        ydx = math.sin(angle) / zoom
        ydy = math.cos(angle) / zoom

        def draw(dest, xo, yo):
            
            if not self.opaque:
                target = pygame.Surface(dest.get_size(), 0,
                                        renpy.game.interface.display.sample_surface)
            else:
                target = dest
            
            dulcx = -dw / 2 - xo
            dulcy = -dh / 2 - yo

            culcx = cw / 2 + xdx * dulcx + xdy * dulcy
            culcy = ch / 2 + ydx * dulcx + ydy * dulcy

            renpy.display.module.transform(surf, target,
                                           culcx, culcy,
                                           xdx, ydx, xdy, ydy)

            if not self.opaque:
                dest.blit(target, (0, 0))

            
        return renpy.display.render.Render(dw, dh, draw_func=draw, opaque=self.opaque)
        

class Viewport(Container):

    __version__ = 1

    def after_upgrade(self, version):
        if version < 1:
            self.xadjustment = renpy.display.behavior.Adjustment(1, 0)
            self.yadjustment = renpy.display.behavior.Adjustment(1, 0)
            self.set_adjustments = False
            self.mousewheel = False
            self.draggable = False
            self.width = 0
            self.height = 0
            
    def __init__(self,
                 child=None,
                 child_size=(None, None),
                 offsets=(None, None),
                 xadjustment=None,
                 yadjustment=None,
                 set_adjustments=True,
                 mousewheel=False,
                 draggable=False,
                 style='viewport',
                 **properties):

        super(Viewport, self).__init__(style=style, **properties)
        child = renpy.easy.displayable(child)
        self.add(child)

        if xadjustment is None:
            self.xadjustment = renpy.display.behavior.Adjustment(1, 0)
        else:
            self.xadjustment = xadjustment
            
        if yadjustment is None:
            self.yadjustment = renpy.display.behavior.Adjustment(1, 0)
        else:
            self.yadjustment = yadjustment
            
        self.set_adjustments = set_adjustments
        
        self.child_width, self.child_height = child_size
        self.xoffset, self.yoffset = offsets
        self.mousewheel = mousewheel
        self.draggable = draggable

        self.width = 0
        self.height = 0

    def per_interact(self):
        self.xadjustment.register(self)
        self.yadjustment.register(self)
        
    def render(self, width, height, st, at):

        self.width = width
        self.height = height
        
        child_width = self.child_width or width
        child_height = self.child_height or height

        surf = render(self.child, child_width, child_height, st, at)

        cw, ch = surf.get_size()

        # width = min(cw, width)
        # height = min(ch, height)

        if self.set_adjustments:
            self.xadjustment.range = max(cw - width, 0)
            self.xadjustment.page = width
            self.yadjustment.range = max(ch - height, 0)
            self.yadjustment.page = height

        if self.xoffset is not None:
            if isinstance(self.xoffset, int):
                value = self.xoffset
            else:
                value = max(cw - width, 0) * self.xoffset
                
            self.xadjustment.value = value
            self.xoffset = None
            
        if self.yoffset is not None:
            if isinstance(self.yoffset, int):
                value = self.yoffset
            else:
                value = max(ch - height, 0) * self.yoffset 

            self.yadjustment.value = value
            self.yoffset = None
                
        cxo = -int(self.xadjustment.value)
        cyo = -int(self.yadjustment.value)

        self.offsets = [ (cxo, cyo) ]
        self.sizes = [ (cw, ch) ]

        rv = renpy.display.render.Render(width, height)
        rv.blit(surf, (cxo, cyo))

        return rv

    def event(self, ev, x, y, st):

        rv = super(Viewport, self).event(ev, x, y, st)
        if rv is not None:
            return rv

        if self.draggable and renpy.display.focus.get_grab() == self:

            oldx, oldy = self.drag_position
            dx = x - oldx
            dy = y - oldy

            self.xadjustment.change(self.xadjustment.value - dx)
            self.yadjustment.change(self.yadjustment.value - dy)

            self.drag_position = (x, y)
            
            if renpy.display.behavior.map_event(ev, 'viewport_drag_end'):
                renpy.display.focus.set_grab(None)
                raise renpy.display.core.IgnoreEvent()
                
        if not ((0 <= x < self.width) and (0 <= y <= self.height)):
            return
                
        if self.mousewheel:

            if renpy.display.behavior.map_event(ev, 'viewport_up'):
                rv = self.yadjustment.change(self.yadjustment.value - self.yadjustment.step)
                if rv is not None:
                    return rv
                else:
                    raise renpy.display.core.IgnoreEvent()

            if renpy.display.behavior.map_event(ev, 'viewport_down'):
                rv = self.yadjustment.change(self.yadjustment.value + self.yadjustment.step)
                if rv is not None:
                    return rv
                else:
                    raise renpy.display.core.IgnoreEvent()

        if self.draggable:

            if renpy.display.behavior.map_event(ev, 'viewport_drag_start'):
                self.drag_position = (x, y)
                renpy.display.focus.set_grab(self)
                raise renpy.display.core.IgnoreEvent()
                
        return None
    
    def set_xoffset(self, offset):
        self.xoffset = offset
        renpy.display.render.redraw(self, 0)
        
    def set_yoffset(self, offset):
        self.yoffset = offset
        renpy.display.render.redraw(self, 0)
        
def LiveCrop(rect, child, **properties):
    x, y, w, h = rect

    child = renpy.easy.displayable(child)    
    return Viewport(child, offsets=(x, y), xmaximum=w, ymaximum=h, **properties)


class Side(Container):

    possible_positions = set([ 'tl', 't', 'tr', 'r', 'br', 'b', 'bl', 'l', 'c'])

    def after_setatate(self):
        self.sized = False
    
    def __init__(self, positions, style='default', **properties):

        super(Side, self).__init__(style=style, **properties)

        if isinstance(positions, basestring):
            positions = positions.split()
        
        for i in positions:
            if not i in Side.possible_positions:
                raise Exception("Side used with impossible position '%s'." % (i,))

        self.positions = tuple(positions)
        self.sized = False
        

    def render(self, width, height, st, at):

        pos_d = { }
        pos_i = { }
        
        for i, (pos, d) in enumerate(zip(self.positions, self.children)):
            pos_d[pos] = d
            pos_i[pos] = i

        # Figure out the size of each widget (and hence where the
        # widget needs to be placed).

        if not self.sized:
            self.sized = True
            
            # Deal with various spacings.
            spacing = self.style.spacing
            
            def spacer(a, b, c, axis):
                if (a in pos_d) or (b in pos_d) or (c in pos_d):
                    return spacing, axis - spacing
                else:
                    return 0, axis
                
            self.left_space, width = spacer('tl', 'l', 'bl', width)
            self.right_space, width = spacer('tr', 'r', 'br', width)
            self.top_space, height = spacer('tl', 't', 'tr', height)
            self.bottom_space, height = spacer('bl', 'b', 'br', height)
            
            # The sizes of the various borders.
            left = 0
            right = 0
            top = 0
            bottom = 0
            cwidth = 0
            cheight = 0
            
            def sizeit(pos, width, height, owidth, oheight):
                if pos not in pos_d:
                    return owidth, oheight
                
                rend = render(pos_d[pos], width, height, st, at)
                return max(owidth, rend.width), max(oheight, rend.height)

            cwidth, cheight = sizeit('c', width, height, 0, 0)
            cwidth, top = sizeit('t', cwidth, height, cwidth, top)
            cwidth, bottom = sizeit('b', cwidth, height, cwidth, bottom)
            left, cheight = sizeit('l', width, cheight, left, cheight) 
            right, cheight = sizeit('r', width, cheight, right, cheight) 

            left, top = sizeit('tl', left, top, left, top)
            left, bottom = sizeit('bl', left, bottom, left, bottom)
            right, top = sizeit('tr', right, top, right, top)
            right, bottom = sizeit('br', right, bottom, right, bottom)
            
            self.cwidth = cwidth
            self.cheight = cheight

            self.top = top
            self.bottom = bottom
            self.left = left
            self.right = right

        else:
            cwidth = self.cwidth
            cheight = self.cheight
            top = self.top
            bottom = self.bottom
            left = self.left
            right = self.right
        
        # Now, place everything onto the render.
        
        self.offsets = [ None ] * len(self.children)
        self.sizes = [ None ] * len(self.children)

        lefts = self.left_space
        rights = self.right_space
        tops = self.top_space
        bottoms = self.bottom_space


        cwidth = min(cwidth, width - left - lefts - right - rights)
        cheight = min(cheight, height - top - tops - bottom - bottoms)
        
        rv = renpy.display.render.Render(left + lefts + cwidth + rights + right,
                                         top + tops + cheight + bottoms + bottom)

        def place(pos, x, y, w, h):

            if pos not in pos_d:
                return

            d = pos_d[pos]
            i = pos_i[pos]
            rend = render(d, w, h, st, at)
            self.sizes[i] = rend.get_size()
            self.offsets[i] = pos_d[pos].place(rv, x, y, w, h, rend)
            
        col1 = 0
        col2 = left + lefts
        col3 = left + lefts + cwidth + rights

        row1 = 0
        row2 = top + tops
        row3 = top + tops + cheight + bottoms

        place('c', col2, row2, cwidth, cheight)

        place('t', col2, row1, cwidth, top)
        place('r', col3, row2, right, cheight)
        place('b', col2, row3, cwidth, bottom)
        place('l', col1, row2, left, cheight)

        place('tl', col1, row1, left, top)
        place('tr', col3, row1, right, top)
        place('br', col3, row3, right, bottom)
        place('bl', col1, row3, left, bottom)

        return rv
        
        

            
