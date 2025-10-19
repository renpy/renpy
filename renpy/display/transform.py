# Copyright 2004-2025 Tom Rothamel <pytom@bishoujo.us>
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
from typing import Any, Callable, Literal, Protocol, TYPE_CHECKING, Self, assert_never

import math

import renpy
from renpy.types import DisplayableLike, Position
from renpy.display.displayable import Displayable, DisplayableArguments, Placement
from renpy.display.layout import Container
from renpy.display.accelerator import RenderTransform
from renpy.display.position import position, absolute


class DualAngle:
    def __init__(self, absolute: float, relative: float):
        self.absolute = absolute
        self.relative = relative

    @classmethod
    def from_any(cls, other):
        if isinstance(other, cls):
            return other

        elif type(other) is float:
            return cls(other, other)

        else:
            raise TypeError(f"Cannot convert {other.__class__} to DualAngle")

    def __add__(self, value: "DualAngle", /):
        if isinstance(value, DualAngle):
            return DualAngle(self.absolute + value.absolute, self.relative + value.relative)

        return NotImplemented

    def __sub__(self, value: "DualAngle", /):
        if isinstance(value, DualAngle):
            return DualAngle(self.absolute - value.absolute, self.relative - value.relative)

        return NotImplemented

    def __mul__(self, value: int | float, /):
        if isinstance(value, (int, float)):
            return DualAngle(self.absolute * value, self.relative * value)

        return NotImplemented

    __rmul__ = __mul__

    @staticmethod
    def get_pos_polar_vector(ts: "TransformState") -> tuple[float, float]:
        """
        Return a tuple of (x, y) representing the position of the anchor point.
        """

        xpos = position(first_not_none(ts.xpos, ts.inherited_xpos, 0))
        xpos = absolute.compute_raw(xpos, ts.available_width)

        ypos = position(first_not_none(ts.ypos, ts.inherited_ypos, 0))
        ypos = absolute.compute_raw(ypos, ts.available_height)

        xaround = absolute.compute_raw(position(ts.xaround), ts.available_width)
        yaround = absolute.compute_raw(position(ts.yaround), ts.available_height)

        return (xpos - xaround, ypos - yaround)

    @staticmethod
    def get_anchor_polar_vector(ts: "TransformState") -> tuple[tuple[float, float], tuple[float, float]]:
        """
        Returns a 2-tuple of 2-tuples,
        where the first small tuple is absolute and the second tuple is relative,
        and the first element of each tuple is in x and the second in y.
        They represent the vector from the anchoraround point to the final anchor point.
        """

        xanchoraround = position(ts.xanchoraround)
        yanchoraround = position(ts.yanchoraround)
        xanchor = position(first_not_none(ts.xanchor, ts.inherited_xanchor, 0))
        yanchor = position(first_not_none(ts.yanchor, ts.inherited_yanchor, 0))

        absolute_vector = (
            xanchor.absolute - xanchoraround.absolute,
            yanchor.absolute - yanchoraround.absolute,
        )
        relative_vector = (
            xanchor.relative - xanchoraround.relative,
            yanchor.relative - yanchoraround.relative,
        )

        return absolute_vector, relative_vector

    @staticmethod
    def set_pos_from_angle_and_radius(ts: "TransformState", angle: float, radius: float):
        xaround = absolute.compute_raw(position(ts.xaround), ts.available_width)
        yaround = absolute.compute_raw(position(ts.yaround), ts.available_height)

        angle = angle * math.pi / 180

        dx = radius * math.sin(angle)
        dy = -radius * math.cos(angle)

        ts.xpos = absolute(xaround + dx)
        ts.ypos = absolute(yaround + dy)

    @staticmethod
    def set_anchor_from_anchorangle_and_anchorradius(
        ts: "TransformState",
        absolute_anchorangle: float,
        relative_anchorangle: float,
        absolute_anchorradius: float,
        relative_anchorradius: float,
    ):
        xanchoraround = position(ts.xanchoraround)
        yanchoraround = position(ts.yanchoraround)

        absolute_anchorangle = absolute_anchorangle * math.pi / 180
        relative_anchorangle = relative_anchorangle * math.pi / 180

        absolute_dx = absolute_anchorradius * math.sin(absolute_anchorangle)
        absolute_dy = -absolute_anchorradius * math.cos(absolute_anchorangle)
        relative_dx = relative_anchorradius * math.sin(relative_anchorangle)
        relative_dy = -relative_anchorradius * math.cos(relative_anchorangle)

        ts.xanchor = position(xanchoraround.absolute + absolute_dx, xanchoraround.relative + relative_dx)
        ts.yanchor = position(yanchoraround.absolute + absolute_dy, yanchoraround.relative + relative_dy)


class Camera(renpy.object.Object):
    """
    :doc: point_to_camera

    Instances of this class can be used with point_to to point
    at the location of the camera for a particular layer.

    `layer`
        The name of the layer.
    """

    def __init__(self, layer: str = "master"):
        self.layer: str = layer


# The null object that's used if we don't have a defined child.
null: renpy.display.layout.Null | None = None


def get_null():
    global null

    if null is None:
        null = renpy.display.layout.Null()
        renpy.display.motion.null = null

    return null


def first_not_none[T, T2](*args: *tuple[*tuple[T | None, ...], T2]) -> T | T2:
    """
    Returns the first argument that is not None, or the last argument if
    all are None.
    """

    for i in args:
        if i is not None:
            return i

    return args[-1]


def limit_angle(n: float) -> float:
    """
    Limits an angle to the range 0 and 360 degrees.
    """

    n = n % 360

    if n < 0:
        n += 360

    return n


def position_or_none(x: Any) -> Position | None:
    if x is None:
        return None

    return position(x)


def any_object(x: Any) -> object:
    return x


def bool_or_none(x: Any) -> bool | None:
    if x is None:
        return x

    return bool(x)


def float_or_none(x: Any) -> float | None:
    if x is None:
        return x

    return float(x)


