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

import renpy.display
import renpy.pyanalysis

import random


def compiling(loc):
    file, number = loc  # @ReservedAssignment

    renpy.game.exception_info = "Compiling ATL code at %s:%d" % (file, number)


def executing(loc):
    file, number = loc  # @ReservedAssignment

    renpy.game.exception_info = "Executing ATL code at %s:%d" % (file, number)


# A map from the name of a time warp function to the function itself.
warpers = { }


def atl_warper(f):
    name = f.func_name
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

position = renpy.object.Sentinel("position")


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

# A dictionary giving property names and the corresponding default
# values.
PROPERTIES = {
    "pos" : (position, position),
    "xpos" : position,
    "ypos" : position,
    "anchor" : (position, position),
    "xanchor" : position,
    "yanchor" : position,
    "xaround" : position,
    "yaround" : position,
    "xanchoraround" : float,
    "yanchoraround" : float,
    "align" : (float, float),
    "xalign" : float,
    "yalign" : float,
    "rotate" : float,
    "rotate_pad" : bool,
    "transform_anchor" : bool,
    "xzoom" : float,
    "yzoom" : float,
    "zoom" : float,
    "nearest" : bool_or_none,
    "alpha" : float,
    "additive" : float,
    "around" : (position, position),
    "alignaround" : (float, float),
    "angle" : float,
    "radius" : float,
    "crop" : (float, float, float, float),
    "crop_relative" : bool,
    "size" : (int, int),
    "corner1" : (float, float),
    "corner2" : (float, float),
    "subpixel" : bool,
    "delay" : float,
    "xoffset" : float,
    "yoffset" : float,
    "offset" : (int, int),
    "xcenter" : position,
    "ycenter" : position,
    "debug" : any_object,
    "events" : bool,
    "xpan" : float_or_none,
    "ypan" : float_or_none,
    "xtile" : int,
    "ytile" : int,
    }


def correct_type(v, b, ty):
    """
    Corrects the type of v to match ty. b is used to inform the match.
    """

    if ty is position:
        if v is None:
            return None
        else:
            return type(b)(v)
    else:
        return ty(v)


def interpolate(t, a, b, type):  # @ReservedAssignment
    """
    Linearly interpolate the arguments.
    """

    # Recurse into tuples.
    if isinstance(b, tuple):
        if a is None:
            a = [ None ] * len(b)

        return tuple(interpolate(t, i, j, ty) for i, j, ty in zip(a, b, type))

    # Deal with booleans, nones, etc.
    elif b is None or isinstance(b, (bool, basestring)):
        if t >= 1.0:
            return b
        else:
            return a

    # Interpolate everything else.
    else:
        if a is None:
            a = 0

        return correct_type(a + t * (b - a), b, type)

# Interpolate the value of a spline. This code is based on Aenakume's code,
# from 00splines.rpy.


def interpolate_spline(t, spline):

    if isinstance(spline[-1], tuple):
        return tuple(interpolate_spline(t, i) for i in zip(*spline))

    if spline[0] is None:
        return spline[-1]

    if len(spline) == 2:
        t_p = 1.0 - t

        rv = t_p * spline[0] + t * spline[-1]

    elif len(spline) == 3:
        t_pp = (1.0 - t)**2
        t_p = 2 * t * (1.0 - t)
        t2 = t**2

        rv = t_pp * spline[0] + t_p * spline[1] + t2 * spline[2]

    elif len(spline) == 4:

        t_ppp = (1.0 - t)**3
        t_pp = 3 * t * (1.0 - t)**2
        t_p = 3 * t**2 * (1.0 - t)
        t3 = t**3

        rv = t_ppp * spline[0] + t_pp * spline[1] + t_p * spline[2] + t3 * spline[3]

    else:
        raise Exception("ATL can't interpolate splines of length %d." % len(spline))

    return correct_type(rv, spline[-1], position)

