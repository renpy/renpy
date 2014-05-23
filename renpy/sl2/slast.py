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

import ast
import collections

import renpy.style
import renpy.display

from renpy.python import py_compile, py_eval_bytecode
from renpy.sl2.pyutil import is_constant

# This file contains the abstract syntax tree for a screen language
# screen.

# A serial number that makes each SLNode unique.
serial = 0

# A sentinel used to indicate we should use the value found in the
# expression.
use_expression = renpy.object.Sentinel("use_expression")

# The filename that's currently being compiled.
filename = '<screen language>'

def compile_expr(node):
    """
    Wraps the node in a python AST, and compiles it.
    """

    expr = ast.Expression(body=node)
    ast.fix_missing_locations(expr)
    return compile(expr, filename, "eval")


class SLContext(object):
    """
    A context object that can be passed to the execute methods.
    """

    def __init__(self, parent=None):
        if parent is not None:
            self.__dict__.update(parent.__dict__)
            return

        # The local scope that python code is evaluated in.
        self.scope = { }

        # The global scope that python code is evaluated in.
        self.globals = { }

        # A list of child displayables that will be added to an outer
        # displayable.
        self.children = [ ]

        # A map from keyword arguments to their values.
        self.keywords = { }

        # The style prefix that is given to children of this displayable.
        self.style_prefix = ""

        # A cache associated with this context. The cache maps from
        # statement serial to information associated with the statement.
        self.cache = { }

        # The number of times a particular use statement has been called
        # in the current screen. We use this to generate a unique name for
        # each call site.
        self.use_index = collections.defaultdict(int)

        # When a constant node uses the scope, we add it to this list, so
        # it may be reused. (If None, no list is used.)
        self.uses_scope = None

        # When a constant node has an id, we added it to this dict, so it
        # may be reused. (If None, no dict is used.)
        self.widgets = None

class SLNode(object):
    """
    The base class for screen language nodes.
    """

    def __init__(self, loc):
        global serial
        serial += 1

        # A unique serial number assigned to this node.
        self.serial = serial

        # The location of this node, a (file, line) tuple.
        self.location = loc

        # True if this is a constant node, always producing an equivalent
        # tree of objects.
        self.constant = True

    def report_traceback(self, name):
        filename, line = self.location

        return [ (filename, line, name, None) ]

    def prepare(self):
        """
        This should be called before the execute code is called, and again
        after init-level code (like the code in a .rpym module or an init
        python block) is called.
        """

        # By default, does nothing.

    def execute(self, context):
        """
        Execute this node, updating context as appropriate.
        """

        raise Exception("execute not implemented by " + type(self).__name__)

    def keywords(self, context):
        """
        Execute this node, updating context.keywords as appropriate.
        """

        # By default, does nothing.
        return

# A sentinel used to indicate a keyword argument was not given.
NotGiven = renpy.object.Sentinel("NotGiven")

class SLBlock(SLNode):
    """
    Represents a screen language block that can contain keyword arguments
    and child displayables.
    """

    def __init__(self, loc):
        SLNode.__init__(self, loc)

        # A list of keyword argument, expr tuples.
        self.keyword = [ ]

        # A list of child SLNodes.
        self.children = [ ]


    def prepare(self):

        for i in self.children:
            i.prepare()

            if not i.constant:
                self.constant = False

        # Compile the keywords.

        keyword_values = { }
        keyword_keys = [ ]
        keyword_exprs = [ ]

        for k, expr in self.keyword:

            node = py_compile(expr, 'eval', ast_node=True)

            if is_constant(node):
                keyword_values[k] = py_eval_bytecode(compile_expr(node))
            else:
                keyword_keys.append(ast.Str(s=k))
                keyword_exprs.append(node) # Will be compiled as part of ast.Dict below.

        if keyword_values:
            self.keyword_values = keyword_values
        else:
            self.keyword_values = None

        if keyword_keys:
            node = ast.Dict(keys=keyword_keys, values=keyword_exprs)
            ast.copy_location(node, keyword_exprs[0])
            self.keyword_exprs = compile_expr(node)

            self.constant = False
        else:
            self.keyword_exprs = None


    def execute(self, context):

        for i in self.children:
            i.execute(context)

    def keywords(self, context):

        keyword_values = self.keyword_values

        if keyword_values is not None:
            context.keywords.update(keyword_values)

        keyword_exprs = self.keyword_exprs

        if keyword_exprs is not None:
            context.keywords.update(eval(keyword_exprs, context.globals, context.scope))

        style_group = context.keywords.pop("style_group", NotGiven)
        if style_group is not NotGiven:
            if style_group is not None:
                context.style_prefix = style_group + "_"
            else:
                context.style_prefix = ""

        for i in self.children:
            i.keywords(context)


