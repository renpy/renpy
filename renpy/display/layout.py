# This file contains classes that handle layout of displayables on
# the screen.

import pygame
from pygame.constants import *

import renpy
from renpy.display.render import render
import time

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

    def get_placement(self):
        return self.style

    def render(self, width, height, st):
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

        for i in args:
            self.add(i)

        super(Container, self).__init__(**properties)


    def find_focusable(self, callback, focus_name):
        super(Container, self).find_focusable(callback, focus_name)

        for i in self.children:
            i.find_focusable(callback, self.focus_name or focus_name)
        

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
        self.child = child

    def render(self, width, height, st):

        rv = render(self.child, width, height, st)
        self.offsets = [ (0, 0) ]
        self.sizes = [ rv.get_size() ]

        return rv

    def get_placement(self):
        return self.child.get_placement()
    
    def event(self, ev, x, y):
        children_offsets = zip(self.children, self.offsets)
        children_offsets.reverse()

        for i, (xo, yo) in children_offsets: 
            rv = i.event(ev, x - xo, y - yo)    
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

    def predict(self, callback):

        super(Container, self).predict(callback)

        for i in self.children:
            i.predict(callback)

class Fixed(Container):
    """
    A container that lays out each of its children at fixed
    coordinates determined by the position style of the child. Each
    widget is given the whole area of this widget, and then placed
    within that area based on its position style.

    The result of this layout is the size of the entire area allocated
    to it. So it's probably only viable for laying out a root window.

    Fixed is used by the display core to render scene lists, and to
    pass them off to transitions.

    """

    def __init__(self, style='default', **properties):
        super(Fixed, self).__init__(style=style, **properties)
        self.times = [ ]

        # A map from layer name to the widget corresponding to
        # that layer.
        self.layers = None

        # The scene list for this widget.
        self.scene_list = [ ]
        

    def add(self, widget, time=None):
        super(Fixed, self).add(widget)
        self.times.append(time)

    def append_scene_list(self, l):
        for tag, time, d in l:
            self.add(d, time)

        self.scene_list.extend(l)

    def get_widget_time_list(self):
        return zip(self.children, self.times)
            
    def get_placement(self):
        return self.style

    def render(self, width, height, st):

        self.offsets = [ ]
        self.sizes = [ ]

        rv = renpy.display.render.Render(width, height)

        t = time.time()

        for child, start in zip(self.children, self.times):

            if start:
                newst = t - start
            else:
                newst = st

            surf = render(child, width, height, newst)

            if surf:
                self.sizes.append(surf.get_size())
                offset = child.place(rv, 0, 0, width, height, surf)
                self.offsets.append(offset)
            else:
                self.sizes.append((0, 0))
                self.offsets.append((0, 0))

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

    def render(self, width, height, st):

        surf = render(self.child, width, height, st)
        cw, ch = surf.get_size()

        self.offsets = [ (0, 0) ]
        self.sizes = [ (cw, ch) ]

        return surf

    def get_placement(self):
        return self.style