class MatrixLike(Protocol):
    origin: "MatrixLike | None" = None

    def __call__(self, other: "MatrixLike", done: float, /) -> renpy.display.matrix.Matrix: ...


def matrix_or_none(x: Any) -> MatrixLike | renpy.display.matrix.Matrix | None:
    if x is None:
        return None
    elif callable(x):
        return x  # type: ignore
    else:
        return renpy.display.matrix.Matrix(x)


type MeshValue = tuple[int, int] | bool


def mesh_or_none(x: Any) -> MeshValue | None:
    if x is None:
        return None
    elif isinstance(x, tuple):
        return x
    else:
        return bool(x)


type MeshPadValue = tuple[int, int] | tuple[int, int, int, int]
type FitValue = Literal["contain", "cover", "fill", "scale-down", "scale-up"]
type PerspectiveValue = bool | float | tuple[float, float, float]
type PointToValue = tuple[float, float, float] | Camera


class TransformProperty[T]:
    name: str
    atl_type: Callable[[object], T] | tuple[Callable[[object], T], ...]
    default: T
    diff: Literal[2, None]
    kind: Literal["field", "alias", "gl", "uniform"]

    def __init__(
        self,
        name: str,
        atl_type: Any = any_object,
        default: T = None,
        diff: Literal[2, None] = 2,
        kind: Literal["field", "alias", "gl", "uniform"] = "field",
    ):
        self.name = name
        self.atl_type = atl_type
        self.default = default
        self.diff = diff
        self.kind = kind

        if isinstance(atl_type, tuple) and default is not None:
            if not isinstance(default, tuple):
                raise TypeError("Default value must be a tuple if atl_type is a tuple.")

            if len(atl_type) != len(default):
                raise TypeError("Length of atl_type and default must be the same.")

    def __get__(self, instance: "TransformProperties", owner) -> T: ...

    def __set__(self, instance: "TransformProperties", value: T): ...