# A list of atl transforms that may need to be compile.
compile_queue = [ ]


def compile_all():
    """
    Called after the init phase is finished and transforms are compiled,
    to compile all transforms.
    """

    global compile_queue

    for i in compile_queue:
        if i.atl.constant == GLOBAL_CONST:
            i.compile()

    compile_queue = [ ]


# This is the context used when compiling an ATL statement. It stores the
# scopes that are used to evaluate the various expressions in the statement,
# and has a method to do the evaluation and return a result.
class Context(object):

    def __init__(self, context):
        self.context = context

    def eval(self, expr):  # @ReservedAssignment
        expr = renpy.python.escape_unicode(expr)
        return eval(expr, renpy.store.__dict__, self.context)  # @UndefinedVariable

    def __eq__(self, other):
        if not isinstance(other, Context):
            return False

        return self.context == other.context

# This is intended to be subclassed by ATLTransform. It takes care of
# managing ATL execution, which allows ATLTransform itself to not care
# much about the contents of this file.


class ATLTransformBase(renpy.object.Object):

    # Compatibility with older saves.
    parameters = renpy.ast.ParameterInfo([ ], [ ], None, None)
    parent_transform = None
    atl_st_offset = 0

    # The block, as first compiled for prediction.
    predict_block = None

    nosave = [ 'parent_transform' ]

    def __init__(self, atl, context, parameters):

        # The constructor will be called by atltransform.

        if parameters is None:
            parameters = ATLTransformBase.parameters

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
        self.atl_st_offset = 0

        if renpy.game.context().init_phase:
            compile_queue.append(self)

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

        super(ATLTransformBase, self).take_execution_state(t)

        self.atl_st_offset = None

        if self is t:
            return
        elif not isinstance(t, ATLTransformBase):
            return
        elif t.atl is not self.atl:
            return

        # Important to do it this way, so we use __eq__. The exception handling
        # optimistically assumes that uncomparable objects are the same.
        try:
            if not (t.context == self.context):
                return
        except:
            pass

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
            self.child = t.child
            self.raw_child = t.raw_child

    def __call__(self, *args, **kwargs):

        _args = kwargs.pop("_args", None)

        context = self.context.context.copy()

        for k, v in self.parameters.parameters:
            if v is not None:
                context[k] = renpy.python.py_eval(v)

        positional = list(self.parameters.positional)
        args = list(args)

        child = None

        if not positional and args:
            child = args.pop(0)

        # Handle positional arguments.
        while positional and args:
            name = positional.pop(0)
            value = args.pop(0)

            if name in kwargs:
                raise Exception('Parameter %r is used as both a positional and keyword argument to a transition.' % name)

            context[name] = value

        if args:
            raise Exception("Too many arguments passed to ATL transform.")

        # Handle keyword arguments.
        for k, v in kwargs.iteritems():

            if k in positional:
                positional.remove(k)
                context[k] = v
            elif k in context:
                context[k] = v
            elif k == 'child':
                child = v
            else:
                raise Exception('Parameter %r is not known by ATL Transform.' % k)

        if child is None:
            child = self.child

        if child is None:
            child = renpy.display.motion.get_null()

        # Create a new ATL Transform.
        parameters = renpy.ast.ParameterInfo({ }, positional, None, None)

        rv = renpy.display.motion.ATLTransform(
            atl=self.atl,
            child=child,
            style=self.style_arg,
            context=context,
            parameters=parameters,
            _args=_args,
            )

        rv.parent_transform = self
        rv.take_state(self)

        return rv

    def compile(self):  # @ReservedAssignment
        """
        Compiles the ATL code into a block. As necessary, updates the
        properties.
        """

        constant = (self.atl.constant == GLOBAL_CONST)

        if not constant:
            for p in self.parameters.positional:
                if p not in self.context.context:
                    raise Exception("Cannot compile ATL Transform at %s:%d, as it's missing positional parameter %s." % (
                        self.atl.loc[0],
                        self.atl.loc[1],
                        self.parameters.positional[0],
                        ))

        if constant and self.parent_transform:
            if self.parent_transform.block:
                self.block = self.parent_transform.block
                self.properties = self.parent_transform.properties
                self.parent_transform = None
                return self.block

        old_exception_info = renpy.game.exception_info

        block = self.atl.compile(self.context)

        if len(block.statements) == 1 and isinstance(block.statements[0], Interpolation):

            interp = block.statements[0]

            if interp.duration == 0 and interp.properties:
                self.properties = interp.properties[:]

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

    def execute(self, trans, st, at):

        if self.done:
            return None

        block = self.get_block()
        if block is None:
            block = self.compile()

        # Propagate transform_events from children.
        if self.child:
            if self.child.transform_event != self.last_child_transform_event:
                self.last_child_transform_event = self.child.transform_event
                self.transform_event = self.child.transform_event

        # Hide request.
        if trans.hide_request:
            self.transform_event = "hide"

        if trans.replaced_request:
            self.transform_event = "replaced"

        # Notice transform events.
        if self.transform_event != self.last_transform_event:
            event = self.transform_event
            self.last_transform_event = self.transform_event
        else:
            event = None

        old_exception_info = renpy.game.exception_info

        if (self.atl_st_offset is None) or (st - self.atl_st_offset) < 0:
            self.atl_st_offset = st

        if self.atl.animation:
            timebase = at
        else:
            timebase = st - self.atl_st_offset

        action, arg, pause = block.execute(trans, timebase, self.atl_state, event)

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

        return self.children + block.visit()

