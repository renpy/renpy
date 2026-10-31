# Copyright 2004-2026 Tom Rothamel <pytom@bishoujo.us>
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

import random
from collections.abc import Callable
from typing import Any

import renpy
from renpy.parameter import Signature, ValuedParameter
from renpy.pyanalysis import GLOBAL_CONST, NOT_CONST, Analysis
from renpy.types import Position


def late_imports():
    global Displayable, Matrix, Camera, position

    from renpy.display.position import position
    from renpy.display.displayable import Displayable
    from renpy.display.matrix import Matrix
    from renpy.display.transform import Camera


def compiling(loc):
    file, number = loc

    renpy.game.exception_info = "Compiling ATL code at %s:%d" % (file, number)


def executing(loc):
    file, number = loc

    renpy.game.exception_info = "Executing ATL code at %s:%d" % (file, number)


# A map from the name of a time warp function to the function itself.
warpers = {}


def atl_warper(f):
    name = f.__name__
    warpers[name] = f
    return f


# The pause warper is used internally when no other warper is
# specified.


@atl_warper
def pause(t):
    if t < 1.0:
        return 0.0
    else:
        return 1.0


@atl_warper
def instant(t):
    return 1.0


class DualAngle(object):
    def __init__(self, absolute, relative):  # for tests, convert to PY2 after
        self.absolute = absolute
        self.relative = relative

    @classmethod
    def from_any(cls, other):
        if isinstance(other, cls):
            return other
        elif type(other) is float:
            return cls(other, other)
        raise TypeError("Cannot convert {} to DualAngle".format(type(other)))

    def __add__(self, other):
        if isinstance(other, DualAngle):
            return DualAngle(self.absolute + other.absolute, self.relative + other.relative)
        return NotImplemented

    def __sub__(self, other):
        return self + -other

    def __mul__(self, other):
        if isinstance(other, (int, float)):
            return DualAngle(self.absolute * other, self.relative * other)
        return NotImplemented

    __rmul__ = __mul__

    def __neg__(self):
        return -1 * self


def position_or_none(x):
    if x is None:
        return None
    return position.from_any(x)


def any_object(x):
    return x


def bool_or_none(x):
    if x is None:
        return x
    return bool(x)


def float_or_none(x):
    if x is None:
        return x
    return float(x)


def matrix(x):
    if x is None:
        return None
    elif callable(x):
        return x
    else:
        return renpy.display.matrix.Matrix(x)


def mesh(x):
    if isinstance(x, (renpy.gl2.gl2mesh2.Mesh2, renpy.gl2.gl2mesh3.Mesh3, tuple)):
        return x

    return bool(x)


def orientation(x: Any) -> Any:
    # This exists so Linear can special-case orientation interpolation.
    return x


# A dictionary giving property names and the corresponding type or
# function. This is massively added to by renpy.display.transform.
PROPERTIES = {}


class Interpolator[T](renpy.object.Object):
    _function: Callable[[float], T] | None = None
    nosave = ["_function"]

    def _build(self) -> Callable[[float], T]:
        raise NotImplementedError

    def build(self) -> Callable[[float], T]:
        """
        Return a callable that takes a float completeness of the interpolation
        and returns the interpolated value of this interpolator.
        """

        if self._function is None:
            self._function = self._build()

        return self._function

    def __call__(self, t: float) -> T:
        return self.build()(t)


class Linear[T](Interpolator[T]):
    def __init__(
        self,
        a: Any,
        b: Any,
        typ: type[Any] | tuple[type[Any], ...] | Callable[[Any], Any],
    ):
        self.a = a
        self.b = b
        self.typ = typ
        self.component: int | None = None
        "If not None, the index in the tuple component of a and b that this spline represents."

    def _build(self) -> Callable[[float], T]:
        a = self.a
        b = self.b
        typ = self.typ
        component = self.component

        if typ is orientation:

            def execute(t: float) -> Any:
                if a is None:
                    start = (0.0, 0.0, 0.0)
                else:
                    start = a

                if b is not None:
                    return renpy.display.quaternion.euler_slerp(t, start, b)
                elif t >= 1:
                    return None
                else:
                    return start

            return execute

        if component is not None:
            a = a[component]
            b = b[component]

        # Values that can't be interpolated: step at the end.
        if b is None or isinstance(b, (bool, str, Displayable, Matrix, Camera)):

            def execute(t: float) -> Any:
                if t >= 1.0:
                    return b
                else:
                    return a

            return execute

        # Tuples: one sub-Linear per component, built once.
        if component is None and isinstance(b, (tuple, list)):
            if not isinstance(a, (tuple, list)):
                a = [None] * len(b)

            subs: list[Linear[Any]] = []
            strict = renpy.config.developer
            if isinstance(typ, (tuple, list)):
                for i, ty in zip(range(len(b)), typ, strict=strict):
                    sub = Linear(a, b, ty)
                    sub.component = i
                    subs.append(sub)
            else:
                for i in range(len(b)):
                    sub = Linear(a, b, typ)
                    sub.component = i
                    subs.append(sub)

            def execute(t: float) -> Any:
                return tuple(s(t) for s in subs)

            return execute

        # Ren'Py's own matrix classes subclass _BaseMatrix.
        if hasattr(b, "value"):
            a_origin = getattr(a, "origin", None)

            # SplineMatrix: the amount is driven by a Spline, then the
            # wrapped matrix does the actual interpolation. Mirrors
            # SplineMatrix.__call__, including that no origin_value
            # is recorded (SplineMatrix has no .value).
            if isinstance(b, renpy.store.SplineMatrix):
                target_matrix = b.matrix

                if type(a_origin) is renpy.store.SplineMatrix:
                    a_origin = a_origin.matrix

                if type(a_origin) is not type(target_matrix):

                    def execute(t: float) -> Any:
                        rv = target_matrix(None, 1.0)
                        rv.origin = b
                        return rv

                    return execute

                spline: Spline[float] = Spline(b.spline[0], b.spline[1:], float)

                def execute(t: float) -> Any:
                    done = min(max(t, 0.0), 1.0)
                    done = spline(done)
                    rv = target_matrix(a_origin, done)
                    rv.origin = b
                    return rv

                return execute

            a_is_matrix = isinstance(a, renpy.display.matrix.Matrix)
            a_origin_value = getattr(a, "origin_value", None)

            # Pass a Matrix directly when `a` is a Matrix (from a previous
            # interpolation) and `b` is a _BaseMatrix.
            # This allows _BaseMatrix.__call__ to use `a.origin_value` so that
            # interpolation after an interruption (e.g. replaced by a new transform)
            # continues from where the old one was interrupted.
            if a_is_matrix and a_origin_value is not None:
                ov_base = a_origin_value
                ov_delta = b.value - a_origin_value
            elif a_origin is not None and hasattr(a_origin, "value"):
                ov_base = a_origin.value
                ov_delta = b.value - ov_base
            else:
                ov_base = None
                ov_delta = 0

            def execute(t: float) -> Any:
                if a_is_matrix:
                    rv = b(a, t)
                else:
                    rv = b(a_origin, t)

                rv.origin = b

                # Record the effective value on the result Matrix, so a
                # future interpolation can continue from here. When no
                # prior origin_value exists, the result is b.value.
                if ov_base is None:
                    rv.origin_value = b.value
                else:
                    rv.origin_value = ov_base + t * ov_delta

                return rv

            return execute

        # Arbitrary user callables.
        if callable(b):
            a_origin = getattr(a, "origin", None)

            def execute(t: float) -> Any:
                rv = b(a_origin, t)
                rv.origin = b  # type: ignore
                return rv

            return execute

        # Numbers and positions.
        if a is None:
            a = 0

        if typ in (position_or_none, position):
            if renpy.config.mixed_position:
                a = position.from_any(a)
                b = position.from_any(b)
                delta = b - a

                def execute(t: float) -> Any:
                    return a + t * delta

                return execute

            typ = type(b)

        delta = b - a

        def execute(t: float) -> Any:
            rv = a + t * delta
            return typ(rv)  # type: ignore

        return execute


def interpolate(t, a, b, typ):
    """
    Linearly interpolate the arguments.
    """

    return Linear(a, b, typ)(t)