class SLCache(object):
    """
    The type of cache associated with an SLDisplayable.
    """

    def __init__(self):

        # The displayable object created.
        self.displayable = None

        # The positional arguments that were used to create the displayable.
        self.positional = None

        # The keyword arguments that were used to created the displayable.
        self.keywords = None

        # The children that were added to self.displayable.
        self.children = None

        # The old transform created.
        self.transform = None

        # The transform that was used to create self.transform.
        self.raw_transform = None

        # The imagemap stack entry we reuse.
        self.imagemap = None

        # If this can be represented as a single constant displayable,
        # do so.
        self.constant = None

        # For a constant statement, a list of our children that use
        # the scope.
        self.constant_uses_scope = [ ]

        # For a constant statement, a map from children to widgets.
        self.constant_widgets = { }

class SLDisplayable(SLBlock):
    """
    A screen language AST node that corresponds to a displayable being
    added to the tree.
    """

    def __init__(self, loc, displayable, scope=False, child_or_fixed=False, style=None, text_style=None, pass_context=False, imagemap=False, replaces=False):
        """
        `displayable`
            A function that, when called with the positional and keyword
            arguments, causes the displayable to be displayed.

        `scope`
            If true, the scope is supplied as an argument to the displayable.

        `child_or_fixed`
            If true and the number of children of this displayable is not one,
            the children are added to a Fixed, and the Fixed is added to the
            displayable.

        `style`
            The base name of the main style.

        `pass_context`
            If given, the context is passed in as the first positonal argument
            of the displayable.

        `imagemap`
            True if this is an imagemap, and should be handled as one.

        `replaces`
            True if the object this displayable replaces should be
            passed to it.
        """

        SLBlock.__init__(self, loc)

        self.displayable = displayable

        self.scope = scope
        self.child_or_fixed = child_or_fixed
        self.style = style
        self.pass_context = pass_context
        self.imagemap = imagemap
        self.replaces = replaces

        # Positional argument expressions.
        self.positional = [ ]

    def prepare(self):

        SLBlock.prepare(self)

        # Prepare the positional arguments.

        exprs = [ ]
        values = [ ]
        has_exprs = False
        has_values = False

        for a in self.positional:
            node = py_compile(a, 'eval', ast_node=True)

            if is_constant(node):
                values.append(py_eval_bytecode(compile_expr(node)))
                exprs.append(ast.Num(n=0))
                has_values = True
            else:
                values.append(use_expression)
                exprs.append(node) # Will be compiled as part of the tuple.
                has_exprs = True

        if has_values:
            self.positional_values = values
        else:
            self.positional_values = None

        if has_exprs:
            t = ast.Tuple(elts=exprs, ctx=ast.Load())
            ast.copy_location(t, exprs[0])
            self.positional_exprs = compile_expr(t)

            self.constant = False
        else:
            self.positional_exprs = None

    def keywords(self, context):
        # We do not want to pass keywords to our parents, so just return.
        return

    def execute(self, context):

        screen = renpy.ui.screen

        cache = context.cache.get(self.serial, None)
        if cache is None:
            context.cache[self.serial] = cache = SLCache()

        if cache.constant:
            context.children.append(cache.constant)
            screen.widgets.update(cache.constant_widgets)

            for i in cache.constant_uses_scope:
                i._scope(context.scope)

            return

        # Evaluate the positional arguments.
        positional_values = self.positional_values
        positional_exprs = self.positional_exprs

        if positional_values and positional_exprs:
            values = eval(positional_exprs, context.globals, context.scope)
            positional = [ b if (a is use_expression) else a for a, b in zip(positional_values, values) ]
        elif positional_values:
            positional = positional_values
        elif positional_exprs:
            positional = eval(positional_exprs, context.globals, context.scope)
        else:
            positional = [ ]

        # Create the context.
        ctx = SLContext(context)
        keywords = ctx.keywords = { }

        if self.constant:
            if ctx.uses_scope is None:
                ctx.uses_scope = [ ]
            if ctx.widgets is None:
                ctx.widgets = { }

        SLBlock.keywords(self, ctx)

        # Get the widget id and transform, if any.
        widget_id = keywords.pop("id", None)
        transform = keywords.pop("at", None)

        # If we don't know the style, figure it out.
        if ("style" not in keywords) and self.style:
            keywords["style"] = renpy.style.get_style(ctx.style_prefix + self.style) # @UndefinedVariable

        if widget_id in screen.widget_properties:
            keywords.update(screen.widget_properties[widget_id])

        if (positional == cache.positional) and (keywords == cache.keywords):
            d = cache.displayable
            reused = True

            if cache.imagemap is not None:
                renpy.ui.imagemap_stack.append(cache.imagemap)

            # The main displayable, if d is a composite displayable. (This is
            # the one that gets the scope, and gets children added to it.)
            main = d._main or d

            if self.scope:
                main._scope(ctx.scope)

        else:
            cache.positional = positional
            cache.keywords = keywords.copy()

            if self.scope:
                keywords["scope"] = ctx.scope

            if self.replaces:
                old_d = cache.displayable

                if old_d is not None:
                    old_d = old_d._main or old_d

                    keywords['replaces'] = old_d

            # Pass the context
            if self.pass_context:
                keywords['context'] = ctx

            d = self.displayable(*positional, **keywords)
            main = d._main or d

            reused = False

        ctx.children = [ ]
        renpy.ui.stack.append(renpy.ui.ChildList(ctx.children, ctx.style_prefix))

        if widget_id is not None:
            screen.widgets[widget_id] = main

        # Evaluate children.
        SLBlock.execute(self, ctx)

        # If we didn't create a displayable, exit early.
        renpy.ui.stack.pop()

        if self.imagemap:
            cache.imagemap = renpy.ui.imagemap_stack.pop()

        if ctx.children != cache.children:

            if reused:
                main._clear()

            if self.child_or_fixed and len(self.children) != 1:
                f = renpy.display.layout.Fixed()

                for i in ctx.children:
                    f.add(i)

                main.add(f)

            else:
                for i in ctx.children:
                    main.add(i)

        cache.displayable = d

        if transform is not None:
            if reused and (transform is cache.raw_transform):
                d = cache.transform
            else:
                cache.raw_transform = transform

                if isinstance(transform, renpy.display.motion.Transform):
                    d = transform(child=d)

                    if cache.transform is not None:
                        d.take_state(cache.transform)
                        d.take_execution_state(cache.transform)
                else:
                    d = transform(d)


            cache.transform = d
        else:
            cache.transform = None
            cache.raw_transform = None

        context.children.append(d)

        if self.constant:
            cache.constant = d

            if widget_id is not None:
                ctx.widgets[widget_id] = main

            if self.scope:
                ctx.uses_scope.append(main)

            if context.widgets is None:
                cache.constant_widgets = ctx.widgets

            if context.uses_scope is None:
                cache.constant_uses_scope = ctx.uses_scope