# This is used in mark_constant to analyze expressions for constness.
is_constant_expr = renpy.pyanalysis.Analysis().is_constant_expr
GLOBAL_CONST = renpy.pyanalysis.GLOBAL_CONST

# The base class for raw ATL statements.


class RawStatement(object):

    constant = None

    def __init__(self, loc):
        super(RawStatement, self).__init__()
        self.loc = loc

    # Compiles this RawStatement into a Statement, by using ctx to
    # evaluate expressions as necessary.
    def compile(self, ctx):  # @ReservedAssignment
        raise Exception("Compile not implemented.")

    # Predicts the images used by this statement.
    def predict(self, ctx):
        return

    def mark_constant(self):
        """
        Sets self.constant to true if all expressions used in this statement
        and its children are constant.
        """

        self.constant = 0

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
    def execute(self, trans, st, state, event):
        raise Exception("Not implemented.")

    # Return a list of displayable children.
    def visit(self):
        return [ ]

# This represents a Raw ATL block.


class RawBlock(RawStatement):

    # Should we use the animation timebase or the showing timebase?
    animation = False

    def __init__(self, loc, statements, animation):

        super(RawBlock, self).__init__(loc)

        # A list of RawStatements in this block.
        self.statements = statements

        self.animation = animation

    def compile(self, ctx):  # @ReservedAssignment
        compiling(self.loc)

        statements = [ i.compile(ctx) for i in self.statements ]

        return Block(self.loc, statements)

    def predict(self, ctx):
        for i in self.statements:
            i.predict(ctx)

    def mark_constant(self):

        constant = GLOBAL_CONST

        for i in self.statements:
            i.mark_constant()
            constant = min(constant, i.constant)

        self.constant = constant


# A compiled ATL block.
class Block(Statement):

    def __init__(self, loc, statements):

        super(Block, self).__init__(loc)

        # A list of statements in the block.
        self.statements = statements

        # The start times of various statements.
        self.times = [ ]

        for i, s in enumerate(statements):
            if isinstance(s, Time):
                self.times.append((s.time, i + 1))

        self.times.sort()

    def execute(self, trans, st, state, event):

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
                action, arg, pause = stmt.execute(trans, target - start, child_state, event)

                # On continue, persist our state.
                if action == "continue":
                    if pause is None:
                        pause = max_pause

                    action, arg, pause = "continue", (index, start, loop_start, repeats, times, arg), min(max_pause, pause)
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

                    if duration <= 0:
                        raise Exception("ATL appears to be in an infinite loop.")

                    # Figure how many durations can occur between the
                    # start of the loop and now.
                    new_repeats = int((target - loop_start) / duration)

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
        return [ j for i in self.statements for j in i.visit() ]

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


