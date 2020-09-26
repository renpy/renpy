# Copyright 2004-2020 Tom Rothamel <pytom@bishoujo.us>
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

# NOTE:
# Transitions need to be able to work even when old_widget and new_widget
# are None, at least to the point of making it through __init__. This is
# so that prediction of images works.

from __future__ import division, absolute_import, with_statement, print_function, unicode_literals
from renpy.compat import *

import renpy.display

# Utility function used by MoveTransition et al.


def position(d):

    xpos, ypos, xanchor, yanchor, _xoffset, _yoffset, _subpixel = d.get_placement()

    if xpos is None:
        xpos = 0
    if ypos is None:
        ypos = 0
    if xanchor is None:
        xanchor = 0
    if yanchor is None:
        yanchor = 0

    return xpos, ypos, xanchor, yanchor


def offsets(d):

    _xpos, _ypos, _xanchor, _yanchor, xoffset, yoffset, _subpixel = d.get_placement()

    if renpy.config.movetransition_respects_offsets:
        return { 'xoffset' : xoffset, 'yoffset' : yoffset }
    else:
        return { }


# These are used by MoveTransition.
def MoveFactory(pos1, pos2, delay, d, **kwargs):
    if pos1 == pos2:
        return d

    return renpy.display.motion.Move(pos1, pos2, delay, d, **kwargs)


def default_enter_factory(pos, delay, d, **kwargs):
    return d


def default_leave_factory(pos, delay, d, **kwargs):
    return None

# These can be used to move things in and out of the screen.


def MoveIn(pos, pos1, delay, d, **kwargs):

    def aorb(a, b):
        if a is None:
            return b
        return a

    pos = tuple([aorb(a, b) for a, b in zip(pos, pos1)])
    return renpy.display.motion.Move(pos, pos1, delay, d, **kwargs)


def MoveOut(pos, pos1, delay, d, **kwargs):

    def aorb(a, b):
        if a is None:
            return b
        return a

    pos = tuple([aorb(a, b) for a, b in zip(pos, pos1)])
    return renpy.display.motion.Move(pos1, pos, delay, d, **kwargs)


def ZoomInOut(start, end, pos, delay, d, **kwargs):

    xpos, ypos, xanchor, yanchor = pos

    FactorZoom = renpy.display.motion.FactorZoom

    if end == 1.0:
        return FactorZoom(start, end, delay, d, after_child=d, opaque=False,
                          xpos=xpos, ypos=ypos, xanchor=xanchor, yanchor=yanchor, **kwargs)
    else:
        return FactorZoom(start, end, delay, d, opaque=False,
                          xpos=xpos, ypos=ypos, xanchor=xanchor, yanchor=yanchor, **kwargs)


def RevolveInOut(start, end, pos, delay, d, **kwargs):
    return renpy.display.motion.Revolve(start, end, delay, d, pos=pos, **kwargs)