class Grid(Container):
    """
    A grid is a widget that evenly allocates space to its children.
    The child widgets should not be greedy, but should instead be
    widgets that only use part of the space available to them.
    """

    def __init__(self, cols, rows, padding=0,
                 transpose=False,
                 style='default', **properties):
        """
        @param cols: The number of columns in this widget.

        @params rows: The number of rows in this widget.

        @params transpose: True if the grid should be transposed.
        """

        super(Grid, self).__init__()

        self.style = renpy.style.Style(style, properties)

        self.cols = cols
        self.rows = rows

        self.padding = padding
        self.transpose = transpose

    def get_placement(self):
        return self.style

    def render(self, width, height, st):

        # For convenience and speed.
        padding = self.padding
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
        
        renders = [ render(i, renwidth, renheight, st) for i in self.children ]
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

    def __init__(self, spacing=None, layout=None, style='default', **properties):

        if spacing is not None:
            properties['box_spacing'] = spacing

        super(MultiBox, self).__init__(style=style, **properties)

        self.default_layout = layout
    
    def get_placement(self):
        return self.style

    def render(self, width, height, st):

        layout = self.style.box_layout
        padding = self.style.box_spacing

        if layout is None:
            layout = self.default_layout
        
        if layout == "horizontal":

            # This is the horizontal path.

            self.offsets = [ ]
            self.sizes = [ ]

            surfaces = [ ]
            xoffsets = [ ]

            remwidth = width
            xo = 0

            myheight = 0

            for i in self.children:

                xoffsets.append(xo)
                surf = render(i, remwidth, height, st)

                sw, sh = surf.get_size()

                remwidth -= sw
                remwidth -= padding

                xo += sw + padding

                myheight = max(sh, myheight)

                surfaces.append(surf)
                self.sizes.append((sw, sh))


            width = xo - padding

            rv = renpy.display.render.Render(width, myheight)

            for surf, child, xo in zip(surfaces, self.children, xoffsets):
                sw, sh = surf.get_size()

                offset = child.place(rv, xo, 0, sw, myheight, surf)
                self.offsets.append(offset)

            return rv
        
        else:
    
            self.offsets = [ ]
            self.sizes = [ ]

            surfaces = [ ]
            yoffsets = [ ]

            remheight = height
            yo = 0

            mywidth = 0

            for i in self.children:

                yoffsets.append(yo)

                surf = render(i, width, remheight, st)

                sw, sh = surf.get_size()

                remheight -= sh
                remheight -= padding

                yo += sh + padding

                mywidth = max(sw, mywidth)

                surfaces.append(surf)
                self.sizes.append((sw, sh))


            height = yo - padding

            rv = renpy.display.render.Render(mywidth, height)

            for surf, child, yo in zip(surfaces, self.children, yoffsets):

                sw, sh = surf.get_size()

                offset = child.place(rv, 0, yo, mywidth, sh, surf)

                self.offsets.append(offset)

            return rv
  

# class HBox(Container):
#     """
#     A box where things are aligned horizontally. The height of the box
#     is equal to the height of the largest thing in the box, or minheight,
#     whichever is larger. For each child that is smaller than the height of the
#     box, alignment * (empty space) is placed above the child, with the rest
#     of the empty space being placed below. (So 0.0 for top, 0.5 for center,
#     and 1.0 for bottom alignment.)

#     If Full, the end result uses all of the width available to it.
    
#     """

#     def __init__(self, padding=0, style='default', **properties):
#         super(HBox, self).__init__()

#         self.padding = padding
#         self.style = renpy.style.Style(style, properties)

#     def get_placement(self):
#         return self.style

#     def render(self, width, height, st):

#         self.offsets = [ ]
#         self.sizes = [ ]

#         surfaces = [ ]
#         xoffsets = [ ]
        
#         remwidth = width
#         xo = 0

#         myheight = 0

#         for i in self.children:

#             xoffsets.append(xo)
#             surf = render(i, remwidth, height, st)

#             sw, sh = surf.get_size()

#             remwidth -= sw
#             remwidth -= self.padding

#             xo += sw + self.padding

#             myheight = max(sh, myheight)

#             surfaces.append(surf)
#             self.sizes.append((sw, sh))


#         width = xo - self.padding
        
#         rv = renpy.display.render.Render(width, myheight)

#         for surf, child, xo in zip(surfaces, self.children, xoffsets):
#             sw, sh = surf.get_size()

#             offset = child.place(rv, xo, 0, sw, myheight, surf)
#             self.offsets.append(offset)

#         return rv
    

# class VBox(Container):
#     """
#     This is a box that lines displayables up vertically. The width of
#     the box is equal to the width of the widest displayable, or the
#     minwidth, whichever is smaller. Algnment * (empty space) of the
#     empty space is placed to the left of each displayable, with the
#     rest being placed to the right. Padding pixels of space are placed
#     between displayables.

