# This file contains classes that handle layout of displayables on
# the screen.

import pygame
from pygame.constants import *

import renpy

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

    def render(self, width, height, st, tt):

        rv = self.child.render(width, height, st, tt)
        self.offsets = [ (0, 0) ]
        self.sizes = [ rv.get_size() ]

        return rv
    
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

class Position(Container):
    """
    Controls how its child is placed inside the space allocated to it.

    Position is used when you have a child that is smaller than the
    space allocated to the child. (For example, an image that is
    smaller than the entire screen.) The parameters that are given to
    Position give the location of an anchor point, both relative to
    the enclosing box and to the child.
    """

    def __init__(self, child, xpos=None, ypos=None, xanchor="center", yanchor="bottom"):
        """
        @param child: The child that is being laid out.

        @param xpos: The position of the anchor point, expressed as a fraction of the width allocated to this displayable, or None to not pad in width.

        @param ypos: The position of the anchor point, expressed as a fraction of the height allocated to this displayable, or None to not pad in height.

        @param xanchor: One of 'left', 'center', or 'right', the position of the anchor relative to the child.

        @param yanchor: One of 'top', 'center', or 'bottom', the position of the anchor relativer to the child.
        """

        super(Position, self).__init__()

        self.add(child)
        self.xpos = xpos
        self.ypos = ypos
        self.xanchor = xanchor
        self.yanchor = yanchor

        if xanchor not in ('left', 'right', 'center'):
            raise Exception("xanchor '%s' is not known." % xanchor)

        if yanchor not in ('top', 'bottom', 'center'):
            raise Exception("yanchor '%s' is not known." % yanchor)
                           


    def render(self, width, height, tt, wt):

        surf = self.child.render(width, height, tt, wt)

        cw, ch = surf.get_size()

        xpos = self.xpos
        ypos = self.ypos

        if isinstance(xpos, float):
            xpos = int(xpos * width)

        if isinstance(ypos, float):
            ypos = int(ypos * height)

        if xpos is None:
            width = cw
            xoff = 0
        else:
            xoff = xpos

            if self.xanchor == 'left':
                xoff -= 0
            elif self.xanchor == 'right':
                xoff -= cw
            elif self.xanchor == 'center':
                xoff -= cw / 2

        if ypos is None:
            height = ch
            yoff = 0
        else:
            yoff = ypos

            if self.yanchor == 'top':
                yoff -= 0
            elif self.yanchor == 'bottom':
                yoff -= ch
            elif self.yanchor == 'center':
                yoff -= ch / 2

        rv = renpy.display.surface.Surface(width, height)
        rv.fill((0,0,0,0))
        rv.blit(surf, (xoff, yoff))

        self.offsets = [ (xoff, yoff) ]
        self.sizes = [ (cw, ch) ]

        return rv
            
class Resize(Container):
    """
    This changes the amount of space allocated to the given
    container.
    """

    def __init__(self, child, width=1.0, height=1.0):

        super(Resize, self).__init__()

        self.add(child)
        self.width = width
        self.height = height

    def render(self, width, height, st, wt):

        if isinstance(self.width, float):
            width = width * self.width
        else:
            width = self.width

        if isinstance(self.height, float):
            height = height * self.height
        else:
            height = self.height

        width = int(width)
        height = int(height)

        self.offsets = [ (0, 0) ]

        rv = self.child.render(width, height, st, wt)

        self.sizes = [ rv.get_size() ]

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

    def __init__(self, padding=0, minheight=0, alignment=0.0, full=False):
        super(HBox, self).__init__()

        self.padding = padding
        self.minheight = minheight
        self.alignment = alignment
        self.full = full

    def render(self, width, height, st, tt):

        self.offsets = [ ]
        self.sizes = [ ]

        surfaces = [ ]
        xoffsets = [ ]
        
        remwidth = width
        xo = 0

        myheight = self.minheight

        for i in self.children:

            xoffsets.append(xo)
            surf = i.render(remwidth, height, st, tt)

            sw, sh = surf.get_size()

            remwidth -= sw
            remwidth -= self.padding

            xo += sw + self.padding

            myheight = max(sh, myheight)

            surfaces.append(surf)
            self.sizes.append((sw, sh))


        if not self.full:
            width = xo - self.padding
        
        rv = renpy.display.surface.Surface(width, myheight)

        for surf, xo in zip(surfaces, xoffsets):
            sw, sh = surf.get_size()

            yo = int((myheight - sh) * self.alignment)

            rv.blit(surf, (xo, yo))

            self.offsets.append((xo, yo))

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

    def __init__(self, padding=0, minwidth=0, alignment=0.0, full=False):
        super(VBox, self).__init__()

        self.padding = padding
        self.minwidth = minwidth
        self.alignment = alignment
        self.full = full

    def render(self, width, height, st, tt):

        self.offsets = [ ]
        self.sizes = [ ]

        surfaces = [ ]
        yoffsets = [ ]

        remheight = height
        yo = 0

        mywidth = self.minwidth

        for i in self.children:

            yoffsets.append(yo)

            surf = i.render(width, remheight, st, tt)

            sw, sh = surf.get_size()

            remheight -= sh
            remheight -= self.padding

            yo += sh + self.padding

            mywidth = max(sw, mywidth)

            surfaces.append(surf)
            self.sizes.append((sw, sh))


        if not self.full:
            height = yo - self.padding
            

        rv = renpy.display.surface.Surface(mywidth, height)

        for surf, yo in zip(surfaces, yoffsets):

            sw, sh = surf.get_size()

            xo = int((mywidth - sw) * self.alignment)

            rv.blit(surf, (xo, yo))

            self.offsets.append((xo, yo))

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


    def render(self, width, height, st, tt):

        # save typing and screen space.
        style = self.style


        # Render the child.
        surf = self.child.render(width  - 2 * style.xmargin - 2 * style.xpadding,
                                 height - 2 * style.ymargin - 2 * style.ypadding,
                                 st, tt)

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

            print bw, bh

            back = style.background.render(bw, bh, st, tt)

            rv.blit(back,
                    (style.xmargin, style.ymargin))
                    # (0, 0, bw, bh))


        xpos = style.xpos
        ypos = style.ypos

        if isinstance(xpos, float):
            xpos = int(xpos * (width - sw - 2 * (style.xmargin + style.xpadding)))

        if isinstance(ypos, float):
            ypos = int(ypos * (height - sh - 2 * (style.ymargin + style.ypadding)))
    

        xo = style.xmargin + style.xpadding + xpos
        yo = style.ymargin + style.ypadding + ypos

        rv.blit(surf, (xo, yo))

        self.offsets = [ (xo, yo) ]
        self.sizes = [ (sw, sh) ]

        return rv
                
            
        