class RawMultipurpose(RawStatement):

    warp_function = None

    def __init__(self, loc):

        super(RawMultipurpose, self).__init__(loc)

        self.warper = None
        self.duration = None
        self.properties = [ ]
        self.expressions = [ ]
        self.splines = [ ]
        self.revolution = None
        self.circles = "0"

    def add_warper(self, name, duration, warp_function):
        self.warper = name
        self.duration = duration
        self.warp_function = warp_function

    def add_property(self, name, exprs):
        self.properties.append((name, exprs))

    def add_expression(self, expr, with_clause):
        self.expressions.append((expr, with_clause))

    def add_revolution(self, revolution):
        self.revolution = revolution

    def add_circles(self, circles):
        self.circles = circles

    def add_spline(self, name, exprs):
        self.splines.append((name, exprs))

    def compile(self, ctx):  # @ReservedAssignment

        compiling(self.loc)

        # Figure out what kind of statement we have. If there's no
        # interpolator, and no properties, than we have either a
        # call, or a child statement.
        if (self.warper is None and
            self.warp_function is None and
            not self.properties and
            not self.splines and
                len(self.expressions) == 1):

            expr, withexpr = self.expressions[0]

            child = ctx.eval(expr)
            if withexpr:
                transition = ctx.eval(withexpr)
            else:
                transition = None

            if isinstance(child, (int, float)):
                return Interpolation(self.loc, "pause", child, [ ], None, 0, [ ])

            child = renpy.easy.displayable(child)

            if isinstance(child, ATLTransformBase):
                child.compile()
                return child.get_block()
            else:
                return Child(self.loc, child, transition)

        compiling(self.loc)

        # Otherwise, we probably have an interpolation statement.

        if self.warp_function:
            warper = ctx.eval(self.warp_function)
        else:
            warper = self.warper or "pause"

            if warper not in warpers:
                raise Exception("ATL Warper %s is unknown at runtime." % warper)

        properties = [ ]

        for name, expr in self.properties:
            if name not in PROPERTIES:
                raise Exception("ATL Property %s is unknown at runtime." % property)

            value = ctx.eval(expr)
            properties.append((name, value))

        splines = [ ]

        for name, exprs in self.splines:
            if name not in PROPERTIES:
                raise Exception("ATL Property %s is unknown at runtime." % property)

            values = [ ctx.eval(i) for i in exprs ]

            splines.append((name, values))

        for expr, _with in self.expressions:
            try:
                value = ctx.eval(expr)
            except:
                raise Exception("Could not evaluate expression %r when compiling ATL." % expr)

            if not isinstance(value, ATLTransformBase):
                raise Exception("Expression %r is not an ATL transform, and so cannot be included in an ATL interpolation." % expr)

            value.compile()

            if value.properties is None:
                raise Exception("ATL transform %r is too complicated to be included in interpolation." % expr)

            properties.extend(value.properties)

        duration = ctx.eval(self.duration)
        circles = ctx.eval(self.circles)

        return Interpolation(self.loc, warper, duration, properties, self.revolution, circles, splines)

    def mark_constant(self):
        constant = GLOBAL_CONST

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

    def predict(self, ctx):

        for i, _j in self.expressions:

            try:
                i = ctx.eval(i)
            except:
                continue

            if isinstance(i, ATLTransformBase):
                i.atl.predict(ctx)
                return

            try:
                renpy.easy.predict(i)
            except:
                continue