class Spline[T](Interpolator[T]):
    def __init__(
        self,
        start: Any,
        spline: list[Any],
        typ: type[Any] | tuple[type[Any], ...],
        loop: bool = False,
    ):
        self.start = start
        self.spline = spline
        self.typ = typ
        self.loop = loop
        self.component = None
        "If not None, the index in the tuple component that this spline represents."

    def _build(self):
        spline = self.spline
        typ = self.typ
        loop = self.loop
        start = self.start
        component = self.component
        n = len(spline) + 1

        def point(i) -> Any:
            if i == 0:
                value = start
            else:
                value = spline[i - 1]

            if component is not None:
                value = value[component]

            if renpy.config.mixed_position and typ in (position_or_none, position):
                value = position(value)

            return value

        first = point(0)
        last = point(n - 1)

        # Recurse into tuple components without constructing component knot lists.
        if component is None and isinstance(last, tuple):
            subs: list[Spline[Any]] = []
            for i, ty in zip(range(len(last)), typ, strict=renpy.config.developer):  # type: ignore
                c_spline = Spline(start, spline, ty, loop)
                c_spline.component = i
                subs.append(c_spline)

            def execute(t: float) -> Any:
                return tuple(s(t) for s in subs)

            return execute

        # Constant.
        if first is None:
            def execute(t: float) -> Any:
                return last

            return execute

        cast = type(last)

        # Linear Bezier.
        if n == 2:
            p0 = first
            p1 = point(1)
            c1 = p1 - p0

            def execute(t: float) -> Any:
                if t == 1.0:
                    return cast(p1)
                return cast(p0 + t * c1)

            return execute

        # Quadratic Bezier, in monomial form.
        if n == 3:
            p0 = first
            p1 = point(1)
            p2 = point(2)
            c1 = 2.0 * (p1 - p0)
            c2 = p0 - 2.0 * p1 + p2

            def execute(t: float) -> Any:
                if t == 1.0:
                    return cast(p2)
                return cast(t * (t * c2 + c1) + p0)

            return execute

        # Cubic Bezier, in monomial form.
        if n == 4:
            p0 = first
            p1 = point(1)
            p2 = point(2)
            p3 = point(3)
            c1 = 3.0 * (p1 - p0)
            c2 = 3.0 * (p0 - 2.0 * p1 + p2)
            c3 = 3.0 * p1 - p0 - 3.0 * p2 + p3

            def execute(t: float) -> Any:
                if t == 1.0:
                    return cast(p3)
                return cast(t * (t * (t * c3 + c2) + c1) + p0)

            return execute

        # Catmull-Rom: precompute per-segment monomial coefficients.
        def adjusted(j) -> Any:
            if j == 0:
                return point(1)
            if j == 1:
                return first
            if j == n - 2:
                return last
            if j == n - 1:
                return point(n - 2)
            return point(j)

        loop = loop and n >= 5

        segments = []

        for i in range(n - 1 if loop else n - 3):
            if loop:
                p_1 = point(n - 2 if i == 0 else i - 1)
                p0 = point(i)
                p1 = point(i + 1)
                p2 = point(1 if i == n - 2 else i + 2)
            else:
                p_1 = adjusted(i)
                p0 = adjusted(i + 1)
                p1 = adjusted(i + 2)
                p2 = adjusted(i + 3)

            segments.append((
                0.5 * (3.0 * p0 - p_1 - 3.0 * p1 + p2),
                0.5 * (2.0 * p_1 - 5.0 * p0 + 4.0 * p1 - p2),
                0.5 * (p1 - p_1),
                p0,
            ))

        count = float(len(segments))
        last_sector = len(segments) - 1

        def execute(t: float) -> Any:
            if t <= 0.0:
                return cast(first)
            if t >= 1.0:
                return cast(last)

            scaled = t * count
            sector = min(int(scaled), last_sector)
            tl = scaled - sector

            c3, c2, c1, c0 = segments[sector]
            return cast(tl * (tl * (tl * c3 + c2) + c1) + c0)

        return execute


def interpolate_spline(t, spline, typ):
    return Spline(spline[0], spline[1:], typ)(t)


# A list of atl transforms that may need to be compiled.
compile_queue = []


def compile_all():
    """
    Called after the init phase is finished and transforms are compiled,
    to compile all constant transforms.
    """

    global compile_queue

    for i in compile_queue:
        if i.atl.constant == GLOBAL_CONST:
            i.compile()

    compile_queue = []


# Used to indicate that a variable is not in the context.
NotInContext = renpy.object.Sentinel("NotInContext")


# This is the context used when compiling an ATL statement. It stores the
# scopes that are used to evaluate the various expressions in the statement,
# and has a method to do the evaluation and return a result.
class Context(object):
    def __init__(self, context):
        self.context = context

    def eval(self, expr):
        return renpy.python.py_eval(expr, locals=self.context)

    def __eq__(self, other):
        if not isinstance(other, Context):
            return False

        return self.context == other.context

    def __ne__(self, other):
        return not (self == other)

    def __repr__(self):
        return "Context({})".format(repr(self.context))


