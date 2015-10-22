# Copyright 2004-2015 Tom Rothamel <pytom@bishoujo.us>
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

# This file contains displayables that move, zoom, rotate, or otherwise
# transform displayables. (As well as displayables that support them.)
import math
import types #@UnresolvedImport

import renpy.display #@UnusedImport
from renpy.display.render import render
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

        self.subpixel = False

        self.crop = None
        self.crop_relative = False
        self.corner1 = None
        self.corner2 = None
        self.size = None

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

        diff4("xpos", newts.xpos, newts.inherited_xpos, self.xpos, self.inherited_xpos)

        diff4("xanchor", newts.xanchor, newts.inherited_xanchor, self.xanchor, self.inherited_xanchor)
        diff2("xoffset", newts.xoffset, self.xoffset)

        diff4("ypos", newts.ypos, newts.inherited_ypos, self.ypos, self.inherited_ypos)
        diff4("yanchor", newts.yanchor, newts.inherited_yanchor, self.yanchor, self.inherited_yanchor)
        diff2("yoffset", newts.yoffset, self.yoffset)

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

    delay = Proxy("delay")

    xoffset = Proxy("xoffset")
    yoffset = Proxy("yoffset")
    offset = Proxy("offset")

    subpixel = Proxy("subpixel")

    xcenter = Proxy("xcenter")
    ycenter = Proxy("ycenter")

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

                 style='transform',
                 focus=None,
                 default=False,

                 **kwargs):

        self.kwargs = kwargs
        self.style_arg = style

        super(Transform, self).__init__(style=style, focus=focus, default=default)

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

        if kind == "hide":
            d.hide_request = True
        else:
            d.replaced_request = True

        d.hide_response = True
        d.replaced_response = True

        if d.function is not None:
            d.function(d, st + d.st_offset, at + d.at_offset)

        new_child = d.child._hide(st, at, kind)

        if new_child is not None:
            d.child = new_child
            d.hide_response = False
            d.replaced_response = False

        if (not d.hide_response) or (not d.replaced_response):
            renpy.display.render.redraw(d, 0)
            return d

        return None

    def set_child(self, child):

        child = renpy.easy.displayable(child)

        self.child = child
        self.children = [ child ]
        self.child_st_base = self.st

        child.per_interact()

        renpy.display.render.invalidate(self)

    def update_state(self):
        """
        This updates the state to that at self.st, self.at.
        """

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

        state = self.state

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

    def __call__(self, child=None, take_state=True):

        if child is None:
            child = self.child

        # If we don't have a child for some reason, set it to null.
        if child is None:
            child = get_null()
        else:
            child = child.parameterize('displayable', [ ])

        rv = Transform(
            child=child,
            function=self.function,
            style=self.style_arg,
            **self.kwargs)

        rv.take_state(self)

        return rv

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

    def parameterize(self, name, parameters):
        if parameters:
            raise Exception("Image '%s' can't take parameters '%s'. (Perhaps you got the name wrong?)" %
                            (' '.join(name), ' '.join(parameters)))

        # Note the call here.
        return self()

    def _show(self):
        self.update_state()

Transform.render = types.MethodType(renpy.display.accelerator.transform_render, None, Transform)