# TODO: Can we get rid of pass_context?


class SLIf(SLNode):
    """
    A screen language AST node that corresponds to an If/Elif/Else statement.
    """

    def __init__(self, loc):
        """
        An AST node that represents an if statement.
        """
        SLNode.__init__(self, loc)

        # A list of entries, with each consisting of an expression (or
        # None, for the else block) and a SLBlock.
        self.entries = [ ]

    def prepare(self):

        # A list of prepared entries, with each consisting of expression
        # bytecode and a SLBlock.
        self.prepared_entries = [ ]

        for cond, block in self.entries:
            if cond is not None:
                node = py_compile(cond, 'eval', ast_node=True)

                if not is_constant(node):
                    self.constant = False

                cond = compile_expr(node)

            block.prepare()

            if not block.constant:
                self.constant = False

            self.prepared_entries.append((cond, block))

    def execute(self, context):

        for cond, block in self.prepared_entries:
            if cond is None or eval(cond, context.globals, context.scope):
                block.execute(context)
                return

    def keywords(self, context):

        for cond, block in self.prepared_entries:
            if cond is None or eval(cond, context.globals, context.scope):
                block.keywords(context)
                return

unhashable = renpy.object.Sentinel("unhashable")

class SLFor(SLBlock):
    """
    The AST node that corresponds to a for statement. This only supports
    simple for loops that assign a single variable.
    """

    def __init__(self, loc, variable, expression):
        SLBlock.__init__(self, loc)

        self.variable = variable
        self.expression = expression

    def prepare(self):
        node = py_compile(self.expression, 'eval', ast_node=True)

        if is_constant(node):
            self.expression_value = py_eval_bytecode(compile_expr(node))
            self.expression_expr = None
        else:
            self.expression_value = None
            self.expression_expr = compile_expr(node)
            self.constant = False

        SLBlock.prepare(self)

    def execute(self, context):

        variable = self.variable
        expr = self.expression_expr

        if expr is not None:
            value = eval(expr, context.globals, context.scope)
        else:
            value = self.expression_value

        newcaches = {}
        oldcaches = context.cache.get(self.serial, {})

        ctx = SLContext(context)

        count = collections.defaultdict(int)

        for v in value:

            ctx.scope[variable] = v

            if type(v) is int:
                index = v
            else:
                index = id(v)

            n = count[index]
            count[index] = n + 1

            if n > 0:
                index = (index, count)

            cache = oldcaches.get(index, None)

            if cache is None:
                cache = {}

            newcaches[index] = cache
            ctx.cache = cache

            SLBlock.execute(self, ctx)

        context.cache[self.serial] = newcaches

    def keywords(self, context):
        return


