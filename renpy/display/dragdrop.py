# Copyright 2004-2010 PyTom <pytom@bishoujo.us>
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

import renpy
from renpy.display.render import render, Render, redraw
from renpy.display.core import absolute
from renpy.display.behavior import map_event

import pygame

class Drag(renpy.display.core.Displayable):
    """
    :doc: dragdrop

    A displayable that represents an object that can be dragged around
    its enclosing area. A draggable can also represent an area that
    other draggables can be dropped on.
    
    A draggable has one child. The child's state reflects the status
    of the drag and drop operation:

    * ``selected_hover`` - when it is being dragged.
    * ``selected_idle`` - when it can be dropped on.
    * ``hover`` - when the draggable will be dragged when the mouse is
      clicked.
    * ``idle`` - otherwise. 

    The drag handle is a rectangle inside the child. Dragging moves the
    entire child, but only the handle is considered when deciding if
    dragging or dropping has occured.
    
    A newly-created draggable is added to the default DragGroup. A draggable
    can only be in a single DragGroup - if it's added to a second group,
    it's removed from the first.
    
    `drag_name`
        If not None, the name of this draggable. This is available
        as the `name` property of draggable objects. If a Draggable
        with the same name is or was in the DragGroup, the starting
        position of this Draggable is taken from that Draggable.

    `draggable`
        If true, the Draggable can be dragged around the screen with
        the mouse.

    `droppable`
        If true, other Draggables can be dropped on this Draggable.

    `drag_raise`
        If true, this Draggable is raised on Drag and Drop. If it has
        been joint to another Draggable, that Draggable is raised as
        well.         

    `dragged`
        A callback that is called when this Draggable has been dragged.
        It is called with two arguments. The first is this Draggable.
        The second is a Draggable that this Draggable has been dropped
        onto, or None no such Draggable exists. If the callback returns
        a value othe than None, that value is returned as the result of
        the interaction.

    `dropped`
        A callback that is called when another Draggable has been dropped
        onto this Draggable. It is called with two arguments, this
        Draggable and the other Draggable. If the callback returns
        a value othe than None, that value is returned as the result of
        the interaction.

    `drag_handle`
        A (x, y, width, height) tuple, giving the position of the drag
        handle within the child. In this tuple, integers are considered
        to be a literal number of pixels, while floats are relative to
        the size of the child. 
    """

    def __init__(self,
                 child=None,
                 drag_name=None,
                 draggable=True,
                 droppable=False,
                 drag_raise=True,
                 dragged=None,
                 dropped=None,
                 drag_handle=(0.0, 0.0, 1.0, 1.0),
                 replaces=None,
                 **properties):

        super(Drag, self).__init__(self, **properties)


        self.drag_name = drag_name
        self.draggable = draggable
        self.droppable = droppable
        self.drag_raise = drag_raise
        self.dragged = dragged 
        self.dropped = dropped
        self.drag_handle = drag_handle
        self.child = None

        # TODO: Add us to a draggroup upon creation.
        # TODO: handle replaces.
        
        # The current x and y coordinates of this displayable.
        self.x = None
        self.y = None

        # The width and height of the child.
        self.w = None
        self.h = None

        # The width and height of our parent.
        self.parent_width = None
        self.parent_height = None
        
        # The target x and y coordinates of this displayable. (The
        # coordinates that we're snapping to.)
        self.target_x = None
        self.target_y = None

        # The relative position we were grabbed at.
        self.grab_x = None
        self.grab_y = None

        # x and y from the last time we rendered.
        self.last_x = None
        self.last_y = None
        
        # The last time we were shown, using the animation timebases.
        self.at = 0

        # The (animation timebase) time at which we should reach
        # the target coordinates.
        self.target_at = 0

        if replaces is not None:
            self.x = replaces.x
            self.y = replaces.y
            self.target_x = replaces.target_x
            self.target_y = replaces.target_y
            self.at = replaces.at
            self.target_at = replaces.target_at
        
        if child is not None:
            self.add(child)

    def add(self, d):
        self.child = renpy.easy.displayable(d)

    def visit(self):
        return [ self.child ]

    def render(self, width, height, st, at):

        self.parent_width = width
        self.parent_height = height
        
        cr = render(self.child, width, height, st, at)
        cw, ch = cr.get_size()
        
        rv = Render(cw, ch)
        rv.blit(cr, (0, 0))

        self.w = cw
        self.h = ch

        # If we don't have a position, run the placement code and use
        # that to compute our placement.
        if self.x is None:
            self.x, self.y = self.place(None, 0, 0, width, height, rv)
            self.x = int(self.x)
            self.y = int(self.y)

            self.target_x = self.x
            self.target_y = self.y
            self.target_at = at

        # Determine if we need to do the snap animation.
        if at >= self.target_at:
            self.x = self.target_x
            self.y = self.target_y
        else:
            done = (at - self.at) / (self.target_at - self.at)
            self.x = absolute(self.x + done * (self.target_x - self.x))
            self.y = absolute(self.y + done * (self.target_y - self.y))
            redraw(self, 0)

        fx, fy, fw, fh = self.drag_handle

        if isinstance(fx, float):
            fx = int(fx * cw)

        if isinstance(fy, float):
            fy = int(fy * ch)

        if isinstance(fw, float):
            fw = int(fw * cw)

        if isinstance(fh, float):
            fh = int(fh * ch)

        rv.add_focus(self, None, fx, fy, fw, fh, fx, fy, cr.subsurface((fx, fy, fw, fh)))

        self.last_x = self.x
        self.last_y = self.y
        self.at = at
        
        return rv
    
    def event(self, ev, x, y, st):

        if not self.draggable or not self.is_focused():
            return self.child.event(ev, x, y, st)

        grabbed = (renpy.display.focus.get_grab() is self)

        if not grabbed and map_event(ev, "drag_activate"):
            renpy.display.focus.set_grab(self)
            grabbed = True

            self.grab_x = x
            self.grab_y = y

            raise renpy.display.core.IgnoreEvent()

        if not grabbed:
            return self.child.event(ev, x, y, st)
            
        dx = 0
        dy = 0

        if ev.type in (pygame.MOUSEMOTION, pygame.MOUSEBUTTONUP, pygame.MOUSEBUTTONDOWN):
            dx = x - self.grab_x 
            dy = y - self.grab_y

        if dx or dy:
            redraw(self, 0)
            
        new_x = int(self.last_x + dx)
        new_y = int(self.last_y + dy)

        new_x = max(new_x, 0)
        new_x = min(new_x, self.parent_width - self.w)

        new_y = max(new_y, 0)
        new_y = min(new_y, self.parent_height - self.h)            
            
        self.target_x = self.x = new_x
        self.target_y = self.y = new_y
        self.target_at = self.at

        if map_event(ev, 'drag_deactivate'):
            renpy.display.focus.set_grab(None)
            self.grab_x = None
            self.grab_y = None

            # TODO: Handle dragged.
            # TODO: Handle dropped.


    def get_placement(self):

        if self.x is not None:
            return self.x, self.y, 0, 0, 0, 0, True
        else:
            return super(Drag, self).get_placement()

