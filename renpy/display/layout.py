# This file contains classes that handle layout of displayables on
# the screen.

import pygame
from pygame.constants import *

import renpy

class Null(renpy.display.core.Displayable):
    """
    This is a displayable that doesn't actually display anything. It's
    useful, I guess, when you need to wrap something with a behavior,
    but don't want to actually have anything there.
    """

    def render(self, width, height, st):
        return renpy.display.surface.Surface(1, 1)


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

    def __init__(self, *args):
        
        self.children = []
        self.child = None

        for i in args:
            self.add(i)

    def add(self, child):
        """
        Adds a child to this container.
        """

        self.children.append(child)
        self.child = child

    def render(self, width, height, st):

        rv = self.child.render(width, height, st)
        self.offsets = [ (0, 0) ]
        self.sizes = [ rv.get_size() ]

        return rv

    def get_placement(self):
        return self.child.get_placement()
    
    def event(self, ev, x, y):
        for i, (xo, yo)  in zip(self.children, self.offsets):
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

class Position(Container):
    """
    Controls the placement of a displayable on the screen, using
    supplied positon properties. This is the non-curried form of
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

        super(Position, self).__init__()

        self.style = renpy.style.Style(style, properties)
        self.add(child)

    def render(self, width, height, st):

        surf = self.child.render(width, height, st)
        cw, ch = surf.get_size()

        self.offsets = [ (0, 0) ]
        self.sizes = [ (cw, ch) ]

        return surf

    def get_placement(self):
        return self.style

            

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
            surf = i.render(remwidth, height, st)

            sw, sh = surf.get_size()

            remwidth -= sw
            remwidth -= self.padding

            xo += sw + self.padding

            myheight = max(sh, myheight)

            surfaces.append(surf)
            self.sizes.append((sw, sh))


        width = xo - self.padding
        
        rv = renpy.display.surface.Surface(width, myheight)

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

            surf = i.render(width, remheight, st)

            sw, sh = surf.get_size()

            remheight -= sh
            remheight -= self.padding

            yo += sh + self.padding

            mywidth = max(sw, mywidth)

            surfaces.append(surf)
            self.sizes.append((sw, sh))


        height = yo - self.padding
        
        rv = renpy.display.surface.Surface(mywidth, height)

        for surf, child, yo in zip(surfaces, self.children, yoffsets):

            sw, sh = surf.get_size()

            offset = child.place(rv, 0, yo, mywidth, sh, surf)

            self.offsets.append(offset)

        return rv
    
class Fixed(Container):
    """
    A container that lays out each of its children at fixed
    coordinates determined by the position style of the child. Each
    widget is given the whole area of this widget, and then placed
    within that area based on its position style.

    The result of this layout is the size of the entire area allocated
    to it. So it's probably only viable for laying out a root window.
    """

    def __init__(self, style='default', **properties):
        super(Fixed, self).__init__()
        self.style = renpy.style.Style(style, properties)

    def get_placement(self):
        return self.style

    def render(self, width, height, st):

        self.offsets = [ ]
        self.sizes = [ ]

        rv = renpy.display.surface.Surface(width, height)

        for child in self.children:
            surf = child.render(width, height, st)
            self.sizes.append(surf.get_size())

            offset = child.place(rv, 0, 0, width, height, surf)
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

        super(Window, self).__init__()

        self.add(child)
        self.style = renpy.style.Style(style, properties)

    def get_placement(self):
        return self.style

    def render(self, width, height, st):

        # save typing and screen space.
        style = self.style


        # Render the child.
        surf = self.child.render(width  - 2 * style.xmargin - 2 * style.xpadding,
                                 height - 2 * style.ymargin - 2 * style.ypadding,
                                 st)

        sw, sh = surf.get_size()

        # If we don't fill, shrink our size to fit.

        if not style.xfill:
            width = max(2 * style.xmargin + 2 * style.xpadding + sw, style.xminimum)

        if not style.yfill:
            height = max(2 * style.ymargin + 2 * style.ypadding + sh, style.yminimum)

        rv = renpy.display.surface.Surface(width, height)

        # Draw the background. The background should render at exactly the
        # requested size. (That is, be a Frame or a Solid).
        if style.background:
            bw = width  - 2 * style.xmargin
            bh = height - 2 * style.ymargin

            back = style.background.render(bw, bh, st)

            rv.blit(back,
                    (style.xmargin, style.ymargin))
                    # (0, 0, bw, bh))

        offsets = self.child.place(rv,
                                   style.xmargin + style.xpadding,
                                   style.ymargin + style.ypadding,
                                   width  - 2 * (style.xmargin + style.xpadding),
                                   height - 2 * (style.ymargin + style.ypadding),
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

        @param startpos: The initial coordinates of the upper-left corner of the screen, relative to the image.

        @param endpos: The coordinates of the upper-left corner of the screen, relative to the image, after time has elapsed.

        @param time: The time it takes to pan from startpos to endpos.
        """

        super(Pan, self).__init__()
        self.add(child)

        self.startpos = startpos
        self.endpos = endpos
        self.time = time
        self.style = renpy.style.Style(style, properties)

    def get_position(self):
        return self.style

    def render(self, width, height, st):

        surf = self.child.render(width, height, st)

        x0, y0 = self.startpos
        x1, y1 = self.endpos

        tfrac = (st / self.time)

        if tfrac > 1.0:
            tfrac = 1.0

        xo = int(x0 * (1.0 - tfrac) + x1 * tfrac)
        yo = int(y0 * (1.0 - tfrac) + y1 * tfrac)
        

        self.offsets = [ (-xo, -yo) ]

        rv = renpy.display.surface.Surface(width, height)
        rv.blit(surf, (-xo, -yo))

        if st < self.time:
            renpy.game.interface.redraw(0)

        return rv