class SLPython(SLNode):

    def __init__(self, loc, code):
        SLNode.__init__(self, loc)

        # A pycode object.
        self.code = code

    def execute(self, context):
        exec self.code.bytecode in context.globals, context.scope

    def prepare(self):
        self.constant = False

class SLPass(SLNode):

    def execute(self, context):
        return


class SLDefault(SLNode):

    def __init__(self, loc, variable, expression):
        SLNode.__init__(self, loc)

        self.variable = variable
        self.expression = expression

    def prepare(self):
        self.expr = py_compile(self.expression, 'eval')
        self.constant = False

    def execute(self, context):
        scope = context.scope
        variable = self.variable

        if variable in scope:
            return

        scope[variable] = eval(self.expr, context.globals, scope)

class SLOn(SLNode):

    def __init__(self, loc, event):
        SLNode.__init__(self, loc)

        self.event = event

        # This stores the action using the 'action' property.
        self.keyword = [ ]

    def prepare(self):

        keywords = dict(self.keyword)

        event_node = py_compile(self.event, 'eval', ast_node=True)
        action_node = py_compile(keywords.get('action', None), 'eval', ast_node=True)

        self.event_expr = compile_expr(event_node)
        self.action_expr = compile_expr(action_node)

        if is_constant(event_node):
            self.event_value = py_eval_bytecode(self.event_expr)
        else:
            self.event_value = None

        if is_constant(action_node):
            self.action_value = py_eval_bytecode(self.action_expr)
        else:
            self.action_value = None

        self.constant = False


    def execute(self, context):

        event = self.event_value
        if event is None:
            event = eval(self.event_expr, context.globals, context.scope)

        action = self.action_value
        if action is None:
            action = eval(self.action_expr, context.globals, context.scope)

        renpy.ui.on(event, action)