#     If full is given, then the height of the returned surface is the
#     full height allocated.
#     """

#     def __init__(self, padding=0, style='default', **properties):
#         super(VBox, self).__init__()

#         self.padding = padding
#         self.style = renpy.style.Style(style, properties)

#     def get_placement(self):
#         return self.style
        
#     def render(self, width, height, st):

#         self.offsets = [ ]
#         self.sizes = [ ]

#         surfaces = [ ]
#         yoffsets = [ ]

#         remheight = height
#         yo = 0

#         mywidth = 0

#         for i in self.children:

#             yoffsets.append(yo)

#             surf = render(i, width, remheight, st)

#             sw, sh = surf.get_size()

#             remheight -= sh
#             remheight -= self.padding

#             yo += sh + self.padding

#             mywidth = max(sw, mywidth)

#             surfaces.append(surf)
#             self.sizes.append((sw, sh))


#         height = yo - self.padding
        
#         rv = renpy.display.render.Render(mywidth, height)

#         for surf, child, yo in zip(surfaces, self.children, yoffsets):

#             sw, sh = surf.get_size()

#             offset = child.place(rv, 0, yo, mywidth, sh, surf)

#             self.offsets.append(offset)

#         return rv
    

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

    def get_placement(self):
        return self.style

    def render(self, width, height, st):

        # save some typing.
        style = self.style

        xminimum = scale(style.xminimum, width)
        yminimum = scale(style.yminimum, height)

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

        # Render the child.
        surf = render(self.child,
                      width  - cxmargin - cxpadding,
                      height - cymargin - cypadding,
                      st)

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

            back = render(style.background, bw, bh, st)

            rv.blit(back,
                    (left_margin, top_margin))
                    # (0, 0, bw, bh))

        offsets = self.child.place(rv,
                                   left_margin + left_padding, 
                                   top_margin + top_padding,
                                   width  - cxmargin - cxpadding,
                                   height - cymargin - cypadding,
                                   surf)

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

    def __init__(self, function, period, child=None, new_widget=None, old_widget=None, repeat=False, bounce=False, delay=None, style='default', **properties):
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

        @param delay: If we are used as a transition, how long we should take. If None, defaults to period.

        This can also be used as a transition. When used as a
        transition, the motion is applied to the new_widget for delay
        seconds.
        """

        if child is None:
            child = new_widget

        if delay is None:
            delay = period

        super(Motion, self).__init__(style=style, **properties)

        self.child = child
        self.function = function
        self.period = period
        self.repeat = repeat
        self.bounce = bounce
        self.delay = delay

    def get_placement(self):
        return self.style

    def render(self, width, height, st):
        
        if self.repeat:
            st = st % self.period
            renpy.display.render.redraw(self, 0)

        else:
            if st > self.period:
                st = self.period
            else:
                renpy.display.render.redraw(self, 0)
                
        st /= self.period

        if self.bounce:
            st = st * 2
            if st > 1.0:
                st = 2.0 - st

        res = self.function(st)

        if len(res) == 2:
            self.style.xpos, self.style.ypos = res
        else:
            self.style.xpos, self.style.ypos, self.style.xanchor, self.style.yanchor = res

        child = render(self.child, width, height, st)
        cw, ch = child.get_size()

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

    def __call__(self, t):

        def interp(a, b):

            rv = (1.0 - t) * a + t * b
            
            if isinstance(a, int) and isinstance(b, int):
                return int(rv)
            else:
                return rv

        return [ interp(a, b) for a, b in zip(self.start, self.end) ]


def Pan(startpos, endpos, time, child=None, repeat=False, bounce=False,
        style='default', **properties):
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
                  **properties)

def Move(startpos, endpos, time, child=None, repeat=False, bounce=False,
        style='default', **properties):
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

    This can be used as a transition. See Motion for details.
    """

    return Motion(Interpolate(startpos, endpos),
                  time,
                  child,
                  repeat=repeat, 
                  bounce=bounce,
                  style=style,
                  **properties)