class ATLTransformBase(renpy.object.Object):
    """
    This is intended to be subclassed by ATLTransform. It takes care of
    managing ATL execution, which allows ATLTransform itself to not care
    much about the contents of this file.
    """

    __version__ = 1

    # Compatibility with older saves.
    parameters = renpy.ast.EMPTY_PARAMETERS
    parent_transform = None  # type: ATLTransformBase|None
    atl_st_offset = 0

    # The block, as first compiled for prediction.
    predict_block = None

    nosave = ["parent_transform"]

    def after_upgrade(self, version):
        if version < 1:
            # any value in the inner scope was treated as a valid keyword parameter
            # so, we turn any inner scope value into a keyword parameter
            rv_parameters = []
            for name, value in self.context.context.items():
                if name not in self.parameters.parameters:
                    rv_parameters.append(ValuedParameter(name, ValuedParameter.KEYWORD_ONLY, default=value))
            if rv_parameters:
                rv_parameters = list(self.parameters.parameters.values()) + rv_parameters
                rv_parameters.sort(key=lambda p: p.kind)
                self.parameters = Signature(rv_parameters)

    def __init__(self, atl, context, parameters):
        # The constructor will be called by atltransform.
        if parameters is None:
            parameters = ATLTransformBase.parameters
        else:
            context = context.copy()
            # Apply the default parameters.
            parameters.apply_defaults(context, scope=context)

        # The parameters that we take.
        self.parameters = parameters

        # The raw code that makes up this ATL statement.
        self.atl = atl

        # The context in which execution occurs.
        self.context = Context(context)

        # The code after it has been compiled into a block.
        self.block = None

        # The same thing, but only if the code was compiled into a block
        # for prediction purposes only.
        self.predict_block = None

        # The properties of the block, if it contains only an
        # Interpolation.
        self.properties = None

        # The state of the statement we are executing. As this can be
        # shared between more than one object (in the case of a hide),
        # the data must not be altered.
        self.atl_state = None

        # Are we done?
        self.done = False

        # The transform event we are going to process.
        self.transform_event = None

        # The transform event we last processed.
        self.last_transform_event = None

        # The child transform event we last processed.
        self.last_child_transform_event = None

        # The child, without any transformations.
        self.raw_child = None

        # The parent transform that was called to create this transform.
        self.parent_transform = None

        # The offset between st and when this ATL block first executed.
        if renpy.config.atl_start_on_show:
            self.atl_st_offset = None
        else:
            self.atl_st_offset = 0

        if renpy.game.context().init_phase:
            compile_queue.append(self)

    @property
    def transition(self):
        """
        Returns true if this is likely to be an ATL transition.
        """

        return "new_widget" in self.context.context

    def _handles_event(self, event):
        if (event == "replaced") and (self.atl_state is None):
            return True

        if (self.block is not None) and (self.block._handles_event(event)):
            return True

        if self.child is None:
            return False

        return self.child._handles_event(event)

    def get_block(self):
        """
        Returns the compiled block to use.
        """

        if self.block:
            return self.block
        elif self.predict_block and renpy.display.predict.predicting:
            return self.predict_block
        else:
            return None

    def take_execution_state(self, t):
        """
        Updates self to begin executing from the same point as t. This
        requires that t.atl is self.atl.
        """

        super(ATLTransformBase, self).take_execution_state(t)  # type: ignore

        if self is t:
            return

        self.atl_st_offset = None
        self.atl_state = None

        if not isinstance(t, ATLTransformBase):
            return
        elif t.atl is not self.atl:
            return

        # Only take the execution state if the contexts haven't changed in
        # a way that would affect the execution of the ATL.

        if t.atl.constant != GLOBAL_CONST:
            block = self.get_block()
            if block is None:
                block = self.compile()

            if not deep_compare(self.block, t.block):
                return

        self.done = t.done
        self.block = t.block
        self.atl_state = t.atl_state
        self.transform_event = t.transform_event
        self.last_transform_event = t.last_transform_event
        self.last_child_transform_event = t.last_child_transform_event

        self.st = t.st
        self.at = t.at
        self.st_offset = t.st_offset
        self.at_offset = t.at_offset
        self.atl_st_offset = t.atl_st_offset

        if self.child is renpy.display.motion.null:
            if t.child and t.child._duplicatable:
                self.child = t.child._duplicate(None)

                if not self._duplicatable:
                    self.child._unique()
            else:
                self.child = t.child

            self.children = [self.child] if self.child is not None else []
            self.raw_child = t.raw_child

            if self.child is t.child:
                self.atl_child = t.atl_child

    def __call__(self, *args, **kwargs):
        _args = kwargs.pop("_args", None)

        scope = self.context.context.copy()
        signature = self.parameters
        child = None

        if renpy.config.atl_pos_only_as_pos_or_kw:
            signature = signature.with_pos_only_as_pos_or_kw()

        present_kinds = {p.kind for p in signature.parameters.values()}

        child_param = signature.parameters.get("child", None)
        old_widget_param = signature.parameters.get("old_widget", None)
        # args_param_name = None
        # if ValuedParameter.VAR_POSITIONAL in present_kinds:
        #     for param in signature.parameters.values():
        #         if param.kind == ValuedParameter.VAR_POSITIONAL:
        #             args_param_name = param.name
        #             break
        # kwargs_param_name = None
        # if ValuedParameter.VAR_KEYWORD in present_kinds:
        #     for param in signature.parameters.values():
        #         if param.kind == ValuedParameter.VAR_KEYWORD:
        #             kwargs_param_name = param.name
        #             break

        ## if a single arg is passed and no positional parameter is there to catch it, set it to be the child
        if args and (present_kinds <= {ValuedParameter.KEYWORD_ONLY, ValuedParameter.VAR_KEYWORD}):
            try:
                (child,) = args
            except Exception:
                raise Exception("Too many arguments passed to ATL transform.")
            args = ()

        if (child_param is None) or (
            child_param.kind not in {ValuedParameter.POSITIONAL_OR_KEYWORD, ValuedParameter.KEYWORD_ONLY}
        ):
            # if kwargs_param_name is None:
            child = kwargs.pop("child", child)
        else:
            child = kwargs.get("child", child)
        if (old_widget_param is not None) and (
            old_widget_param.kind in {ValuedParameter.POSITIONAL_OR_KEYWORD, ValuedParameter.KEYWORD_ONLY}
        ):
            # if getattr(signature.parameters.get("new_widget", None), "kind", None) in {ValuedParameter.POSITIONAL_OR_KEYWORD, ValuedParameter.KEYWORD_ONLY}: # Gamma-ter
            child = kwargs.get("old_widget", child)

        new_scope = signature.apply(args, kwargs, partial=True, apply_defaults=False)

        ## when *args and **kwargs are enabled
        # if args_param_name:
        #     var_args = new_scope.pop(args_param_name, ())
        #     if args_param_name in scope:
        #         scope[args_param_name] += var_args
        #     else:
        #         scope[args_param_name] = var_args
        # if kwargs_param_name:
        #     var_kwargs = new_scope.pop(kwargs_param_name, {})
        #     if kwargs_param_name in scope:
        #         scope[kwargs_param_name].update(var_kwargs)
        #     else:
        #         scope[kwargs_param_name] = var_kwargs

        scope.update(new_scope)

        if child is None:
            ## if a child parameter gets a value by a positional argument
            if child_param and (
                child_param.kind in {ValuedParameter.POSITIONAL_ONLY, ValuedParameter.POSITIONAL_OR_KEYWORD}
            ):
                child = new_scope.get("child", child)

        rv_parameters = []
        for name, param in signature.parameters.items():
            passed = name in new_scope
            pkind = param.kind

            ## when *args and **kwargs are enabled
            # if name in (args_param_name, kwargs_param_name):
            #     pass

            ## when positional-only parameters are enabled
            # elif passed and (pkind == param.POSITIONAL_ONLY):
            #     continue

            if passed:  # turn into elif when possible
                param = ValuedParameter(name, param.KEYWORD_ONLY, default=scope[name])

            elif param.has_default:
                param = ValuedParameter(name, pkind, default=scope[name])

            else:
                ## not passed and no default value
                pass

            rv_parameters.append(param)

        rv_parameters.sort(key=lambda p: p.kind)

        if child is None:
            child = self.child

        if getattr(child, "_duplicatable", False):
            child = child._duplicate(_args)

        rv = renpy.display.motion.ATLTransform(
            atl=self.atl,
            child=child,
            style=self.style_arg,  # type: ignore
            context=scope,
            parameters=Signature(rv_parameters),
            _args=_args,
        )

        rv.parent_transform = self
        rv.take_state(self)

        return rv

    def compile(self):
        """
        Compiles the ATL code into a block. As necessary, updates the
        properties.
        """

        constant = self.atl.constant == GLOBAL_CONST

        if not constant:
            missing = set(self.parameters.parameters) - set(self.context.context)
            if missing:
                last = missing.pop()
                raise Exception(
                    "Cannot compile ATL Transform at {}:{}, as it's missing parameters {}.".format(
                        self.atl.loc[0],
                        self.atl.loc[1],
                        "{} and {!r}".format(", ".join(map(repr, missing)), last) if missing else repr(last),
                    )
                )

        if constant and self.parent_transform:
            if self.parent_transform.block:
                self.block = self.parent_transform.block
                self.properties = self.parent_transform.properties
                self.parent_transform = None
                return self.block

        old_exception_info = renpy.game.exception_info

        if constant and self.atl.compiled_block is not None:
            block = self.atl.compiled_block
        else:
            block = self.atl.compile(self.context)

        if all(isinstance(statement, Interpolation) and statement.duration == 0 for statement in block.statements):
            self.properties = []
            for interp in block.statements:
                self.properties.extend(interp.properties)

        if not constant and renpy.display.predict.predicting:
            self.predict_block = block
        else:
            self.block = block
            self.predict_block = None

        renpy.game.exception_info = old_exception_info

        if constant and self.parent_transform:
            self.parent_transform.block = self.block
            self.parent_transform.properties = self.properties
            self.parent_transform = None

        return block

    def change_block_child(self, old, new):
        """
        Changes the compiled block of this transform so that child statements
        showing one of the displayables in `old` show `new` instead. The
        execution state is updated to match, so the ATL keeps running from
        where it was. Does nothing if the block has not been compiled yet, or
        if the ATL has no statement that could be a child statement.
        """

        if self.block is None:
            return

        if not self.atl.has_child:
            return

        self.block, self.atl_state = self.block.change_child(old, new, self.atl_state)

    def execute(self, trans, st, at):
        if self.done:
            return None

        block = self.get_block()
        if block is None:
            block = self.compile()

        events = []

        # Hide request.
        if trans.hide_request:
            self.transform_event = "hide"

        if trans.replaced_request:
            self.transform_event = "replaced"

        # Notice transform events.
        if renpy.config.atl_multiple_events:
            if self.transform_event != self.last_transform_event:
                events.append(self.transform_event)
                self.last_transform_event = self.transform_event

        # Propagate transform_events from children.
        if (self.child is not None) and self.child.transform_event != self.last_child_transform_event:
            self.last_child_transform_event = self.child.transform_event

            if self.child.transform_event is not None:
                self.transform_event = self.child.transform_event

        # Notice transform events, again.
        if self.transform_event != self.last_transform_event:
            events.append(self.transform_event)
            self.last_transform_event = self.transform_event

        if self.transform_event in renpy.config.repeat_transform_events:
            self.transform_event = None
            self.last_transform_event = None

        old_exception_info = renpy.game.exception_info

        if (self.atl_st_offset is None) or (st - self.atl_st_offset) < 0:
            self.atl_st_offset = st

        if self.atl.animation or self.transition:
            timebase = at
        else:
            timebase = st - self.atl_st_offset

        action, arg, pause = block.execute(trans, timebase, self.atl_state, events)

        renpy.game.exception_info = old_exception_info

        if action == "continue" and not renpy.display.predict.predicting:
            self.atl_state = arg
        else:
            self.done = True

        return pause

    def predict_one(self):
        self.atl.predict(self.context)

    def visit(self):
        block = self.get_block()

        if block is None:
            block = self.compile()

        return self.children + block.visit()  # type: ignore


# The base class for raw ATL statements.