def OldMoveTransition(delay, old_widget=None, new_widget=None, factory=None, enter_factory=None, leave_factory=None, old=False, layers=[ 'master' ]):
    """
    Returns a transition that attempts to find images that have changed
    position, and moves them from the old position to the new transition, taking
    delay seconds to complete the move.

    If `factory` is given, it is expected to be a function that takes as
    arguments: an old position, a new position, the delay, and a
    displayable, and to return a displayable as an argument. If not
    given, the default behavior is to move the displayable from the
    starting to the ending positions. Positions are always given as
    (xpos, ypos, xanchor, yanchor) tuples.

    If `enter_factory` or `leave_factory` are given, they are expected
    to be functions that take as arguments a position, a delay, and a
    displayable, and return a displayable. They are applied to
    displayables that are entering or leaving the scene,
    respectively. The default is to show in place displayables that
    are entering, and not to show those that are leaving.

    If `old` is True, then factory moves the old displayable with the
    given tag. Otherwise, it moves the new displayable with that
    tag.

    `layers` is a list of layers that the transition will be applied
    to.

    Images are considered to be the same if they have the same tag, in
    the same way that the tag is used to determine which image to
    replace or to hide. They are also considered to be the same if
    they have no tag, but use the same displayable.

    Computing the order in which images are displayed is a three-step
    process. The first step is to create a list of images that
    preserves the relative ordering of entering and moving images. The
    second step is to insert the leaving images such that each leaving
    image is at the lowest position that is still above all images
    that were below it in the original scene. Finally, the list
    is sorted by zorder, to ensure no zorder violations occur.

    If you use this transition to slide an image off the side of the
    screen, remember to hide it when you are done. (Or just use
    a leave_factory.)
    """

    if factory is None:
        factory = MoveFactory

    if enter_factory is None:
        enter_factory = default_enter_factory

    if leave_factory is None:
        leave_factory = default_leave_factory

    use_old = old

    def merge_slide(old, new):

        # If new does not have .layers or .scene_list, then we simply
        # insert a move from the old position to the new position, if
        # a move occured.

        if (not isinstance(new, renpy.display.layout.MultiBox)
                or (new.layers is None and new.layer_name is None)):

            if use_old:
                child = old
            else:
                child = new

            old_pos = position(old)
            new_pos = position(new)

            if old_pos != new_pos:
                return factory(old_pos,
                               new_pos,
                               delay,
                               child,
                               **offsets(child)
                               )

            else:
                return child

        # If we're in the layers_root widget, merge the child widgets
        # for each layer.
        if new.layers:

            rv = renpy.display.layout.MultiBox(layout='fixed')
            rv.layers = { }

            for layer in renpy.config.layers:

                f = new.layers[layer]

                if (isinstance(f, renpy.display.layout.MultiBox)
                    and layer in layers
                        and f.scene_list is not None):

                    f = merge_slide(old.layers[layer], new.layers[layer])

                rv.layers[layer] = f
                rv.add(f)

            return rv

        # Otherwise, we recompute the scene list for the two widgets, merging
        # as appropriate.

        # Wraps the displayable found in SLE so that the various timebases
        # are maintained.
        def wrap(sle):
            return renpy.display.layout.AdjustTimes(sle.displayable, sle.show_time, sle.animation_time)

        def tag(sle):
            return sle.tag or sle.displayable

        def merge(sle, d):
            rv = sle.copy()
            rv.show_time = 0
            rv.displayable = d
            return rv

        def entering(sle):
            new_d = wrap(new_sle)
            move = enter_factory(position(new_d), delay, new_d, **offsets(new_d))

            if move is None:
                return

            rv_sl.append(merge(new_sle, move))

        def leaving(sle):
            old_d = wrap(sle)
            move = leave_factory(position(old_d), delay, old_d, **offsets(old_d))

            if move is None:
                return

            move = renpy.display.layout.IgnoresEvents(move)
            rv_sl.append(merge(old_sle, move))

        def moving(old_sle, new_sle):
            old_d = wrap(old_sle)
            new_d = wrap(new_sle)

            if use_old:
                child = old_d
            else:
                child = new_d

            move = factory(position(old_d), position(new_d), delay, child, **offsets(child))
            if move is None:
                return

            rv_sl.append(merge(new_sle, move))

        # The old, new, and merged scene_lists.
        old_sl = old.scene_list[:]
        new_sl = new.scene_list[:]
        rv_sl = [ ]

        # A list of tags in old_sl, new_sl, and rv_sl.
        old_map = dict((tag(i), i) for i in old_sl if i is not None)
        new_tags = set(tag(i) for i in new_sl if i is not None)
        rv_tags = set()

        while old_sl or new_sl:

            # If we have something in old_sl, then
            if old_sl:

                old_sle = old_sl[0]
                old_tag = tag(old_sle)

                # If the old thing has already moved, then remove it.
                if old_tag in rv_tags:
                    old_sl.pop(0)
                    continue

                # If the old thing does not match anything in new_tags,
                # have it enter.
                if old_tag not in new_tags:
                    leaving(old_sle)
                    rv_tags.add(old_tag)
                    old_sl.pop(0)
                    continue

            # Otherwise, we must have something in new_sl. We want to
            # either move it or have it enter.

            new_sle = new_sl.pop(0)
            new_tag = tag(new_sle)

            # If it exists in both, move.
            if new_tag in old_map:
                old_sle = old_map[new_tag]

                moving(old_sle, new_sle)
                rv_tags.add(new_tag)
                continue

            else:
                entering(new_sle)
                rv_tags.add(new_tag)
                continue

        # Sort everything by zorder, to ensure that there are no zorder
        # violations in the result.
        rv_sl.sort(key=lambda a : a.zorder)

        layer = new.layer_name
        rv = renpy.display.layout.MultiBox(layout='fixed', focus=layer, **renpy.game.interface.layer_properties[layer])
        rv.append_scene_list(rv_sl)
        rv.layer_name = layer

        return rv

    # This calls merge_slide to actually do the merging.

    rv = merge_slide(old_widget, new_widget)
    rv.delay = delay  # W0201

    return rv