class TransformProperties(Protocol):
    # NOTE: Explicit type annotation for protocol member forces type checker to
    # take precedence over the type annotation in the protocol implementation.

    # Positioning
    pos: TransformProperty[tuple[Position | None, Position | None]] = TransformProperty(
        "pos", (position_or_none,) * 2, (None, None), kind="alias"
    )
    xpos: TransformProperty[Position | None] = TransformProperty("xpos", position_or_none)
    ypos: TransformProperty[Position | None] = TransformProperty("ypos", position_or_none)

    anchor: TransformProperty[tuple[Position | None, Position | None]] = TransformProperty(
        "anchor", (position_or_none,) * 2, (None, None), kind="alias"
    )
    xanchor: TransformProperty[Position | None] = TransformProperty("xanchor", position_or_none)
    yanchor: TransformProperty[Position | None] = TransformProperty("yanchor", position_or_none)

    align: TransformProperty[tuple[Position | None, Position | None]] = TransformProperty(
        "align", (position_or_none,) * 2, (None, None), kind="alias"
    )
    xalign: TransformProperty[Position | None] = TransformProperty("xalign", position_or_none, kind="alias")
    yalign: TransformProperty[Position | None] = TransformProperty("yalign", position_or_none, kind="alias")

    xycenter: TransformProperty[tuple[Position | None, Position | None]] = TransformProperty(
        "xycenter", (position_or_none,) * 2, (None, None), kind="alias"
    )
    xcenter: TransformProperty[Position | None] = TransformProperty("xcenter", position_or_none, kind="alias")
    ycenter: TransformProperty[Position | None] = TransformProperty("ycenter", position_or_none, kind="alias")

    offset: TransformProperty[tuple[absolute | int, absolute | int]] = TransformProperty(
        "offset", (absolute,) * 2, (absolute(0), absolute(0)), kind="alias"
    )
    xoffset: TransformProperty[absolute | int] = TransformProperty("xoffset", absolute, absolute(0))
    yoffset: TransformProperty[absolute | int] = TransformProperty("yoffset", absolute, absolute(0))

    subpixel: TransformProperty[bool] = TransformProperty("subpixel", bool, False)

    # Rotation
    rotate: TransformProperty[float | None] = TransformProperty("rotate", float_or_none)
    rotate_pad: TransformProperty[bool] = TransformProperty("rotate_pad", bool, True)
    transform_anchor: TransformProperty[bool] = TransformProperty("transform_anchor", bool, False)

    # Zoom and Flip
    zoom: TransformProperty[float] = TransformProperty("zoom", float, 1.0)
    xzoom: TransformProperty[float] = TransformProperty("xzoom", float, 1.0)
    yzoom: TransformProperty[float] = TransformProperty("yzoom", float, 1.0)

    # Pixel Effects
    nearest: TransformProperty[bool | None] = TransformProperty("nearest", bool_or_none)
    alpha: TransformProperty[float] = TransformProperty("alpha", float, 1.0)
    additive: TransformProperty[float] = TransformProperty("additive", float, 0.0)
    matrixcolor: TransformProperty[MatrixLike | renpy.display.matrix.Matrix | None] = TransformProperty(
        "matrixcolor", matrix_or_none
    )
    blur: TransformProperty[float | None] = TransformProperty("blur", float_or_none)

    # Polar Positioning
    around: TransformProperty[tuple[Position, Position]] = TransformProperty(
        "around", (position,) * 2, (position(0), position(0)), kind="alias"
    )
    xaround: TransformProperty[Position] = TransformProperty("xaround", position, position(0))
    yaround: TransformProperty[Position] = TransformProperty("yaround", position, position(0))
    angle: TransformProperty[float] = TransformProperty("angle", float, 0.0, kind="alias")
    radius: TransformProperty[Position] = TransformProperty("radius", position, position(0), kind="alias")

    # Polar Positioning of the Anchor
    anchoraround: TransformProperty[tuple[Position, Position]] = TransformProperty(
        "anchoraround", (position,) * 2, (0.5, 0.5), kind="alias"
    )
    xanchoraround: TransformProperty[Position] = TransformProperty("xanchoraround", position, 0.5)
    yanchoraround: TransformProperty[Position] = TransformProperty("yanchoraround", position, 0.5)
    anchorangle: TransformProperty[DualAngle | float] = TransformProperty(
        "anchorangle", DualAngle.from_any, 0.0, kind="alias"
    )
    anchorradius: TransformProperty[Position] = TransformProperty("anchorradius", position, position(0), kind="alias")

    # Cropping and Resizing
    crop: TransformProperty[tuple[Position, Position, Position, Position] | None] = TransformProperty(
        "crop", (position,) * 4
    )
    corner1: TransformProperty[tuple[Position, Position] | None] = TransformProperty("corner1", (position,) * 2)
    corner2: TransformProperty[tuple[Position, Position] | None] = TransformProperty("corner2", (position,) * 2)

    xysize: TransformProperty[tuple[Position | None, Position | None]] = TransformProperty(
        "xysize", (position_or_none,) * 2, (None, None), kind="alias"
    )
    xsize: TransformProperty[Position | None] = TransformProperty("xsize", position_or_none)
    ysize: TransformProperty[Position | None] = TransformProperty("ysize", position_or_none)

    fit: TransformProperty[FitValue | None] = TransformProperty("fit")

    # Panning and Tiling
    xpan: TransformProperty[float | None] = TransformProperty("xpan", float_or_none)
    ypan: TransformProperty[float | None] = TransformProperty("ypan", float_or_none)
    xtile: TransformProperty[int] = TransformProperty("xtile", int, 1)
    ytile: TransformProperty[int] = TransformProperty("ytile", int, 1)

    # Transitions
    delay: TransformProperty[float] = TransformProperty("delay", float, 0.0)
    events: TransformProperty[bool] = TransformProperty("events", bool, True)

    # Other
    fps: TransformProperty[float | None] = TransformProperty("fps", float_or_none)
    show_cancels_hide: TransformProperty[bool] = TransformProperty("show_cancels_hide", bool, True)

    # 3D Stage properties
    point_to: TransformProperty[PointToValue | None] = TransformProperty("point_to")

    orientation: TransformProperty[tuple[float, float, float] | None] = TransformProperty(
        "orientation", (float_or_none,) * 3
    )
    xrotate: TransformProperty[float | None] = TransformProperty("xrotate", float_or_none)
    yrotate: TransformProperty[float | None] = TransformProperty("yrotate", float_or_none)
    zrotate: TransformProperty[float | None] = TransformProperty("zrotate", float_or_none)

    matrixanchor: TransformProperty[tuple[Position, Position] | None] = TransformProperty(
        "matrixanchor", (position_or_none,) * 2
    )
    matrixtransform: TransformProperty[MatrixLike | renpy.display.matrix.Matrix | None] = TransformProperty(
        "matrixtransform", matrix_or_none
    )
    perspective: TransformProperty[PerspectiveValue | None] = TransformProperty("perspective")
    zpos: TransformProperty[float] = TransformProperty("zpos", float, 0.0)
    zzoom: TransformProperty[bool] = TransformProperty("zzoom", bool, False)

    # Model-based rendering properties
    mesh: TransformProperty[MeshValue | None] = TransformProperty("mesh", mesh_or_none, diff=None)
    mesh_pad: TransformProperty[MeshPadValue | None] = TransformProperty("mesh_pad")
    shader: TransformProperty[str | list[str] | None] = TransformProperty("shader", diff=None)
    blend: TransformProperty[str | None] = TransformProperty("blend")

    # GL Properties
    gl_anisotropic: TransformProperty[Any | None] = TransformProperty("gl_anisotropic", diff=None, kind="gl")
    gl_blend_func: TransformProperty[Any | None] = TransformProperty("gl_blend_func", diff=None, kind="gl")
    gl_color_mask: TransformProperty[Any | None] = TransformProperty("gl_color_mask", diff=None, kind="gl")
    gl_cull_face: TransformProperty[Any | None] = TransformProperty("gl_cull_face", diff=None, kind="gl")
    gl_depth: TransformProperty[Any | None] = TransformProperty("gl_depth", diff=None, kind="gl")
    gl_drawable_resolution: TransformProperty[Any | None] = TransformProperty(
        "gl_drawable_resolution", diff=None, kind="gl"
    )
    gl_mipmap: TransformProperty[Any | None] = TransformProperty("gl_mipmap", diff=None, kind="gl")
    gl_pixel_perfect: TransformProperty[Any | None] = TransformProperty("gl_pixel_perfect", diff=None, kind="gl")
    gl_texture_scaling: TransformProperty[Any | None] = TransformProperty("gl_texture_scaling", diff=None, kind="gl")
    gl_texture_wrap: TransformProperty[Any | None] = TransformProperty("gl_texture_wrap", diff=None, kind="gl")
    gl_texture_wrap_tex0: TransformProperty[Any | None] = TransformProperty(
        "gl_texture_wrap_tex0", diff=None, kind="gl"
    )
    gl_texture_wrap_tex1: TransformProperty[Any | None] = TransformProperty(
        "gl_texture_wrap_tex1", diff=None, kind="gl"
    )
    gl_texture_wrap_tex2: TransformProperty[Any | None] = TransformProperty(
        "gl_texture_wrap_tex2", diff=None, kind="gl"
    )
    gl_texture_wrap_tex3: TransformProperty[Any | None] = TransformProperty(
        "gl_texture_wrap_tex3", diff=None, kind="gl"
    )

    # Other
    debug: TransformProperty[Any | None] = TransformProperty("debug")
    _reset: TransformProperty[bool] = TransformProperty("_reset", bool, False, kind="alias")

    # Deprecated properties
    if not TYPE_CHECKING:
        crop_relative: TransformProperty[bool | None] = TransformProperty("crop_relative", bool_or_none)
        alignaround: TransformProperty[tuple[float, float]] = TransformProperty(
            "alignaround", (float,) * 2, (0.0, 0.0), kind="alias"
        )
        size: TransformProperty[tuple[int, int] | None] = TransformProperty("size", (int,) * 2, kind="alias")
        maxsize: TransformProperty[tuple[int, int] | None] = TransformProperty("maxsize", (int,) * 2)