class RawStatement(object):
    constant = None

    has_child = True
    """
    True if this statement, or a statement it contains, may compile into a
    Child statement. Set by mark_constant. Defaults to True, so statements that
    were never analyzed, or were loaded from an older .rpyc, are not skipped.
    """

    def __init__(self, loc):
        super(RawStatement, self).__init__()
        self.loc = loc

    # Compiles this RawStatement into a Statement, by using ctx to
    # evaluate expressions as necessary.
    def compile(self, ctx):
        raise Exception("Compile not implemented.")

    # Predicts the images used by this statement.
    def predict(self, ctx):
        return

    # RawBlock also has an analysis method which creates an Analysis
    # object, applies passed parameters and calls mark_constant

    def mark_constant(self, analysis):
        """
        Sets self.constant to GLOBAL_CONST if all expressions used in
        this statement and its children are constant.
        `analysis`
            A pyanalysis.Analysis object containing the analysis of this ATL.
        """

        self.constant = NOT_CONST


# The base class for compiled ATL Statements.


class Statement(renpy.object.Object):
    def __init__(self, loc):
        super(Statement, self).__init__()
        self.loc = loc

    # trans is the transform we're working on.
    # st is the time since this statement started executing.
    # state is the state stored by this statement, or None if
    # we've just started executing this statement.
    # event is an event we're triggering.
    #
    # "continue", state, pause - Causes this statement to execute
    # again, with the given state passed in the second time around.
    #
    #
    # "next", timeleft, pause - Causes the next statement to execute,
    # with timeleft being the amount of time left after this statement
    # finished.
    #
    # "event", (name, timeleft), pause - Causes an event to be reported,
    # and control to head up to the event handler.
    #
    # "repeat", (count, timeleft), pause - Causes the repeat behavior
    # to occur.
    #
    # As the Repeat statement can only appear in a block, only Block
    # needs to deal with the repeat behavior.
    #
    # Pause is the amount of time until execute should be called again,
    # or None if there's no need to call execute ever again.
    def execute(self, trans, st, state, events):
        raise Exception("Not implemented.")

    # Return a list of displayable children.
    def visit(self):
        return []

    def in_current_store(self):
        return self

    def change_child(self, old, new, state):
        """
        Replaces the displayable shown by child statements in this statement.

        `old`
            A list of displayables. A child statement showing one of these
            (compared by identity) is replaced with one showing `new`.

        `state`
            The execution state of this statement, or None.

        Returns a (statement, state) tuple. The statement is self if nothing
        was replaced, and otherwise a copy, so compiled blocks that are shared
        are never changed. The state is rewritten to refer to any copied
        blocks it contains.
        """

        return self, state

    # Does this respond to an event?
    def _handles_event(self, event):
        return False


# This represents a Raw ATL block.


class RawBlock(RawStatement):
    # Should we use the animation timebase or the showing timebase?
    animation = False

    # If this block uses only constant values we can once compile it
    # and use this value for all ATLTransform that use us as an atl.
    compiled_block = None

    def __init__(self, loc, statements, animation):
        super(RawBlock, self).__init__(loc)

        # A list of RawStatements in this block.
        self.statements = statements

        self.animation = animation

    def compile(self, ctx):
        compiling(self.loc)

        statements = [i.compile(ctx) for i in self.statements]

        return Block(self.loc, statements)

    def predict(self, ctx):
        for i in self.statements:
            i.predict(ctx)

    def analyze(self, parameters=None):
        analysis = Analysis(None)

        # Apply the passed parameters to take into account
        # the names that are not constant in this context
        if parameters is not None:
            analysis.parameters(parameters)

        self.mark_constant(analysis)

        # We can only be a constant if we do not use values
        # from parameters or do not have them at all.
        # So we can pass an empty context for compilation.
        if self.constant == GLOBAL_CONST:
            self.compile_block()

    def compile_block(self):
        # This may failed if we use another transfrom
        # which use non constant value.
        # In this case we also non constant.
        old_exception_info = renpy.game.exception_info
        try:
            block = self.compile(Context({}))
        except RecursionError:
            raise Exception("This transform refers to itself in a cycle.")
        except Exception:
            self.constant = NOT_CONST
        else:
            self.compiled_block = block
        renpy.game.exception_info = old_exception_info

    def mark_constant(self, analysis):
        constant = GLOBAL_CONST
        has_child = False

        for i in self.statements:
            i.mark_constant(analysis)
            constant = min(constant, i.constant)
            has_child = has_child or i.has_child

        self.constant = constant
        self.has_child = has_child


# A compiled ATL block.
class Block(Statement):
    def __init__(self, loc, statements):
        super(Block, self).__init__(loc)

        # A list of statements in the block.
        self.statements = statements

        # The start times of various statements.
        self.times = []

        for i, s in enumerate(statements):
            if isinstance(s, Time):
                self.times.append((s.time, i + 1))

        self.times.sort()

    def in_current_store(self):
        statements = [i.in_current_store() for i in self.statements]
        return Block(self.loc, statements)

    def change_child(self, old, new, state):
        if state is not None:
            index, start, loop_start, repeats, times, child_state = state
        else:
            index = None
            child_state = None

        changed = False
        statements = []

        for i, stmt in enumerate(self.statements):
            if i == index:
                new_stmt, child_state = stmt.change_child(old, new, child_state)
            else:
                new_stmt, _ = stmt.change_child(old, new, None)

            changed = changed or (new_stmt is not stmt)
            statements.append(new_stmt)

        if not changed:
            return self, state

        if state is not None:
            state = (index, start, loop_start, repeats, times, child_state)  # type: ignore

        return Block(self.loc, statements), state

    def _handles_event(self, event):
        for i in self.statements:
            if i._handles_event(event):
                return True

        return False

    def execute(self, trans, st, state, events):
        executing(self.loc)

        # Unpack the state.
        if state is not None:
            index, start, loop_start, repeats, times, child_state = state
        else:
            index, start, loop_start, repeats, times, child_state = 0, 0, 0, 0, self.times[:], None

        # What we might be returning.
        action = "continue"
        arg = None
        pause = None

        while action == "continue":
            # Target is the time we're willing to execute to.
            # Max_pause is how long we'll wait before executing again.

            # If we have times queued up, then use them to inform target
            # and time.
            if times:
                time, tindex = times[0]
                target = min(time, st)
                max_pause = time - target

            # Otherwise, take the defaults.
            else:
                target = st
                max_pause = 15

            while True:
                # If we've hit the last statement, it's the end of
                # this block.
                if index >= len(self.statements):
                    return "next", target - start, None

                # Find the statement and try to run it.
                stmt = self.statements[index]
                action, arg, pause = stmt.execute(trans, target - start, child_state, events)

                # On continue, persist our state.
                if action == "continue":
                    if pause is None:
                        pause = max_pause

                    action, arg, pause = (
                        "continue",
                        (index, start, loop_start, repeats, times, arg),
                        min(max_pause, pause),
                    )
                    break

                elif action == "event":
                    return action, arg, pause

                # On next, advance to the next statement in the block.
                elif action == "next":
                    index += 1
                    start = target - arg
                    child_state = None

                # On repeat, either terminate the block, or go to
                # the first statement.
                elif action == "repeat":
                    count, arg = arg
                    loop_end = target - arg
                    duration = loop_end - loop_start

                    if (state is None) and (duration <= 0):
                        raise Exception("ATL appears to be in an infinite loop.")

                    # Figure how many durations can occur between the
                    # start of the loop and now.

                    if duration:
                        new_repeats = int((target - loop_start) / duration)
                    else:
                        new_repeats = 0

                    if count is not None:
                        if repeats + new_repeats >= count:
                            new_repeats = count - repeats
                            loop_start += new_repeats * duration
                            return "next", target - loop_start, None

                    repeats += new_repeats
                    loop_start = loop_start + new_repeats * duration
                    start = loop_start
                    index = 0
                    child_state = None

            if times:
                time, tindex = times[0]
                if time <= target:
                    times.pop(0)

                    index = tindex
                    start = time
                    child_state = None

                    continue

            return action, arg, pause

    def visit(self):
        return [j for i in self.statements for j in i.visit()]


# A list of properties
incompatible_props = {
    "alignaround": {"xaround", "yaround", "xanchoraround", "yanchoraround"},
    "align": {"xanchor", "yanchor", "xpos", "ypos"},
    "anchor": {"xanchor", "yanchor"},
    "angle": {"xpos", "ypos"},
    "anchorangle": {"xangle", "yangle"},
    "around": {"xaround", "yaround", "xanchoraround", "yanchoraround"},
    "offset": {"xoffset", "yoffset"},
    "pos": {"xpos", "ypos"},
    "radius": {"xpos", "ypos"},
    "anchorradius": {"xanchor", "yanchor"},
    "size": {"xsize", "ysize"},
    "xalign": {"xpos", "xanchor"},
    "xcenter": {"xpos", "xanchor"},
    "xycenter": {"xpos", "ypos", "xanchor", "yanchor"},
    "xysize": {"xsize", "ysize"},
    "yalign": {"ypos", "yanchor"},
    "ycenter": {"ypos", "yanchor"},
}

