# Copyright 2004-2017 Tom Rothamel <pytom@bishoujo.us>
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

# This file contains code to manage focus on the display.

import pygame_sdl2 as pygame
import renpy.display


class Focus(object):

    def __init__(self, widget, arg, x, y, w, h, screen):

        self.widget = widget
        self.arg = arg
        self.x = x
        self.y = y
        self.w = w
        self.h = h
        self.screen = screen

    def copy(self):
        return Focus(
            self.widget,
            self.arg,
            self.x,
            self.y,
            self.w,
            self.h,
            self.screen)

    def __repr__(self):
        return "<Focus: %r %r (%r, %r, %r, %r) %r>" % (
            self.widget,
            self.arg,
            self.x,
            self.y,
            self.w,
            self.h,
            self.screen)


# The current focus argument.
argument = None

# The screen of the currently focused widget.
screen_of_focused = None

# The widget currently grabbing the input, if any.
grab = None

# The default focus for the current screen.
default_focus = None

# The type of input that caused the focus to change last. One of
# "keyboard" (for keyboard-like focus devices) or "mouse" (for mouse-like)
# focus devices.)
focus_type = "mouse"

# The same, but for the most recent input that might potentially cause
# the focus to change.
pending_focus_type = "mouse"

# Sets the currently focused widget.


def set_focused(widget, arg, screen):
    global argument
    argument = arg

    global screen_of_focused
    screen_of_focused = screen

    renpy.game.context().scene_lists.focused = widget

    renpy.display.tts.displayable(widget)

# Gets the currently focused widget.


def get_focused():
    return renpy.game.context().scene_lists.focused

# Get the mouse cursor for the focused widget.


def get_mouse():
    focused = get_focused()
    if focused is None:
        return None
    else:
        return focused.style.mouse


def set_grab(widget):
    global grab
    grab = widget

    renpy.exports.cancel_gesture()


def get_grab():
    return grab

# The current list of focuses that we know about.
focus_list = [ ]

# This takes in a focus list from the rendering system.


def take_focuses():
    global focus_list
    focus_list = [ ]

    renpy.display.render.take_focuses(focus_list)

    global default_focus
    default_focus = None

    for f in focus_list:
        if f.x is None:
            default_focus = f

    if (default_focus is not None) and (get_focused() is None):
        change_focus(default_focus, True)


def focus_coordinates():
    """
    :doc: other

    This attempts to find the coordinates of the currently-focused
    displayable. If it can, it will return them as a (x, y, w, h)
    tuple. If not, it will return a (None, None, None, None) tuple.
    """

    current = get_focused()

    for i in focus_list:
        if i.widget == current and i.arg == argument:
            return i.x, i.y, i.w, i.h

    return None, None, None, None


# A map from id(displayable) to the displayable that replaces it.
replaced_by = { }


def before_interact(roots):
    """
    Called before each interaction to choose the focused and grabbed
    displayables.
    """

    global new_grab
    global grab

    # a list of focusable, name, screen tuples.
    fwn = [ ]

    def callback(f, n):
        fwn.append((f, n, renpy.display.screen._current_screen))

    for root in roots:
        root.find_focusable(callback, None)

    # Assign a full name to each focusable.

    namecount = { }

    fwn2 = [ ]

    for fwn_tuple in fwn:

        f, n, screen = fwn_tuple

        serial = namecount.get(n, 0)
        namecount[n] = serial + 1

        if f is None:
            continue

        f.full_focus_name = n, serial

        replaced_by[id(f)] = f

        fwn2.append(fwn_tuple)

    fwn = fwn2

    # We assume id(None) is not in replaced_by.
    replaced_by.pop(None, None)

    # If there's something with the same full name as the current widget,
    # it becomes the new current widget.

    current = get_focused()
    current = replaced_by.get(id(current), current)

    if current is not None:
        current_name = current.full_focus_name

        for f, n, screen in fwn:
            if f.full_focus_name == current_name:
                current = f
                set_focused(f, None, screen)
                break
        else:
            current = None

    # Otherwise, focus the default widget, or nothing.
    if current is None:

        for f, n, screen in fwn:
            if f.default:
                current = f
                set_focused(f, None, screen)
                break
        else:
            set_focused(None, None, None)

    # Finally, mark the current widget as the focused widget, and
    # all other widgets as unfocused.
    for f, n, screen in fwn:
        if f is not current:
            renpy.display.screen.push_current_screen(screen)
            try:
                f.unfocus(default=True)
            finally:
                renpy.display.screen.pop_current_screen()

    if current:
        renpy.display.screen.push_current_screen(screen_of_focused)
        try:
            current.focus(default=True)
        finally:
            renpy.display.screen.pop_current_screen()

    # Update the grab.
    grab = replaced_by.get(id(grab), None)

    # Clear replaced_by.
    replaced_by.clear()