class TransformState(renpy.object.Object, TransformProperties if TYPE_CHECKING else object):
    # Most fields on this object are set by _register_properties at the bottom of this file.

    # An xpos (etc) inherited from our child overrides an xpos inherited
    # from an old transform, but not an xpos set in the current transform.

    # inherited_xpos stores the oldts.xpos, which is overridden by the xpos, if not None.
    inherited_xpos: Position | None = None
    inherited_ypos: Position | None = None
    inherited_xanchor: Position | None = None
    inherited_yanchor: Position | None = None

    # This is used to schedule event on transform when ts.events changes.
    last_events: bool = True
    "Last value of events property."

    # Set in transform render, and used in various properties to determine
    # the available space.
    available_width: float = 0
    available_height: float = 0

    # Those fields are used by polar positioning.
    last_angle: float | None = None
    last_relative_anchorangle: float | None = None
    last_absolute_anchorangle: float | None = None
    radius_sign: Literal[1, -1] = 1
    relative_anchor_radius_sign: Literal[1, -1] = 1
    absolute_anchor_radius_sign: Literal[1, -1] = 1

    texture_uniforms: set[str] | None = None
    "If not None, the set of uniforms that provide textures."

    if TYPE_CHECKING:
        # Other properties, e.g. shader uniforms can be defined at runtime,
        # and accessing them is valid.
        def __getattr__(self, name: str) -> Any: ...

    def take_state(self, ts: "TransformState", /):
        """
        Update this transform state from `ts`.
        """

        # Take all non-default values from ts and reset the rest to default.
        d = self.__dict__
        ts_d = ts.__dict__
        for name in all_properties:
            # But skip inheritable properties.
            if name in ("xpos", "ypos", "xanchor", "yanchor"):
                continue

            if name in ts_d:
                d[name] = ts_d[name]
            else:
                d.pop(name, None)

        # Take placement of ts, but put it in inherited_ properties, and also
        # take the computed position properties, not the raw ones.
        (
            self.inherited_xpos,
            self.inherited_ypos,
            self.inherited_xanchor,
            self.inherited_yanchor,
            _,
            _,
            _,
        ) = ts.get_placement()

        # Update other state-only properties.
        self.last_angle = ts.last_angle
        self.radius_sign = ts.radius_sign
        self.relative_anchor_radius_sign = ts.relative_anchor_radius_sign
        self.absolute_anchor_radius_sign = ts.absolute_anchor_radius_sign
        self.last_absolute_anchorangle = ts.last_absolute_anchorangle
        self.last_relative_anchorangle = ts.last_relative_anchorangle
        self.last_events = ts.last_events

        self.available_width = ts.available_width
        self.available_height = ts.available_height

    def diff(self, newts: "TransformState", /) -> dict[str, tuple[Any, Any]]:
        """
        Returns a dict, with p -> (old, new) where p is a property that
        has changed between this object and the new object.
        """

        rv = {}

        for prop in diff2_properties:
            new = getattr(newts, prop)
            old = getattr(self, prop)

            if new != old:
                rv[prop] = (old, new)

        for prop in ("xpos", "ypos", "xanchor", "yanchor"):
            new = getattr(newts, prop)
            if new is None:
                new = getattr(newts, f"inherited_{prop}")

            old = getattr(self, prop)
            if old is None:
                old = getattr(self, f"inherited_{prop}")

            if new != old:
                rv[prop] = (old, new)

        return rv

    def get(self, prop: str, /) -> Any | None:
        """
        Returns the value of a property, taking inherited values into account.
        """

        old_xpos = self.xpos
        old_ypos = self.ypos
        old_xanchor = self.xanchor
        old_yanchor = self.yanchor

        try:
            if self.xpos is None:
                self.xpos = self.inherited_xpos

            if self.ypos is None:
                self.ypos = self.inherited_ypos

            if self.xanchor is None:
                self.xanchor = self.inherited_xanchor

            if self.yanchor is None:
                self.yanchor = self.inherited_yanchor

            return getattr(self, prop)

        finally:
            self.xpos = old_xpos
            self.ypos = old_ypos
            self.xanchor = old_xanchor
            self.yanchor = old_yanchor

    def get_placement(self, cxoffset: absolute | int = 0, cyoffset: absolute | int = 0) -> Placement:
        if self.perspective is not None:
            return (0, 0, 0, 0, cxoffset, cyoffset, False)

        return (
            first_not_none(self.xpos, self.inherited_xpos),
            first_not_none(self.ypos, self.inherited_ypos),
            first_not_none(self.xanchor, self.inherited_xanchor),
            first_not_none(self.yanchor, self.inherited_yanchor),
            self.xoffset + cxoffset,
            self.yoffset + cyoffset,
            self.subpixel,
        )

    # Define all alias transform properties as data descriptors.
    @property
    def pos(self) -> tuple[Position | None, Position | None]:
        return self.xpos, self.ypos

    @pos.setter
    def pos(self, value: tuple[Position | None, Position | None]):
        self.xpos, self.ypos = value

    @property
    def anchor(self) -> tuple[Position | None, Position | None]:
        return self.xanchor, self.yanchor

    @anchor.setter
    def anchor(self, value: tuple[Position | None, Position | None]):
        self.xanchor, self.yanchor = value

    @property
    def align(self) -> tuple[Position | None, Position | None]:
        return self.xpos, self.ypos

    @align.setter
    def align(self, value: tuple[Position | None, Position | None]):
        self.xpos, self.ypos = self.xanchor, self.yanchor = value

    @property
    def xalign(self) -> Position | None:
        return self.xpos

    @xalign.setter
    def xalign(self, value: Position | None):
        self.xpos = self.xanchor = value

    @property
    def yalign(self) -> Position | None:
        return self.ypos

    @yalign.setter
    def yalign(self, value: Position | None):
        self.ypos = self.yanchor = value

    @property
    def xycenter(self) -> tuple[Position | None, Position | None]:
        return self.xpos, self.ypos

    @xycenter.setter
    def xycenter(self, value: tuple[Position | None, Position | None]):
        self.xpos, self.ypos = value
        self.xanchor = 0.5
        self.yanchor = 0.5

    @property
    def xcenter(self) -> Position | None:
        return self.xpos

    @xcenter.setter
    def xcenter(self, value: Position | None):
        self.xpos = value
        self.xanchor = 0.5

    @property
    def ycenter(self) -> Position | None:
        return self.ypos

    @ycenter.setter
    def ycenter(self, value: Position | None):
        self.ypos = value
        self.yanchor = 0.5

    @property
    def offset(self) -> tuple[absolute | int, absolute | int]:
        return self.xoffset, self.yoffset

    @offset.setter
    def offset(self, value: tuple[absolute | int, absolute | int]):
        self.xoffset, self.yoffset = value

    @property
    def around(self) -> tuple[Position, Position]:
        return self.xaround, self.yaround

    @around.setter
    def around(self, value: tuple[Position, Position]):
        self.xaround, self.yaround = value

    @property
    def angle(self) -> float:
        vector_x, vector_y = DualAngle.get_pos_polar_vector(self)

        radius = math.hypot(vector_x, vector_y)
        angle = math.atan2(vector_x, -vector_y) / math.pi * 180

        if angle < 0:
            angle += 360

        if radius < 0.001 and self.last_angle is not None:
            angle = self.last_angle
        elif self.radius_sign == -1:
            angle = limit_angle(angle + 180)

        return angle

    @angle.setter
    def angle(self, value: float):
        self.last_angle = limit_angle(value)

        radius = self.radius

        if radius < 0:
            value = limit_angle(value + 180)
            radius = -radius

        DualAngle.set_pos_from_angle_and_radius(self, value, radius)

    @property
    def radius(self) -> absolute:
        vector_x, vector_y = DualAngle.get_pos_polar_vector(self)
        return absolute(math.hypot(vector_x, vector_y) * self.radius_sign)

    @radius.setter
    def radius(self, value: Position):
        room = min(self.available_width, self.available_height)
        value = absolute.compute_raw(position(value), room)
        angle = self.angle

        if value < 0:
            angle = limit_angle(angle + 180)
            value = -value
            self.radius_sign = -1
        elif value > 0:
            self.radius_sign = 1

        DualAngle.set_pos_from_angle_and_radius(self, angle, value)

    @property
    def anchoraround(self) -> tuple[Position, Position]:
        return self.xanchoraround, self.yanchoraround

    @anchoraround.setter
    def anchoraround(self, value: tuple[Position, Position]):
        self.xanchoraround, self.yanchoraround = value

    @property
    def anchorangle(self) -> DualAngle:
        (
            (absolute_vector_x, absolute_vector_y),
            (relative_vector_x, relative_vector_y),
        ) = DualAngle.get_anchor_polar_vector(self)

        absolute_radius = math.hypot(absolute_vector_x, absolute_vector_y)
        relative_radius = math.hypot(relative_vector_x, relative_vector_y)
        absolute_angle = math.atan2(absolute_vector_x, -absolute_vector_y) / math.pi * 180
        relative_angle = math.atan2(relative_vector_x, -relative_vector_y) / math.pi * 180

        if absolute_angle < 0:
            absolute_angle += 360
        if relative_angle < 0:
            relative_angle += 360

        if (absolute_radius < 0.001) and (self.last_absolute_anchorangle is not None):
            absolute_angle = self.last_absolute_anchorangle
        elif self.absolute_anchor_radius_sign < 0:
            absolute_angle = absolute_angle + 180

        if (relative_radius < 0.001) and (self.last_relative_anchorangle is not None):
            relative_angle = self.last_relative_anchorangle
        elif self.relative_anchor_radius_sign < 0:
            relative_angle = relative_angle + 180

        absolute_angle = limit_angle(absolute_angle)
        relative_angle = limit_angle(relative_angle)

        return DualAngle(absolute_angle, relative_angle)

    @anchorangle.setter
    def anchorangle(self, value: DualAngle | float):
        if isinstance(value, DualAngle):
            absolute_anchorangle = value.absolute
            relative_anchorangle = value.relative
        else:
            absolute_anchorangle = relative_anchorangle = value

        self.last_absolute_anchorangle = limit_angle(absolute_anchorangle)
        self.last_relative_anchorangle = limit_angle(relative_anchorangle)

        anchorradius = self.anchorradius
        absolute_anchorradius = anchorradius.absolute
        relative_anchorradius = anchorradius.relative

        if absolute_anchorradius < 0:
            absolute_anchorangle = limit_angle(absolute_anchorangle + 180)
            absolute_anchorradius = -absolute_anchorradius
        if relative_anchorradius < 0:
            relative_anchorangle = limit_angle(relative_anchorangle + 180)
            relative_anchorradius = -relative_anchorradius

        DualAngle.set_anchor_from_anchorangle_and_anchorradius(
            self,
            absolute_anchorangle,
            relative_anchorangle,
            absolute_anchorradius,
            relative_anchorradius,
        )

    @property
    def anchorradius(self) -> position:
        (
            (absolute_vector_x, absolute_vector_y),
            (relative_vector_x, relative_vector_y),
        ) = DualAngle.get_anchor_polar_vector(self)

        return position(
            math.hypot(absolute_vector_x, absolute_vector_y) * self.absolute_anchor_radius_sign,
            math.hypot(relative_vector_x, relative_vector_y) * self.relative_anchor_radius_sign,
        )

    @anchorradius.setter
    def anchorradius(self, value: Position):
        value = position(value)

        anchorangle = self.anchorangle
        old_anchorradius = self.anchorradius

        absolute_anchorangle = anchorangle.absolute
        relative_anchorangle = anchorangle.relative

        if (not old_anchorradius.absolute) and (self.last_absolute_anchorangle is not None):
            absolute_anchorangle = self.last_absolute_anchorangle
        if (not old_anchorradius.relative) and (self.last_relative_anchorangle is not None):
            relative_anchorangle = self.last_relative_anchorangle

        if value.absolute < 0:
            absolute_anchorangle = limit_angle(absolute_anchorangle + 180)
            self.absolute_anchor_radius_sign = -1
        elif value.absolute > 0:
            self.absolute_anchor_radius_sign = 1

        if value.relative < 0:
            relative_anchorangle = limit_angle(relative_anchorangle + 180)
            self.relative_anchor_radius_sign = -1
        elif value.relative > 0:
            self.relative_anchor_radius_sign = 1

        DualAngle.set_anchor_from_anchorangle_and_anchorradius(
            self,
            absolute_anchorangle,
            relative_anchorangle,
            value.absolute,
            value.relative,
        )

    @property
    def xysize(self) -> tuple[Position | None, Position | None]:
        return self.xsize, self.ysize

    @xysize.setter
    def xysize(self, value: tuple[Position | None, Position | None]):
        self.xsize, self.ysize = value

    @property
    def _reset(self) -> bool:
        return False

    @_reset.setter
    def _reset(self, value: bool):
        if value:
            self.take_state(TransformState())

    # Deprecated properties.
    if not TYPE_CHECKING:

        @property
        def alignaround(self) -> tuple[float, float]:
            return self.xaround, self.yaround

        @alignaround.setter
        def alignaround(self, value: tuple[float, float]):
            self.xanchor, self.yanchor = value
            self.xaround, self.yaround = value
            self.xanchoraround, self.yanchoraround = value

        @property
        def size(self) -> tuple[int, int] | None:
            if self.xsize is None or self.ysize is None:
                return None

            xsize = int(absolute.compute_raw(self.xsize, self.available_width))
            ysize = int(absolute.compute_raw(self.ysize, self.available_height))
            return xsize, ysize

        @size.setter
        def size(self, value: tuple[int | float, int | float] | None):
            if value is None:
                self.xsize = self.ysize = None
            else:
                self.xsize = int(value[0])
                self.ysize = int(value[1])


