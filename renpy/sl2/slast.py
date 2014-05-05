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

from renpy.python import py_compile, py_eval_bytecode, py_exec_bytecode
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

            # The scope that python methods are evaluated in.
            self.scope = parent.scope

            # A list of child displayables that will be added to an outer
            # displayable.
            self.children = parent.children

            # A list of keywords.
            self.keywords = parent.keywords

            # The style prefix that is given to children of this displayable.
            self.style_prefix = parent.style_prefix

            # A cache associated with this context. These map from
            # statement serial to information associated with the statement.
            self.cache = parent.cache

            # The number of times a particular use statement has been called
            # in the current screen. We use this to generate a unique name for
            # each call site.
            self.use_index = parent.use_index

        else:
            self.scope = { }
            self.children = [ ]
            self.keywords = { }
            self.style_prefix = ""
            self.cache = { }
            self.use_index = collections.defaultdict(int)


class SLNode(object):
    """
    The base class for screen language nodes.
    """

    def __init__(self, loc):
        global serial
        serial += 1

        self.serial = serial
        self.location = loc

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
                keyword_exprs.append(node)

        if keyword_values:
            self.keyword_values = keyword_values
        else:
            self.keyword_values = None

        if keyword_keys:
            node = ast.Dict(keys=keyword_keys, values=keyword_exprs)
            ast.copy_location(node, keyword_exprs[0])
            self.keyword_exprs = compile_expr(node)
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
            context.keywords.update(py_eval_bytecode(keyword_exprs, locals=context.scope))

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

        # The keywords arguments that were used to created the displayable.
        self.keyword = None

        # The children that were added to self.displayable.
        self.children = None

        # The old transform created.
        self.transform = None

        # The transform that was used to create self.transform.
        self.raw_transform = None

        # The imagemap stack entry we reuse.
        self.imagemap = None


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
                exprs.append(node)
                has_exprs = True

        if has_values:
            self.positional_values = values
        else:
            self.positional_values = None

        if has_exprs:
            t = ast.Tuple(elts=exprs, ctx=ast.Load())
            ast.copy_location(t, exprs[0])
            self.positional_exprs = compile_expr(t)
        else:
            self.positional_exprs = None

    def execute(self, context):

        cache = context.cache.get(self.serial, None)
        if cache is None:
            context.cache[self.serial] = cache = SLCache()

        # Evaluate the positional arguments.
        positional_values = self.positional_values
        positional_exprs = self.positional_exprs

        if positional_values and positional_exprs:
            values = py_eval_bytecode(positional_exprs, context.scope)
            positional = [ b if (a is use_expression) else a for a, b in zip(positional_values, values) ]
        elif positional_values:
            positional = positional_values
        elif positional_exprs:
            positional = py_eval_bytecode(positional_exprs, locals=context.scope)
        else:
            positional = [ ]

        # Create the context.
        ctx = SLContext(context)
        keywords = ctx.keywords = { }

        SLBlock.keywords(self, ctx)

        # Pass the context
        if self.pass_context:
            positional.insert(0, ctx)

        # Get the widget id and transform, if any.
        widget_id = keywords.pop("id", None)
        transform = keywords.pop("at", None)

        # If we don't know the style, figure it out.
        if ("style" not in keywords) and self.style:
            keywords["style"] = renpy.style.get_style(ctx.style_prefix + self.style) # @UndefinedVariable

        # Create and add the displayables.
        screen = renpy.ui.screen

        if widget_id in screen.widget_properties:
            keywords.update(screen.widget_properties[widget_id])

        if (positional == cache.positional) and (keywords == cache.keywords):
            d = cache.displayable
            reused = True
            print "REUSED", d

            if cache.imagemap is not None:
                renpy.ui.imagemap_stack.append(cache.imagemap)

        else:
            cache.positional = positional
            cache.keywords = keywords.copy()

            if self.scope:
                keywords["scope"] = ctx.scope

            if self.replaces:
                keywords['replaces'] = cache.displayable

            d = self.displayable(*positional, **keywords)

            reused = False

        if d is not None:
            ctx.children = [ ]
            renpy.ui.stack.append(renpy.ui.ChildList(ctx.children, ctx.style_prefix))

        # Evaluate children.
        SLBlock.execute(self, ctx)

        # If we didn't create a displayable, exit early.
        if d is None:
            return

        renpy.ui.stack.pop()

        if self.imagemap:
            cache.imagemap = renpy.ui.imagemap_stack.pop()

        if ctx.children != cache.children:

            if reused:
                d._clear()

            if self.child_or_fixed and len(self.children) != 1:
                f = renpy.display.layout.Fixed()

                for i in ctx.children:
                    f.add(i)

                d.add(f)

            else:
                for i in ctx.children:
                    d.add(i)

        cache.displayable = d

        if widget_id is not None:
            screen.widgets[widget_id] = d

        if transform is not None:
            if transform is not cache.raw_transform:
                cache.raw_transform = transform
                d = transform(d)

                if cache.transform is not None:
                    d.take_state(cache.transform)
                    d.take_execution_state(cache.transform)

            cache.transform = d

        context.children.append(d)


# TODO: If a displayable is entirely constant, do not re-create it. If a
# tree is entirely constant, reuse it. Be sure to handle imagemaps properly,
# using the stack.

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
                cond = py_compile(cond, 'eval')

            block.prepare()

            self.prepared_entries.append((cond, block))

    def execute(self, context):

        for cond, block in self.prepared_entries:
            if cond is None or py_eval_bytecode(cond, locals=context.scope):
                block.execute(context)
                return

    def keywords(self, context):

        for cond, block in self.prepared_entries:
            if cond is None or py_eval_bytecode(cond, locals=context.scope):
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

        SLBlock.prepare(self)

    def execute(self, context):

        variable = self.variable
        expr = self.expression_expr

        if expr is not None:
            value = py_eval_bytecode(expr, locals=context.scope)
        else:
            value = self.expression_value

        newcaches = collections.defaultdict(dict)
        oldcaches = context.cache.get(self.serial, newcaches)

        ctx = SLContext(context)

        for i, v in enumerate(value):

            ctx.scope[variable] = v

            # TODO: use indexes of id(v) to get the cache.

            cache = oldcaches[i]
            newcaches[i] = cache
            ctx.cache = cache

            SLBlock.execute(self, ctx)

    def keywords(self, context):
        return


class SLPython(SLNode):

    def __init__(self, loc, code):
        SLNode.__init__(self, loc)

        # A pycode object.
        self.code = code

    def execute(self, context):
        py_exec_bytecode(self.code.bytecode, locals=context.scope)


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

    def execute(self, context):
        scope = context.scope
        variable = self.variable

        if variable in scope:
            return

        scope[variable] = py_eval_bytecode(self.expr, locals=scope)


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
            return
        if ts.ast is None:
            return

        self.ast = ts.ast
        self.ast.prepare()

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
            self.prepared = True
            SLBlock.prepare(self)

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