# This changes the focus to be the widget contained inside the new
# focus object.


def change_focus(newfocus, default=False):
    rv = None

    if grab:
        return

    if newfocus is None:
        widget = None
    else:
        widget = newfocus.widget

    current = get_focused()

    # Nothing to do.
    if current is widget and (newfocus is None or newfocus.arg == argument):
        return rv

    global focus_type
    focus_type = pending_focus_type

    if current is not None:
        try:
            renpy.display.screen.push_current_screen(screen_of_focused)
            current.unfocus(default=default)
        finally:
            renpy.display.screen.pop_current_screen()

    current = widget

    if newfocus is not None:
        set_focused(current, newfocus.arg, newfocus.screen)
    else:
        set_focused(None, None, None)

    if widget is not None:
        try:
            renpy.display.screen.push_current_screen(screen_of_focused)
            rv = widget.focus(default=default)
        finally:
            renpy.display.screen.pop_current_screen()

    return rv


def clear_focus():
    """
    Clears the focus when the window loses mouse focus.
    """

    change_focus(None)

# This handles mouse events, to see if they change the focus.


def mouse_handler(ev, x, y, default=False):
    """
    Handle mouse events, to see if they change the focus.

    `ev`
        If ev is not None, this function checks to see if it is a mouse event.
    """

    global pending_focus_type

    if ev is not None:
        if ev.type not in (pygame.MOUSEMOTION, pygame.MOUSEBUTTONUP, pygame.MOUSEBUTTONDOWN):
            return
        else:
            pending_focus_type = "mouse"

    new_focus = renpy.display.render.focus_at_point(x, y)

    if new_focus is None:
        new_focus = default_focus

    return change_focus(new_focus, default=default)


# This focuses an extreme widget, which is one of the widgets that's
# at an edge. To do this, we multiply the x, y, width, and height by
# the supplied multiplers, add them all up, and take the focus with
# the largest value.
def focus_extreme(xmul, ymul, wmul, hmul):

    max_focus = None
    max_score = -(65536**2)

    for f in focus_list:

        if f.x is None:
            continue

        score = (f.x * xmul +
                 f.y * ymul +
                 f.w * wmul +
                 f.h * hmul)

        if score > max_score:
            max_score = score
            max_focus = f

    if max_focus:
        return change_focus(max_focus)


# This calculates the distance between two points, applying
# the given fudge factors. The distance is left squared.
def points_dist(x0, y0, x1, y1, xfudge, yfudge):
    return (( x0 - x1 ) * xfudge ) ** 2 + \
           (( y0 - y1 ) * yfudge ) ** 2


# This computes the distance between two horizontal lines. (So the
# distance is either vertical, or has a vertical component to it.)
#
# The distance is left squared.
def horiz_line_dist(ax0, ay0, ax1, ay1, bx0, by0, bx1, by1):

    # The lines overlap in x.
    if bx0 <= ax0 <= ax1 <= bx1 or \
       ax0 <= bx0 <= bx1 <= ax1 or \
       ax0 <= bx0 <= ax1 <= bx1 or \
       bx0 <= ax0 <= bx1 <= ax1:
        return (ay0 - by0) ** 2

    # The right end of a is to the left of the left end of b.
    if ax0 <= ax1 <= bx0 <= bx1:
        return points_dist(ax1, ay1, bx0, by0, renpy.config.focus_crossrange_penalty, 1.0)
    else:
        return points_dist(ax0, ay0, bx1, by1, renpy.config.focus_crossrange_penalty, 1.0)


# This computes the distance between two vertical lines. (So the
# distance is either hortizontal, or has a horizontal component to it.)
#
# The distance is left squared.
def verti_line_dist(ax0, ay0, ax1, ay1, bx0, by0, bx1, by1):

    # The lines overlap in x.
    if by0 <= ay0 <= ay1 <= by1 or \
       ay0 <= by0 <= by1 <= ay1 or \
       ay0 <= by0 <= ay1 <= by1 or \
       by0 <= ay0 <= by1 <= ay1:
        return (ax0 - bx0) ** 2

    # The right end of a is to the left of the left end of b.
    if ay0 <= ay1 <= by0 <= by1:
        return points_dist(ax1, ay1, bx0, by0, 1.0, renpy.config.focus_crossrange_penalty)
    else:
        return points_dist(ax0, ay0, bx1, by1, 1.0, renpy.config.focus_crossrange_penalty)