##############################################################################
# New Move Transition (since 6.14)


class MoveInterpolate(renpy.display.core.Displayable):
    """
    This displayable has two children. It interpolates between the positions
    of its two children to place them on the screen.
    """

    def __init__(self, delay, old, new, use_old, time_warp):
        super(MoveInterpolate, self).__init__()

        # The old and new displayables.
        self.old = old
        self.new = new

        # Should we display the old displayable?
        self.use_old = use_old

        # Time warp function or None.
        self.time_warp = time_warp

        # The width of the screen.
        self.screen_width = 0
        self.screen_height = 0

        # The width of the selected child.
        self.child_width = 0
        self.child_height = 0

        # The delay and st.
        self.delay = delay
        self.st = 0

    def render(self, width, height, st, at):
        self.screen_width = width
        self.screen_height = height

        old_r = renpy.display.render.render(self.old, width, height, st, at)
        new_r = renpy.display.render.render(self.new, width, height, st, at)

        if self.use_old:
            cr = old_r
        else:
            cr = new_r

        self.child_width, self.child_height = cr.get_size()
        self.st = st

        if self.st < self.delay:
            renpy.display.render.redraw(self, 0)

        return cr

    def child_placement(self, child):

        def based(v, base):
            if v is None:
                return 0
            elif isinstance(v, int):
                return v
            elif isinstance(v, renpy.display.core.absolute):
                return v
            else:
                return v * base

        xpos, ypos, xanchor, yanchor, xoffset, yoffset, subpixel = child.get_placement()

        xpos = based(xpos, self.screen_width)
        ypos = based(ypos, self.screen_height)
        xanchor = based(xanchor, self.child_width)
        yanchor = based(yanchor, self.child_height)

        return xpos, ypos, xanchor, yanchor, xoffset, yoffset, subpixel

    def get_placement(self):

        if self.st > self.delay:
            done = 1.0
        else:
            done = self.st / self.delay

        if self.time_warp is not None:
            done = self.time_warp(done)

        absolute = renpy.display.core.absolute

        def I(a, b):
            return absolute(a + done * (b - a))

        old_xpos, old_ypos, old_xanchor, old_yanchor, old_xoffset, old_yoffset, old_subpixel = self.child_placement(self.old)
        new_xpos, new_ypos, new_xanchor, new_yanchor, new_xoffset, new_yoffset, new_subpixel = self.child_placement(self.new)

        xpos = I(old_xpos, new_xpos)
        ypos = I(old_ypos, new_ypos)
        xanchor = I(old_xanchor, new_xanchor)
        yanchor = I(old_yanchor, new_yanchor)
        xoffset = I(old_xoffset, new_xoffset)
        yoffset = I(old_yoffset, new_yoffset)
        subpixel = old_subpixel or new_subpixel

        return xpos, ypos, xanchor, yanchor, xoffset, yoffset, subpixel


