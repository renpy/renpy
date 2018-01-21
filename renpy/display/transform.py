# Copyright 2004-2018 Tom Rothamel <pytom@bishoujo.us>
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

from __future__ import print_function

# This file contains displayables that move, zoom, rotate, or otherwise
# transform displayables. (As well as displayables that support them.)
import math
import types  # @UnresolvedImport

import renpy.display  # @UnusedImport
from renpy.display.layout import Container

import renpy.display.accelerator

# The null object that's used if we don't have a defined child.
null = None


def get_null():
    global null

    if null is None:
        null = renpy.display.layout.Null()

    return null

# Convert a position from cartesian to polar coordinates.


def cartesian_to_polar(x, y, xaround, yaround):
    """
    Converts cartesian coordinates to polar coordinates.
    """

    dx = x - xaround
    dy = y - yaround

    radius = math.hypot(dx, dy)
    angle = math.atan2(dx, -dy) / math.pi * 180

    if angle < 0:
        angle += 360

    return angle, radius


def polar_to_cartesian(angle, radius, xaround, yaround):
    """
    Converts polart coordinates to cartesian coordinates.
    """

    angle = angle * math.pi / 180

    dx = radius * math.sin(angle)
    dy = -radius * math.cos(angle)

    x = type(xaround)(xaround + dx)
    y = type(yaround)(yaround + dy)

    return x, y


def first_not_none(*args):
    """
    Returns the first argument that is not None.
    """

    for i in args:
        if i is not None:
            return i
    return i