# This lets us have an ATL transform as our child.


class RawContainsExpr(RawStatement):

    def __init__(self, loc, expr):

        super(RawContainsExpr, self).__init__(loc)

        self.expression = expr

    def compile(self, ctx):  # @ReservedAssignment
        compiling(self.loc)
        child = ctx.eval(self.expression)
        return Child(self.loc, child, None)

    def mark_constant(self):
        self.constant = is_constant_expr(self.expression)


# This allows us to have multiple ATL transforms as children.
class RawChild(RawStatement):

    def __init__(self, loc, child):

        super(RawChild, self).__init__(loc)

        self.children = [ child ]

    def compile(self, ctx):  # @ReservedAssignment

        children = [ ]

        for i in self.children:
            children.append(renpy.display.motion.ATLTransform(i, context=ctx.context))

        box = renpy.display.layout.MultiBox(layout='fixed')

        for i in children:
            box.add(i)

        return Child(self.loc, box, None)

    def mark_constant(self):

        constant = GLOBAL_CONST

        for i in self.children:
            i.mark_constant()
            constant = min(constant, i.constant)

        self.constant = constant


# This changes the child of this statement, optionally with a transition.
class Child(Statement):

    def __init__(self, loc, child, transition):

        super(Child, self).__init__(loc)

        self.child = child
        self.transition = transition

    def execute(self, trans, st, state, event):

        executing(self.loc)

        old_child = trans.raw_child

        child = self.child

        if child._duplicatable:
            child = self.child._duplicate(trans._args)
            child._unique()

        if (old_child is not None) and (old_child is not renpy.display.motion.null) and (self.transition is not None):
            child = self.transition(old_widget=old_child,
                                    new_widget=child)
            child._unique()
        else:
            child = child

        trans.set_child(child, duplicate=False)
        trans.raw_child = self.child

        return "next", st, None

    def visit(self):
        return [ self.child ]


# This causes interpolation to occur.
class Interpolation(Statement):

    def __init__(self, loc, warper, duration, properties, revolution, circles, splines):

        super(Interpolation, self).__init__(loc)

        self.warper = warper
        self.duration = duration
        self.properties = properties
        self.splines = splines

        # The direction we revolve in: cw, ccw, or None.
        self.revolution = revolution

        # The number of complete circles we make.
        self.circles = circles

    def execute(self, trans, st, state, event):

        executing(self.loc)

        warper = warpers.get(self.warper, self.warper)

        if self.duration:
            complete = min(1.0, st / self.duration)
        else:
            complete = 1.0

        complete = warper(complete)

        if state is None:

            # Create a new transform state, and apply the property
            # changes to it.
            newts = renpy.display.motion.TransformState()
            newts.take_state(trans.state)

            for k, v in self.properties:
                setattr(newts, k, v)

            # Now, the things we change linearly are in the difference
            # between the new and old states.
            linear = trans.state.diff(newts)

            revolution = None
            splines = [ ]

            # Clockwise revolution.
            if self.revolution is not None:

                # Remove various irrelevant motions.
                for i in [ 'xpos', 'ypos',
                           'xanchor', 'yanchor',
                           'xaround', 'yaround',
                           'xanchoraround', 'yanchoraround',
                           ]:

                    linear.pop(i, None)

                if newts.xaround is not None:

                    # Ensure we rotate around the new point.
                    trans.state.xaround = newts.xaround
                    trans.state.yaround = newts.yaround
                    trans.state.xanchoraround = newts.xanchoraround
                    trans.state.yanchoraround = newts.yanchoraround

                    # Get the start and end angles and radii.
                    startangle = trans.state.angle
                    endangle = newts.angle
                    startradius = trans.state.radius
                    endradius = newts.radius

                    # Make sure the revolution is in the appropriate direction,
                    # and contains an appropriate number of circles.

                    if self.revolution == "clockwise":
                        if endangle < startangle:
                            startangle -= 360

                        startangle -= self.circles * 360

                    elif self.revolution == "counterclockwise":
                        if endangle > startangle:
                            startangle += 360

                        startangle += self.circles * 360

                    # Store the revolution.
                    revolution = (startangle, endangle, startradius, endradius)

            # Figure out the splines.
            for name, values in self.splines:
                splines.append((name, [ getattr(trans.state, name) ] + values))

            state = (linear, revolution, splines)

            # Ensure that we set things, even if they don't actually
            # change from the old state.
            for k, v in self.properties:
                if k not in linear:
                    setattr(trans.state, k, v)

        else:
            linear, revolution, splines = state

        # Linearly interpolate between the things in linear.
        for k, (old, new) in linear.iteritems():
            value = interpolate(complete, old, new, PROPERTIES[k])

            setattr(trans.state, k, value)

        # Handle the revolution.
        if revolution is not None:
            startangle, endangle, startradius, endradius = revolution
            trans.state.angle = interpolate(complete, startangle, endangle, float)
            trans.state.radius = interpolate(complete, startradius, endradius, float)

        # Handle any splines we might have.
        for name, values in splines:
            value = interpolate_spline(complete, values)
            setattr(trans.state, name, value)

        if st >= self.duration:
            return "next", st - self.duration, None
        else:
            if not self.properties and not self.revolution and not self.splines:
                return "continue", state, self.duration - st
            else:
                return "continue", state, 0


