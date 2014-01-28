# Copyright 2004-2014 Tom Rothamel <pytom@bishoujo.us>
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

# TODO: Use overlap (rather than simple pointer location) to determine
# drag and drop.

import renpy.display
from renpy.display.render import render, Render, redraw
from renpy.display.core import absolute
from renpy.display.behavior import map_event, run

import pygame

def default_drag_group():
    """
    Gets the default drag group. If it doesn't exist yet, creates it.
    """

    sls = renpy.game.context().scene_lists

    rv = sls.drag_group

    if rv is None:
        rv = DragGroup()
        sls.drag_group = rv

    return rv

def default_drag_joined(drag):
    return [ (drag, 0, 0) ]

class Drag(renpy.display.core.Displayable, renpy.python.RevertableObject):
    """
    :doc: drag_drop class
    :args: (d=None, drag_name=None, draggable=True, droppable=True, drag_raise=True, dragged=None, dropped=None, drag_handle=(0.0, 0.0, 1.0, 1.0), drag_joined=..., clicked=None, hovered=None, unhovered=None, **properties)

    A displayable that represents an object that can be dragged around
    its enclosing area. A Drag can also represent an area that
    other Drags can be dropped on.

    A Drag can be moved around inside is parent. Generally, its parent
    should be either a :func:`Fixed` or :class:`DragGroup`.

    A Drag has one child. The child's state reflects the status
    of the drag and drop operation:

    * ``selected_hover`` - when it is being dragged.
    * ``selected_idle`` - when it can be dropped on.
    * ``hover`` - when the draggable will be dragged when the mouse is
      clicked.
    * ``idle`` - otherwise.

    The drag handle is a rectangle inside the child. The mouse must be over
    a non-transparent pixel inside the drag handle for dragging or clicking
    to occur.

    A newly-created draggable is added to the default DragGroup. A draggable
    can only be in a single DragGroup - if it's added to a second group,
    it's removed from the first.

    When a Drag is first rendered, if it's position cannot be determined
    from the DragGroup it is in, the position of its upper-left corner
    is computed using the standard layout algorithm. Once that position


    `d`
        If present, the child of this Drag. Drags use the child style
        in preference to this, if it's not None.

    `drag_name`
        If not None, the name of this draggable. This is available
        as the `name` property of draggable objects. If a Drag
        with the same name is or was in the DragGroup, the starting
        position of this Drag is taken from that Draggable.

    `draggable`
        If true, the Drag can be dragged around the screen with
        the mouse.

    `droppable`
        If true, other Drags can be dropped on this Drag.

    `drag_raise`
        If true, this Drag is raised to the top when it is dragged. If
        it is joined to other Drags, all joined drags are raised.

    `dragged`
        A callback (or list of callbacks) that is called when the Drag
        has been dragged. It is called with two arguments. The first is
        a list of Drags that are being dragged. The second is either
        a Drag that is being dropped onto, or None of a drop did not
        occur. If the callback returns a value other than None, that
        value is returned as the result of the interaction.

    `dropped`
        A callback (or list of callbacks) that is called when this Drag
        is dropped onto. It is called with two arguments. The first
        is the Drag being dropped onto. The second is a list of Drags that
        are being dragged.  If the callback returns a value other than None,
        that value is returned as the result of the interaction.

        When a dragged and dropped callback are triggered for the same
        event, the dropped callback is only called if dragged returns
        None.

    `clicked`
        A callback this is called, with no arguments, when the Drag is
        clicked without being moved. A droppable can also be focused
        and clicked.  If the callback returns a value othe than None,
        that value is returned as the result of the interaction.

    `drag_handle`
        A (x, y, width, height) tuple, giving the position of the drag
        handle within the child. In this tuple, integers are considered
        to be a literal number of pixels, while floats are relative to
        the size of the child.

    `drag_joined`
        This is called with the current Drag as an argument. It's
        expected to return a list of [ (drag, x, y) ] tuples, giving
        the draggables to drag as a unit. `x` and `y` are the offsets
        of the drags relative to each other, they are not relative
        to the corner of this drag.

    Except for `d`, all of the parameters are available as fields (with
    the same name) on the Drag object. In addition, after the drag has
    been rendered, the following fields become available:

    `x`, `y`
         The position of the Drag relative to its parent, in pixels.

    `w`, `h`
         The width and height of the Drag's child, in pixels.
        """

    def __init__(self,
                 d=None,
                 drag_name=None,
                 draggable=True,
                 droppable=True,
                 drag_raise=True,
                 dragged=None,
                 dropped=None,
                 drag_handle=(0.0, 0.0, 1.0, 1.0),
                 drag_joined=default_drag_joined,
                 clicked=None,
                 hovered=None,
                 unhovered=None,
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
        self.drag_joined = drag_joined
        self.clicked = clicked
        self.hovered = hovered
        self.unhovered = unhovered

        self.child = None

        # Add us to a drag group on creation.
        if drag_name:
            self.drag_group = default_drag_group()

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

        # The offset from the location of the mouse to the "grab point",
        # which is where the things that are being moved are offset from.
        self.grab_x = None
        self.grab_y = None

        # x and y from the last time we rendered.
        self.last_x = None
        self.last_y = None

        # The abs_x and abs_y from when we started the grab.
        self.start_x = 0
        self.start_y = 0

        # The last time we were shown, using the animation timebases.
        self.at = 0

        # The (animation timebase) time at which we should reach
        # the target coordinates.
        self.target_at = 0

        # The displayable we were last dropping on.
        self.last_drop = None

        # Did we move over the course of this drag?
        self.drag_moved = False

        if replaces is not None:
            self.x = replaces.x
            self.y = replaces.y
            self.at = replaces.at
            self.target_x = replaces.target_x
            self.target_y = replaces.target_y
            self.target_at = replaces.target_at

        if d is not None:
            self.add(d)


    def snap(self, x, y, delay=0):
        """
        :doc: drag_drop method

        Changes the position of the drag. If the drag is not showing,
        then the position change is instantaneous. Otherwise, the
        position change takes `delay` seconds, and is animated as a
        linear move.
        """

        self.target_x = x
        self.target_y = y

        if self.x is not None:
            self.target_at = self.at + delay
        else:
            self.target_at = self.at
            self.x = x
            self.y = y

        redraw(self, 0)

    def set_style_prefix(self, prefix, root):
        super(Drag, self).set_style_prefix(prefix, root)

        if self.child is not None:
            self.child.set_style_prefix(prefix, False)

    def add(self, d):
        if self.child is not None:
            raise Exception("Drag expects either zero or one children.")

        self.child = renpy.easy.displayable(d)

    def set_child(self, d):
        """
        :doc: drag_drop method

        Changes the child of this drag to `d`.
        """

        d.per_interact()
        self.child = renpy.easy.displayable(d)

    def top(self):
        """
        :doc: drag_drop method

        Raises this displayable to the top of its drag_group.
        """

        if self.drag_group is not None:
            self.drag_group.raise_children([ self ])

    def visit(self):
        return [ self.child ]

    def focus(self, default=False):
        super(Drag, self).focus(default)

        rv = None

        if not default:
            rv = run(self.hovered)

        return rv

    def unfocus(self, default=False):
        super(Drag, self).unfocus(default)

        if not default:
            run(self.unhovered)

    def render(self, width, height, st, at):

        child = self.style.child
        if child is None:
            child = self.child

        self.parent_width = width
        self.parent_height = height

        cr = render(child, width, height, st, at)
        cw, ch = cr.get_size()

        rv = Render(cw, ch)
        rv.blit(cr, (0, 0))

        self.w = cw
        self.h = ch

        # If we don't have a position, then look for it in a drag group.
        if (self.x is None) and (self.drag_group is not None) and (self.drag_name is not None):
            if self.drag_name in self.drag_group.positions:
                self.x, self.y = self.drag_group.positions[self.drag_name]

        # If we don't have a position, run the placement code and use
        # that to compute our placement.
        if self.x is None:
            self.x, self.y = self.place(None, 0, 0, width, height, rv)
            self.x = int(self.x)
            self.y = int(self.y)

        if self.target_x is None:
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

        if self.draggable or self.clicked is not None:

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

        if not self.is_focused():
            return self.child.event(ev, x, y, st)

        # if not self.draggable:
        #    return self.child.event(ev, x, y, st)

        # Mouse, in parent-relative coordinates.
        par_x = self.last_x + x
        par_y = self.last_y + y

        grabbed = (renpy.display.focus.get_grab() is self)

        if grabbed:
            joined_offsets = self.drag_joined(self)
            joined = [ i[0] for i in joined_offsets ]

        elif self.draggable and map_event(ev, "drag_activate"):

            joined_offsets = self.drag_joined(self)
            joined = [ i[0] for i in joined_offsets ]

            if not joined:
                raise renpy.display.core.IgnoreEvent()

            renpy.display.focus.set_grab(self)

            self.grab_x = x
            self.grab_y = y

            # If we're not the only thing we're joined with, we
            # might need to adjust our grab point.
            for i, xo, yo in joined_offsets:
                if i is self:
                    self.grab_x += xo
                    self.grab_y += yo
                    break

            self.drag_moved = False
            self.start_x = par_x
            self.start_y = par_y

            grabbed = True

        # Handle clicking on droppables.
        if not grabbed:
            if self.clicked is not None and map_event(ev, "drag_deactivate"):
                rv = run(self.clicked)
                if rv is not None:
                    return rv

                raise renpy.display.core.IgnoreEvent()

            return self.child.event(ev, x, y, st)

        # Handle moves by moving things relative to the grab point.
        if ev.type in (pygame.MOUSEMOTION, pygame.MOUSEBUTTONUP, pygame.MOUSEBUTTONDOWN):

            if not self.drag_moved and (self.start_x != par_x or self.start_y != par_y):
                self.drag_moved = True

                # We may not be in the drag_joined group.
                self.set_style_prefix("idle_", True)

                # Set the style.
                for i in joined:
                    i.set_style_prefix("selected_hover_", True)

                # Raise the joined items.
                if self.drag_raise and self.drag_group is not None:
                    self.drag_group.raise_children(joined)

            if self.drag_moved:
                for i, xo, yo in joined_offsets:

                    new_x = par_x - self.grab_x + xo
                    new_y = par_y - self.grab_y + yo
                    new_x = max(new_x, 0)
                    new_x = min(new_x, int(i.parent_width - i.w))
                    new_y = max(new_y, 0)
                    new_y = min(new_y, int(i.parent_height - i.h))

                    if i.drag_group is not None and i.drag_name is not None:
                        i.drag_group.positions[i.drag_name] = (new_x, new_y)

                    i.x = new_x
                    i.y = new_y
                    i.target_x = new_x
                    i.target_y = new_y
                    i.target_at = self.at
                    redraw(i, 0)

        if (self.drag_group is not None) and self.drag_moved:
            drop = self.drag_group.get_best_drop(joined)
        else:
            drop = None

        if drop is not self.last_drop:

            if self.last_drop is not None:
                self.last_drop.set_style_prefix("idle_", True)

            if drop is not None:
                drop.set_style_prefix("selected_idle_", True)

            self.last_drop = drop

        if map_event(ev, 'drag_deactivate'):
            renpy.display.focus.set_grab(None)

            if drop is not None:
                drop.set_style_prefix("idle_", True)

            for i in joined:
                i.set_style_prefix("idle_", True)

            self.set_style_prefix("hover_", True)

            self.grab_x = None
            self.grab_y = None
            self.last_drop = None

            if self.drag_moved:

                # Call the drag callback.
                drag = joined[0]
                if drag.dragged is not None:
                    rv = run(drag.dragged, joined, drop)
                    if rv is not None:
                        return rv

                # Call the drop callback.
                if drop is not None and drop.dropped is not None:
                    rv = run(drop.dropped, drop, joined)
                    if rv is not None:
                        return rv

            else:

                # Call the clicked callback.
                if self.clicked:
                    rv = run(self.clicked)
                    if rv is not None:
                        return rv

        raise renpy.display.core.IgnoreEvent()


    def get_placement(self):

        if self.x is not None:
            return self.x, self.y, 0, 0, 0, 0, True
        else:
            return super(Drag, self).get_placement()

    def per_interact(self):
        self.set_style_prefix("idle_", True)
        super(Drag, self).per_interact()


class DragGroup(renpy.display.layout.MultiBox):
    """
    :doc: drag_drop class

    Represents a group of Drags. A Drag is limited to the boundary of
    its DragGroup. Dropping only works between Drags that are in the
    same DragGroup. Drags may only be raised when they are inside a
    DragGroup.

    A DragGroup is laid out like a :func:`Fixed`.

    All positional parameters to the DragGroup constructor should be
    Drags, that are added to the DragGroup.
    """

    _list_type = renpy.python.RevertableList

    def __init__(self, *children, **properties):
        properties.setdefault("style", "fixed")
        properties.setdefault("layout", "fixed")

        replaces = properties.pop("replaces", None)

        super(DragGroup, self).__init__(**properties)

        if replaces is not None:
            self.positions = renpy.python.RevertableDict(replaces.positions)
            self.sensitive = replaces.sensitive
        else:
            self.positions = renpy.python.RevertableDict()
            self.sensitive = True

        for i in children:
            self.add(i)


    def add(self, child):
        """
        :doc: drag_drop method

        Adds `child`, which must be a Drag, to this DragGroup.
        """

        if not isinstance(child, Drag):
            raise Exception("Only drags can be added to a drag group.")

        child.drag_group = self
        super(DragGroup, self).add(child)

    def remove(self, child):
        """
        :doc: drag_drop method

        Removes `child` from this DragGroup.
        """


        if not isinstance(child, Drag):
            raise Exception("Only drags can be removed from a drag group.")

        child.x = None
        super(DragGroup, self).remove(child)


    def event(self, ev, x, y, st):

        if not self.sensitive:
            return None

        return super(DragGroup, self).event(ev, x, y, st)

    def raise_children(self, l):
        """
        Raises the children in `l` to the top of this drag_group, using the
        order given in l for those children.
        """

        s = set(l)

        offset_map = { }

        children = [ ]
        offsets = [ ]

        for i, c in enumerate(self.children):
            if i < len(self.offsets):
                o = self.offsets[i]
            else:
                o = (0, 0)

            if c not in s:
                children.append(c)
                offsets.append(o)
            else:
                offset_map[c] = o

        for c in l:
            if c in offset_map:
                children.append(c)
                offsets.append(offset_map[c])

        self.children = self._list_type(children)
        self.offsets = self._list_type(offsets)


    def get_best_drop(self, joined):
        """
        Returns the droppable that the members of joined overlap the most.
        """

        max_overlap = 0
        rv = 0

        joined_set = set(joined)

        for d in joined:

            r1 = (d.x, d.y, d.w, d.h)

            for c in self.children:
                if c in joined_set:
                    continue

                if not c.droppable:
                    continue

                r2 = (c.x, c.y, c.w, c.h)

                overlap = rect_overlap_area(r1, r2)

                if overlap >= max_overlap:
                    rv = c
                    max_overlap = overlap

        if max_overlap <= 0:
            return None
        else:
            return rv

    def get_children(self):
        """
        Returns a list of Drags that are the children of
        this DragGroup.
        """

        return renpy.python.RevertableList(self.children)

    def get_child_by_name(self, name):
        """
        :doc: drag_drop method

        Returns the first child of this DragGroup that has a drag_name
        of name.
        """

        for i in self.children:
            if i.drag_name == name:
                return i

        return None


def rect_overlap_area(r1, r2):
    """
    Returns the number of pixels by which rectangles r1 and r2 overlap.
    """

    x1, y1, w1, h1 = r1
    x2, y2, w2, h2 = r2

    maxleft = max(x1, x2)
    minright = min(x1 + w1, x2 + w2)
    maxtop = max(y1, y2)
    minbottom = min(y1 + h1, y2 + h2)

    if minright < maxleft:
        return 0

    if minbottom < maxtop:
        return 0

    return (minright - maxleft) * (minbottom - maxtop)