class Transform(Container, TransformProperties if TYPE_CHECKING else object):
    """
    Documented in sphinx, because we can't scan this object.
    """

    __version__ = 5
    transform_event_responder = True

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
            self.style_arg = "transform"

        if version < 5:
            self.replaced_request = False
            self.replaced_response = True

    DEFAULT_ARGUMENTS: dict[str, dict[str, Any]] = {
        "selected_activate": {},
        "selected_hover": {},
        "selected_idle": {},
        "selected_insensitive": {},
        "activate": {},
        "hover": {},
        "idle": {},
        "insensitive": {},
        "": {},
    }

    children: list[Displayable] = []
    child: Displayable | None = None
    original_child: Displayable | None = None

    active = False
    "True if the transform was updated at least once."

    arguments: dict[str, dict[str, Any]] | None = DEFAULT_ARGUMENTS
    """
    A map from prefix to a dictionary of properties for that prefix, computed from
    the arguments that were passed to the transform constructor.
    Transform will update its state to the values of current active prefix on
    each redraw, but before using transform function, so any changes made from
    the outside will be overwritten.

    If no properties were given, this will be None.
    """

    child_size: tuple[float, float] = (0, 0)
    "Size of the child. This is set after the first render."

    render_size: tuple[float, float] = (0, 0)
    "Size of the render after apllying transform properties. This is set after the first render."

    type TransformFunction = Callable[["Transform", float, float], float | None]
    """
    A function that takes a current transform, show time, animation time, and
    returns the amount of seconds it should be redrawn in, or None to stop redrawing.
    """

    forward: renpy.display.matrix.Matrix | None = None
    reverse: renpy.display.matrix.Matrix | None = None

    hide_request: bool = False
    "True if the transform has been requested to be hidden."

    hide_response: bool = True
    "True if transform and its child is ready to be hidden."

    replaced_request: bool = False
    "True if the transform has been requested to be replaced."

    replaced_response: bool = True
    "True if transform and its is child ready to be replaced."

    st: float = 0
    at: float = 0
    st_offset: float = 0
    at_offset: float = 0

    child_st_base: float = 0
    """
    Offset of the child's show time. This is used to reset the child's show time
    when transform child is changed.
    """

    def __init__(
        self,
        child: DisplayableLike | None = None,
        function: TransformFunction | None = None,
        style: str = "default",
        focus: str | None = None,
        default: bool = False,
        _args: DisplayableArguments | None = None,
        *,
        reset: bool = False,
        **kwargs: Any,
    ):
        properties = {k: kwargs.pop(k) for k in style_properties if k in kwargs}

        if reset:
            kwargs.setdefault("_reset", True)

        self.kwargs: dict[str, Any] = kwargs
        self.style_arg = style

        super().__init__(style=style, focus=focus, default=default, _args=_args, **properties)

        self.function = function

        child = renpy.easy.displayable_or_none(child)
        if child is not None:
            self.add(child)

        self.original_child = child
        "The child that was passed to the constructor."

        self.state = TransformState()

        if kwargs:
            prefixes = Transform.DEFAULT_ARGUMENTS
            splited_kwargs = renpy.easy.split_properties(kwargs, *prefixes)

            self.arguments = {}
            known_properties = renpy.atl.PROPERTIES
            for prefix, dictionary in zip(prefixes, splited_kwargs):
                if not dictionary:
                    continue

                self.arguments[prefix] = {}
                for k, v in dictionary.items():
                    if k in known_properties:
                        self.arguments[prefix][k] = v
                    else:
                        raise Exception(f"Unknown transform property: {k}")

            # Apply the default values.
            for k, v in self.arguments.get("", {}).items():
                setattr(self.state, k, v)

        else:
            self.arguments = None

    def take_state(self, t: "Transform", /):
        """
        Takes the transformation state from transform `t` into current transform.

        That is, apllies all changed transform properties from t, as well as
        takes the child from `t` if current transform has no child.

        Note, that this will cancel any changed transform properties made on
        current transform.
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

    def take_execution_state(self, t: "Transform", /):
        """
        Takes the execution state from object t into this object.

        That is, takes the placement from t and child show time offset.

        This is overridden by renpy.atl.TransformBase.
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

    def __call__(
        self,
        child: DisplayableLike | None = None,
        take_state: bool = True,
        _args: DisplayableArguments | None = None,
    ) -> "Transform":
        """
        Creates a new transform with the same properties as this transform,
        with a duplicated child.

        `child`
            The child to use for the new transform. If None, the child of
            this transform is used.
        """

        child = self.child if child is None else child
        child = renpy.easy.displayable_or_none(child)
        if child is not None and child._duplicatable:
            child = child._duplicate(_args)

        rv = Transform(
            child=child,
            function=self.function,
            style=self.style_arg,
            _args=_args,
            **self.kwargs,
        )

        rv.take_state(self)
        return rv

    def copy(self) -> "Transform":
        """
        Makes a copy of this transform including execution state.
        """

        d = self()
        d.kwargs = {}
        # take_state already called in __call__
        d.take_execution_state(self)
        d.st = self.st
        d.at = self.at

        return d

    def visit(self) -> list[Displayable]:
        if self.child is None:
            return []
        else:
            return [self.child]

    # The default function chooses entries from self.arguments that match
    # the style prefix, and applies them to the state.
    def default_function(self, state: "Transform", st: float, at: float) -> None:
        if self.arguments is None:
            return None

        prefix = self.style.prefix.strip("_")
        prefixes = []

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

    def set_transform_event(self, event: str):
        if self.child is not None:
            self.child.set_transform_event(event)
            self.last_child_transform_event = event

        super().set_transform_event(event)

    def _change_transform_child(self, child) -> "Transform":
        rv = self.copy()

        if self.child is not None:
            rv.set_child(self.child._change_transform_child(child))

        return rv

    def _handles_event(self, event: str):
        if (event == "replaced") and (not self.active):
            return True

        if self.function is not None:
            return True

        if self.child and self.child._handles_event(event):
            return True

        return False

    def adjust_for_fps(self, st: float, at: float, /) -> tuple[float, float]:
        "Adjusts timebases for fps transform property."

        if self.state.fps is None:
            return st, at

        modulus = 1.0 / self.state.fps
        st += modulus / 2
        st -= st % modulus
        at += modulus / 2
        at -= at % modulus
        return st, at

    def _hide(self, st, at, kind) -> "Self | None":
        if kind == "cancel":
            if self.state.show_cancels_hide:
                return None
            else:
                return self

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

        if isinstance(self, ATLTransform) and isinstance(d, ATLTransform):
            d.atl_st_offset = self.st_offset if self.atl_st_offset is None else self.atl_st_offset

        if kind == "hide":
            d.hide_request = True
        elif kind == "replaced":
            d.replaced_request = True
        else:
            assert_never(kind)

        d.hide_response = True
        d.replaced_response = True

        fst, fat = self.adjust_for_fps(st, at)

        if d.function is not None:
            d.function(d, fst, fat)
        elif isinstance(d, ATLTransform):
            d.execute(d, fst, fat)

        new_child = d.child._hide(
            st - self.st_offset,
            at - self.at_offset,
            kind,
        )

        if new_child is not None:
            d.child = new_child
            d.hide_response = False
            d.replaced_response = False

        # if (not d.hide_response) or (not d.replaced_response):
        if d.hide_response and d.replaced_response:
            return None

        renpy.display.render.redraw(d, 0)
        return d  # type: ignore

    def set_child(self, child: DisplayableLike, duplicate: bool = True) -> None:
        """
        Change the child of this transform and rerender it immediately.
        """

        child = renpy.easy.displayable(child)

        if duplicate and child._duplicatable:
            child = child._duplicate(self._args)

            if not self._duplicatable:
                child._unique()

        self.child = child
        self.children = [child]

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

        fst, fat = self.adjust_for_fps(self.st, self.at)

        # If we have to, call the function that updates this transform.
        if self.arguments is not None:
            self.default_function(self, fst, fat)

        if self.function is not None:
            fr = self.function(self, fst, fat)

            # Order a redraw, if necessary.
            if fr is not None:
                renpy.display.render.redraw(self, fr)

        self.active = True

        if self.state.last_events != self.state.events:
            if self.state.events and renpy.game.interface is not None:
                renpy.game.interface.timeout(0)
            self.state.last_events = self.state.events

    def render(self, width: float, height: float, st: float, at: float) -> renpy.display.render.Render:
        # Prevent time from ticking backwards, as can happen if we replace a
        # transform but keep its state.
        if st + self.st_offset <= self.st:
            self.st_offset = self.st - st
        if at + self.at_offset <= self.at:
            self.at_offset = self.at - at

        self.st = st = st + self.st_offset
        self.at = at = at + self.at_offset

        self.state.available_width = width
        self.state.available_height = height

        # Update the state.
        self.update_state()

        return RenderTransform(self).render(width, height, st, at)

    def event(self, ev, x, y, st):
        if self.hide_request:
            return None

        if not self.state.events:
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

    def _unique(self):
        if self._duplicatable:
            if self.child is not None:
                self.child._unique()

            self._duplicatable = False

    def get_placement(self) -> Placement:
        if not self.active:
            self.update_state()

        if self.child is not None:
            (
                cxpos,
                cypos,
                cxanchor,
                cyanchor,
                cxoffset,
                cyoffset,
                csubpixel,
            ) = self.child.get_placement()

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

                xanchor = absolute.compute_raw(xanchor, cw)
                yanchor = absolute.compute_raw(yanchor, ch)

                if self.reverse is not None:
                    xanchor -= cw / 2.0
                    yanchor -= ch / 2.0

                    xanchor, yanchor = self.reverse.transform(xanchor, yanchor)

                    xanchor += rw / 2.0
                    yanchor += rh / 2.0

                xanchor = absolute(xanchor)
                yanchor = absolute(yanchor)

                rv = (xpos, ypos, xanchor, yanchor, xoffset, yoffset, subpixel)

        return rv

    def update(self):
        """
        This should be called when a transform property field is updated outside
        of the callback method, to ensure that the change takes effect.
        """

        renpy.display.render.invalidate(self)

    _duplicatable = True

    def _duplicate(self, args: DisplayableArguments) -> Self:
        if args and args.args:
            args.extraneous()

        if not self._duplicatable:
            return self

        rv = self(_args=args)
        rv.take_execution_state(self)

        return rv  # type: ignore

    def _in_current_store(self):
        if self.child is None:
            return self

        child = self.child._in_current_store()
        if child is self.child:
            return self

        # This forestalls any _duplicate attempts while building the transform.
        child._unique()

        rv = self(child=child)
        rv.take_execution_state(self)
        rv._unique()

        return rv

    def _repr_info(self):
        return repr(self.child)