class ATLTransform(renpy.atl.ATLTransformBase, Transform):

    def __init__(self, atl, child=None, context={}, parameters=None, **properties):
        renpy.atl.ATLTransformBase.__init__(self, atl, context, parameters)
        Transform.__init__(self, child=child, function=self.execute, **properties)

        self.raw_child = self.child

    def __repr__(self):
        return "<ATL Transform {:x} {!r}>".format(id(self), self.atl.loc)

    def _show(self):
        super(ATLTransform, self)._show()
        self.execute(self, self.st, self.at)


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

    def __init__(self, function, period, child=None, new_widget=None, old_widget=None, repeat=False, bounce=False, delay=None, anim_timebase=False, tag_start=None, time_warp=None, add_sizes=False, style='motion', **properties):
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

        @param delay: How long this motion should take. If repeat is None, defaults to period.

        @param anim_timebase: If True, use the animation timebase rather than the shown timebase.

        @param time_warp: If not None, this is a function that takes a
        fraction of the period (between 0.0 and 1.0), and returns a
        new fraction of the period. Use this to warp time, applying
        acceleration and deceleration to motions.

        This can also be used as a transition. When used as a
        transition, the motion is applied to the new_widget for delay
        seconds.
        """

        if child is None:
            child = new_widget

        if delay is None and not repeat:
            delay = period

        super(Motion, self).__init__(style=style, **properties)

        if child is not None:
            self.add(child)

        self.function = function
        self.period = period
        self.repeat = repeat
        self.bounce = bounce
        self.delay = delay
        self.anim_timebase = anim_timebase
        self.time_warp = time_warp
        self.add_sizes = add_sizes

        self.position = None


    def update_position(self, t, sizes):

        if renpy.game.less_updates:
            if self.delay:
                t = self.delay
                if self.repeat:
                    t = t % self.period
            else:
                t = self.period
        elif self.delay and t >= self.delay:
            t = self.delay
            if self.repeat:
                t = t % self.period
        elif self.repeat:
            t = t % self.period
            renpy.display.render.redraw(self, 0)
        else:
            if t > self.period:
                t = self.period
            else:
                renpy.display.render.redraw(self, 0)

        if self.period > 0:
            t /= self.period
        else:
            t = 1

        if self.time_warp:
            t = self.time_warp(t)

        if self.bounce:
            t = t * 2
            if t > 1.0:
                t = 2.0 - t

        if self.add_sizes:
            res = self.function(t, sizes)
        else:
            res = self.function(t)

        res = tuple(res)

        if len(res) == 2:
            self.position = res + (self.style.xanchor, self.style.yanchor)
        else:
            self.position = res

    def get_placement(self):

        if self.position is None:
            if self.add_sizes:
                # Almost certainly gives the wrong placement, but there's nothing
                # we can do.
                return super(Motion, self).get_placement()
            else:
                self.update_position(0.0, None)

        return self.position + (self.style.xoffset, self.style.yoffset, self.style.subpixel)

    def render(self, width, height, st, at):

        if self.anim_timebase:
            t = at
        else:
            t = st

        child = render(self.child, width, height, st, at)
        cw, ch = child.get_size()

        self.update_position(t, (width, height, cw, ch))

        rv = renpy.display.render.Render(cw, ch)
        rv.blit(child, (0, 0))

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

    def __call__(self, t, sizes=(None, None, None, None)):

        types = (renpy.atl.position,) * len(self.start)
        return renpy.atl.interpolate(t, tuple(self.start), tuple(self.end), types)


def Pan(startpos, endpos, time, child=None, repeat=False, bounce=False,
        anim_timebase=False, style='motion', time_warp=None, **properties):
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

    @param anim_timebase: True if we use the animation timebase, False to use the
    displayable timebase.

    @param time_warp: If not None, this is a function that takes a
    fraction of the period (between 0.0 and 1.0), and returns a
    new fraction of the period. Use this to warp time, applying
    acceleration and deceleration to motions.

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
                  anim_timebase=anim_timebase,
                  time_warp=time_warp,
                  **properties)

def Move(startpos, endpos, time, child=None, repeat=False, bounce=False,
         anim_timebase=False, style='motion', time_warp=None, **properties):
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

    @param anim_timebase: True if we use the animation timebase, False to use the
    displayable timebase.

    @param time_warp: If not None, this is a function that takes a
    fraction of the period (between 0.0 and 1.0), and returns a
    new fraction of the period. Use this to warp time, applying
    acceleration and deceleration to motions.

    This can be used as a transition. See Motion for details.
    """

    return Motion(Interpolate(startpos, endpos),
                  time,
                  child,
                  repeat=repeat,
                  bounce=bounce,
                  anim_timebase=anim_timebase,
                  style=style,
                  time_warp=time_warp,
                  **properties)


class Revolver(object):

    def __init__(self, start, end, child, around=(0.5, 0.5), cor=(0.5, 0.5), pos=None):
        self.start = start
        self.end = end
        self.around = around
        self.cor = cor
        self.pos = pos
        self.child = child

    def __call__(self, t, (w, h, cw, ch)):

        # Converts a float to an integer in the given range, passes
        # integers through unchanged.
        def fti(x, r):
            if x is None:
                x = 0

            if isinstance(x, float):
                return int(x * r)
            else:
                return x

        if self.pos is None:
            pos = self.child.get_placement()
        else:
            pos = self.pos

        xpos, ypos, xanchor, yanchor, _xoffset, _yoffset, _subpixel = pos

        xpos = fti(xpos, w)
        ypos = fti(ypos, h)
        xanchor = fti(xanchor, cw)
        yanchor = fti(yanchor, ch)

        xaround, yaround = self.around

        xaround = fti(xaround, w)
        yaround = fti(yaround, h)

        xcor, ycor = self.cor

        xcor = fti(xcor, cw)
        ycor = fti(ycor, ch)

        angle = self.start + (self.end - self.start) * t
        angle *= math.pi / 180

        # The center of rotation, relative to the xaround.
        x = xpos - xanchor + xcor - xaround
        y = ypos - yanchor + ycor - yaround

        # Rotate it.
        nx = x * math.cos(angle) - y * math.sin(angle)
        ny = x * math.sin(angle) + y * math.cos(angle)

        # Project it back.
        nx = nx - xcor + xaround
        ny = ny - ycor + yaround

        return (renpy.display.core.absolute(nx), renpy.display.core.absolute(ny), 0, 0)