# Implementation of the repeat statement.
class RawRepeat(RawStatement):

    def __init__(self, loc, repeats):

        super(RawRepeat, self).__init__(loc)

        self.repeats = repeats

    def compile(self, ctx):  # @ReservedAssignment

        compiling(self.loc)

        repeats = self.repeats

        if repeats is not None:
            repeats = ctx.eval(repeats)

        return Repeat(self.loc, repeats)

    def mark_constant(self):
        self.constant = is_constant_expr(self.repeats)


class Repeat(Statement):

    def __init__(self, loc, repeats):

        super(Repeat, self).__init__(loc)

        self.repeats = repeats

    def execute(self, trans, st, state, event):
        return "repeat", (self.repeats, st), 0


# Parallel statement.

class RawParallel(RawStatement):

    def __init__(self, loc, block):

        super(RawParallel, self).__init__(loc)
        self.blocks = [ block ]

    def compile(self, ctx):  # @ReservedAssignment
        return Parallel(self.loc, [i.compile(ctx) for i in self.blocks])

    def predict(self, ctx):
        for i in self.blocks:
            i.predict(ctx)

    def mark_constant(self):
        constant = GLOBAL_CONST

        for i in self.blocks:
            i.mark_constant()
            constant = min(constant, i.constant)

        self.constant = constant


class Parallel(Statement):

    def __init__(self, loc, blocks):
        super(Parallel, self).__init__(loc)
        self.blocks = blocks

    def execute(self, trans, st, state, event):

        executing(self.loc)

        if state is None:
            state = [ (i, None) for i in self.blocks ]

        # The amount of time left after finishing this block.
        left = [ ]

        # The duration of the pause.
        pauses = [ ]

        # The new state structure.
        newstate = [ ]

        for i, istate in state:

            action, arg, pause = i.execute(trans, st, istate, event)

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
        return [ j for i in self.blocks for j in i.visit() ]


# The choice statement.

class RawChoice(RawStatement):

    def __init__(self, loc, chance, block):
        super(RawChoice, self).__init__(loc)

        self.choices = [ (chance, block) ]

    def compile(self, ctx):  # @ReservedAssignment
        compiling(self.loc)
        return Choice(self.loc, [ (ctx.eval(chance), block.compile(ctx)) for chance, block in self.choices])

    def predict(self, ctx):
        for _i, j in self.choices:
            j.predict(ctx)

    def mark_constant(self):
        constant = GLOBAL_CONST

        for _chance, block in self.choices:
            block.mark_constant()
            constant = min(constant, block.constant)

        self.constant = constant


