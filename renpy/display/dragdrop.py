# Copyright 2004-2023 Tom Rothamel <pytom@bishoujo.us>
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

from __future__ import division, absolute_import, with_statement, print_function, unicode_literals
from renpy.compat import PY2, basestring, bchr, bord, chr, open, pystr, range, round, str, tobytes, unicode # *


import pygame_sdl2 as pygame

import renpy
from renpy.display.render import render, Render, redraw
from renpy.display.core import absolute
from renpy.display.behavior import map_event, run, run_unhovered


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


def default_drop_allowable(drop, drags):
    return True


class Drag(renpy.display.core.Displayable, renpy.revertable.RevertableObject):
    """
    :doc: drag_drop class
    :args: (d=None, drag_name=None, draggable=True, droppable=True, drag_raise=True, dragging=None, dragged=None, dropped=None, drag_handle=(0.0, 0.0, 1.0, 1.0), drag_joined=..., clicked=None, hovered=None, unhovered=None, mouse_drop=False, **properties)

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
    a pixel inside the drag handle for dragging or clicking to occur. If the
    :propref:`focus_mask` property is True, that pixel must not be transparent.

    A newly-created draggable is added to the default DragGroup. A draggable
    can only be in a single DragGroup - if it's added to a second group,
    it's removed from the first.

    When a Drag is first rendered, if it's position cannot be determined
    from the DragGroup it is in, the position of its upper-left corner
    is computed using the standard layout algorithm. Once that position
    has been computed, the layout properties are ignored in favor of the
    position stored inside the Drag.

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

    `activated`
        A callback (or list of callbacks) that is called when the mouse
        is pressed down on the drag. It is called with one argument, a
        a list of Drags that are being dragged. The return value of this
        callback is ignored.

    `dragging`
        A callback (or list of callbacks) that is called when the Drag is being
        dragged. It is called with one argument, a list of Drags that are
        being dragged. If the callback returns a value other than None, that
        value is returned as the result of the interaction.

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
        and clicked.  If the callback returns a value other than None,
        that value is returned as the result of the interaction.

    `alternate`
        An action that is run when the Drag is right-clicked (on the
        desktop) or long-pressed without moving (on mobile). It may
        be necessary to increase :var:`config.longpress_duration` if
        this triggers to early on mobile platforms.

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

    `drag_offscreen`
        Determines the conditions under which the drag is allowed
        to be dragged offscreen. Allowing offscreen dragging can be
        dangerous to use with drag_joined or drags that can change
        size, as the drags can leave the screen entirely, with no
        way to get them back on the screen.

        This should be one of:

        False
            To disallow dragging the drag offscreen. (The default)

        True
            To allow dragging offscreen, in any direction.

        "horizontal"
            To allow dragging offscreen in the horizontal direction only.

        "vertical"
            To allow dragging offscreen in the vertical direction only.

        (width, height)
            Both width and height must be integers. The drag can be
            dragged offscreen as long as a (width, height)-sized part
            of it remains on-screen. So, (100, 100) will ensure that
            at least a 100x100 pixel area of the displayable will
            remain on-screen even while the rest of the displayable
            can be dragged offscreen. Setting this to the width and
            height of the displayable being dragged is equivalent to
            not allowing the drag to go offscreen at all.

        (min_x, max_x, min_y, max_y)
            Where each of min_x, max_x, min_y, and max_y are integers.
            min_x is the number of pixels away from the left border,
            and max_x is the number of pixels away from the right
            border. The same goes for min_y and max_y on the top and
            bottom borders respectively. The drag can be moved until
            one of its edges hit the specified border. (0, 0, 0, 0)
            is equivalent to not allowing dragging offscreen at all.

            For example, (-100, 200, 0, 0) would allow the drag to be
            dragged 100 pixels off the left edge of the screen and 200
            pixels off the right edge of the screen, but does not
            allow it to be dragged offscreen at the top nor bottom.

            This can also be used to constrain the drag within the
            screen bounds. (200, -200, 200, -200) would only allow
            the drag within 200 pixels of the edges of the screen.

            You can envision this as an additional "border" around
            the drag, which may go outside the bounds of the screen,
            that constrains the drag to remain within it.

        callable
            A callable can be provided to drag_offscreen. It must
            take two arguments: an x and a y position which
            represents the dragged position of the top left corner of
            the drag, and it must return an (x, y) tuple which is the
            new (x, y) position the drag should be in. This callable
            is called frequently, whenever the drag is moved. For
            example, the following function snaps the drag into place
            every 300 pixels::

                def drag_snap(x, y):

                    if y < 300:
                        y = 0
                    elif y < 600:
                        y = 300
                    else:
                        y = 600

                    return 200, y

    `mouse_drop`
        If true, the drag is dropped on the first droppable under the cursor.
        If false, the default, the drag is dropped onto the droppable with
        the largest degree of overlap.

    `drop_allowable`
        A callback that is called to determine whether this drop will allow
        the current drags to be dropped onto it. It is called with two arguments.
        The first is the Drag which determines its sensitivity.
        The second is a list of Drags that are being dragged.

    Except for `d`, all of the parameters are available as fields (with
    the same name) on the Drag object. In addition, after the drag has
    been rendered, the following fields become available:

    `x`, `y`
        The position of the Drag relative to its parent, in pixels.

    `start_x`, `start_y`
        The drag start position of the Drag relative to its parent, in pixels.

    `w`, `h`
        The width and height of the Drag's child, in pixels.
    """

    z = 0

    focusable = True

    drag_group = None
    old_position = None
    drag_offscreen = False
    activated = None
    alternate = None
    dragging = None

    # The time a click started, or None if a click is not in progress.
    click_time = None

    def __init__(self,
                 d=None,
                 drag_name=None,
                 draggable=True,
                 droppable=True,
                 drag_raise=True,
                 dragged=None,
                 dropped=None,
                 drop_allowable=default_drop_allowable,
                 drag_handle=(0.0, 0.0, 1.0, 1.0),
                 drag_joined=default_drag_joined,
                 clicked=None,
                 hovered=None,
                 unhovered=None,
                 replaces=None,
                 drag_offscreen=False,
                 mouse_drop=False,
                 activated=None,
                 alternate=None,
                 style="drag",
                 dragging=None,
                 **properties):

        super(Drag, self).__init__(style=style, **properties)

        self.drag_name = drag_name
        self.draggable = draggable
        self.droppable = droppable
        self.drag_raise = drag_raise
        self.dragging = dragging
        self.dragged = dragged
        self.dropped = dropped
        self.drop_allowable = drop_allowable
        self.drag_handle = drag_handle
        self.drag_joined = drag_joined
        self.clicked = clicked
        self.hovered = hovered
        self.unhovered = unhovered
        self.activated = activated
        self.alternate = alternate
        self.drag_offscreen = drag_offscreen
        # if mouse_drop_check is True (default False), the drop will not
        #  use default major overlap between droppables but instead
        #  will use mouse coordinates to select droppable
        self.mouse_drop = mouse_drop

        # We're focusable if we can be dragged.
        self.focusable = draggable

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

        self.old_position = None

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
        # the target coordinates for the currently executing snap animation.
        self.target_at = 0

        # The duration of a new snap animation to execute starting at
        # the next render() call
        self.target_at_delay = 0

        # The displayable we were last dropping on.
        self.last_drop = None # type: renpy.display.core.Displayable|None

        # Did we move over the course of this drag?
        self.drag_moved = False

        # A z index that's changed when something is raised or lowered.
        self.z = 0

        if isinstance(replaces, Drag):
            self.x = replaces.x
            self.y = replaces.y
            self.at = replaces.at
            self.target_x = replaces.target_x
            self.target_y = replaces.target_y
            self.target_at = replaces.target_at
            self.target_at_delay = replaces.target_at_delay
            self.grab_x = replaces.grab_x
            self.grab_y = replaces.grab_y
            self.last_x = replaces.last_x
            self.last_y = replaces.last_y
            self.old_position = replaces.old_position
            self.drag_moved = replaces.drag_moved
            self.last_drop = replaces.last_drop
            self.mouse_drop = replaces.mouse_drop
            self.click_time = replaces.click_time
            self.z = replaces.z

        if d is not None:
            self.add(d)

    @property
    def _draggable(self):
        return self.draggable

    def snap(self, x, y, delay=0):
        """
        :doc: drag_drop method

        Changes the position of the drag. If the drag is not showing,
        then the position change is instantaneous. Otherwise, the
        position change takes `delay` seconds, and is animated as a
        linear move.
        """

        if (type(x) is float) and self.parent_width is not None:
            x = int(x * self.parent_width)

        if (type(y) is float) and self.parent_height is not None:
            y = int(y * self.parent_height)

        self.target_x = x
        self.target_y = y

        if self.x is not None:
            self.target_at_delay = delay
        else:
            self.target_at = self.at
            self.x = x
            self.y = y

        if self.drag_group is not None:
            self.drag_group.positions[self.drag_name] = (x, y, self.old_position)

        redraw(self, 0)

    def set_style_prefix(self, prefix, root):
        if root:
            super(Drag, self).set_style_prefix(prefix, root)

            if self.child is not None:
                self.child.set_style_prefix(prefix, False)

    def add(self, d):
        if self.child is not None:
            raise Exception("Drag expects either zero or one children.")

        self.child = renpy.easy.displayable(d)
        renpy.display.render.invalidate(self)

    def _clear(self):
        self.child = None
        renpy.display.render.redraw(self, 0)

    def set_child(self, d):
        """
        :doc: drag_drop method

        Changes the child of this drag to `d`.
        """

        self.child = renpy.easy.displayable(d)
        self.child.per_interact()
        renpy.display.render.invalidate(self)

    def top(self):
        """
        :doc: drag_drop method

        Raises this displayable to the top of its drag_group.
        """

        if self.drag_group is not None:
            self.drag_group.raise_children([ self ])

    def bottom(self):
        """
        :doc: drag_drop method

        Lowers this displayable to the bottom of its drag_group.
        """

        if self.drag_group is not None:
            self.drag_group.lower_children([ self ])

    def update_style_prefix(self):
        """
        This updates the style prefix for all Drag's associated
        with this drag movement.
        """
        # We may not be in the drag_joined group.
        self.set_style_prefix("idle_", True)

        # Set the style for joined_set
        for i in [i[0] for i in self.drag_joined(self)]:
            i.set_style_prefix("selected_hover_", True)

        if self.last_drop is not None:
            self.last_drop.set_style_prefix("selected_idle_", True)

    def visit(self):
        return [ self.child ]

    def focus(self, default=False):
        super(Drag, self).focus(default)

        # Update state back after restart_interaction
        if default and self.drag_moved:
            self.update_style_prefix()

        rv = None

        if not default:
            rv = run(self.hovered)

        return rv

    def unfocus(self, default=False):
        super(Drag, self).unfocus(default)

        if not default:
            run_unhovered(self.hovered)
            run(self.unhovered)

    def render(self, width, height, st, at):

        child = self.style.child
        if child is None:
            child = self.child

        self.parent_width = renpy.display.render.render_width
        self.parent_height = renpy.display.render.render_height

        cr = render(child, width, height, st, at)
        cw, ch = cr.get_size()

        rv = Render(cw, ch)
        rv.blit(cr, (0, 0))

        self.w = cw
        self.h = ch

        position = (self.style.xpos, self.style.ypos, self.style.xanchor, self.style.yanchor, self.style.xoffset, self.style.yoffset)

        # If we don't have a position, then look for it in a drag group.
        if (self.x is None) and (self.drag_group is not None) and (self.drag_name is not None):
            if self.drag_name in self.drag_group.positions:
                dgp = self.drag_group.positions[self.drag_name]
                if len(dgp) == 3:
                    self.x, self.y, self.old_position = dgp
                else:
                    self.x, self.y = dgp
                    self.old_position = position

        if self.old_position != position:
            place = True
        elif self.x is None:
            place = True
        else:
            place = False

        # If we don't have a position, run the placement code and use
        # that to compute our placement.
        if place:
            # This is required to get get_placement to work properly.
            self.x = None

            place_x, place_y = self.place(None, 0, 0, width, height, rv)

            self.x = int(place_x)
            self.y = int(place_y)

            self.target_x = None

            self.old_position = position

        if self.target_x is None:
            self.target_x = self.x
            self.target_y = self.y
            self.target_at = at

        # Determine if we need to do the snap animation.
        if self.target_at_delay:
            # Snap starts now
            self.target_at = at + self.target_at_delay
            self.target_at_delay = 0
            redraw(self, 0)
        elif self.target_at <= at or self.target_at <= self.at:
            # Snap complete
            self.x = self.target_x
            self.y = self.target_y
        else:
            # Snap in progress
            done = (at - self.at) / (self.target_at - self.at)
            self.x = absolute(self.x + done * (self.target_x - self.x)) # type: ignore
            self.y = absolute(self.y + done * (self.target_y - self.y)) # type: ignore
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

            mask = self.style.focus_mask

            if mask is True:
                mask = cr.subsurface((fx, fy, fw, fh))
            elif mask is not None:
                try:
                    mask = renpy.display.render.render(mask, fw, fh, st, at)
                except Exception:
                    if callable(mask):
                        mask = mask
                    else:
                        raise Exception("Focus_mask must be None, True, a displayable, or a callable.")

            if mask is not None:
                fmx = 0
                fmy = 0
            else:
                fmx = None
                fmy = None

            rv.add_focus(self, None, fx, fy, fw, fh, fmx, fmy, mask)

        self.last_x = self.x
        self.last_y = self.y
        self.at = at

        return rv

    def event(self, ev, x, y, st):

        if not self.is_focused():
            return self.child.event(ev, x, y, st)

        # Mouse, in parent-relative coordinates.
        par_x = int(self.last_x + x)
        par_y = int(self.last_y + y)

        grabbed = (renpy.display.focus.get_grab() is self)

        if (self.alternate is not None) and renpy.display.touch and map_event(ev, "drag_activate"):
            self.click_time = st
            renpy.game.interface.timeout(renpy.config.longpress_duration)

        joined = [ ] # typing

        if grabbed:
            joined_offsets = self.drag_joined(self)
            joined = [ i[0] for i in joined_offsets ] # type: list[Drag]

        elif self.draggable and map_event(ev, "drag_activate"):

            joined_offsets = self.drag_joined(self)
            joined = [ i[0] for i in joined_offsets ] # type: list[Drag]

            if not joined:
                raise renpy.display.core.IgnoreEvent()

            renpy.display.focus.set_grab(self)

            run(joined[0].activated, joined)

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

            renpy.exports.play(self.style.activate_sound)

        elif (self.alternate is not None) and map_event(ev, "button_alternate"):
            rv = run(self.alternate)
            if rv is not None:
                return rv

            raise renpy.display.core.IgnoreEvent()

        if (
            (self.alternate is not None) and
            renpy.display.touch and
            (self.click_time is not None) and
            ((st - self.click_time) > renpy.config.longpress_duration)
        ):

            self.click_time = None

            rv = run(self.alternate)
            if rv is not None:
                return rv

            renpy.exports.vibrate(renpy.config.longpress_vibrate)

        # Handle clicking on droppables.
        if not grabbed:
            if self.clicked is not None and map_event(ev, "drag_deactivate"):

                self.click_time = None

                rv = run(self.clicked)
                if rv is not None:
                    return rv

                raise renpy.display.core.IgnoreEvent()

            return self.child.event(ev, x, y, st)

        # Handle moves by moving things relative to the grab point.
        if ev.type in (pygame.MOUSEMOTION, pygame.MOUSEBUTTONUP, pygame.MOUSEBUTTONDOWN):

            handled = True

            if (not self.drag_moved) and (self.start_x != par_x or self.start_y != par_y):
                self.drag_moved = True
                self.click_time = None

                # Raise the joined items.
                if self.drag_raise and self.drag_group is not None:
                    self.drag_group.raise_children(joined) # type: ignore

            if self.drag_moved:
                for i, xo, yo in joined_offsets: # type: ignore

                    new_x = int(par_x - self.grab_x + xo) # type: ignore
                    new_y = int(par_y - self.grab_y + yo) # type: ignore

                    # Constrain x-axis
                    if not self.drag_offscreen or self.drag_offscreen == "vertical":
                        new_x = max(new_x, 0)
                        new_x = min(new_x, int(i.parent_width - i.w))
                    # Constrain y-axis
                    if not self.drag_offscreen or self.drag_offscreen == "horizontal":
                        new_y = max(new_y, 0)
                        new_y = min(new_y, int(i.parent_height - i.h))

                    if isinstance(self.drag_offscreen, tuple):
                        if len(self.drag_offscreen) not in (2, 4):
                            raise Exception("Invalid number of arguments to drag_offscreen.")

                        # Tuple of (x_min, x_max, y_min, y_max)
                        if len(self.drag_offscreen) == 4:
                            x_min, x_max, y_min, y_max = self.drag_offscreen
                            new_x = max(new_x, x_min)
                            new_x = min(new_x, int(i.parent_width - i.w + x_max))
                            new_y = max(new_y, y_min)
                            new_y = min(new_y, int(i.parent_height - i.h + y_max))
                        else: # 2 arguments; (width, height)
                            x_width, y_height = self.drag_offscreen
                            new_x = max(new_x, int(x_width - i.w))
                            new_x = min(new_x, int(i.parent_width - x_width))
                            new_y = max(new_y, int(y_height - i.h))
                            new_y = min(new_y, int(i.parent_height - y_height))

                    # Callable called with x, y position
                    elif callable(self.drag_offscreen):
                        new_x, new_y = self.drag_offscreen(new_x, new_y)

                    if i.drag_group is not None and i.drag_name is not None:
                        i.drag_group.positions[i.drag_name] = (new_x, new_y, self.old_position)

                    i.x = new_x
                    i.y = new_y
                    i.target_x = new_x
                    i.target_y = new_y
                    i.target_at = self.at
                    # Call the dragging callback.
                    drag = joined[0]
                    if drag.dragging is not None:
                        rv = run(drag.dragging, joined)
                        if rv is not None:
                            return rv
                    redraw(i, 0)

        else:
            handled = False

        if (self.drag_group is not None) and self.drag_moved:
            if self.mouse_drop:
                drop = self.drag_group.get_drop_at(joined, par_x, par_y) # type: ignore
            else:
                drop = self.drag_group.get_best_drop(joined) # type: ignore
        else:
            drop = None

        if drop is not self.last_drop:

            if self.last_drop is not None:
                self.last_drop.set_style_prefix("idle_", True)

            self.last_drop = drop # type: ignore

        if self.drag_moved:
            self.update_style_prefix()

        if map_event(ev, 'drag_deactivate'):

            self.click_time = None

            renpy.display.focus.set_grab(None)

            if drop is not None:
                drop.set_style_prefix("idle_", True) # type: ignore

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
                if drop is not None and drop.dropped is not None: # type: ignore
                    rv = run(drop.dropped, drop, joined) # type: ignore
                    if rv is not None:
                        return rv

            else:

                # Call the clicked callback.
                if self.clicked:
                    rv = run(self.clicked)
                    if rv is not None:
                        return rv

        if handled:
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


    `min_overlap`
        An integer which means the minimum number of pixels at the
        overlap for the drop to be allowed.
    """

    z_serial = 0
    sorted = False

    _list_type = renpy.revertable.RevertableList

    def __init__(self, *children, **properties):
        properties.setdefault("style", "fixed")
        properties.setdefault("layout", "fixed")

        replaces = properties.pop("replaces", None)

        min_overlap = properties.pop("min_overlap", 0)
        self.min_overlap = min_overlap

        super(DragGroup, self).__init__(**properties)

        self.sorted = False

        if isinstance(replaces, DragGroup):
            self.positions = renpy.revertable.RevertableDict(replaces.positions)
            self.sensitive = replaces.sensitive
            self.z_serial = replaces.z_serial
        else:
            self.positions = renpy.revertable.RevertableDict()
            self.sensitive = True
            self.z_serial = 0

        for i in children:
            self.add(i)

    def add(self, child):
        """
        :doc: drag_drop method

        Adds `child`, which must be a Drag, to this DragGroup.
        """

        if not isinstance(child, Drag):
            raise Exception("Only drags can be added to a drag group.")

        super(DragGroup, self).add(child)

        self.sorted = False
        renpy.display.render.invalidate(self)

    def remove(self, child):
        """
        :doc: drag_drop method

        Removes `child` from this DragGroup.
        """

        if not isinstance(child, Drag):
            raise Exception("Only drags can be removed from a drag group.")

        child.x = None
        super(DragGroup, self).remove(child)

    def render(self, width, height, st, at):

        for i in self.children:
            i.drag_group = self

        if not self.sorted:
            self.children.sort(key=lambda i : i.z)
            self.sorted = True

        return super(DragGroup, self).render(width, height, st, at)

    def event(self, ev, x, y, st):

        if not self.sensitive:
            return None

        return super(DragGroup, self).event(ev, x, y, st)

    def raise_children(self, l):
        """
        Raises the children in the list `l` to the top of this drag group.
        Each is raised in the order that it appears in `l`, which means that
        the last element of `l` will be raised closest to the player.
        """

        self.sorted = False

        for i in l:
            self.z_serial += 1
            i.z = self.z_serial

        renpy.display.render.redraw(self, 0)

    def lower_children(self, l):
        """
        Lowers the children in the list `l` to the bottom of this drag group.
        Each is lowered in the order that it appears in `l`, which means that
        the last element of `l` will be the lowest of the children.

        Lowers the children in `l` to the bottom of this drag group, with
        the one at the bottom being the lowest.
        """

        self.sorted = False

        for i in l:
            self.z_serial += 1
            i.z = -self.z_serial

        renpy.display.render.redraw(self, 0)

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

                if c.x is None:
                    continue

                r2 = (c.x, c.y, c.w, c.h)

                overlap = rect_overlap_area(r1, r2)

                if (
                    overlap >= max_overlap and
                    overlap >= self.min_overlap and
                    c.drop_allowable(c, joined)
                ):
                    rv = c
                    max_overlap = overlap

        if max_overlap <= 0:
            return None
        else:
            return rv

    def get_drop_at(self, joined, x, y):
        """
        Returns the droppable that is exactly at x, y.
        """

        joined_set = set(joined)
        for c in self.children:
            if c in joined_set:
                continue

            if not c.droppable:
                continue

            if c.x is None:
                continue

            if (
                x >= c.x and y >= c.y and
                x < (c.x + c.w) and y < (c.y + c.h) and
                c.drop_allowable(c, joined)
            ):
                return c

    def get_children(self):
        """
        Returns a list of Drags that are the children of
        this DragGroup.
        """

        return renpy.revertable.RevertableList(self.children)

    def get_child_by_name(self, name):
        """
        :doc: drag_drop method

        Returns the first child of this DragGroup that has a drag_name
        of `name`.
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