# A list of sets of pairs of properties that do not conflict.
compatible_pairs = [{"radius", "angle"}, {"anchorradius", "anchorangle"}]

# This can become one of four things:
#
# - A pause.
# - An interpolation (which optionally can also reference other
# blocks, as long as they're not time-dependent, and have the same
# arity as the interpolation).
# - A call to another block.
# - A command to change the image, perhaps with a transition.
#
# We won't decide which it is until runtime, as we need the
# values of the variables here.


def check_spline_types(value):
    if isinstance(value, (position, int, float)):
        return True

    if isinstance(value, tuple):
        return all(check_spline_types(i) for i in value)

    return False


class RawMultipurpose(RawStatement):
    warp_function = None
    loop_splines_indexes: list[int] = ()  # type: ignore

    def __init__(self, loc):
        super().__init__(loc)

        self.warper = None
        self.duration = None
        self.properties = []
        self.expressions = []
        self.splines: list[tuple[str, list[Any]]] = []
        self.loop_splines_indexes = []
        self.revolution = None
        self.circles = "0"

    def add_warper(self, name, duration, warp_function):
        self.warper = name
        self.duration = duration
        self.warp_function = warp_function

    def add_property(self, name, exprs):
        """
        Checks if the property is compatible with any previously included, and
        sets it.
        Either returns the previously-set property, if any, or None.
        """
        newly_set = incompatible_props.get(name, set()) | {name}

        for old, _e in self.properties:
            if newly_set.intersection(incompatible_props.get(old, (old,))):
                break
        else:
            old = None

        self.properties.append((name, exprs))

        if old is not None:
            pair = {old, name}

            for i in compatible_pairs:
                if pair == i:
                    old = None

        return old

    def add_expression(self, expr, with_clause):
        self.expressions.append((expr, with_clause))

    def add_revolution(self, revolution):
        self.revolution = revolution

    def add_circles(self, circles):
        self.circles = circles

    def add_spline(self, name: str, exprs: list[Any], loop: bool) -> None:
        if loop:
            self.loop_splines_indexes.append(len(self.splines))

        self.splines.append((name, exprs))

    def compile(self, ctx):
        compiling(self.loc)

        # Figure out what kind of statement we have. If there's no
        # interpolator, and no properties, than we have either a
        # call, or a child statement.
        if (
            self.warper is None
            and self.warp_function is None
            and not self.properties
            and not self.splines
            and len(self.expressions) == 1
        ):
            expr, withexpr = self.expressions[0]

            child = ctx.eval(expr)
            if withexpr:
                transition = ctx.eval(withexpr)
            else:
                transition = None

            if isinstance(child, (int, float)):
                return Interpolation(
                    self.loc,
                    "pause",
                    child,
                    [],
                    None,
                    0,
                    [],
                )

            child = renpy.easy.displayable(child)

            if isinstance(child, ATLTransformBase) and (child.child is None):
                child.compile()
                return child.get_block()
            else:
                return Child(self.loc, child, transition)

        compiling(self.loc)

        # Otherwise, we probably have an interpolation statement.

        if self.warp_function:
            warper = ctx.eval(self.warp_function)
        else:
            warper = self.warper or "instant"

            if warper not in warpers:
                raise Exception(f"ATL Warper {warper} is unknown at runtime.")

        properties = []

        for name, expr in self.properties:
            if name not in PROPERTIES:
                raise Exception(f"ATL Property {name} is unknown at runtime.")

            value = ctx.eval(expr)
            properties.append((name, value))

        splines: list[tuple[str, list[Any], bool]] = []

        for i, (name, exprs) in enumerate(self.splines):
            if name not in PROPERTIES:
                raise Exception(f"ATL Property {name} is unknown at runtime.")

            values = [ctx.eval(i) for i in exprs]

            if not all(check_spline_types(i) for i in values):
                err = Exception(f"Spline interpolation of property {name} requires position types.")
                if name in ("matrixtransform", "matrixcolor"):
                    err.add_note("You may want to use SplineMatrix.")
                raise err

            splines.append((name, values, i in self.loop_splines_indexes))

        for expr, _with in self.expressions:
            try:
                value = ctx.eval(expr)
            except Exception:
                raise Exception(f"Could not evaluate expression {expr!r} when compiling ATL.")

            if not isinstance(value, ATLTransformBase):
                raise Exception(
                    f"Expression {expr!r} is not an ATL transform, and so cannot be included in an ATL interpolation."
                )

            value.compile()

            if value.properties is None:
                raise Exception(f"ATL transform {expr!r} is too complicated to be included in interpolation.")

            properties.extend(value.properties)

        duration = ctx.eval(self.duration)
        circles = ctx.eval(self.circles)

        return Interpolation(
            self.loc,
            warper,
            duration,
            properties,
            self.revolution,
            circles,
            splines,
        )

    def mark_constant(self, analysis):
        constant = GLOBAL_CONST
        is_constant_expr = analysis.is_constant_expr

        constant = min(constant, is_constant_expr(self.warp_function))
        constant = min(constant, is_constant_expr(self.duration))
        constant = min(constant, is_constant_expr(self.circles))

        for _name, expr in self.properties:
            constant = min(constant, is_constant_expr(expr))

        for _name, exprs in self.splines:
            for expr in exprs:
                constant = min(constant, is_constant_expr(expr))

        for expr, withexpr in self.expressions:
            constant = min(constant, is_constant_expr(expr))
            constant = min(constant, is_constant_expr(withexpr))

        self.constant = constant

        # The same test compile uses to decide this is a child statement.
        self.has_child = (
            self.warper is None
            and self.warp_function is None
            and not self.properties
            and not self.splines
            and len(self.expressions) == 1
        )

    def predict(self, ctx):
        for i, _j in self.expressions:
            try:
                i = ctx.eval(i)
            except Exception:
                continue

            if isinstance(i, ATLTransformBase) and (i.child is None):
                i.atl.predict(ctx)
                return

            try:
                renpy.easy.predict(i)
            except Exception:
                continue

        for k, e in self.properties:
            if k[:2] == "u_":
                try:
                    d = ctx.eval(e)
                except Exception:
                    continue

                if isinstance(d, str):
                    d = renpy.easy.displayable(d)

                if not isinstance(d, Displayable):
                    continue

                try:
                    d = renpy.display.im.unoptimized_texture(d)
                    renpy.easy.predict(d)
                except Exception:
                    continue


# This lets us have an ATL transform as our child.
class RawContainsExpr(RawStatement):
    def __init__(self, loc, expr):
        super(RawContainsExpr, self).__init__(loc)

        self.expression = expr

    def compile(self, ctx):
        compiling(self.loc)
        child = ctx.eval(self.expression)
        return Child(self.loc, child, None)

    def mark_constant(self, analysis):
        self.constant = analysis.is_constant_expr(self.expression)
        self.has_child = True


# This allows us to have multiple ATL transforms as children.
class RawChild(RawStatement):
    def __init__(self, loc, child):
        super(RawChild, self).__init__(loc)

        self.children = [child]

    def compile(self, ctx):
        children = []

        for i in self.children:
            children.append(renpy.display.motion.ATLTransform(i, context=ctx.context))

        box = renpy.display.layout.MultiBox(layout="fixed")

        for i in children:
            box.add(i)

        return Child(self.loc, box, None)

    def mark_constant(self, analysis):
        constant = GLOBAL_CONST
        has_child = False

        for i in self.children:
            i.mark_constant(analysis)
            constant = min(constant, i.constant)
            has_child = has_child or i.has_child

        self.constant = constant
        self.has_child = has_child


# This changes the child of this statement, optionally with a transition.
class Child(Statement):
    def __init__(self, loc, child, transition):
        super(Child, self).__init__(loc)

        self.child = child
        self.transition = transition

    def execute(self, trans, st, state, events):
        executing(self.loc)

        # Transition from the child that's being shown. If an earlier child
        # statement's transition is still in progress, transition from that
        # statement's child rather than nesting the transitions.
        old_child = trans.atl_child if trans.atl_child is not None else trans.child

        child = self.child

        if child._duplicatable:
            child = self.child._duplicate(trans._args)
            child._unique()

        atl_child = child

        if (old_child is not None) and (old_child is not renpy.display.motion.null) and (self.transition is not None):
            child = self.transition(old_widget=old_child, new_widget=child)
            child._unique()

        trans.set_child(child, duplicate=False)
        trans.raw_child = self.child
        trans.atl_child = atl_child

        return "next", st, None

    def in_current_store(self):
        child = self.child._in_current_store()
        return Child(self.loc, child, self.transition)

    def change_child(self, old, new, state):
        if any(self.child is i for i in old):
            return Child(self.loc, new, self.transition), state

        return self, state

    def visit(self):
        return [self.child]