class SLUse(SLNode):

    def __init__(self, loc, target, args):

        SLNode.__init__(self, loc)

        # The name of the screen we're accessing.
        self.target = target

        # If the target is an SL2 screen, the SLScreen node at the root of
        # the ast for that screen.
        self.ast = None

        # If arguments are given, those arguments.
        self.args = args


    def prepare(self):

        ts = renpy.display.screen.get_screen_variant(self.target)

        if ts is None:
            self.constant = False
            return

        if ts.ast is None:
            self.constant = False
            return

        self.ast = ts.ast
        self.ast.prepare()

        self.constant = self.ast.constant

    def execute_use_screen(self, context):

        # Create an old-style displayable name for this call site.
        serial = context.use_index[self.serial]
        context.use_index[self.serial] = serial + 1

        name = (
            context.scope.get("_name", ()),
            self.serial,
            serial)

        if self.args:
            args, kwargs = self.args.evaluate(context.scope)
        else:
            args = [ ]
            kwargs = { }

        renpy.display.screen.use_screen(self.target, _name=name, _scope=context.scope, *args, **kwargs)

    def execute(self, context):

        ast = self.ast

        # If self.ast is not an SL2 screen, run it using renpy.display.screen.use_screen.
        if ast is None:
            self.execute_use_screen(context)
            return

        # Otherwise, run it directly.

        ctx = SLContext(context)

        # Create a new scope for the context, based on the parameters.
        scope = dict(context.scope)

        if self.args:
            args, kwargs = self.args.evaluate(context.scope)
        else:
            args = [ ]
            kwargs = { }

        if ast.parameters is not None:
            newscope = ast.parameters.apply(args, kwargs)
        else:
            if args:
                raise Exception("Screen {} does not take positional arguments. ({} given)".format(self.target, len(args)))

            newscope = kwargs

        scope.update(newscope)
        ctx.scope = scope

        # Use a call-site specific cache. (Otherwise, two uses of the same screen would
        # be sharing cache locations.

        cache = context.cache.get(self.serial, None)

        if cache is None:
            context.cache[self.serial] = cache = { }

        ctx.cache = cache

        # Run the child screen.
        ast.execute(ctx)


class SLScreen(SLBlock):
    """
    This represents a screen defined in the screen language 2.
    """

    def __init__(self, loc):

        SLBlock.__init__(self, loc)

        # The name of the screen.
        self.name = None

        # Should this screen be declared as modal?
        self.modal = "False"

        # The screen's zorder.
        self.zorder = "0"

        # The screen's tag.
        self.tag = None

        # The variant of screen we're defining.
        self.variant = "None" # expr.

        # Should we predict this screen?
        self.predict = "None" # expr.

        # The parameters this screen takes.
        self.parameters = None

        # True if this screen has been prepared.
        self.prepared = False

    def define(self):
        """
        Defines a screen.
        """

        renpy.display.screen.define_screen(
            self.name,
            self,
            modal=self.modal,
            zorder=self.zorder,
            tag=self.tag,
            variant=renpy.python.py_eval(self.variant),
            predict=renpy.python.py_eval(self.predict),
            parameters=self.parameters,
            )

    def prepare(self):
        if not self.prepared:

            self.constant = False
            SLBlock.prepare(self)
            self.prepared = True

    def report_traceback(self, name):
        if name == "__call__":
            return [ ]

        return SLBlock.report_traceback(self, name)

    def __call__(self, *args, **kwargs):
        scope = kwargs["_scope"]

        if self.parameters:

            args = scope.get("_args", ())
            kwargs = scope.get("_kwargs", { })

            values = renpy.ast.apply_arguments(self.parameters, args, kwargs)
            scope.update(values)

        self.prepare()

        context = SLContext()
        context.scope = scope
        context.globals = renpy.python.store_dicts["store"]

        name = scope["_name"]
        main_cache = renpy.display.screen.current_screen().cache

        cache = main_cache.get(name, None)
        if cache is None:
            cache = { }
            main_cache[name] = cache

        context.cache = cache

        self.execute(context)

        for i in context.children:
            renpy.ui.add(i)