def Revolve(start, end, time, child, around=(0.5, 0.5), cor=(0.5, 0.5), pos=None, **properties):

    return Motion(Revolver(start, end, child, around=around, cor=cor, pos=pos),
                  time,
                  child,
                  add_sizes=True,
                  **properties)



def zoom_render(crend, x, y, w, h, zw, zh, bilinear):
    """
    This creates a render that zooms its child.

    `crend` - The render of the child.
    `x`, `y`, `w`, `h` - A rectangle inside the child.
    `zw`, `zh` - The size the rectangle is rendered to.
    `bilinear` - Should we be rendering in bilinear mode?
    """

    rv = renpy.display.render.Render(zw, zh)

    if zw == 0 or zh == 0 or w == 0 or h == 0:
        return rv


    rv.forward = renpy.display.render.Matrix2D(w / zw, 0, 0, h / zh)
    rv.reverse = renpy.display.render.Matrix2D(zw / w, 0, 0, zh / h)

    rv.clipping = True

    rv.blit(crend, rv.reverse.transform(-x, -y))

    return rv


class ZoomCommon(renpy.display.core.Displayable):
    def __init__(self,
                 time, child,
                 end_identity=False,
                 after_child=None,
                 time_warp=None,
                 bilinear=True,
                 opaque=True,
                 anim_timebase=False,
                 repeat=False,
                 style='motion',
                 **properties):
        """
        @param time: The amount of time it will take to
        interpolate from the start to the end rectange.

        @param child: The child displayable.

        @param after_child: If present, a second child
        widget. This displayable will be rendered after the zoom
        completes. Use this to snap to a sharp displayable after
        the zoom is done.

        @param time_warp: If not None, this is a function that takes a
        fraction of the period (between 0.0 and 1.0), and returns a
        new fraction of the period. Use this to warp time, applying
        acceleration and deceleration to motions.
        """

        super(ZoomCommon, self).__init__(style=style, **properties)

        child = renpy.easy.displayable(child)

        self.time = time
        self.child = child
        self.repeat = repeat

        if after_child:
            self.after_child = renpy.easy.displayable(after_child)
        else:
            if end_identity:
                self.after_child = child
            else:
                self.after_child = None

        self.time_warp = time_warp
        self.bilinear = bilinear
        self.opaque = opaque
        self.anim_timebase = anim_timebase


    def visit(self):
        return [ self.child, self.after_child ]

    def render(self, width, height, st, at):

        if self.anim_timebase:
            t = at
        else:
            t = st

        if self.time:
            done = min(t / self.time, 1.0)
        else:
            done = 1.0

        if self.repeat:
            done = done % 1.0

        if renpy.game.less_updates:
            done = 1.0

        self.done = done

        if self.after_child and done == 1.0:
            return renpy.display.render.render(self.after_child, width, height, st, at)

        if self.time_warp:
            done = self.time_warp(done)

        rend = renpy.display.render.render(self.child, width, height, st, at)

        rx, ry, rw, rh, zw, zh = self.zoom_rectangle(done, rend.width, rend.height)

        if rx < 0 or ry < 0 or rx + rw > rend.width or ry + rh > rend.height:
            raise Exception("Zoom rectangle %r falls outside of %dx%d parent surface." % ((rx, ry, rw, rh), rend.width, rend.height))

        rv = zoom_render(rend, rx, ry, rw, rh, zw, zh, self.bilinear)

        if self.done < 1.0:
            renpy.display.render.redraw(self, 0)

        return rv

    def event(self, ev, x, y, st):

        if not self.time:
            done = 1.0
        else:
            done = min(st / self.time, 1.0)

        if done == 1.0 and self.after_child:
            return self.after_child.event(ev, x, y, st)
        else:
            return None


class Zoom(ZoomCommon):

    def __init__(self, size, start, end, time, child, **properties):

        end_identity = (end == (0.0, 0.0) + size)

        super(Zoom, self).__init__(time, child, end_identity=end_identity, **properties)

        self.size = size
        self.start = start
        self.end = end

    def zoom_rectangle(self, done, width, height):

        rx, ry, rw, rh = [ (a + (b - a) * done) for a, b in zip(self.start, self.end) ]

        return rx, ry, rw, rh, self.size[0], self.size[1]