class ATLTransform(renpy.atl.ATLTransformBase, Transform):
    raw_child: Displayable | None = None

    def __init__(
        self,
        atl: "renpy.atl.RawBlock",
        child: DisplayableLike | None = None,
        context: dict[str, Any] = {},
        parameters: "renpy.parameter.Signature | None" = None,
        **properties: Any,
    ):
        renpy.atl.ATLTransformBase.__init__(self, atl, context, parameters)
        Transform.__init__(self, child=child, **properties)

        self.raw_child = self.child

    def update_state(self):
        """
        This updates the state to that at self.st, self.at.
        """

        self.hide_response = True
        self.replaced_response = True

        fst, fat = self.adjust_for_fps(self.st, self.at)

        fr = self.execute(self, fst, fat)

        # Order a redraw, if necessary.
        if fr is not None:
            renpy.display.render.redraw(self, fr)

        self.active = True

        if self.state.last_events != self.state.events:
            if self.state.events and renpy.game.interface is not None:
                renpy.game.interface.timeout(0)
            self.state.last_events = self.state.events

    def _repr_info(self):
        return repr((self.child, self.atl.loc))


style_properties: set[str] = {"alt"}
"Names of style properties that should be sent to the parent."

all_properties: dict[str, Any] = {}
"Names of all non-alias transform properties, and its default values."