# This causes interpolation to occur.
class InterpolationState(renpy.object.Object):
    linear: dict[str, Linear[Any]]
    splines: dict[str, Spline[Any]]
    interpolator_functions: list[tuple[str, Callable[[float], Any]]]
    nosave = ["interpolator_functions"]

    def __init__(
        self,
        interpolation: "Interpolation",
        start_state: "renpy.display.motion.TransformState",
        change_state: bool,
    ):
        self.linear = {}
        self.splines = {}
        self.interpolator_functions = []

        new_state = renpy.display.motion.TransformState()
        new_state.take_state(start_state)

        has_angle = False
        has_radius = False
        has_anchorangle = False
        has_anchorradius = False

        for name, value in interpolation.properties:
            setattr(new_state, name, value)
            if name == "angle":
                has_angle = True
            elif name == "radius":
                has_radius = True
            elif name == "anchorangle":
                has_anchorangle = True
            elif name == "anchorradius":
                has_anchorradius = True

        # Now, the things we change linearly are in the difference
        # between the new and old states.
        changes = start_state.diff(new_state)
        for name, (start, end) in changes.items():
            self.linear[name] = Linear(start, end, PROPERTIES[name])

        revolution = interpolation.revolution
        circles = interpolation.circles

        if (
            revolution
            or ((has_angle or has_radius) and renpy.config.automatic_polar_motion)
            or has_anchorangle
            or has_anchorradius
        ):
            # Remove various irrelevant motions.
            for name in (
                "xpos",
                "ypos",
                "xanchor",
                "yanchor",
                "xaround",
                "yaround",
                "xanchoraround",
                "yanchoraround",
            ):
                self.linear.pop(name, None)

            if revolution is not None:
                start_angle = start_state.angle
                end_angle = new_state.angle
                start_anchorangle = start_state.anchorangle
                start_anchorangle_absolute = start_anchorangle.absolute
                start_anchorangle_relative = start_anchorangle.relative
                end_anchorangle = new_state.anchorangle
                end_anchorangle_absolute = end_anchorangle.absolute
                end_anchorangle_relative = end_anchorangle.relative

                # Make sure the angle is in the appropriate direction,
                # and contains an appropriate number of circles.

                if revolution == "clockwise":
                    if end_angle < start_angle:
                        start_angle -= 360
                    if end_anchorangle_absolute < start_anchorangle_absolute:
                        start_anchorangle_absolute -= 360
                    if end_anchorangle_relative < start_anchorangle_relative:
                        start_anchorangle_relative -= 360

                    start_angle -= circles * 360
                    start_anchorangle_absolute -= circles * 360
                    start_anchorangle_relative -= circles * 360

                elif revolution == "counterclockwise":
                    if end_angle > start_angle:
                        start_angle += 360
                    if end_anchorangle_absolute > start_anchorangle_absolute:
                        start_anchorangle_absolute += 360
                    if end_anchorangle_relative > start_anchorangle_relative:
                        start_anchorangle_relative += 360

                    start_angle += circles * 360
                    start_anchorangle_absolute += circles * 360
                    start_anchorangle_relative += circles * 360

                # Angle and radius need to go after the linear changes, as
                # around or alignaround must be set first.
                self.linear.pop("angle", None)
                self.linear["angle"] = Linear(start_angle, end_angle, float)
                self.linear.pop("radius", None)
                self.linear["radius"] = Linear(start_state.radius, new_state.radius, position_or_none)
                self.linear.pop("anchorangle", None)
                self.linear["anchorangle"] = Linear(
                    DualAngle(start_anchorangle_absolute, start_anchorangle_relative),
                    DualAngle(end_anchorangle_absolute, end_anchorangle_relative),
                    DualAngle.from_any,
                )
                self.linear.pop("anchorradius", None)
                self.linear["anchorradius"] = Linear(
                    start_state.anchorradius,
                    new_state.anchorradius,
                    position_or_none,
                )

            else:
                if has_angle:
                    start = start_state.angle
                    end = new_state.last_angle
                    if end - start > 180:
                        start += 360
                    if end - start < -180:
                        start -= 360
                    self.linear.pop("angle", None)
                    self.linear["angle"] = Linear(start, end, float)

                if has_radius:
                    self.linear.pop("radius", None)
                    self.linear["radius"] = Linear(start_state.radius, new_state.radius, position_or_none)

                if has_anchorangle:
                    start = start_state.anchorangle
                    start_absolute = start.absolute
                    start_relative = start.relative
                    end_absolute = new_state.last_absolute_anchorangle
                    end_relative = new_state.last_relative_anchorangle

                    if end_absolute - start_absolute > 180:
                        start_absolute += 360
                    if end_absolute - start_absolute < -180:
                        start_absolute -= 360
                    if end_relative - start_relative > 180:
                        start_relative += 360
                    if end_relative - start_relative < -180:
                        start_relative -= 360

                    self.linear.pop("anchorangle", None)
                    self.linear["anchorangle"] = Linear(
                        DualAngle(start_absolute, start_relative),
                        DualAngle(end_absolute, end_relative),
                        DualAngle.from_any,
                    )

                if has_anchorradius:
                    self.linear.pop("anchorradius", None)
                    self.linear["anchorradius"] = Linear(
                        start_state.anchorradius,
                        new_state.anchorradius,
                        position_or_none,
                    )

        for name, values, loop in interpolation.splines:
            self.splines[name] = Spline(start_state.get(name), values, PROPERTIES[name], loop)

        if change_state:
            if revolution is not None:
                # Ensure we rotate around the new point.
                start_state.xaround = new_state.xaround or 0.0
                start_state.yaround = new_state.yaround or 0.0
                start_state.xanchoraround = new_state.xanchoraround
                start_state.yanchoraround = new_state.yanchoraround

            # Ensure that we set things, even if they don't actually
            # change from the old state.
            for name, value in interpolation.properties:
                if name not in self.linear:
                    setattr(start_state, name, value)

        self._fill_executors()

    def after_setstate(self):
        self.interpolator_functions = []
        self._fill_executors()

    def _fill_executors(self):
        for name, interpolator in self.linear.items():
            self.interpolator_functions.append((name, interpolator.build()))

        for name, interpolator in self.splines.items():
            self.interpolator_functions.append((name, interpolator.build()))


class Interpolation(Statement):
    __version__ = 1

    def __init__(
        self,
        loc,
        warper,
        duration,
        properties,
        revolution,
        circles,
        splines: list[tuple[str, list[Any], bool]],
    ):
        super().__init__(loc)

        self.warper = warper
        self.duration = duration
        self.properties = properties
        self.splines: list[tuple[str, list[Any], bool]] = splines

        # The direction we revolve in: cw, ccw, or None.
        self.revolution = revolution

        # The number of complete circles we make.
        self.circles = circles

    def after_upgrade(self, version):
        if version < 1:
            splines: list = self.splines
            self.splines = [(name, values, False) for name, values in splines]

    def execute(self, trans, st, state, events):
        executing(self.loc)

        warper = warpers.get(self.warper, self.warper)

        # Special case `pause 0` to always display a frame. This is intended to
        # support single-frame animations that shouldn't skip.
        if state is None and self.warper == "pause" and self.duration == 0 and renpy.config.atl_one_frame:
            force_frame = True
        else:
            force_frame = False

        if self.duration:
            complete = min(1.0, st / self.duration)
        else:
            complete = 1.0

        if complete < 0.0:
            complete = 0.0
        elif complete > 1.0:
            complete = 1.0

        complete = warper(complete)

        if not isinstance(state, InterpolationState):
            state = InterpolationState(self, trans.state, state is None)

        for name, func in state.interpolator_functions:
            setattr(trans.state, name, func(complete))

        if (st >= self.duration) and (not force_frame):
            return "next", st - self.duration, None
        else:
            if not self.properties and not self.revolution and not self.splines:
                return "continue", state, max(0, self.duration - st)
            else:
                return "continue", state, 0


# Implementation of the repeat statement.
class RawRepeat(RawStatement):
    def __init__(self, loc, repeats):
        super(RawRepeat, self).__init__(loc)

        self.repeats = repeats

    def compile(self, ctx):
        compiling(self.loc)

        repeats = self.repeats

        if repeats is not None:
            repeats = ctx.eval(repeats)

        return Repeat(self.loc, repeats)

    def mark_constant(self, analysis):
        self.constant = analysis.is_constant_expr(self.repeats)
        self.has_child = False


class Repeat(Statement):
    def __init__(self, loc, repeats):
        super(Repeat, self).__init__(loc)

        self.repeats = repeats

    def execute(self, trans, st, state, events):
        return "repeat", (self.repeats, st), 0