class FactorZoom(ZoomCommon):

    def __init__(self, start, end, time, child, **properties):

        end_identity = (end == 1.0)

        super(FactorZoom, self).__init__(time, child, end_identity=end_identity, **properties)

        self.start = start
        self.end = end

    def zoom_rectangle(self, done, width, height):

        factor = self.start + (self.end - self.start) * done

        return 0, 0, width, height, factor * width, factor * height



class SizeZoom(ZoomCommon):

    def __init__(self, start, end, time, child, **properties):

        end_identity = False

        super(SizeZoom, self).__init__(time, child, end_identity=end_identity, **properties)

        self.start = start
        self.end = end

    def zoom_rectangle(self, done, width, height):

        sw, sh = self.start
        ew, eh = self.end

        zw = sw + (ew - sw) * done
        zh = sh + (eh - sh) * done

        return 0, 0, width, height, zw, zh


class RotoZoom(renpy.display.core.Displayable):

    transform = None

    def __init__(self,
                 rot_start,
                 rot_end,
                 rot_delay,
                 zoom_start,
                 zoom_end,
                 zoom_delay,
                 child,
                 rot_repeat=False,
                 zoom_repeat=False,
                 rot_bounce=False,
                 zoom_bounce=False,
                 rot_anim_timebase=False,
                 zoom_anim_timebase=False,
                 rot_time_warp=None,
                 zoom_time_warp=None,
                 opaque=False,
                 style='motion',
                 **properties):

        super(RotoZoom, self).__init__(style=style, **properties)

        self.rot_start = rot_start
        self.rot_end = rot_end
        self.rot_delay = rot_delay

        self.zoom_start = zoom_start
        self.zoom_end = zoom_end
        self.zoom_delay = zoom_delay

        self.child = renpy.easy.displayable(child)

        self.rot_repeat = rot_repeat
        self.zoom_repeat = zoom_repeat

        self.rot_bounce = rot_bounce
        self.zoom_bounce = zoom_bounce

        self.rot_anim_timebase = rot_anim_timebase
        self.zoom_anim_timebase = zoom_anim_timebase

        self.rot_time_warp = rot_time_warp
        self.zoom_time_warp = zoom_time_warp

        self.opaque = opaque


    def visit(self):
        return [ self.child ]


    def render(self, width, height, st, at):

        if self.rot_anim_timebase:
            rot_time = at
        else:
            rot_time = st

        if self.zoom_anim_timebase:
            zoom_time = at
        else:
            zoom_time = st

        if self.rot_delay == 0:
            rot_time = 1.0
        else:
            rot_time /= self.rot_delay

        if self.zoom_delay == 0:
            zoom_time = 1.0
        else:
            zoom_time /= self.zoom_delay

        if self.rot_repeat:
            rot_time %= 1.0

        if self.zoom_repeat:
            zoom_time %= 1.0

        if self.rot_bounce:
            rot_time *= 2
            rot_time = min(rot_time, 2.0 - rot_time)

        if self.zoom_bounce:
            zoom_time *= 2
            zoom_time = min(zoom_time, 2.0 - zoom_time)

        if renpy.game.less_updates:
            rot_time = 1.0
            zoom_time = 1.0

        rot_time = min(rot_time, 1.0)
        zoom_time = min(zoom_time, 1.0)

        if self.rot_time_warp:
            rot_time = self.rot_time_warp(rot_time)

        if self.zoom_time_warp:
            zoom_time = self.zoom_time_warp(zoom_time)


        angle = self.rot_start + (1.0 * self.rot_end - self.rot_start) * rot_time
        zoom = self.zoom_start + (1.0 * self.zoom_end - self.zoom_start) * zoom_time
        # angle = -angle * math.pi / 180

        zoom = max(zoom, 0.001)

        if self.transform is None:
            self.transform = Transform(self.child)

        self.transform.rotate = angle
        self.transform.zoom = zoom

        rv = renpy.display.render.render(self.transform, width, height, st, at)

        if rot_time <= 1.0 or zoom_time <= 1.0:
            renpy.display.render.redraw(self.transform, 0)

        return rv


# For compatibility with old games.
renpy.display.layout.Transform = Transform
renpy.display.layout.RotoZoom = RotoZoom
renpy.display.layout.SizeZoom = SizeZoom
renpy.display.layout.FactorZoom = FactorZoom
renpy.display.layout.Zoom = Zoom
renpy.display.layout.Revolver = Revolver
renpy.display.layout.Motion = Motion
renpy.display.layout.Interpolate = Interpolate

# Leave these functions around - they might have been pickled somewhere.
renpy.display.layout.Revolve = Revolve # function
renpy.display.layout.Move = Move # function
renpy.display.layout.Pan = Pan # function