diff2_properties: set[str] = set()
"Names of transform properties that should be handled with diff2."

uniforms: set[str] = set()
"Names of transform properties that are uniforms."

gl_properties: set[str] = set()
"Names of transform properties that are GL properties."


# Register all transform properties from TransformProperties attributes.
class Proxy:
    """
    This class proxies a field from the transform to its state.
    """

    def __init__(self, name: str):
        self.name = name

    def __get__(self, instance: Transform | None, owner: Any) -> Any:
        if instance is None:
            return self

        rv = getattr(instance.state, self.name)
        if isinstance(rv, tuple):
            return tuple(i.simplify() if isinstance(i, position) else i for i in rv)
        elif isinstance(rv, position):
            return rv.simplify()
        else:
            return rv

    def __set__(self, instance: Transform, value: Any) -> None:
        return setattr(instance.state, self.name, value)


def _register_properties():
    for value in TransformProperties.__dict__.values():
        if not isinstance(value, TransformProperty):
            continue

        if value.name in all_properties:
            raise Exception(f"Transform property {value.name} is already defined.")

        # Aliases should be known by ATL and Transform class.
        setattr(Transform, value.name, Proxy(value.name))
        renpy.atl.PROPERTIES[value.name] = value.atl_type

        if value.kind == "alias":
            if not hasattr(TransformState, value.name):
                raise Exception(f"Transform property {value.name} is an alias, but TransformState does not define it.")

            continue

        setattr(TransformState, value.name, value.default)

        all_properties[value.name] = value.default
        if value.diff == 2:
            diff2_properties.add(value.name)

        if value.kind == "uniform":
            uniforms.add(value.name)
        elif value.kind == "gl":
            gl_properties.add(value.name)