class TransformState(renpy.object.Object):

    nearest = None
    xoffset = None
    yoffset = None
    inherited_xpos = None
    inherited_ypos = None
    inherited_xanchor = None
    inherited_yanchor = None
    transform_anchor = False
    additive = 0.0
    debug = None
    events = True
    crop_relative = False
    xpan = None
    ypan = None
    xtile = 1
    ytile = 1
    last_angle = None
    maxsize = None

    def __init__(self):
        self.alpha = 1
        self.nearest = None
        self.additive = 0.0
        self.rotate = None
        self.rotate_pad = True
        self.transform_anchor = False
        self.zoom = 1
        self.xzoom = 1
        self.yzoom = 1

        self.xpos = None
        self.ypos = None
        self.xanchor = None
        self.yanchor = None
        self.xoffset = 0
        self.yoffset = 0

        self.xaround = 0.0
        self.yaround = 0.0
        self.xanchoraround = 0.0
        self.yanchoraround = 0.0

        self.xpan = None
        self.ypan = None
        self.xtile = 1
        self.ytile = 1

        self.subpixel = False

        self.crop = None
        self.crop_relative = False
        self.corner1 = None
        self.corner2 = None
        self.size = None
        self.maxsize = None

        self.delay = 0

        self.debug = None
        self.events = True

        # Note: When adding a new property, we need to add it to:
        # - take_state
        # - diff
        # - renpy.atl.PROPERTIES
        # - Proxies in Transform

        # An xpos (etc) inherited from our child overrides an xpos inherited
        # from an old transform, but not an xpos set in the current transform.
        #
        # inherited_xpos stores the inherited_xpos, which is overridden by the
        # xpos, if not None.
        self.inherited_xpos = None
        self.inherited_ypos = None
        self.inherited_xanchor = None
        self.inherited_yanchor = None

    def take_state(self, ts):

        self.nearest = ts.nearest
        self.alpha = ts.alpha
        self.additive = ts.additive
        self.rotate = ts.rotate
        self.rotate_pad = ts.rotate_pad
        self.transform_anchor = ts.transform_anchor
        self.zoom = ts.zoom
        self.xzoom = ts.xzoom
        self.yzoom = ts.yzoom

        self.xaround = ts.xaround
        self.yaround = ts.yaround
        self.xanchoraround = ts.xanchoraround
        self.yanchoraround = ts.yanchoraround

        self.crop = ts.crop
        self.crop_relative = ts.crop_relative
        self.corner1 = ts.corner1
        self.corner2 = ts.corner2
        self.size = ts.size
        self.maxsize = ts.maxsize

        self.xpan = ts.xpan
        self.ypan = ts.ypan
        self.xtile = ts.xtile
        self.ytile = ts.ytile

        self.last_angle = ts.last_angle

        self.debug = ts.debug
        self.events = ts.events

        # Take the computed position properties, not the
        # raw ones.
        (self.inherited_xpos,
         self.inherited_ypos,
         self.inherited_xanchor,
         self.inherited_yanchor,
         _,
         _,
         _) = ts.get_placement()

        self.xoffset = ts.xoffset
        self.yoffset = ts.yoffset
        self.subpixel = ts.subpixel

    # Returns a dict, with p -> (old, new) where p is a property that
    # has changed between this object and the new object.
    def diff(self, newts):

        rv = { }

        def diff2(prop, new, old):
            if new != old:
                rv[prop] = (old, new)

        def diff4(prop, new, inherited_new, old, inherited_old):
            if new is None:
                new_value = inherited_new
            else:
                new_value = new

            if old is None:
                old_value = inherited_old
            else:
                old_value = old

            if new_value != old_value:
                rv[prop] = (old_value, new_value)

        diff2("nearest", newts.nearest, self.nearest)
        diff2("alpha", newts.alpha, self.alpha)
        diff2("additive", newts.additive, self.additive)
        diff2("rotate", newts.rotate, self.rotate)
        diff2("rotate_pad", newts.rotate_pad, self.rotate_pad)
        diff2("transform_anchor", newts.transform_anchor, self.transform_anchor)
        diff2("zoom", newts.zoom, self.zoom)
        diff2("xzoom", newts.xzoom, self.xzoom)
        diff2("yzoom", newts.yzoom, self.yzoom)

        diff2("xaround", newts.xaround, self.xaround)
        diff2("yaround", newts.yaround, self.yaround)
        diff2("xanchoraround", newts.xanchoraround, self.xanchoraround)
        diff2("yanchoraround", newts.yanchoraround, self.yanchoraround)

        diff2("subpixel", newts.subpixel, self.subpixel)

        diff2("crop", newts.crop, self.crop)
        diff2("crop_relative", newts.crop_relative, self.crop_relative)
        diff2("corner1", newts.corner1, self.corner1)
        diff2("corner2", newts.corner2, self.corner2)
        diff2("size", newts.size, self.size)
        diff2("maxsize", newts.maxsize, self.maxsize)

        diff4("xpos", newts.xpos, newts.inherited_xpos, self.xpos, self.inherited_xpos)
        diff4("xanchor", newts.xanchor, newts.inherited_xanchor, self.xanchor, self.inherited_xanchor)
        diff2("xoffset", newts.xoffset, self.xoffset)

        diff4("ypos", newts.ypos, newts.inherited_ypos, self.ypos, self.inherited_ypos)
        diff4("yanchor", newts.yanchor, newts.inherited_yanchor, self.yanchor, self.inherited_yanchor)
        diff2("yoffset", newts.yoffset, self.yoffset)

        diff2("xpan", newts.xpan, self.xpan)
        diff2("ypan", newts.ypan, self.ypan)

        diff2("xtile", newts.xtile, self.xtile)
        diff2("ytile", newts.ytile, self.ytile)

        diff2("debug", newts.debug, self.debug)
        diff2("events", newts.events, self.events)

        return rv

    def get_placement(self, cxoffset=0, cyoffset=0):

        return (
            first_not_none(self.xpos, self.inherited_xpos),
            first_not_none(self.ypos, self.inherited_ypos),
            first_not_none(self.xanchor, self.inherited_xanchor),
            first_not_none(self.yanchor, self.inherited_yanchor),
            self.xoffset + cxoffset,
            self.yoffset + cyoffset,
            self.subpixel,
            )

    # These update various properties.
    def get_xalign(self):
        return self.xpos

    def set_xalign(self, v):
        self.xpos = v
        self.xanchor = v

    xalign = property(get_xalign, set_xalign)

    def get_yalign(self):
        return self.ypos

    def set_yalign(self, v):
        self.ypos = v
        self.yanchor = v

    yalign = property(get_yalign, set_yalign)

    def get_around(self):
        return (self.xaround, self.yaround)

    def set_around(self, value):
        self.xaround, self.yaround = value
        self.xanchoraround, self.yanchoraround = None, None

    def set_alignaround(self, value):
        self.xaround, self.yaround = value
        self.xanchoraround, self.yanchoraround = value

    around = property(get_around, set_around)
    alignaround = property(get_around, set_alignaround)

    def get_angle(self):
        xpos = first_not_none(self.xpos, self.inherited_xpos, 0)
        ypos = first_not_none(self.ypos, self.inherited_ypos, 0)
        angle, _radius = cartesian_to_polar(xpos, ypos, self.xaround, self.yaround)
        return angle

    def get_radius(self):
        xpos = first_not_none(self.xpos, self.inherited_xpos, 0)
        ypos = first_not_none(self.ypos, self.inherited_ypos, 0)
        _angle, radius = cartesian_to_polar(xpos, ypos, self.xaround, self.yaround)
        return radius

    def set_angle(self, value):
        xpos = first_not_none(self.xpos, self.inherited_xpos, 0)
        ypos = first_not_none(self.ypos, self.inherited_ypos, 0)
        _angle, radius = cartesian_to_polar(xpos, ypos, self.xaround, self.yaround)
        angle = value
        self.xpos, self.ypos = polar_to_cartesian(angle, radius, self.xaround, self.yaround)

        if self.xanchoraround:
            self.xanchor, self.yanchor = polar_to_cartesian(angle, radius, self.xaround, self.yaround)

    def set_radius(self, value):
        xpos = first_not_none(self.xpos, self.inherited_xpos, 0)
        ypos = first_not_none(self.ypos, self.inherited_ypos, 0)
        angle, _radius = cartesian_to_polar(xpos, ypos, self.xaround, self.yaround)
        radius = value
        self.xpos, self.ypos = polar_to_cartesian(angle, radius, self.xaround, self.yaround)

        if self.xanchoraround:
            self.xanchor, self.yanchor = polar_to_cartesian(angle, radius, self.xaround, self.yaround)

    angle = property(get_angle, set_angle)
    radius = property(get_radius, set_radius)

    def get_pos(self):
        return self.xpos, self.ypos

    def set_pos(self, value):
        self.xpos, self.ypos = value

    pos = property(get_pos, set_pos)

    def get_anchor(self):
        return self.xanchor, self.yanchor

    def set_anchor(self, value):
        self.xanchor, self.yanchor = value

    anchor = property(get_anchor, set_anchor)

    def get_align(self):
        return self.xpos, self.ypos

    def set_align(self, value):
        self.xanchor, self.yanchor = value
        self.xpos, self.ypos = value

    align = property(get_align, set_align)

    def get_offset(self):
        return self.xoffset, self.yoffset

    def set_offset(self, value):
        self.xoffset, self.yoffset = value

    offset = property(get_offset, set_offset)

    def set_xcenter(self, value):
        self.xpos = value
        self.xanchor = 0.5

    def get_xcenter(self):
        return self.xpos

    def set_ycenter(self, value):
        self.ypos = value
        self.yanchor = 0.5

    def get_ycenter(self):
        return self.ypos

    xcenter = property(get_xcenter, set_xcenter)
    ycenter = property(get_ycenter, set_ycenter)


