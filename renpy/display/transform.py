# Copyright 2004-2022 Tom Rothamel <pytom@bishoujo.us>
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

from __future__ import division, absolute_import, with_statement, print_function, unicode_literals
from renpy.compat import PY2, basestring, bchr, bord, chr, open, pystr, range, round, str, tobytes, unicode # *

from typing import Any

# This file contains displayables that move, zoom, rotate, or otherwise
# transform displayables. (As well as displayables that support them.)
import math
import types # @UnresolvedImport

import renpy
from renpy.display.layout import Container
from renpy.display.accelerator import transform_render
from renpy.atl import position, any_object, bool_or_none, float_or_none, matrix, mesh

# The null object that's used if we don't have a defined child.
null = None


def get_null():
    global null

    if null is None:
        null = renpy.display.layout.Null()
        renpy.display.motion.null = null

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
    Returns the first argument that is not None, or the last argument if
    all are None.
    """

    for i in args:
        if i is not None:
            return i

    return args[-1]


class TransformState(renpy.object.Object):

    last_angle = None
    last_events = True

    def __init__(self):

        # Most fields on this object are set by add_property, at the bottom
        # of this file.

        # An xpos (etc) inherited from our child overrides an xpos inherited
        # from an old transform, but not an xpos set in the current transform.
        #
        # inherited_xpos stores the inherited_xpos, which is overridden by the
        # xpos, if not None.
        self.inherited_xpos = None
        self.inherited_ypos = None
        self.inherited_xanchor = None
        self.inherited_yanchor = None

        # The last angle that was rotated to.
        self.last_angle = None

    def take_state(self, ts):

        d = self.__dict__

        for k in all_properties:
            d[k] = getattr(ts, k)

        self.last_angle = ts.last_angle
        self.last_events = ts.last_events

        # Set the position and anchor to None, so inheritance works.
        if self.perspective is None: # type: ignore
            self.xpos = None
            self.ypos = None
            self.xanchor = None
            self.yanchor = None

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

        for prop in diff2_properties:
            new = getattr(newts, prop)
            old = getattr(self, prop)

            if new != old:
                rv[prop] = (old, new)

        for prop in diff4_properties:

            new = getattr(newts, prop)
            old = getattr(self, prop)

            if new is None:
                new = getattr(newts, "inherited_" + prop)
            if old is None:
                old = getattr(self, "inherited_" + prop)

            if new != old:
                rv[prop] = (old, new)

        return rv

    def get_placement(self, cxoffset=0, cyoffset=0):

        if self.perspective is not None: # type: ignore
            return (
                0,
                0,
                0,
                0,
                cxoffset,
                cyoffset,
                False,
                )

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

    def get_xysize(self):
        return self.xsize, self.ysize

    def set_xysize(self, value):
        if value is None:
            value = (None, None)
        self.xsize, self.ysize = value

    xysize = property(get_xysize, set_xysize)

    def set_size(self, value):
        if value is None:
            self.xysize = None
        else:
            self.xysize = tuple(int(x) if isinstance(x, float) else x for x in value)

    size = property(get_xysize, set_size)

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

    def get_xycenter(self):
        return self.xcenter, self.ycenter

    def set_xycenter(self, value):
        if value is None:
            value = (None, None)
        self.xcenter, self.ycenter = value

    xycenter = property(get_xycenter, set_xycenter)


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

    def after_upgrade(self, version):

        if version < 1:
            self.active = False
            self.state = TransformState()

            self.state.xpos = self.xpos or 0 # type: ignore
            self.state.ypos = self.ypos or 0 # type: ignore
            self.state.xanchor = self.xanchor or 0 # type: ignore
            self.state.yanchor = self.yanchor or 0 # type: ignore
            self.state.alpha = self.alpha # type: ignore
            self.state.rotate = self.rotate # type: ignore
            self.state.zoom = self.zoom # type: ignore
            self.state.xzoom = self.xzoom # type: ignore
            self.state.yzoom = self.yzoom # type: ignore

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
    children = [ ]
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
                 alt=None,

                 **kwargs):

        self.kwargs = kwargs
        self.style_arg = style

        super(Transform, self).__init__(style=style, focus=focus, default=default, _args=_args, alt=alt)

        self.function = function

        child = renpy.easy.displayable_or_none(child)
        if child is not None:
            self.add(child)

        self.state = TransformState() # type: Any

        if kwargs:

            # A map from prefix -> (prop -> value)
            self.arguments = { }

            # Fill self.arguments with a
            for k, v in kwargs.items():

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
                for k, v in self.arguments[""].items():
                    setattr(self.state, k, v)

        else:
            self.arguments = None

        # This is the matrix transforming our coordinates into child coordinates.
        self.forward = None # type: renpy.display.matrix.Matrix|None
        self.reverse = None # type: renpy.display.matrix.Matrix|None

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

        self.child_size = (0, 0)
        self.render_size = (0, 0)

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

            for k, v in d.items():
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

        if isinstance(self.child, Transform) and isinstance(t.child, Transform):
            self.child.take_state(t.child)

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

        if (event == "replaced") and (not self.active):
            return True

        if self.function is not None:
            return True

        if self.child and self.child._handles_event(event):
            return True

        return False

    def _hide(self, st, at, kind):

        # Prevent time from ticking backwards, as can happen if we replace a
        # transform but keep its state.
        if st + self.st_offset <= self.st:
            self.st_offset = self.st - st
        if at + self.at_offset <= self.at:
            self.at_offset = self.at - at

        self.st = st = st + self.st_offset
        self.at = at = at + self.at_offset

        if not self.active:
            self.update_state()

        if not self.child:
            return None

        if not (self.hide_request or self.replaced_request):
            d = self.copy()
        else:
            d = self

        d.st_offset = self.st_offset
        d.at_offset = self.at_offset

        if isinstance(self, ATLTransform):
            d.atl_st_offset = self.atl_st_offset if (self.atl_st_offset is not None) else self.st_offset # type: ignore

        if kind == "hide":
            d.hide_request = True
        else:
            d.replaced_request = True

        d.hide_response = True
        d.replaced_response = True

        if d.function is not None:
            d.function(d, st, at)
        elif isinstance(d, ATLTransform):
            d.execute(d, st, at)

        new_child = d.child._hide(st - self.st_offset, at - self.st_offset, kind)

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

            if not self._duplicatable:
                child._unique()

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

        if self.state.last_events != self.state.events:
            if self.state.events:
                renpy.game.interface.timeout(0)
            self.state.last_events = self.state.events

    # The render method is now defined in accelerator.pyx.
    def render(self, width, height, st, at):
        return transform_render(self, width, height, st, at)

    def event(self, ev, x, y, st):

        if self.hide_request:
            return None

        if not self.state.events: # type: ignore
            return

        children = self.children
        offsets = self.offsets

        if not offsets:
            return None

        for i in range(len(self.children) - 1, -1, -1):

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

        if getattr(child, '_duplicatable', False):
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
        if self._duplicatable:

            if self.child is not None:
                self.child._unique()

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

        if args and args.args:
            args.extraneous()

        if not self._duplicatable:
            return self

        rv = self(_args=args)
        rv.take_execution_state(self)

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

    def _repr_info(self):
        return repr(self.child)


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

        if self.state.last_events != self.state.events:
            if self.state.events:
                renpy.game.interface.timeout(0)
            self.state.last_events = self.state.events


    def _repr_info(self):
        return repr((self.child, self.atl.loc))


# Names of transform properties, and if the property should be handled with
# diff2 or diff4.
all_properties = set()
diff2_properties = set()
diff4_properties = set()

# Uniforms and GL properties.
uniforms = set()
gl_properties = set()


def add_property(name, atl=any_object, default=None, diff=2): # type: (str, Any, Any, int|None) -> None
    """
    Adds an ATL property.
    """

    if name in all_properties:
        return

    all_properties.add(name)
    setattr(TransformState, name, default)
    setattr(Transform, name, Proxy(name))
    renpy.atl.PROPERTIES[name] = atl

    if diff == 2:
        diff2_properties.add(name)
    elif diff == 4:
        diff4_properties.add(name)


def add_uniform(name):
    """
    Adds a uniform with `name` to Transform and ATL.
    """

    if not name.startswith("u_"):
        return

    if name in renpy.gl2.gl2draw.standard_uniforms:
        return

    add_property(name, diff=2)

    uniforms.add(name)


def add_gl_property(name):
    """
    Adds a GL property with `name` to Transform and ATL.
    """

    add_property(name, diff=None)

    gl_properties.add(name)


add_property("additive", float, 0.0)
add_property("alpha", float, 1.0)
add_property("blend", any_object, None)
add_property("blur", float_or_none, None)
add_property("corner1", (position, position), None)
add_property("corner2", (position, position), None)
add_property("crop", (position, position, position, position), None)
add_property("crop_relative", bool_or_none, None)
add_property("debug", any_object, None)
add_property("delay", float, 0)
add_property("events", bool, True)
add_property("fit", str, None)
add_property("matrixanchor", (position, position), None)
add_property("matrixcolor", matrix, None)
add_property("matrixtransform", matrix, None)
add_property("maxsize", (int, int), None)
add_property("mesh", mesh, False, diff=None)
add_property("mesh_pad", any_object, None)
add_property("nearest", bool_or_none, None)
add_property("perspective", any_object, None)
add_property("rotate", float, None)
add_property("rotate_pad", bool, True)
add_property("shader", any_object, None, diff=None)
add_property("subpixel", bool, False)
add_property("transform_anchor", bool, False)
add_property("zoom", float, 1.0)

add_property("xanchoraround", float, 0.0)
add_property("xanchor", position, None, diff=4)
add_property("xaround", position, 0.0)
add_property("xoffset", float, 0.0)
add_property("xpan", float_or_none, None)
add_property("xpos", position, None, diff=4)
add_property("xsize", position, None)
add_property("xtile", int, 1)
add_property("xzoom", float, 1.0)

add_property("yanchoraround", float, 0.0)
add_property("yanchor", position, None, diff=4)
add_property("yaround", position, 0.0)
add_property("yoffset", float, 0.0)
add_property("ypan", float_or_none, None)
add_property("ypos", position, None, diff=4)
add_property("ysize", position, None)
add_property("ytile", int, 1)
add_property("yzoom", float, 1.0)

add_property("zpos", float, 0.0)
add_property("zzoom", bool, False)

add_gl_property("gl_anisotropic")
add_gl_property("gl_blend_func")
add_gl_property("gl_color_mask")
add_gl_property("gl_depth")
add_gl_property("gl_drawable_resolution")
add_gl_property("gl_mipmap")
add_gl_property("gl_pixel_perfect")
add_gl_property("gl_texture_scaling")
add_gl_property("gl_texture_wrap")

ALIASES = {
    "alignaround" : (float, float),
    "align" : (float, float),
    "anchor" : (position, position),
    "angle" : float,
    "around" : (position, position),
    "offset" : (int, int),
    "pos" : (position, position),
    "radius" : float,
    "size" : (int, int),
    "xalign" : float,
    "xcenter" : position,
    "xycenter" : (position, position),
    "xysize" : (position, position),
    "yalign" : float,
    "ycenter" : position,
    }

renpy.atl.PROPERTIES.update(ALIASES)

for name in ALIASES:
    setattr(Transform, name, Proxy(name))