_register_properties()
del _register_properties


class TextureUniform:
    """
    Descriptor for a sampler2D uniform.
    """

    def __init__(self, name: str):
        self.name = name

    def __get__(self, instance: "TransformState", owner) -> Displayable | None:
        return instance.__dict__.get(self.name, None)

    def __set__(self, instance: "TransformState", value: DisplayableLike):
        value = renpy.easy.displayable(value)

        value = renpy.display.im.unoptimized_texture(value)

        if instance.texture_uniforms is None:
            instance.texture_uniforms = set()

        instance.texture_uniforms.add(self.name)

        instance.__dict__[self.name] = value


def add_uniform(name: str, uniform_type: str):
    """
    Adds a uniform with `name` to Transform and ATL.

    This is called from places that define GLSL uniforms, e.g. register_shader.
    """

    if not name.startswith("u_"):
        return

    if name in renpy.gl2.gl2draw.standard_uniforms:
        return

    if name in all_properties:
        return

    setattr(TransformProperties, name, TransformProperty(name, kind="uniform"))

    if uniform_type == "sampler2D":
        setattr(TransformState, name, TextureUniform(name))
    else:
        setattr(TransformState, name, None)

    setattr(Transform, name, Proxy(name))
    renpy.atl.PROPERTIES[name] = any_object

    all_properties[name] = None
    diff2_properties.add(name)
    uniforms.add(name)