# Parallel statement.


class RawParallel(RawStatement):
    def __init__(self, loc, block):
        super(RawParallel, self).__init__(loc)
        self.blocks = [block]

    def compile(self, ctx):
        return Parallel(self.loc, [i.compile(ctx) for i in self.blocks])

    def predict(self, ctx):
        for i in self.blocks:
            i.predict(ctx)

    def mark_constant(self, analysis):
        constant = GLOBAL_CONST
        has_child = False

        for i in self.blocks:
            i.mark_constant(analysis)
            constant = min(constant, i.constant)
            has_child = has_child or i.has_child

        self.constant = constant
        self.has_child = has_child


class Parallel(Statement):
    def __init__(self, loc, blocks):
        super(Parallel, self).__init__(loc)
        self.blocks = blocks

    def in_current_store(self):
        blocks = [i.in_current_store() for i in self.blocks]
        return Parallel(self.loc, blocks)

    def change_child(self, old, new, state):
        # Maps the id of each block that is still running to its state.
        states = {id(i): istate for i, istate in state} if state is not None else {}

        # Maps the id of each block to its replacement and the replacement's state.
        replacements = {id(i): i.change_child(old, new, states.get(id(i), None)) for i in self.blocks}

        if all(replacements[id(i)][0] is i for i in self.blocks):
            return self, state

        if state is not None:
            state = [replacements[id(i)] for i, _ in state]

        return Parallel(self.loc, [replacements[id(i)][0] for i in self.blocks]), state

    def _handles_event(self, event):
        for i in self.blocks:
            if i._handles_event(event):
                return True

        return False

    def execute(self, trans, st, state, events):
        executing(self.loc)

        if state is None:
            state = [(i, None) for i in self.blocks]

        # The amount of time left after finishing this block.
        left = []

        # The duration of the pause.
        pauses = []

        # The new state structure.
        newstate = []

        for i, istate in state:
            action, arg, pause = i.execute(trans, st, istate, events)

            if pause is not None:
                pauses.append(pause)

            if action == "continue":
                newstate.append((i, arg))
            elif action == "next":
                left.append(arg)
            elif action == "event":
                return action, arg, pause

        if newstate:
            return "continue", newstate, min(pauses)
        else:
            return "next", min(left), None

    def visit(self):
        return [j for i in self.blocks for j in i.visit()]


# The choice statement.


class RawChoice(RawStatement):
    def __init__(self, loc, chance, block):
        super(RawChoice, self).__init__(loc)

        self.choices = [(chance, block)]

    def compile(self, ctx):
        compiling(self.loc)
        return Choice(self.loc, [(ctx.eval(chance), block.compile(ctx)) for chance, block in self.choices])

    def predict(self, ctx):
        for _i, j in self.choices:
            j.predict(ctx)

    def mark_constant(self, analysis):
        constant = GLOBAL_CONST
        has_child = False

        for _chance, block in self.choices:
            block.mark_constant(analysis)
            constant = min(constant, block.constant)
            has_child = has_child or block.has_child

        self.constant = constant
        self.has_child = has_child


class Choice(Statement):
    def __init__(self, loc, choices):
        super(Choice, self).__init__(loc)

        self.choices = choices

    def in_current_store(self):
        choices = [(chance, block.in_current_store()) for chance, block in self.choices]
        return Choice(self.loc, choices)

    def change_child(self, old, new, state):
        if state is not None:
            choice, cstate = state
        else:
            choice = None
            cstate = None

        changed = False
        choices = []

        for chance, block in self.choices:
            if block is choice:
                new_block, cstate = block.change_child(old, new, cstate)
                choice = new_block
            else:
                new_block, _ = block.change_child(old, new, None)

            changed = changed or (new_block is not block)
            choices.append((chance, new_block))

        if not changed:
            return self, state

        if state is not None:
            state = (choice, cstate)

        return Choice(self.loc, choices), state

    def _handles_event(self, event):
        for i in self.choices:
            if i[1]._handles_event(event):
                return True

        return False

    def execute(self, trans, st, state, events):
        executing(self.loc)

        choice = None  # For typing purposes.

        if state is None:
            total = 0

            for chance, choice in self.choices:
                total += chance

            n = random.uniform(0, total)

            for chance, choice in self.choices:
                if n < chance:
                    break
                n -= chance

            cstate = None

        else:
            choice, cstate = state

        action, arg, pause = choice.execute(trans, st, cstate, events)

        if action == "continue":
            return "continue", (choice, arg), pause
        else:
            return action, arg, None

    def visit(self):
        return [j for i in self.choices for j in i[1].visit()]


# The Time statement.


class RawTime(RawStatement):
    def __init__(self, loc, time):
        super(RawTime, self).__init__(loc)
        self.time = time

    def compile(self, ctx):
        compiling(self.loc)
        return Time(self.loc, ctx.eval(self.time))

    def mark_constant(self, analysis):
        self.constant = analysis.is_constant_expr(self.time)
        self.has_child = False


class Time(Statement):
    def __init__(self, loc, time):
        super(Time, self).__init__(loc)

        self.time = time

    def execute(self, trans, st, state, events):
        return "continue", None, None


# The On statement.


class RawOn(RawStatement):
    def __init__(self, loc, names, block):
        super(RawOn, self).__init__(loc)

        self.handlers = {}

        for i in names:
            self.handlers[i] = block

    def compile(self, ctx):
        compiling(self.loc)

        handlers = {}

        for k, v in self.handlers.items():
            handlers[k] = v.compile(ctx)

        return On(self.loc, handlers)

    def predict(self, ctx):
        for i in self.handlers.values():
            i.predict(ctx)

    def mark_constant(self, analysis):
        constant = GLOBAL_CONST
        has_child = False

        for block in self.handlers.values():
            block.mark_constant(analysis)
            constant = min(constant, block.constant)
            has_child = has_child or block.has_child

        self.constant = constant
        self.has_child = has_child


class On(Statement):
    def __init__(self, loc, handlers):
        super(On, self).__init__(loc)

        self.handlers = handlers

    def in_current_store(self):
        handlers = {k: v.in_current_store() for k, v in self.handlers.items()}
        return On(self.loc, handlers)

    def change_child(self, old, new, state):
        if state is not None:
            name, start, cstate = state
        else:
            name = None
            cstate = None

        changed = False
        handlers = {}

        for k, v in self.handlers.items():
            if k == name:
                handlers[k], cstate = v.change_child(old, new, cstate)
            else:
                handlers[k] = v.change_child(old, new, None)[0]

            changed = changed or (handlers[k] is not v)

        if not changed:
            return self, state

        if state is not None:
            state = (name, start, cstate)  # type: ignore

        return On(self.loc, handlers), state

    def _handles_event(self, event):
        if event in self.handlers:
            return True
        else:
            return False

    def execute(self, trans, st, state, events):
        executing(self.loc)

        # If it's our first time through, start in the start state.
        if state is None:
            name, start, cstate = ("start", st, None)
        else:
            name, start, cstate = state

        # If we have an external event, and we have a handler for it,
        # handle it.
        for event in events:
            while event:
                if event in self.handlers:
                    break

                event = event.partition("_")[2]

            if not event:
                continue

            # Do not allow people to abort the hide or replaced event.
            lock_event = (name == "hide" and trans.hide_request) or (name == "replaced" and trans.replaced_request)

            if not lock_event:
                name = event
                start = st
                cstate = None

        while True:
            # If we don't have a handler, return until we change event.
            if name not in self.handlers:
                return "continue", (name, start, cstate), None

            action, arg, pause = self.handlers[name].execute(trans, st - start, cstate, events)

            # If we get a continue, save our state.
            if action == "continue":
                # If it comes from a hide block, indicate that.
                if name == "hide" or name == "replaced":
                    trans.hide_response = False
                    trans.replaced_response = False

                return "continue", (name, start, arg), pause

            # If we get a next, then try going to the default
            # event, unless we're already in default, in which case we
            # go to None.
            elif action == "next":
                if name == "default" or name == "hide" or name == "replaced":
                    name = None
                else:
                    name = "default"

                start = st - arg
                cstate = None

                continue

            # If we get an event, then either handle it if we can, or
            # pass it up the stack if we can't.
            elif action == "event":
                name, arg = arg

                if name in self.handlers:
                    start = max(st - arg, st - 30)
                    cstate = None
                    continue

                return "event", (name, arg), None

    def visit(self):
        return [j for i in self.handlers.values() for j in i.visit()]


# Event statement.