# This focuses the widget that is nearest to the current widget. To
# determine nearest, we compute points on the widgets using the
# {from,to}_{x,y}off values. We pick the nearest, applying a fudge
# multiplier to the distances in each direction, that satisfies
# the condition (which is given a Focus object to evaluate).
#
# If no focus can be found matching the above, we look for one
# with an x of None, and make that the focus. Otherwise, we do
# nothing.
#
# If no widget is focused, we pick one and focus it.
#
# If the current widget has an x of None, we pass things off to
# focus_extreme to deal with.
def focus_nearest(from_x0, from_y0, from_x1, from_y1,
                  to_x0, to_y0, to_x1, to_y1,
                  line_dist,
                  condition,
                  xmul, ymul, wmul, hmul):

    global pending_focus_type
    pending_focus_type = "keyboard"

    if not focus_list:
        return

    # No widget focused.
    current = get_focused()

    if not current:
        change_focus(focus_list[0])
        return

    # Find the current focus.
    for f in focus_list:
        if f.widget is current and f.arg == argument:
            from_focus = f
            break
    else:
        # If we can't pick something.
        change_focus(focus_list[0])
        return

    # If placeless, focus_extreme.
    if from_focus.x is None:
        focus_extreme(xmul, ymul, wmul, hmul)
        return

    fx0 = from_focus.x + from_focus.w * from_x0
    fy0 = from_focus.y + from_focus.h * from_y0
    fx1 = from_focus.x + from_focus.w * from_x1
    fy1 = from_focus.y + from_focus.h * from_y1

    placeless = None
    new_focus = None

    # a really big number.
    new_focus_dist = (65536.0 * renpy.config.focus_crossrange_penalty) ** 2

    for f in focus_list:

        if f is from_focus:
            continue

        if not f.widget.style.keyboard_focus:
            continue

        if f.x is None:
            placeless = f
            continue

        if not condition(from_focus, f):
            continue

        tx0 = f.x + f.w * to_x0
        ty0 = f.y + f.h * to_y0
        tx1 = f.x + f.w * to_x1
        ty1 = f.y + f.h * to_y1

        dist = line_dist(fx0, fy0, fx1, fy1,
                         tx0, ty0, tx1, ty1)

        if dist < new_focus_dist:
            new_focus = f
            new_focus_dist = dist

    # If we couldn't find anything, try the placeless focus.
    new_focus = new_focus or placeless

    # If we have something, switch to it.
    if new_focus:
        return change_focus(new_focus)

    # And, we're done.


def focus_ordered(delta):

    global pending_focus_type
    pending_focus_type = "keyboard"

    placeless = None

    candidates = [ ]
    index = 0

    current = get_focused()
    current_index = None

    for f in focus_list:

        if f.x is None:
            placeless = f
            continue

        if f.arg is not None:
            continue

        if not f.widget.style.keyboard_focus:
            continue

        if f.widget is current:
            current_index = index

        candidates.append(f)
        index += 1

    new_focus = None

    if current_index is None:
        if candidates:
            if delta > 0:
                new_focus = candidates[delta - 1]
            else:
                new_focus = candidates[delta]
    else:
        new_index = current_index + delta

        if 0 <= new_index < len(candidates):
            new_focus = candidates[new_index]

    new_focus = new_focus or placeless

    return change_focus(new_focus)


def key_handler(ev):

    map_event = renpy.display.behavior.map_event

    if renpy.game.preferences.self_voicing:
        if map_event(ev, 'focus_right') or map_event(ev, 'focus_down'):
            return focus_ordered(1)

        if map_event(ev, 'focus_left') or map_event(ev, 'focus_up'):
            return focus_ordered(-1)

    else:

        if map_event(ev, 'focus_right'):
            return focus_nearest(0.9, 0.1, 0.9, 0.9,
                                 0.1, 0.1, 0.1, 0.9,
                                 verti_line_dist,
                                 lambda old, new : old.x + old.w <= new.x,
                                 -1, 0, 0, 0)

        if map_event(ev, 'focus_left'):
            return focus_nearest(0.1, 0.1, 0.1, 0.9,
                                 0.9, 0.1, 0.9, 0.9,
                                 verti_line_dist,
                                 lambda old, new : new.x + new.w <= old.x,
                                 1, 0, 1, 0)

        if map_event(ev, 'focus_up'):
            return focus_nearest(0.1, 0.1, 0.9, 0.1,
                                 0.1, 0.9, 0.9, 0.9,
                                 horiz_line_dist,
                                 lambda old, new : new.y + new.h <= old.y,
                                 0, 1, 0, 1)

        if map_event(ev, 'focus_down'):
            return focus_nearest(0.1, 0.9, 0.9, 0.9,
                                 0.1, 0.1, 0.9, 0.1,
                                 horiz_line_dist,
                                 lambda old, new : old.y + old.h <= new.y,
                                 0, -1, 0, 0)