class Choice(Statement):

    def __init__(self, loc, choices):

        super(Choice, self).__init__(loc)

        self.choices = choices

    def execute(self, trans, st, state, event):

        executing(self.loc)

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

        action, arg, pause = choice.execute(trans, st, cstate, event)

        if action == "continue":
            return "continue", (choice, arg), pause
        else:
            return action, arg, None

    def visit(self):
        return [ j for i in self.choices for j in i[1].visit() ]


# The Time statement.

class RawTime(RawStatement):

    def __init__(self, loc, time):

        super(RawTime, self).__init__(loc)
        self.time = time

    def compile(self, ctx):  # @ReservedAssignment
        compiling(self.loc)
        return Time(self.loc, ctx.eval(self.time))

    def mark_constant(self):
        self.constant = is_constant_expr(self.time)


class Time(Statement):

    def __init__(self, loc, time):
        super(Time, self).__init__(loc)

        self.time = time

    def execute(self, trans, st, state, event):
        return "continue", None, None


# The On statement.

class RawOn(RawStatement):

    def __init__(self, loc, names, block):
        super(RawOn, self).__init__(loc)

        self.handlers = { }

        for i in names:
            self.handlers[i] = block

    def compile(self, ctx):  # @ReservedAssignment

        compiling(self.loc)

        handlers = { }

        for k, v in self.handlers.iteritems():
            handlers[k] = v.compile(ctx)

        return On(self.loc, handlers)

    def predict(self, ctx):
        for i in self.handlers.itervalues():
            i.predict(ctx)

    def mark_constant(self):
        constant = GLOBAL_CONST

        for block in self.handlers.itervalues():
            block.mark_constant()
            constant = min(constant, block.constant)

        self.constant = constant


class On(Statement):

    def __init__(self, loc, handlers):
        super(On, self).__init__(loc)

        self.handlers = handlers

    def execute(self, trans, st, state, event):

        executing(self.loc)

        # If it's our first time through, start in the start state.
        if state is None:
            name, start, cstate = ("start", st, None)
        else:
            name, start, cstate = state

        # If we have an external event, and we have a handler for it,
        # handle it.
        if event in self.handlers:

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

            action, arg, pause = self.handlers[name].execute(trans, st - start, cstate, event)

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
        return [ j for i in self.handlers.itervalues() for j in i.visit() ]


# Event statement.

class RawEvent(RawStatement):

    def __init__(self, loc, name):
        super(RawEvent, self).__init__(loc)

        self.name = name

    def compile(self, ctx):  # @ReservedAssignment
        return Event(self.loc, self.name)

    def mark_constant(self):
        self.constant = GLOBAL_CONST


class Event(Statement):

    def __init__(self, loc, name):
        super(Event, self).__init__(loc)

        self.name = name

    def execute(self, trans, st, state, event):
        return "event", (self.name, st), None


class RawFunction(RawStatement):

    def __init__(self, loc, expr):
        super(RawFunction, self).__init__(loc)

        self.expr = expr

    def compile(self, ctx):  # @ReservedAssignment
        compiling(self.loc)
        return Function(self.loc, ctx.eval(self.expr))

    def mark_constant(self):
        self.constant = is_constant_expr(self.expr)


class Function(Statement):

    def __init__(self, loc, function):
        super(Function, self).__init__(loc)

        self.function = function

    def execute(self, trans, st, state, event):
        fr = self.function(trans, st, trans.at)

        if fr is not None:
            return "continue", None, fr
        else:
            return "next", 0, None