class RawEvent(RawStatement):
    def __init__(self, loc, name):
        super(RawEvent, self).__init__(loc)

        self.name = name

    def compile(self, ctx):
        return Event(self.loc, self.name)

    def mark_constant(self, analysis):
        self.constant = GLOBAL_CONST
        self.has_child = False


class Event(Statement):
    def __init__(self, loc, name):
        super(Event, self).__init__(loc)

        self.name = name

    def execute(self, trans, st, state, events):
        return "event", (self.name, st), None


class RawFunction(RawStatement):
    def __init__(self, loc, expr):
        super(RawFunction, self).__init__(loc)

        self.expr = expr

    def compile(self, ctx):
        compiling(self.loc)
        return Function(self.loc, ctx.eval(self.expr))

    def mark_constant(self, analysis):
        self.constant = analysis.is_constant_expr(self.expr)
        self.has_child = False


class Function(Statement):
    def __init__(self, loc, function):
        super(Function, self).__init__(loc)

        self.function = function

    def _handles_event(self, event):
        return True

    def execute(self, trans, st, state, events):
        block = state or renpy.config.atl_function_always_blocks

        fr = self.function(trans, st if block else 0, trans.at)

        if (not block) and (fr is not None):
            block = True
            fr = self.function(trans, st, trans.at)

        if fr is not None:
            return "continue", True, fr
        else:
            return "next", 0 if block else st, None


# This parses an ATL block.
def parse_atl(l):
    l.advance()
    block_loc = l.get_location()

    statements = []

    animation = False

    while not l.eob:
        loc = l.get_location()

        if l.keyword("repeat"):
            repeats = l.simple_expression()
            statements.append(RawRepeat(loc, repeats))

        elif l.keyword("block"):
            l.require(":")
            l.expect_eol()
            l.expect_block("block")

            block = parse_atl(l.subblock_lexer())
            statements.append(block)

        elif l.keyword("contains"):
            expr = l.simple_expression()

            if expr:
                l.expect_noblock("contains expression")
                statements.append(RawContainsExpr(loc, expr))

            else:
                l.require(":")
                l.expect_eol()
                l.expect_block("contains")

                block = parse_atl(l.subblock_lexer())
                statements.append(RawChild(loc, block))

        elif l.keyword("parallel"):
            l.require(":")
            l.expect_eol()
            l.expect_block("parallel")

            block = parse_atl(l.subblock_lexer())
            statements.append(RawParallel(loc, block))

        elif l.keyword("choice"):
            chance = l.simple_expression()
            if not chance:
                chance = "1.0"

            l.require(":")
            l.expect_eol()
            l.expect_block("choice")

            block = parse_atl(l.subblock_lexer())
            statements.append(RawChoice(loc, chance, block))

        elif l.keyword("on"):
            names = [l.require(l.word)]

            while l.match(","):
                name = l.word()

                if name is None:
                    break

                names.append(name)

            l.require(":")
            l.expect_eol()
            l.expect_block("on")

            block = parse_atl(l.subblock_lexer())
            statements.append(RawOn(loc, names, block))

        elif l.keyword("time"):
            time = l.require(l.simple_expression)
            l.expect_noblock("time")

            statements.append(RawTime(loc, time))

        elif l.keyword("function"):
            expr = l.require(l.simple_expression)
            l.expect_noblock("function")

            statements.append(RawFunction(loc, expr))

        elif l.keyword("event"):
            name = l.require(l.word)
            l.expect_noblock("event")

            statements.append(RawEvent(loc, name))

        elif l.keyword("pass"):
            l.expect_noblock("pass")
            statements.append(None)

        elif l.keyword("animation"):
            l.expect_noblock("animation")
            animation = True

        else:
            # If we can't assign it to a statement more specifically,
            # we try to parse it into a RawMultipurpose. That will
            # then be turned into another statement, as appropriate.

            # The RawMultipurpose we add things to.
            rm = renpy.atl.RawMultipurpose(loc)

            # Is the last clause an expression?
            last_expression = False

            # Is this clause an expression?
            this_expression = False

            # First, look for a warper.
            cp = l.checkpoint()
            warper = l.name()

            if warper in warpers:
                duration = l.require(l.simple_expression)
                warp_function = None

            elif warper == "warp":
                warper = None
                warp_function = l.require(l.simple_expression)
                duration = l.require(l.simple_expression)

            else:
                l.revert(cp)

                warper = None
                warp_function = None
                duration = "0"

            rm.add_warper(warper, duration, warp_function)

            ll = l
            has_block = False

            # Now, look for properties and simple_expressions.
            while True:
                if ((warper is not None) or (warp_function is not None)) and (not has_block) and ll.match(":"):
                    ll.expect_eol()
                    ll.expect_block("ATL")
                    has_block = True
                    ll = l.subblock_lexer()
                    ll.advance()
                    ll.expect_noblock("ATL")

                if has_block and ll.eol():
                    ll.advance()
                    ll.expect_noblock("ATL")

                # Update expression status.
                last_expression = this_expression
                this_expression = False

                if ll.keyword("pass"):
                    continue

                # Parse revolution keywords.
                if ll.keyword("clockwise"):
                    rm.add_revolution("clockwise")
                    continue

                if ll.keyword("counterclockwise"):
                    rm.add_revolution("counterclockwise")
                    continue

                if ll.keyword("circles"):
                    expr = l.require(l.simple_expression)
                    rm.add_circles(expr)
                    continue

                # Try to parse a property.
                cp = ll.checkpoint()

                prop = ll.name()

                good_prop = prop in PROPERTIES
                if not prop:
                    good_prop = False
                elif prop.startswith("u_"):
                    good_prop = True
                elif prop.startswith("gl_texture_wrap_"):
                    good_prop = True
                elif prop.startswith("gl_texture_scaling_"):
                    good_prop = True

                if good_prop:
                    expr = ll.require(ll.simple_expression)

                    # We either have a property or a spline. It's the
                    # presence of knots that determine which one it is.

                    knots = []

                    while ll.keyword("knot"):
                        knots.append(ll.require(ll.simple_expression))

                    if knots:
                        if prop == "orientation":
                            raise Exception("Orientation doesn't support spline.")
                        loop = bool(ll.keyword("loop"))
                        if loop and len(knots) < 3:
                            raise Exception("Spline loops require at least 3 knots.")
                        knots.append(expr)
                        rm.add_spline(prop, knots, loop)
                    else:
                        addprop_rv = rm.add_property(prop, expr)
                        if addprop_rv == prop:
                            ll.deferred_error(
                                "check_conflicting_properties",
                                "property {!r} is given a value more than once".format(prop),
                            )
                        elif addprop_rv:
                            ll.deferred_error(
                                "check_conflicting_properties",
                                "properties {!r} and {!r} conflict with each other".format(prop, addprop_rv),
                            )

                    continue

                # Otherwise, try to parse it as a simple expressoon,
                # with an optional with clause.

                ll.revert(cp)

                expr = ll.simple_expression()

                if not expr:
                    break

                if last_expression:
                    ll.error(
                        "ATL statement contains two expressions in a row; is one of them a misspelled property? If not, separate them with pass."
                    )

                this_expression = True

                if ll.keyword("with"):
                    with_expr = ll.require(ll.simple_expression)
                else:
                    with_expr = None

                rm.add_expression(expr, with_expr)

            if not has_block:
                l.expect_noblock("ATL")

            statements.append(rm)

        if l.eol():
            l.advance()
            continue

        l.require(",", "comma or end of line")

    # Merge together statements that need to be merged together.

    merged = []
    old = None

    for new in statements:
        if isinstance(old, RawParallel) and isinstance(new, RawParallel):
            old.blocks.extend(new.blocks)
            continue

        elif isinstance(old, RawChoice) and isinstance(new, RawChoice):
            old.choices.extend(new.choices)
            continue

        elif isinstance(old, RawChild) and isinstance(new, RawChild):
            old.children.extend(new.children)
            continue

        elif isinstance(old, RawOn) and isinstance(new, RawOn):
            old.handlers.update(new.handlers)
            continue

        # None is a pause statement, which gets skipped, but also
        # prevents things from combining.
        elif new is None:
            old = new
            continue

        merged.append(new)
        old = new

    return RawBlock(block_loc, merged, animation)


def deep_compare(a, b):
    """
    Compares two trees of ATL statements for equality.
    """

    if type(a) != type(b):
        return False

    if isinstance(a, (list, tuple)):
        return all(deep_compare(i, j) for i, j in zip(a, b))

    if isinstance(a, dict):
        if len(a) != len(b):
            return False

        return all((k in b) and deep_compare(a[k], b[k]) for k in a)

    if isinstance(a, Statement):
        return deep_compare(a.__dict__, b.__dict__)

    try:
        return a == b
    except Exception:
        return True