class Proxy(object):
    """
    This class proxies a field from the transform to its state.
    """

    def __init__(self, name):
        self.name = name

    def __get__(self, instance, owner):
        return getattr(instance.state, self.name)

    def __set__(self, instance, value):
        return setattr(instance.state, self.name, value)


class Transform(Container):
    """
    Documented in sphinx, because we can't scan this object.
    """

    __version__ = 5
    transform_event_responder = True

    # Proxying things over to our state.
    nearest = Proxy("nearest")
    alpha = Proxy("alpha")
    additive = Proxy("additive")
    rotate = Proxy("rotate")
    rotate_pad = Proxy("rotate_pad")
    transform_anchor = Proxy("transform_anchor")
    zoom = Proxy("zoom")
    xzoom = Proxy("xzoom")
    yzoom = Proxy("yzoom")

    xpos = Proxy("xpos")
    ypos = Proxy("ypos")
    xanchor = Proxy("xanchor")
    yanchor = Proxy("yanchor")

    xalign = Proxy("xalign")
    yalign = Proxy("yalign")

    around = Proxy("around")
    alignaround = Proxy("alignaround")
    angle = Proxy("angle")
    radius = Proxy("radius")

    xaround = Proxy("xaround")
    yaround = Proxy("yaround")
    xanchoraround = Proxy("xanchoraround")
    yanchoraround = Proxy("yanchoraround")

    pos = Proxy("pos")
    anchor = Proxy("anchor")
    align = Proxy("align")

    crop = Proxy("crop")
    crop_relative = Proxy("crop_relative")
    corner1 = Proxy("corner1")
    corner2 = Proxy("corner2")
    size = Proxy("size")
    maxsize = Proxy("maxsize")

    delay = Proxy("delay")

    xoffset = Proxy("xoffset")
    yoffset = Proxy("yoffset")
    offset = Proxy("offset")

    subpixel = Proxy("subpixel")

    xcenter = Proxy("xcenter")
    ycenter = Proxy("ycenter")

    xpan = Proxy("xpan")
    ypan = Proxy("ypan")
    xtile = Proxy("xtile")
    ytile = Proxy("ytile")

    debug = Proxy("debug")
    events = Proxy("events")

    def after_upgrade(self, version):

        if version < 1:
            self.active = False
            self.state = TransformState()

            self.state.xpos = self.xpos or 0
            self.state.ypos = self.ypos or 0
            self.state.xanchor = self.xanchor or 0
            self.state.yanchor = self.yanchor or 0
            self.state.alpha = self.alpha
            self.state.rotate = self.rotate
            self.state.zoom = self.zoom
            self.state.xzoom = self.xzoom
            self.state.yzoom = self.yzoom

            self.hide_request = False
            self.hide_response = True

        if version < 2:
            self.st = 0
            self.at = 0

        if version < 3:
            self.st_offset = 0
            self.at_offset = 0
            self.child_st_base = 0

        if version < 4:
            self.style_arg = 'transform'

        if version < 5:
            self.replaced_request = False
            self.replaced_response = True

    DEFAULT_ARGUMENTS = {
        "selected_activate" : { },
        "selected_hover" : { },
        "selected_idle" : { },
        "selected_insensitive" : { },
        "activate" : { },
        "hover" : { },
        "idle" : { },
        "insensitive" : { },
        "" : { },
        }

    # Compatibility with old versions of the class.
    active = False
    children = False
    arguments = DEFAULT_ARGUMENTS

    # Default before we set this.
    child_size = (0, 0)

    def __init__(self,
                 child=None,
                 function=None,
                 style="default",
                 focus=None,
                 default=False,
                 _args=None,

                 **kwargs):

        self.kwargs = kwargs
        self.style_arg = style

        super(Transform, self).__init__(style=style, focus=focus, default=default, _args=_args)

        self.function = function

        child = renpy.easy.displayable_or_none(child)
        if child is not None:
            self.add(child)

        self.state = TransformState()

        if kwargs:

            # A map from prefix -> (prop -> value)
            self.arguments = { }

            # Fill self.arguments with a
            for k, v in kwargs.iteritems():

                prefix = ""
                prop = k

                while True:

                    if prop in renpy.atl.PROPERTIES and (not prefix or prefix in Transform.DEFAULT_ARGUMENTS):

                        if prefix not in self.arguments:
                            self.arguments[prefix] = { }

                        self.arguments[prefix][prop] = v
                        break

                    new_prefix, _, prop = prop.partition("_")

                    if not prop:
                        raise Exception("Unknown transform property: %r" % k)

                    if prefix:
                        prefix = prefix + "_" + new_prefix
                    else:
                        prefix = new_prefix

            if "" in self.arguments:
                for k, v in self.arguments[""].iteritems():
                    setattr(self.state, k, v)

        else:
            self.arguments = None

        # This is the matrix transforming our coordinates into child coordinates.
        self.forward = None

        # Have we called the function at least once?
        self.active = False

        # Have we been requested to hide?
        self.hide_request = False

        # True if it's okay for us to hide.
        self.hide_response = True

        # Have we been requested to replaced?
        self.replaced_request = False

        # True if it's okay for us to replaced.
        self.replaced_response = True

        self.st = 0
        self.at = 0
        self.st_offset = 0
        self.at_offset = 0

        self.child_st_base = 0

    def visit(self):
        if self.child is None:
            return [ ]
        else:
            return [ self.child ]

    # The default function chooses entries from self.arguments that match
    # the style prefix, and applies them to the state.
    def default_function(self, state, st, at):

        if self.arguments is None:
            return None

        prefix = self.style.prefix.strip("_")
        prefixes = [ ]

        while prefix:
            prefixes.insert(0, prefix)
            _, _, prefix = prefix.partition("_")

        prefixes.insert(0, "")

        for i in prefixes:
            d = self.arguments.get(i, None)

            if d is None:
                continue

            for k, v in d.iteritems():
                setattr(state, k, v)

        return None

    def set_transform_event(self, event):
        if self.child is not None:
            self.child.set_transform_event(event)
            self.last_child_transform_event = event

        super(Transform, self).set_transform_event(event)

    def take_state(self, t):
        """
        Takes the transformation state from object t into this object.
        """

        if self is t:
            return

        if not isinstance(t, Transform):
            return

        self.state.take_state(t.state)

        if (self.child is None) and (t.child is not None):
            self.add(t.child)
            self.child_st_base = t.child_st_base

        # The arguments will be applied when the default function is
        # called.

    def take_execution_state(self, t):
        """
        Takes the execution state from object t into this object. This is
        overridden by renpy.atl.TransformBase.
        """

        if self is t:
            return

        if not isinstance(t, Transform):
            return

        self.hide_request = t.hide_request
        self.replaced_request = t.replaced_request

        self.state.xpos = t.state.xpos
        self.state.ypos = t.state.ypos
        self.state.xanchor = t.state.xanchor
        self.state.yanchor = t.state.yanchor

        self.child_st_base = t.child_st_base

        if isinstance(self.child, Transform) and isinstance(t.child, Transform):
            self.child.take_execution_state(t.child)

    def copy(self):
        """
        Makes a copy of this transform.
        """

        d = self()
        d.kwargs = { }
        d.take_state(self)
        d.take_execution_state(self)
        d.st = self.st
        d.at = self.at

        return d

    def _change_transform_child(self, child):
        rv = self.copy()

        if self.child is not None:
            rv.set_child(self.child._change_transform_child(child))

        return rv

    def _handles_event(self, event):
        if self.function is not None:
            return True

        if self.child and self.child._handles_event(event):
            return True

        return False

    def _hide(self, st, at, kind):

        if not self.child:
            return None

        # Prevent time from ticking backwards, as can happen if we replace a
        # transform but keep its state.
        if st + self.st_offset <= self.st:
            self.st_offset = self.st - st
        if at + self.at_offset <= self.at:
            self.at_offset = self.at - at

        self.st = st = st + self.st_offset
        self.at = at = at + self.at_offset

        if not (self.hide_request or self.replaced_request):
            d = self.copy()
        else:
            d = self

        d.st_offset = self.st_offset
        d.at_offset = self.at_offset

        if not (self.hide_request or self.replaced_request):
            d.atl_st_offset = None

        if kind == "hide":
            d.hide_request = True
        else:
            d.replaced_request = True

        d.hide_response = True
        d.replaced_response = True

        if d.function is not None:
            d.function(d, st + d.st_offset, at + d.at_offset)
        elif isinstance(d, ATLTransform):
            d.execute(d, st + d.st_offset, at + d.at_offset)

        new_child = d.child._hide(st, at, kind)

        if new_child is not None:
            d.child = new_child
            d.hide_response = False
            d.replaced_response = False

        if (not d.hide_response) or (not d.replaced_response):
            renpy.display.render.redraw(d, 0)
            return d

        return None

    def set_child(self, child, duplicate=True):

        child = renpy.easy.displayable(child)

        if duplicate and child._duplicatable:
            child = child._duplicate(self._args)
            child._unique()

        if child._duplicatable:
            self._duplicatable = True

        self.child = child
        self.children = [ child ]
        self.child_st_base = self.st

        child.per_interact()

        renpy.display.render.invalidate(self)

    def update_state(self):
        """
        This updates the state to that at self.st, self.at.
        """

        # NOTE: This function is duplicated (more or less) in ATLTransform.

        self.hide_response = True
        self.replaced_response = True

        # If we have to, call the function that updates this transform.
        if self.arguments is not None:
            self.default_function(self, self.st, self.at)

        if self.function is not None:
            fr = self.function(self, self.st, self.at)

            # Order a redraw, if necessary.
            if fr is not None:
                renpy.display.render.redraw(self, fr)

        self.active = True

    # The render method is now defined in accelerator.pyx.

    def event(self, ev, x, y, st):

        if self.hide_request:
            return None

        if not self.state.events:
            return

        children = self.children
        offsets = self.offsets

        if not offsets:
            return None

        for i in xrange(len(self.children)-1, -1, -1):

            d = children[i]
            xo, yo = offsets[i]

            cx = x - xo
            cy = y - yo

            # Transform screen coordinates to child coordinates.
            cx, cy = self.forward.transform(cx, cy)

            rv = d.event(ev, cx, cy, st)
            if rv is not None:
                return rv

        return None

    def __call__(self, child=None, take_state=True, _args=None):

        if child is None:
            child = self.child

        if (child is not None) and (child._duplicatable):
            child = child._duplicate(_args)

        rv = Transform(
            child=child,
            function=self.function,
            style=self.style_arg,
            _args=_args,
            **self.kwargs)

        rv.take_state(self)

        return rv

    def _unique(self):
        if self.child and self.child._duplicatable:
            self._duplicatable = True
        else:
            self._duplicatable = False

    def get_placement(self):

        if not self.active:
            self.update_state()

        if self.child is not None:
            cxpos, cypos, cxanchor, cyanchor, cxoffset, cyoffset, csubpixel = self.child.get_placement()

            # Use non-None elements of the child placement as defaults.
            state = self.state

            if renpy.config.transform_uses_child_position:

                if cxpos is not None:
                    state.inherited_xpos = cxpos
                if cxanchor is not None:
                    state.inherited_xanchor = cxanchor
                if cypos is not None:
                    state.inherited_ypos = cypos
                if cyanchor is not None:
                    state.inherited_yanchor = cyanchor

                state.subpixel |= csubpixel

        else:
            cxoffset = 0
            cyoffset = 0

        cxoffset = cxoffset or 0
        cyoffset = cyoffset or 0

        rv = self.state.get_placement(cxoffset, cyoffset)

        if self.state.transform_anchor:

            xpos, ypos, xanchor, yanchor, xoffset, yoffset, subpixel = rv
            if (xanchor is not None) and (yanchor is not None):

                cw, ch = self.child_size
                rw, rh = self.render_size

                if xanchor.__class__ is float:
                    xanchor *= cw
                if yanchor.__class__ is float:
                    yanchor *= ch

                xanchor -= cw / 2.0
                yanchor -= ch / 2.0

                xanchor, yanchor = self.reverse.transform(xanchor, yanchor)

                xanchor += rw / 2.0
                yanchor += rh / 2.0

                xanchor = renpy.display.core.absolute(xanchor)
                yanchor = renpy.display.core.absolute(yanchor)

                rv = (xpos, ypos, xanchor, yanchor, xoffset, yoffset, subpixel)

        return rv

    def update(self):
        """
        This should be called when a transform property field is updated outside
        of the callback method, to ensure that the change takes effect.
        """

        renpy.display.render.invalidate(self)

    _duplicatable = True

    def _duplicate(self, args):

        if not self._duplicatable:
            return self

        rv = self(_args=args)
        rv.take_execution_state(self)
        rv._unique()

        return rv

    def _in_current_store(self):

        if self.child is None:
            return self

        child = self.child._in_current_store()
        if child is self.child:
            return self
        rv = self()
        rv.take_execution_state(self)
        rv.child = child
        rv._unique()

        return rv

    def _show(self):
        self.update_state()


Transform.render = types.MethodType(renpy.display.accelerator.transform_render, None, Transform)


class ATLTransform(renpy.atl.ATLTransformBase, Transform):

    def __init__(self, atl, child=None, context={}, parameters=None, **properties):
        renpy.atl.ATLTransformBase.__init__(self, atl, context, parameters)
        Transform.__init__(self, child=child, **properties)

        self.raw_child = self.child

    def update_state(self):
        """
        This updates the state to that at self.st, self.at.
        """

        self.hide_response = True
        self.replaced_response = True

        fr = self.execute(self, self.st, self.at)

        # Order a redraw, if necessary.
        if fr is not None:
            renpy.display.render.redraw(self, fr)

        self.active = True

    def __repr__(self):
        return "<ATL Transform {:x} {!r}>".format(id(self), self.atl.loc)

    def _show(self):
        super(ATLTransform, self)._show()
        self.execute(self, self.st, self.at)
