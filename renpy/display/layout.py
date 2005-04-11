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

    def __init__(self, width=0, height=0, focusable=False, style='default', **properties):
        super(Null, self).__init__()

        self.style = renpy.style.Style(style, properties)
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

    def add(self, widget, time=None):
        super(Fixed, self).add(widget)
        self.times.append(time)

    def append_scene_list(self, l):
        for tag, time, d in l:
            self.add(d, time)

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
                 style='default', **properties):
        """
        @param cols: The number of columns in this widget.

        @params rows: The number of rows in this widget.
        """

        super(Grid, self).__init__()

        self.style = renpy.style.Style(style, properties)

        self.cols = cols
        self.rows = rows

        self.padding = padding

    def render(self, width, height, st):

        # For convenience and speed.
        padding = self.padding
        cols = self.cols
        rows = self.rows

        if len(self.children) != cols * rows:
            raise Exception("Grid not completely full.")

        renders = [ render(i, width, height, st) for i in self.children ]
        self.sizes = [ i.get_size() for i in renders ]

        cwidth = 0
        cheight = 0

        for w, h in self.sizes:
            cwidth = max(cwidth, w)
            cheight = max(cheight, h)

        if self.style.xfill:
            cwidth = (width - (cols - 1) * padding) / cols

        if self.style.yfill:
            cheight = (height - (rows - 1) * padding) / rows

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

class HBox(Container):
    """
    A box where things are aligned horizontally. The height of the box
    is equal to the height of the largest thing in the box, or minheight,
    whichever is larger. For each child that is smaller than the height of the
    box, alignment * (empty space) is placed above the child, with the rest
    of the empty space being placed below. (So 0.0 for top, 0.5 for center,
    and 1.0 for bottom alignment.)

    If Full, the end result uses all of the width available to it.
    
    """

    def __init__(self, padding=0, style='default', **properties):
        super(HBox, self).__init__()

        self.padding = padding
        self.style = renpy.style.Style(style, properties)

    def get_placement(self):
        return self.style

    def render(self, width, height, st):

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
            remwidth -= self.padding

            xo += sw + self.padding

            myheight = max(sh, myheight)

            surfaces.append(surf)
            self.sizes.append((sw, sh))


        width = xo - self.padding
        
        rv = renpy.display.render.Render(width, myheight)

        for surf, child, xo in zip(surfaces, self.children, xoffsets):
            sw, sh = surf.get_size()

            offset = child.place(rv, xo, 0, sw, myheight, surf)
            self.offsets.append(offset)

        return rv
    

class VBox(Container):
    """
    This is a box that lines displayables up vertically. The width of
    the box is equal to the width of the widest displayable, or the
    minwidth, whichever is smaller. Algnment * (empty space) of the
    empty space is placed to the left of each displayable, with the
    rest being placed to the right. Padding pixels of space are placed
    between displayables.

    If full is given, then the height of the returned surface is the
    full height allocated.
    """

    def __init__(self, padding=0, style='default', **properties):
        super(VBox, self).__init__()

        self.padding = padding
        self.style = renpy.style.Style(style, properties)

    def get_placement(self):
        return self.style
        
    def render(self, width, height, st):

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
            remheight -= self.padding

            yo += sh + self.padding

            mywidth = max(sw, mywidth)

            surfaces.append(surf)
            self.sizes.append((sw, sh))


        height = yo - self.padding
        
        rv = renpy.display.render.Render(mywidth, height)

        for surf, child, yo in zip(surfaces, self.children, yoffsets):

            sw, sh = surf.get_size()

            offset = child.place(rv, 0, yo, mywidth, sh, surf)

            self.offsets.append(offset)

        return rv
    

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


class Pan(Container):
    """
    This is used to pan over a child displayable, which is almost
    always an image. It works by interpolating the placement of the
    upper-left corner of the image, over time. It's only really
    suitable for use with images that are larger than the screen, as
    we don't do any cropping on the image.
    """

    def __init__(self, startpos, endpos, time, child,
                 style='image_placement', **properties):
        """
        @param child: The child displayable.

        @param startpos: The initial coordinates of the upper-left
        corner of the screen, relative to the image.

        @param endpos: The coordinates of the upper-left corner of the
        screen, relative to the image, after time has elapsed.

        @param time: The time it takes to pan from startpos to endpos.
        """

        super(Pan, self).__init__()
        self.add(child)

        self.startpos = startpos
        self.endpos = endpos
        self.time = time
        self.style = renpy.style.Style(style, properties)

    def get_placement(self):
        return self.style

    def render(self, width, height, st):

        surf = render(self.child, width, height, st)
        self.sizes = [ surf.get_size() ]

        x0, y0 = self.startpos
        x1, y1 = self.endpos

        if self.time > 0:
            tfrac = (st / self.time)
        else:
            tfrac = 1.0

        if tfrac > 1.0:
            tfrac = 1.0

        xo = int(x0 * (1.0 - tfrac) + x1 * tfrac)
        yo = int(y0 * (1.0 - tfrac) + y1 * tfrac)
        

        self.offsets = [ (-xo, -yo) ]

        rv = renpy.display.render.Render(width, height)

        # print surf

        subsurf = surf.subsurface((xo, yo, width, height))
        rv.blit(subsurf, (0, 0))

        # rv.blit(surf, (-xo, -yo))

        if st < self.time:
            renpy.display.render.redraw(self, 0)

        return rv

class Move(Container):
    """
    This moves a child relative to the thing containing it. This
    motion is done by manipulating the xpos and ypos properties in a
    placement style.
    """

    def __init__(self, startpos, endpos, time, child,
                 style='default', **properties):

        super(Move, self).__init__()
        self.add(child)

        self.startpos = startpos
        self.endpos = endpos
        self.time = time

        self.st = 0.0

        self.style = renpy.style.Style(style, properties)

    def get_placement(self):
        st = self.st

        x0, y0 = self.startpos
        x1, y1 = self.endpos

        if self.time > 0:
            tfrac = (st / self.time)
        else:
            tfrac = 1.0

        if tfrac > 1.0:
            tfrac = 1.0

        xo = x0 * (1.0 - tfrac) + x1 * tfrac
        yo = y0 * (1.0 - tfrac) + y1 * tfrac

        if isinstance(x1, int):
            xo = int(xo)

        if isinstance(y1, int):
            yo = int(yo)

        self.style.xpos = xo
        self.style.ypos = yo

        return self.style

    def render(self, width, height, st):
        self.st = st
        rv = render(self.child, width, height, st)

        self.sizes = [ rv.get_size() ]
        self.offsets = [ (0, 0) ]

        if st < self.time:
            renpy.display.render.redraw(self, 0)

        return rv

    
class Sizer(Container):
    """
    This is a widget that can change the size allocated to the widget that
    it contains. Please note that it can only shrink the widget, and that
    not all widgets respond well to having their areas shrunk. (For example,
    this has no effect on an image.)
    """

    def __init__(self, maxwidth, maxheight, child,
                 style='default', **properties):

        super(Sizer, self).__init__()
        self.add(child)

        self.maxwidth = maxwidth
        self.maxheight = maxheight

        self.style = renpy.style.Style(style, properties)

    def render(self, width, height, st):

        if self.maxwidth:
            width = min(width, self.maxwidth)

        if self.maxheight:
            height = min(height, self.maxheight)

        return super(Sizer, self).render(width, height, st)