# This parses an ATL block.
def parse_atl(l):

    l.advance()
    block_loc = l.get_location()

    statements = [ ]

    animation = False

    while not l.eob:

        loc = l.get_location()

        if l.keyword('repeat'):

            repeats = l.simple_expression()
            statements.append(RawRepeat(loc, repeats))

        elif l.keyword('block'):
            l.require(':')
            l.expect_eol()
            l.expect_block('block')

            block = parse_atl(l.subblock_lexer())
            statements.append(block)

        elif l.keyword('contains'):

            expr = l.simple_expression()

            if expr:

                l.expect_noblock('contains expression')
                statements.append(RawContainsExpr(loc, expr))

            else:

                l.require(':')
                l.expect_eol()
                l.expect_block('contains')

                block = parse_atl(l.subblock_lexer())
                statements.append(RawChild(loc, block))

        elif l.keyword('parallel'):
            l.require(':')
            l.expect_eol()
            l.expect_block('parallel')

            block = parse_atl(l.subblock_lexer())
            statements.append(RawParallel(loc, block))

        elif l.keyword('choice'):

            chance = l.simple_expression()
            if not chance:
                chance = "1.0"

            l.require(':')
            l.expect_eol()
            l.expect_block('choice')

            block = parse_atl(l.subblock_lexer())
            statements.append(RawChoice(loc, chance, block))

        elif l.keyword('on'):

            names = [ l.require(l.word) ]

            while l.match(','):
                name = l.word()

                if name is None:
                    break

                names.append(name)

            l.require(':')
            l.expect_eol()
            l.expect_block('on')

            block = parse_atl(l.subblock_lexer())
            statements.append(RawOn(loc, names, block))

        elif l.keyword('time'):
            time = l.require(l.simple_expression)
            l.expect_noblock('time')

            statements.append(RawTime(loc, time))

        elif l.keyword('function'):
            expr = l.require(l.simple_expression)
            l.expect_noblock('function')

            statements.append(RawFunction(loc, expr))

        elif l.keyword('event'):
            name = l.require(l.word)
            l.expect_noblock('event')

            statements.append(RawEvent(loc, name))

        elif l.keyword('pass'):
            l.expect_noblock('pass')
            statements.append(None)

        elif l.keyword('animation'):
            l.expect_noblock('animation')
            animation = True

        else:

            # If we can't assign it it a statement more specifically,
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

            # Now, look for properties and simple_expressions.
            while True:

                # Update expression status.
                last_expression = this_expression
                this_expression = False

                if l.keyword('pass'):
                    continue

                # Parse revolution keywords.
                if l.keyword('clockwise'):
                    rm.add_revolution('clockwise')
                    continue

                if l.keyword('counterclockwise'):
                    rm.add_revolution('counterclockwise')
                    continue

                if l.keyword('circles'):
                    expr = l.require(l.simple_expression)
                    rm.add_circles(expr)

                # Try to parse a property.
                cp = l.checkpoint()

                prop = l.name()

                if prop in PROPERTIES:

                    expr = l.require(l.simple_expression)

                    # We either have a property or a spline. It's the
                    # presence of knots that determine which one it is.

                    knots = [ ]

                    while l.keyword('knot'):
                        knots.append(l.require(l.simple_expression))

                    if knots:
                        knots.append(expr)
                        rm.add_spline(prop, knots)
                    else:
                        rm.add_property(prop, expr)

                    continue

                # Otherwise, try to parse it as a simple expressoon,
                # with an optional with clause.

                l.revert(cp)

                expr = l.simple_expression()

                if not expr:
                    break

                if last_expression:
                    l.error('ATL statement contains two expressions in a row; is one of them a misspelled property? If not, separate them with pass.')

                this_expression = True

                if l.keyword("with"):
                    with_expr = l.require(l.simple_expression)
                else:
                    with_expr = None

                rm.add_expression(expr, with_expr)

            l.expect_noblock('ATL')

            statements.append(rm)

        if l.eol():
            l.advance()
            continue

        l.require(",", "comma or end of line")

    # Merge together statements that need to be merged together.

    merged = [ ]
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