def MoveTransition(delay, old_widget=None, new_widget=None, enter=None, leave=None, old=False, layers=[ 'master' ], time_warp=None, enter_time_warp=None, leave_time_warp=None):
    """
    :doc: transition function
    :args: (delay, enter=None, leave=None, old=False, layers=['master'], time_warp=None, enter_time_warp=None, leave_time_warp=None)
    :name: MoveTransition

    Returns a transition that interpolates the position of images (with the
    same tag) in the old and new scenes.

    `delay`
        The time it takes for the interpolation to finish.

    `enter`
        If not None, images entering the scene will also be moved. The value
        of `enter` should be a transform that is applied to the image to
        get its starting position.

    `leave`
        If not None, images leaving the scene will also be move. The value
        of `leave` should be a transform that is applied to the image to
        get its ending position.

    `old`
        If true, the old image will be used in preference to the new one.

    `layers`
        A list of layers that moves are applied to.

    `time_warp`
        A time warp function that's applied to the interpolation. This
        takes a number between 0.0 and 1.0, and should return a number in
        the same range.

    `enter_time_warp`
        A time warp function that's applied to images entering the scene.

    `leave_time_warp`
        A time warp function that's applied to images leaving the scene.

    """

    use_old = old

    def merge_slide(old, new, merge_slide):

        # This function takes itself as an argument to prevent a reference
        # loop that occurs when it refers to itself in the it's parent's
        # scope.

        # If new does not have .layers or .scene_list, then we simply
        # insert a move from the old position to the new position, if
        # a move occured.

        if (not isinstance(new, renpy.display.layout.MultiBox)
                or (new.layers is None and new.layer_name is None)):

            if old is new:
                return new
            else:
                return MoveInterpolate(delay, old, new, use_old, time_warp)

        # If we're in the layers_root widget, merge the child widgets
        # for each layer.
        if new.layers:

            rv = renpy.display.layout.MultiBox(layout='fixed')
            rv.layers = { }

            for layer in renpy.config.layers:

                f = new.layers[layer]

                if (isinstance(f, renpy.display.layout.MultiBox)
                    and layer in layers
                        and f.scene_list is not None):

                    f = merge_slide(old.layers[layer], new.layers[layer], merge_slide)

                rv.layers[layer] = f
                rv.add(f)

            return rv

        # Otherwise, we recompute the scene list for the two widgets, merging
        # as appropriate.

        # Wraps the displayable found in SLE so that the various timebases
        # are maintained.
        def wrap(sle):
            return renpy.display.layout.AdjustTimes(sle.displayable, sle.show_time, sle.animation_time)

        def tag(sle):
            return sle.tag or sle.displayable

        def merge(sle, d):
            rv = sle.copy()
            rv.show_time = 0
            rv.displayable = d
            return rv

        def entering(sle):

            if not enter:
                return

            new_d = wrap(new_sle)
            move = MoveInterpolate(delay, enter(new_d), new_d, False, enter_time_warp)
            rv_sl.append(merge(new_sle, move))

        def leaving(sle):

            if not leave:
                return

            old_d = wrap(sle)
            move = MoveInterpolate(delay, old_d, leave(old_d), True, leave_time_warp)
            move = renpy.display.layout.IgnoresEvents(move)
            rv_sl.append(merge(old_sle, move))

        def moving(old_sle, new_sle):

            if old_sle.displayable is new_sle.displayable:
                rv_sl.append(new_sle)
                return

            old_d = wrap(old_sle)
            new_d = wrap(new_sle)

            move = MoveInterpolate(delay, old_d, new_d, use_old, time_warp)

            rv_sl.append(merge(new_sle, move))

        # The old, new, and merged scene_lists.
        old_sl = old.scene_list[:]
        new_sl = new.scene_list[:]
        rv_sl = [ ]

        # A list of tags in old_sl, new_sl, and rv_sl.
        old_map = dict((tag(i), i) for i in old_sl if i is not None)
        new_tags = set(tag(i) for i in new_sl if i is not None)
        rv_tags = set()

        while old_sl or new_sl:

            # If we have something in old_sl, then
            if old_sl:

                old_sle = old_sl[0]
                old_tag = tag(old_sle)

                # If the old thing has already moved, then remove it.
                if old_tag in rv_tags:
                    old_sl.pop(0)
                    continue

                # If the old thing does not match anything in new_tags,
                # have it enter.
                if old_tag not in new_tags:
                    leaving(old_sle)
                    rv_tags.add(old_tag)
                    old_sl.pop(0)
                    continue

            # Otherwise, we must have something in new_sl. We want to
            # either move it or have it enter.

            new_sle = new_sl.pop(0)
            new_tag = tag(new_sle)

            # If it exists in both, move.
            if new_tag in old_map:
                old_sle = old_map[new_tag]

                moving(old_sle, new_sle)
                rv_tags.add(new_tag)
                continue

            else:
                entering(new_sle)
                rv_tags.add(new_tag)
                continue

        # Sort everything by zorder, to ensure that there are no zorder
        # violations in the result.
        rv_sl.sort(key=lambda a : a.zorder)

        layer = new.layer_name
        rv = renpy.display.layout.MultiBox(layout='fixed', focus=layer, **renpy.game.interface.layer_properties[layer])
        rv.append_scene_list(rv_sl)

        return rv

    # Call merge_slide to actually do the merging.
    rv = merge_slide(old_widget, new_widget, merge_slide)
    rv.delay = delay

    return rv
