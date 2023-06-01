# coding=utf-8
# Copyright 2004-2023 Tom Rothamel <pytom@bishoujo.us>
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

#########################################################################
# WARNING WARNING WARNING WARNING WARNING WARNING WARNING WARNING WARNING
#
# When adding fields to a class in an __init__ method, we need to ensure that
# field is copied in the copy() method.

from __future__ import division, absolute_import, with_statement, print_function, unicode_literals
from renpy.compat import PY2, basestring, bchr, bord, chr, open, pystr, range, round, str, tobytes, unicode # *

from typing import Optional, Any

from renpy.compat.pickle import loads, dumps

import ast
import collections
import linecache
import zlib
import weakref

import renpy

from renpy.display.transform import Transform, ATLTransform
from renpy.display.layout import Fixed
from renpy.display.predict import displayable as predict_displayable

from renpy.python import py_eval_bytecode
from renpy.pyanalysis import Analysis, NOT_CONST, LOCAL_CONST, GLOBAL_CONST, ccache

import hashlib
import time

# This file contains the abstract syntax tree for a screen language
# screen.

# A serial number that makes each SLNode unique.
serial = int(time.time() * 1000000)

# A sentinel used to indicate we should use the value found in the
# expression.
use_expression = renpy.object.Sentinel("use_expression")

# The filename that's currently being compiled.
filename = '<screen language>'

# A log that's used for profiling information.
profile_log = renpy.log.open("profile_screen", developer=True, append=False, flush=False)


def compile_expr(loc, node):
    """
    Wraps the node in a python AST, and compiles it.
    """

    filename = loc[0]
    if filename in renpy.python.py3_files:
        flags = renpy.python.py3_compile_flags
    else:
        flags = renpy.python.new_compile_flags

    expr = ast.Expression(body=node)
    renpy.python.fix_locations(expr, 1, 0)
    return compile(expr, filename, "eval", flags, True)

class SLContext(renpy.ui.Addable):
    """
    A context object that can be passed to the execute methods, and can also
    be placed in renpy.ui.stack.
    """

    def __init__(self, parent=None):
        if parent is not None:
            self.__dict__.update(parent.__dict__)
            return

        # The local scope that python code is evaluated in.
        self.scope = { } # type: dict[str, Any]

        # The scope of the top-level screen.
        self.root_scope = self.scope

        # The global scope that python code is evaluated in.
        self.globals = { } # type: dict[str, Any]

        # A list of child displayables that will be added to an outer
        # displayable.
        self.children = [ ] # type: list[renpy.display.core.Displayable]

        # A map from keyword arguments to their values.
        self.keywords = { } # type: Optional[dict[str, Any]]

        # The style prefix that is given to children of this displayable.
        self.style_prefix = None

        # A cache associated with this context. The cache maps from
        # statement serial to information associated with the statement.
        self.new_cache = { } # type: dict[Any, Any]

        # The old cache, used to take information from the old version of
        # this displayable.
        self.old_cache = { } # type: dict[Any, Any]

        # The miss cache, used to take information that isn't present in
        # old_cache.
        self.miss_cache = { } # type: dict[Any, Any]

        # The number of times a particular use statement has been called
        # in the current screen. We use this to generate a unique name for
        # each call site.
        self.use_index = collections.defaultdict(int)

        # When a constant node uses the scope, we add it to this list, so
        # it may be reused. (If None, no list is used.)
        self.uses_scope = None # type: Optional[list[Any]]

        # When a constant node has an id, we added it to this dict, so it
        # may be reused. (If None, no dict is used.)
        self.widgets = None # type: Optional[dict[str, Any]]

        # True if we should dump debug information to the profile log.
        self.debug = False

        # True if we're predicting the screen.
        self.predicting = False

        # True if we're updating the screen.
        self.updating = False

        # A list of nodes we've predicted, for cases where predicting more than
        # once could be a performance problem.
        self.predicted = set() # type: set[Any]

        # True if we're in a true showif block, False if we're in a false showif
        # block, or None if we're not in a showif block.
        self.showif = None # type: Optional[bool]

        # True if there was a failure in this statement or any of its children.
        # Fails can only occur when predicting, as otherwise an exception
        # would be thrown.
        self.fail = False

        # The parent context of a use statement with a block.
        self.parent = None # type: Any

        # The use statement containing the transcluded block.
        self.transclude = None # type: Any

        # True if it's unlikely this node will run. This is used in prediction
        # to speed things up.
        self.unlikely = False

        # The old and new generations of the use_cache.
        self.new_use_cache = { } # type: dict[Any, Any]
        self.old_use_cache = { } # type: dict[Any, Any]

    def add(self, d, key):
        self.children.append(d)

    def close(self, d):
        raise Exception("Spurious ui.close().")


class SLNode(object):
    """
    The base class for screen language nodes.
    """

    # The type of constant this node is.
    constant = GLOBAL_CONST

    # True if this node has at least one keyword that applies to its
    # parent. False otherwise.
    has_keyword = False

    # True if this node should be the last keyword parsed.
    last_keyword = False

    def __init__(self, loc):
        global serial
        serial += 1

        # A unique serial number assigned to this node.
        self.serial = serial

        # The location of this node, a (file, line) tuple.
        self.location = loc

    def instantiate(self, transclude):
        """
        Instantiates a new instance of this class, copying the global
        attributes of this class onto the new instance.
        """

        cls = type(self)

        rv = cls.__new__(cls)
        rv.serial = self.serial
        rv.location = self.location

        return rv

    def copy(self, transclude):
        """
        Makes a copy of this node.

        `transclude`
            The constness of transclude statements.
        """

        raise Exception("copy not implemented by " + type(self).__name__)

    def report_traceback(self, name, last):
        if last:
            return None

        filename, line = self.location

        return [ (filename, line, name, None) ]

    def analyze(self, analysis):
        """
        Performs static analysis on Python code used in this statement.
        """

        # By default, does nothing.

    def prepare(self, analysis):
        """
        This should be called before the execute code is called, and again
        after init-level code (like the code in a .rpym module or an init
        python block) is called.

        `analysis`
            A pyanalysis.Analysis object containing the analysis of this screen.
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

    def copy_on_change(self, cache):
        """
        Flags the displayables that are created by this node and its children
        as copy-on-change.
        """

        return

    def debug_line(self):
        """
        Writes information about the line we're on to the debug log.
        """

        filename, lineno = self.location
        full_filename = renpy.exports.unelide_filename(filename)

        line = linecache.getline(full_filename, lineno) or ""

        profile_log.write("  %s:%d %s", filename, lineno, line.rstrip())

        if self.constant:
            profile_log.write("    potentially constant")

    def used_screens(self, callback):
        """
        Calls callback with the name of each screen this node and its
        children use.
        """

        return

    def has_transclude(self):
        """
        Returns true if this node is a transclude or has a transclude as a child.
        """

        return False

    def has_python(self):
        """
        Returns true if this node is Python or has a python node as a child.
        """

        return False

    def dump_const(self, prefix):
        """
        Dumps a tree-representation of this node, to help determine what
        Ren'Py is treating as const and not.
        """

        raise Exception("dump_const not implemented by " + type(self).__name__)

    def dc(self, prefix, text, *args):
        """
        Adds a line of const dump information to the debug log.
        """

        if self.constant == GLOBAL_CONST:
            const_type = "global "
        elif self.constant == LOCAL_CONST:
            const_type = "local  "
        else:
            const_type = "not    "

        formatted = text.format(*args)

        profile_log.write("%s", "    {}{}{} ({}:{})".format(const_type, prefix, formatted, self.location[0], self.location[1]))


def analyze_keywords(node, analysis, conditional=GLOBAL_CONST):
    """
    Analyzes the keywords that can be applied to this statement,
    including those provided by if statements.
    """

    rv = GLOBAL_CONST

    for _, expr in node.keyword:
        rv = min(rv, analysis.is_constant_expr(expr), conditional)

    for n in node.children:
        if isinstance(n, SLIf):

            for cond, block in n.entries:
                if cond is not None:
                    conditional = min(conditional, analysis.is_constant_expr(cond))

                rv = min(rv, analyze_keywords(block, analysis, conditional))

    return rv


# A sentinel used to indicate a keyword argument was not given.
NotGiven = renpy.object.Sentinel("NotGiven")


class SLBlock(SLNode):
    """
    Represents a screen language block that can contain keyword arguments
    and child displayables.
    """

    # RawBlock from parse or None if not present.
    atl_transform = None

    # The actual transform created from the atl transform.
    transform = None

    def __init__(self, loc):
        SLNode.__init__(self, loc)

        # A list of keyword argument, expr tuples.
        self.keyword = [ ]

        # A list of child SLNodes.
        self.children = [ ]

    def instantiate(self, transclude):
        rv = SLNode.instantiate(self, transclude)
        rv.keyword = self.keyword # type: ignore
        rv.children = [ i.copy(transclude) for i in self.children ] # type: ignore
        rv.atl_transform = self.atl_transform # type: ignore

        return rv

    def copy(self, transclude):
        return self.instantiate(transclude)

    def analyze(self, analysis):

        for i in self.children:
            i.analyze(analysis)

    def prepare(self, analysis):

        for i in self.children:
            i.prepare(analysis)
            self.constant = min(self.constant, i.constant)

        # Compile the keywords.

        keyword_values = { }
        keyword_keys = [ ]
        keyword_exprs = [ ]

        for k, expr in self.keyword:

            node = ccache.ast_eval(expr)

            const = analysis.is_constant(node)

            if const == GLOBAL_CONST:
                keyword_values[k] = py_eval_bytecode(compile_expr(self.location, node))
            else:
                keyword_keys.append(ast.Str(s=k))
                keyword_exprs.append(node) # Will be compiled as part of ast.Dict below.

            self.constant = min(self.constant, const)

        if keyword_values:
            self.keyword_values = keyword_values
        else:
            self.keyword_values = None

        if keyword_keys:
            node = ast.Dict(keys=keyword_keys, values=keyword_exprs)
            ast.copy_location(node, keyword_exprs[0])
            self.keyword_exprs = compile_expr(self.location, node)
        else:
            self.keyword_exprs = None

        self.has_keyword = bool(self.keyword)
        self.keyword_children = [ ]

        if self.atl_transform is not None:
            self.has_keyword = True

            # We use screen analysis object, since it
            # have all knowlege about our constants
            self.atl_transform.mark_constant(analysis)

            # We can only be a constant if we do not rely
            # on screen arguments or other internal variables.
            # So we can pass an empty context for compilation.
            if self.atl_transform.constant == GLOBAL_CONST:
                self.atl_transform.compile_block()

            # Check constant again after compilation try,
            # this set its constant to NOT_CONST if failed.
            const = self.atl_transform.constant
            self.constant = min(self.constant, const)

            self.transform = renpy.display.transform.ATLTransform(self.atl_transform)
            renpy.atl.compile_queue.append(self.transform)

        was_last_keyword = False
        for i in self.children:
            if i.has_keyword:

                if was_last_keyword:
                    raise Exception("Properties are not allowed here.")

                self.keyword_children.append(i)
                self.has_keyword = True

            if i.last_keyword:
                self.last_keyword = True
                was_last_keyword = True
                if not renpy.config.developer:
                    break

    def execute(self, context):

        # Note: SLBlock.execute() is inlined in various locations for performance
        # reasons.

        for i in self.children:

            try:
                i.execute(context)
            except Exception:
                if not context.predicting:
                    raise

    def keywords(self, context):

        keyword_values = self.keyword_values

        if keyword_values is not None:
            context.keywords.update(keyword_values)

        keyword_exprs = self.keyword_exprs

        if keyword_exprs is not None:
            context.keywords.update(eval(keyword_exprs, context.globals, context.scope))

        for i in self.keyword_children:
            i.keywords(context)

        if self.atl_transform is not None:
            transform = ATLTransform(self.atl_transform, context=context.scope)
            transform.parent_transform = self.transform # type: ignore

            if "at" in context.keywords:
                try:
                    at_list = list(context.keywords["at"])
                except TypeError:
                    at_list = [ context.keywords["at"] ]

                at_list.append(transform)
                context.keywords["at"] = at_list
            else:
                context.keywords["at"] = transform

        style_prefix = context.keywords.pop("style_prefix", NotGiven)

        if style_prefix is NotGiven:
            style_prefix = context.keywords.pop("style_group", NotGiven)

        if style_prefix is not NotGiven:
            context.style_prefix = style_prefix

    def copy_on_change(self, cache):
        for i in self.children:
            i.copy_on_change(cache)

    def used_screens(self, callback):
        for i in self.children:
            i.used_screens(callback)

    def has_transclude(self):
        for i in self.children:
            if i.has_transclude():
                return True

        return False

    def has_python(self):
        return any(i.has_python() for i in self.children)

    def has_noncondition_child(self):
        """
        Returns true if this block has a child that is not an SLIf statement,
        or false otherwise.
        """

        worklist = list(self.children)

        while worklist:

            n = worklist.pop(0)

            if type(n) is SLBlock:
                worklist.extend(n.children)
            elif isinstance(n, SLIf):
                for _, block in n.entries:
                    worklist.append(block)
            else:
                return True

        return False

    def keyword_exist(self, name):
        """
        Returns true if this block or it's SLIf children have parsed `name` keyword,
        or false otherwise.
        """

        if name in dict(self.keyword):
            return True

        for n in self.children:

            if isinstance(n, SLIf):
                if n.keyword_exist(name):
                    return True

        return False

    def dump_const(self, prefix):
        self.dc(prefix, "block")

        for i in self.children:
            i.dump_const(prefix + "  ")


list_or_tuple = (list, tuple)


class SLCache(object):
    """
    The type of cache associated with an SLDisplayable.
    """

    def __init__(self):

        # The displayable object created.
        self.displayable = None # type: Optional[renpy.display.core.Displayable]

        # The positional arguments that were used to create the displayable.
        self.positional = None # type: Any

        # The keyword arguments that were used to created the displayable.
        self.keywords = None # type: Optional[dict[str, Any]]

        # A list of the children that were added to self.displayable.
        self.children = None # type: Optional[list[renpy.display.core.Displayable]]

        # The outermost old transform.
        self.outer_transform = None # type: Optional[Any]

        # The innermost old transform.
        self.inner_transform = None # type: Optional[Any]

        # The transform (or list of transforms) that was used to create self.transform.
        self.raw_transform = None # type: Optional[Any]

        # The imagemap stack entry we reuse.
        self.imagemap = None # type: Optional[Any]

        # If this can be represented as a single constant displayable,
        # do so.
        self.constant = None # type: Optional[Any]

        # For a constant statement, a list of our children that use
        # the scope.
        self.constant_uses_scope = [ ] # type: Optional[list[Any]]

        # For a constant statement, a map from children to widgets.
        self.constant_widgets = { } # type: dict[Any, Any]

        # True if the displayable should be re-created if its arguments
        # or children are changed.
        self.copy_on_change = False

        # The ShowIf this statement was wrapped in the last time it was wrapped.
        self.old_showif = None # type: Any

        # The SLUse that was transcluded by this SLCache statement.
        self.transclude = None # type: Any

        # The style prefix used when this statement was first created.
        self.style_prefix = None # type: Optional[str]


# A magic value that, if returned by a displayable function, is not added to
# the parent.
NO_DISPLAYABLE = renpy.display.layout.Null()


class SLDisplayable(SLBlock):
    """
    A screen language AST node that corresponds to a displayable being
    added to the tree.
    """

    hotspot = False
    variable = None
    name = ""

    unique = False

    # A list of variables that are locally constant.
    local_constant = [ ]

    def __init__(self, loc, displayable, scope=False, child_or_fixed=False, style=None, text_style=None, pass_context=False, imagemap=False, replaces=False, default_keywords={}, hotspot=False, variable=None, name="", unique=True):
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
            If given, the context is passed in as the first positional argument
            of the displayable.

        `imagemap`
            True if this is an imagemap, and should be handled as one.

        `hotspot`
            True if this is a hotspot that depends on the imagemap it was
            first displayed with.

        `replaces`
            True if the object this displayable replaces should be
            passed to it.

        `default_keywords`
            The default keyword arguments to supply to the displayable.

        `variable`
            A variable that the main displayable is assigned to.

        `name`
            The name of the displayable, used for debugging.
        """

        SLBlock.__init__(self, loc)

        self.displayable = displayable

        self.scope = scope
        self.child_or_fixed = child_or_fixed
        self.style = style
        self.pass_context = pass_context
        self.imagemap = imagemap
        self.hotspot = hotspot
        self.replaces = replaces
        self.default_keywords = default_keywords
        self.variable = variable
        self.unique = unique

        # Positional argument expressions.
        self.positional = [ ]

        self.name = name

    def copy(self, transclude):
        rv = self.instantiate(transclude)

        rv.displayable = self.displayable # type: ignore
        rv.scope = self.scope # type: ignore
        rv.child_or_fixed = self.child_or_fixed # type: ignore
        rv.style = self.style # type: ignore
        rv.pass_context = self.pass_context # type: ignore
        rv.imagemap = self.imagemap # type: ignore
        rv.hotspot = self.hotspot # type: ignore
        rv.replaces = self.replaces # type: ignore
        rv.default_keywords = self.default_keywords # type: ignore
        rv.variable = self.variable # type: ignore
        rv.positional = self.positional # type: ignore
        rv.name = self.name # type: ignore
        rv.unique = self.unique # type: ignore

        return rv

    def analyze(self, analysis):

        if self.imagemap:
            const = analyze_keywords(self, analysis)
            analysis.push_control(imagemap=(const != GLOBAL_CONST))

        if self.hotspot:
            self.constant = min(analysis.imagemap(), self.constant)

        SLBlock.analyze(self, analysis)

        if self.imagemap:
            analysis.pop_control()

        # If we use a scope, store the local constants that need to be
        # kept and placed into the scope.
        if self.scope:
            self.local_constant = list(analysis.local_constant)

        if self.variable is not None:
            const = self.constant

            for i in self.positional:
                const = min(self.constant, analysis.is_constant_expr(i))

            for _k, v in self.keyword:
                const = min(self.constant, analysis.is_constant_expr(v))

            if self.keyword_exist("id"):
                const = NOT_CONST

            if const == LOCAL_CONST:
                analysis.mark_constant(self.variable)
            elif const == NOT_CONST:
                analysis.mark_not_constant(self.variable)

    def prepare(self, analysis):

        SLBlock.prepare(self, analysis)

        # Prepare the positional arguments.

        exprs = [ ]
        values = [ ]
        has_exprs = False
        has_values = False

        for a in self.positional:
            node = ccache.ast_eval(a)

            const = analysis.is_constant(node)

            if const == GLOBAL_CONST:
                values.append(py_eval_bytecode(compile_expr(self.location, node)))
                exprs.append(ast.Num(n=0))
                has_values = True
            else:
                values.append(use_expression)
                exprs.append(node) # Will be compiled as part of the tuple.
                has_exprs = True

            self.constant = min(self.constant, const)

        if has_values:
            self.positional_values = values
        else:
            self.positional_values = None

        if has_exprs:
            t = ast.Tuple(elts=exprs, ctx=ast.Load())
            ast.copy_location(t, exprs[0])
            self.positional_exprs = compile_expr(self.location, t)
        else:
            self.positional_exprs = None

        # We do not pass keywords to our parents.
        self.has_keyword = False

        # We want to preserve last_keyword, however, in case we run a
        # python block.

        # If we have the id property, we're not constant - since we may get
        # additional keywords via id. (It's unlikely, but id should be pretty
        # rare.)
        if self.keyword_exist("id"):
            self.constant = NOT_CONST

        if self.variable is not None:
            self.constant = NOT_CONST

    def keywords(self, context):
        # We do not want to pass keywords to our parents, so just return.
        return

    def execute(self, context):

        debug = context.debug

        screen = renpy.ui.screen

        cache = context.old_cache.get(self.serial, None) or context.miss_cache.get(self.serial, None)

        if not isinstance(cache, SLCache):
            cache = SLCache()

        context.new_cache[self.serial] = cache

        copy_on_change = cache.copy_on_change

        if debug:
            self.debug_line()

        if cache.constant and (cache.style_prefix == context.style_prefix):

            for i, local_scope, context_scope in cache.constant_uses_scope:

                if context_scope is None:
                    context_scope = context.root_scope

                if local_scope:
                    scope = dict(context_scope)
                    scope.update(local_scope)
                else:
                    scope = context_scope

                if copy_on_change:
                    if i._scope(scope, False):
                        cache.constant = None
                        break
                else:
                    i._scope(scope, True)

            else:

                d = cache.constant

                if d is not NO_DISPLAYABLE:
                    if context.showif is not None:
                        d = self.wrap_in_showif(d, context, cache)

                    context.children.append(d)

                if context.uses_scope is not None:
                    context.uses_scope.extend(cache.constant_uses_scope)

                if debug:
                    profile_log.write("    reused constant displayable")

                return

        # Create the context.
        ctx = SLContext(context)

        # True if we encountered an exception that we're recovering from
        # due to being in prediction mode.
        fail = False

        # The main displayable we're predicting.
        main = None

        # True if we've pushed something onto the imagemap stack.
        imagemap = False

        # True if we're reusing a displayable.
        reused = False

        try:
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

            keywords = ctx.keywords = self.default_keywords.copy()

            if self.constant:
                ctx.uses_scope = [ ] # type: ignore

            SLBlock.keywords(self, ctx)

            arguments = keywords.pop("arguments", None)
            if arguments:
                positional += arguments

            properties = keywords.pop("properties", None)
            if properties:
                keywords.update(properties)

            # Get the widget id and transform, if any.
            widget_id = keywords.pop("id", None)
            transform = keywords.pop("at", None)
            prefer_screen_to_id = keywords.pop("prefer_screen_to_id", False)

            if widget_id and (widget_id in screen.widget_properties):

                if prefer_screen_to_id:
                    new_keywords = screen.widget_properties[widget_id].copy()
                    new_keywords.update(keywords)
                    keywords = new_keywords
                else:
                    keywords.update(screen.widget_properties[widget_id])

            # If we don't know the style, figure it out.
            style_suffix = keywords.pop("style_suffix", None) or self.style
            if ("style" not in keywords) and style_suffix:
                if ctx.style_prefix is None:
                    keywords["style"] = style_suffix
                else:
                    keywords["style"] = ctx.style_prefix + "_" + style_suffix

            old_d = cache.displayable
            if old_d:
                old_main = old_d._main or old_d
            else:
                old_main = None

            if debug:
                self.report_arguments(cache, positional, keywords, transform)

            can_reuse = (old_d is not None) and (positional == cache.positional) and (keywords == cache.keywords) and (context.style_prefix == cache.style_prefix)
            if (self.variable is not None) and copy_on_change:
                can_reuse = False

            # A hotspot can only be reused if the imagemap it belongs to has
            # not changed.
            if self.hotspot:

                imc = renpy.ui.imagemap_stack[-1]
                if cache.imagemap is not imc:
                    can_reuse = False

                cache.imagemap = imc

            if can_reuse:
                reused = True
                d = old_d

                # The main displayable, if d is a composite displayable. (This is
                # the one that gets the scope, and gets children added to it.)
                main = old_main

                if widget_id and not ctx.unlikely:
                    screen.widgets[widget_id] = main
                    screen.base_widgets[widget_id] = d

                if self.scope and main._uses_scope: # type: ignore
                    if copy_on_change:
                        if main._scope(ctx.scope, False): # type: ignore
                            reused = False
                    else:
                        main._scope(ctx.scope, True) # type: ignore

            if reused and self.imagemap:
                imagemap = True
                cache.imagemap.reuse()
                renpy.ui.imagemap_stack.append(cache.imagemap)

            if not reused:
                cache.positional = positional
                cache.keywords = keywords.copy()

                # This child creation code is copied below, for the copy_on_change
                # case.
                if self.scope:
                    keywords["scope"] = ctx.scope

                if self.replaces and ctx.updating:
                    keywords['replaces'] = old_main

                # Pass the context
                if self.pass_context:
                    keywords['context'] = ctx

                d = self.displayable(*positional, **keywords)
                d._unique()
                main = d._main or d

                main._location = self.location

                if widget_id and not ctx.unlikely:
                    screen.widgets[widget_id] = main
                    screen.base_widgets[widget_id] = d
                # End child creation code.

                imagemap = self.imagemap

                cache.copy_on_change = False # We no longer need to copy on change.
                cache.children = None # Re-add the children.

            if debug:
                if reused:
                    profile_log.write("    reused displayable")
                elif self.constant:
                    profile_log.write("    created constant displayable")
                else:
                    profile_log.write("    created displayable")

        except Exception:
            if not context.predicting:
                raise
            fail = True

        if self.variable is not None:
            context.scope[self.variable] = main

        ctx.children = [ ]
        ctx.showif = None

        stack = renpy.ui.stack
        stack.append(ctx) # type: ignore

        try:

            # Evaluate children. (Inlined SLBlock.execute)
            for i in self.children:
                try:
                    i.execute(ctx)
                except Exception:
                    if not context.predicting:
                        raise
                    fail = True

        finally:

            ctx.keywords = None

            stack.pop()

            if imagemap:
                cache.imagemap = renpy.ui.imagemap_stack.pop()
                cache.imagemap.cache.finish()

        # If a failure occurred during prediction, predict main (if known),
        # and ctx.children, and return.
        if fail:
            predict_displayable(main)

            for i in ctx.children:
                predict_displayable(i)

            context.fail = True

            return


        if ctx.children != cache.children:

            if reused and copy_on_change:

                keywords = keywords # type: ignore

                # This is a copy of the child creation code from above.
                if self.scope:
                    keywords["scope"] = ctx.scope

                if self.replaces and context.updating:
                    keywords['replaces'] = old_main # type: ignore

                if self.pass_context:
                    keywords['context'] = ctx

                d = self.displayable(*positional, **keywords) # type: ignore
                main = d._main or d

                main._location = self.location

                if widget_id: # type: ignore
                    screen.widgets[widget_id] = main
                    screen.base_widgets[widget_id] = d
                # End child creation code.

                cache.copy_on_change = False
                reused = False

            if reused:
                main._clear()

            if self.child_or_fixed and len(ctx.children) != 1:
                f = Fixed()

                for i in ctx.children:
                    f.add(i)

                main.add(f) # type: ignore

            else:
                for i in ctx.children:
                    main.add(i) # type: ignore

        d = d # type: ignore
        old_d = old_d # type: ignore

        # Inform the focus system about replacement displayables.
        if (not context.predicting) and (old_d is not None):
            replaced_by = renpy.display.focus.replaced_by
            replaced_by[id(old_d)] = d

            if d is not main:
                for old_part, new_part in zip(old_d._composite_parts, d._composite_parts):
                    replaced_by[id(old_part)] = new_part

        cache.displayable = d
        cache.children = ctx.children
        cache.style_prefix = context.style_prefix

        if not transform:
            transform = None

        if (transform is not None) and (d is not NO_DISPLAYABLE):
            if reused and (transform == cache.raw_transform):

                if isinstance(cache.inner_transform, renpy.display.transform.Transform):
                    if cache.inner_transform.child is not d:
                        cache.inner_transform.set_child(d, duplicate=False)

                d = cache.outer_transform

            else:
                old_outer_transform = cache.outer_transform

                cache.raw_transform = transform
                cache.inner_transform = None
                cache.outer_transform = None

                if isinstance(transform, Transform):
                    d = transform(child=d)
                    d._unique()

                    cache.inner_transform = d
                    cache.outer_transform = d

                elif isinstance(transform, list_or_tuple):
                    for t in transform:
                        if isinstance(t, Transform):
                            d = t(child=d)

                            cache.outer_transform = d
                            if cache.inner_transform is None:
                                cache.inner_transform = d

                        else:
                            d = t(d)
                            cache.raw_transform = None
                            cache.outer_transform = None
                            cache.inner_transform = None

                        d._unique()

                else:
                    d = transform(d)
                    d._unique()
                    cache.raw_transform = None
                    cache.outer_transform = None
                    cache.inner_transform = None

                if isinstance(d, Transform):

                    if not context.updating:
                        old_outer_transform = None

                    d.take_state(old_outer_transform)
                    d.take_execution_state(old_outer_transform)

        else:
            cache.inner_transform = None
            cache.outer_transform = None
            cache.raw_transform = None

        if ctx.fail:
            context.fail = True

        else:
            if self.constant:
                cache.constant = d

                if self.scope and main._uses_scope:

                    local_scope = { }

                    for i in self.local_constant:
                        if i in ctx.scope:
                            local_scope[i] = ctx.scope[i]

                    if ctx.scope is context.root_scope:
                        ctx.uses_scope.append((main, local_scope, None))
                    else:
                        ctx.uses_scope.append((main, local_scope, ctx.scope))

                cache.constant_uses_scope = ctx.uses_scope

                if context.uses_scope is not None:
                    context.uses_scope.extend(ctx.uses_scope)

        if d is not NO_DISPLAYABLE:

            if context.showif is not None:
                d = self.wrap_in_showif(d, context, cache)

            context.children.append(d)

    def wrap_in_showif(self, d, context, cache):
        """
        Wraps `d` in a ShowIf displayable.
        """

        rv = renpy.sl2.sldisplayables.ShowIf(context.showif, cache.old_showif)
        rv.add(d)

        if not context.predicting:
            cache.old_showif = rv

        return rv

    def report_arguments(self, cache, positional, keywords, transform):
        if positional:
            report = [ ]

            values = self.positional_values or ([ use_expression ] * len(positional))

            for i in range(len(positional)):

                if values[i] is not use_expression:
                    report.append("const")
                elif cache.positional is None:
                    report.append("new")
                elif cache.positional[i] == positional[i]:
                    report.append("equal")
                else:
                    report.append("not-equal")

            profile_log.write("    args: %s", " ".join(report))

        values = self.keyword_values or { }

        if keywords:
            report = { }

            if cache.keywords is None:
                for k in keywords:

                    if k in values:
                        report[k] = "const"
                        continue

                    report[k] = "new"

            else:
                for k in keywords:
                    k = str(k)

                    if k in values:
                        report[k] = "const"
                        continue

                    if k not in cache.keywords:
                        report[k] = "new-only"
                        continue

                    if keywords[k] == cache.keywords[k]:
                        report[k] = "equal"
                    else:
                        report[k] = "not-equal"

                for k in cache.keywords:
                    if k not in keywords:
                        report[k] = "old-only"

            profile_log.write("    kwargs: %r", report)

        if transform is not None:
            if "at" in values:
                profile_log.write("    at: const")
            elif cache.raw_transform is None:
                profile_log.write("    at: new")
            elif cache.raw_transform == transform:
                profile_log.write("    at: equal")
            else:
                profile_log.write("    at: not-equal")

    def copy_on_change(self, cache):
        c = cache.get(self.serial, None)

        if isinstance(c, SLCache):
            c.copy_on_change = True

        for i in self.children:
            i.copy_on_change(cache)

    def dump_const(self, prefix):
        self.dc(prefix, self.name)

        for i in self.children:
            i.dump_const(prefix + "  ")


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

    def copy(self, transclude):
        rv = self.instantiate(transclude)

        rv.entries = [ (expr, block.copy(transclude)) for expr, block in self.entries ]

        return rv

    def analyze(self, analysis):

        const = GLOBAL_CONST

        for cond, _block in self.entries:
            if cond is not None:
                const = min(const, analysis.is_constant_expr(cond))

        analysis.push_control(const)

        for _cond, block in self.entries:
            block.analyze(analysis)

        analysis.pop_control()

    def prepare(self, analysis):

        # A list of prepared entries, with each consisting of expression
        # bytecode and a SLBlock.
        self.prepared_entries = [ ]

        for cond, block in self.entries:
            if cond is not None:
                node = ccache.ast_eval(cond)

                cond_const = analysis.is_constant(node)
                self.constant = min(self.constant, cond_const)

                cond = compile_expr(self.location, node)
            else:
                cond_const = True

            block.prepare(analysis)
            self.constant = min(self.constant, block.constant)
            self.prepared_entries.append((cond, block, cond_const))

            self.has_keyword |= block.has_keyword
            self.last_keyword |= block.last_keyword

    def execute(self, context):

        if context.predicting:
            self.execute_predicting(context)
            return

        for cond, block, _cond_const in self.prepared_entries:
            if cond is None or eval(cond, context.globals, context.scope):
                for i in block.children:
                    i.execute(context)
                return

    def execute_predicting(self, context):
        # A variant of the this code that runs while predicting, executing
        # all paths of the if.

        # True if no block has been the main choice yet.
        first = True


        # Should we predict false branches?
        predict_false = self.serial not in context.predicted
        context.predicted.add(self.serial)


        for cond, block, const_cond in self.prepared_entries:
            try:
                cond_value = (cond is None) or eval(cond, context.globals, context.scope)
            except Exception:
                cond_value = False

            # The taken branch.
            if first and cond_value:
                first = False

                for i in block.children:
                    try:
                        i.execute(context)
                    except Exception:
                        pass

                if const_cond:
                    break

            elif predict_false:

                ctx = SLContext(context)
                ctx.children = [ ]
                ctx.unlikely = True

                for i in block.children:
                    try:
                        i.execute(ctx)
                    except Exception:
                        pass

                for i in ctx.children:
                    predict_displayable(i)



    def keywords(self, context):

        for cond, block, _cond_const in self.prepared_entries:
            if cond is None or eval(cond, context.globals, context.scope):
                block.keywords(context)
                return

    def copy_on_change(self, cache):
        for _cond, block in self.entries:
            block.copy_on_change(cache)

    def used_screens(self, callback):
        for _cond, block in self.entries:
            block.used_screens(callback)

    def has_transclude(self):
        for _cond, block in self.entries:
            if block.has_transclude():
                return True

        return False

    def has_python(self):
        return any(i[1].has_python() for i in self.entries)

    def keyword_exist(self, name):
        return any(i[1].keyword_exist(name) for i in self.entries)

    def dump_const(self, prefix):

        first = True

        for cond, block in self.entries:

            if first:
                self.dc(prefix, "if {}", cond)
            else:
                self.dc(prefix, "elif {}", cond)

            first = False

            for i in block.children:
                i.dump_const(prefix + "  ")

class SLShowIf(SLNode):
    """
    The AST node that corresponds to the showif statement.
    """

    def __init__(self, loc):
        """
        An AST node that represents an if statement.
        """
        SLNode.__init__(self, loc)

        # A list of entries, with each consisting of an expression (or
        # None, for the else block) and a SLBlock.
        self.entries = [ ]

    def copy(self, transclude):
        rv = self.instantiate(transclude)

        rv.entries = [ (expr, block.copy(transclude)) for expr, block in self.entries ]

        return rv

    def analyze(self, analysis):

        for _cond, block in self.entries:
            block.analyze(analysis)

    def prepare(self, analysis):

        # A list of prepared entries, with each consisting of expression
        # bytecode and a SLBlock.
        self.prepared_entries = [ ]

        for cond, block in self.entries:
            if cond is not None:
                node = ccache.ast_eval(cond)

                self.constant = min(self.constant, analysis.is_constant(node))

                cond = compile_expr(self.location, node)

            block.prepare(analysis)
            self.constant = min(self.constant, block.constant)
            self.prepared_entries.append((cond, block))

        self.last_keyword = True

    def execute(self, context):

        # This is true when the block should be executed - when no outer
        # showif is False, and when no prior block in this showif has
        # executed.
        first_true = context.showif is not False

        for cond, block in self.prepared_entries:

            ctx = SLContext(context)

            if not first_true:
                ctx.showif = False
            else:
                if cond is None or eval(cond, context.globals, context.scope):
                    ctx.showif = True
                    first_true = False
                else:
                    ctx.showif = False

            for i in block.children:
                i.execute(ctx)

            if ctx.fail:
                context.fail = True

    def copy_on_change(self, cache):
        for _cond, block in self.entries:
            block.copy_on_change(cache)

    def used_screens(self, callback):
        for _cond, block in self.entries:
            block.used_screens(callback)

    def has_transclude(self):
        for _cond, block in self.entries:
            if block.has_transclude():
                return True

        return False

    def has_python(self):
        return any(i[1].has_python() for i in self.entries)

    def dump_const(self, prefix):

        first = True

        for cond, block in self.entries:

            if first:
                self.dc(prefix, "showif {}", cond)
            else:
                self.dc(prefix, "else {}", cond)

            first = False

            for i in block.children:
                i.dump_const(prefix + "  ")

class SLFor(SLBlock):
    """
    The AST node that corresponds to a for statement. This only supports
    simple for loops that assign a single variable.
    """

    index_expression = None

    def __init__(self, loc, variable, expression, index_expression):
        SLBlock.__init__(self, loc)

        self.variable = variable
        self.expression = expression
        self.index_expression = index_expression

    def copy(self, transclude):
        rv = self.instantiate(transclude)

        rv.variable = self.variable # type: ignore
        rv.expression = self.expression # type: ignore
        rv.index_expression = self.index_expression # type: ignore

        return rv

    def analyze(self, analysis):

        const = analysis.is_constant_expr(self.expression) == GLOBAL_CONST

        while True:

            if const:
                analysis.push_control(True, loop=True)
                analysis.mark_constant(self.variable)
            else:
                analysis.push_control(False, loop=True)
                analysis.mark_not_constant(self.variable)

            SLBlock.analyze(self, analysis)

            new_const = analysis.control.const

            analysis.pop_control()

            if new_const == const:
                break

            const = new_const

    def prepare(self, analysis):
        node = ccache.ast_eval(self.expression)

        const = analysis.is_constant(node)

        if const == GLOBAL_CONST:
            self.expression_value = list(py_eval_bytecode(compile_expr(self.location, node)))
            self.expression_expr = None
        else:
            self.expression_value = None
            self.expression_expr = compile_expr(self.location, node)

        self.constant = min(self.constant, const)

        SLBlock.prepare(self, analysis)

        self.last_keyword = True

    def execute(self, context):

        variable = self.variable
        expr = self.expression_expr

        try:
            if expr is not None:
                value = eval(expr, context.globals, context.scope)
            else:
                value = self.expression_value
        except Exception:
            if not context.predicting:
                raise

            value = [ 0 ]

        newcaches = { }

        oldcaches = context.old_cache.get(self.serial, newcaches) or { }

        if not isinstance(oldcaches, dict):
            oldcaches = { }

        misscaches = context.miss_cache.get(self.serial, newcaches) or { }

        if not isinstance(misscaches, dict):
            misscaches = { }

        ctx = SLContext(context)

        for index, v in enumerate(value): # type: ignore

            ctx.scope[variable] = v

            children_i = iter(self.children)

            # If we have a variable expression as a tuple, it is necessary
            # to execute the first child before evaluating the index value,
            # because the index can be one of this tuple member.
            if variable == "_sl2_i":
                sl_python = next(children_i)
                # It can only fail if the unpacking fails, but it can still
                try:
                    sl_python.execute(ctx)
                except Exception:
                    if not context.predicting:
                        raise

            if self.index_expression is not None:
                index = eval(self.index_expression, ctx.globals, ctx.scope)

            ctx.old_cache = oldcaches.get(index, None) or { }

            if not isinstance(ctx.old_cache, dict):
                ctx.old_cache = {}

            ctx.miss_cache = misscaches.get(index, None) or { }

            if not isinstance(ctx.miss_cache, dict):
                ctx.miss_cache = {}

            newcaches[index] = ctx.new_cache = { }

            # Inline of SLBlock.execute.

            try:
                for i in children_i:
                    try:
                        i.execute(ctx)
                    except SLForException:
                        raise
                    except Exception:
                        if not context.predicting:
                            raise
            except SLBreakException:
                break
            except SLContinueException:
                continue

            if context.unlikely:
                break

        context.new_cache[self.serial] = newcaches

        if ctx.fail:
            context.fail = True

    def keywords(self, context):
        return

    def copy_on_change(self, cache):
        c = cache.get(self.serial, None)

        if not isinstance(c, dict):
            return

        for child_cache in c.values():
            for i in self.children:
                i.copy_on_change(child_cache)

    def dump_const(self, prefix):

        self.dc(prefix, "for {} in {}", self.variable, self.expression)

        for i in self.children:
            i.dump_const(prefix + "  ")

class SLForException(Exception): pass

class SLBreakException(SLForException): pass

class SLContinueException(SLForException): pass

class SLBreak(SLNode):

    def analyze(self, analysis):
        analysis.exit_loop()

    def execute(self, context):
        raise SLBreakException()

    def copy(self, transclude):
        rv = self.instantiate(transclude)

        return rv

    def dump_const(self, prefix):
        self.dc(prefix, "break")

class SLContinue(SLNode):

    def analyze(self, analysis):
        analysis.exit_loop()

    def execute(self, context):
        raise SLContinueException()

    def copy(self, transclude):
        rv = self.instantiate(transclude)

        return rv

    def dump_const(self, prefix):
        self.dc(prefix, "continue")

class SLPython(SLNode):

    def __init__(self, loc, code):
        SLNode.__init__(self, loc)

        # A pycode object.
        self.code = code

    def copy(self, transclude):
        rv = self.instantiate(transclude)

        rv.code = self.code

        return rv

    def analyze(self, analysis):
        analysis.python(self.code.source)

    def execute(self, context):
        exec(self.code.bytecode, context.globals, context.scope)

    def prepare(self, analysis):
        self.constant = NOT_CONST
        self.last_keyword = True

    def has_python(self):
        return True

    def dump_const(self, prefix):
        self.dc(prefix, "python")


class SLPass(SLNode):

    def execute(self, context):
        return

    def copy(self, transclude):
        rv = self.instantiate(transclude)

        return rv

    def dump_const(self, prefix):
        self.dc(prefix, "pass")


class SLDefault(SLNode):

    def __init__(self, loc, variable, expression):
        SLNode.__init__(self, loc)

        self.variable = variable
        self.expression = expression

    def copy(self, transclude):
        rv = self.instantiate(transclude)

        rv.variable = self.variable
        rv.expression = self.expression

        return rv

    def analyze(self, analysis):
        analysis.mark_not_constant(self.variable)

    def prepare(self, analysis):
        self.expr = compile_expr(self.location, ccache.ast_eval(self.expression))
        self.constant = NOT_CONST
        self.last_keyword = True

    def execute(self, context):
        scope = context.scope
        variable = self.variable

        if variable in scope:
            return

        scope[variable] = eval(self.expr, context.globals, scope)

    def has_python(self):
        return True

    def dump_const(self, prefix):
        self.dc(prefix, "default {} = {}", self.variable, self.expression)

class SLUse(SLNode):

    id = None
    block = None

    def __init__(self, loc, target, args, id_expr, block):

        SLNode.__init__(self, loc)

        # The name of the screen we're accessing.
        self.target = target

        # If the target is an SL2 screen, the SLScreen node at the root of
        # the ast for that screen.
        self.ast = None

        # If arguments are given, those arguments.
        self.args = args

        # An expression, if the id property is given.
        self.id = id_expr

        # A block for transclusion, or None if the statement does not have a
        # block.
        self.block = block

    def copy(self, transclude):

        rv = self.instantiate(transclude)

        rv.target = self.target
        rv.args = self.args
        rv.id = self.id

        if self.block is not None:
            rv.block = self.block.copy(transclude)
        else:
            rv.block = None

        rv.ast = None

        return rv

    def analyze(self, analysis):

        self.last_keyword = True

        if self.id:
            self.constant = NOT_CONST

        if self.block:
            self.block.analyze(analysis)

    def prepare(self, analysis):

        self.ast = None

        if self.block:
            self.block.prepare(analysis)

            if self.block.constant == GLOBAL_CONST:
                const = True
            else:
                const = False
        else:
            const = True

        if isinstance(self.target, renpy.ast.PyExpr):

            self.constant = NOT_CONST
            const = False
            self.ast = None

        else:

            target = renpy.display.screen.get_screen_variant(self.target)

            if target is None:
                self.constant = NOT_CONST

                if renpy.config.developer:
                    raise Exception("A screen named {} does not exist.".format(self.target))
                else:
                    return

            if target.ast is None:
                self.constant = NOT_CONST
                return

            if const:
                self.ast = target.ast.const_ast
            else:
                self.ast = target.ast.not_const_ast

            self.constant = min(self.constant, self.ast.constant)


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

        if isinstance(self.target, renpy.ast.PyExpr):

            target_name = eval(self.target, context.globals, context.scope)
            target = renpy.display.screen.get_screen_variant(target_name)

            if target is None:
                raise Exception("A screen named {} does not exist.".format(target_name))

            ast = target.ast.not_const_ast

            id_prefix = "_use_expression"

        else:
            id_prefix = self.target
            ast = self.ast

        # If self.ast is not an SL2 screen, run it using renpy.display.screen.use_screen.
        if ast is None:
            self.execute_use_screen(context)
            return

        # Otherwise, run the use statement directly.

        # Figure out the cache to use.

        ctx = SLContext(context)
        ctx.new_cache = context.new_cache[self.serial] = { "ast" : ast }
        ctx.miss_cache = context.miss_cache.get(self.serial, None) or { }

        if self.id:

            use_id = (id_prefix, eval(self.id, context.globals, context.scope))

            ctx.old_cache = context.old_use_cache.get(use_id, None) or context.old_cache.get(self.serial, None) or { }

            ctx.new_use_cache[use_id] = ctx.new_cache

        else:

            ctx.old_cache = context.old_cache.get(self.serial, None) or { }


        if not isinstance(ctx.old_cache, dict):
            ctx.old_cache = { }
        if not isinstance(ctx.miss_cache, dict):
            ctx.miss_cache = { }

        # Evaluate the arguments.
        try:
            if self.args:
                args, kwargs = self.args.evaluate(context.scope)
            else:
                args = [ ]
                kwargs = { }
        except Exception:
            if not context.predicting:
                raise

            args = [ ]
            kwargs = { }

        scope = ctx.old_cache.get("scope", None) or ctx.miss_cache.get("scope", None) or { }
        if not ctx.updating:
            scope.clear()

        # Apply the arguments to the parameters (if present) or to the scope of the used screen.
        if ast.parameters is not None:
            new_scope = ast.parameters.apply(args, kwargs, ignore_errors=context.predicting)

            scope.update(new_scope)

        else:

            if args:
                raise Exception("Screen {} does not take positional arguments. ({} given)".format(self.target, len(args)))

            scope.clear()
            scope.update(context.scope)
            scope.update(kwargs)

        scope["_scope"] = scope
        ctx.new_cache["scope"] = scope

        # Run the child screen.
        ctx.scope = scope
        ctx.parent = weakref.ref(context)

        ctx.transclude = self.block

        try:
            ast.execute(ctx)
        finally:
            del scope["_scope"]

        if ctx.fail:
            context.fail = True

    def copy_on_change(self, cache):

        c = cache.get(self.serial, None)

        if c is None:
            return

        ast = c.get("ast", None)

        if ast is not None:
            ast.copy_on_change(c)

    def used_screens(self, callback):
        if not isinstance(self.target, renpy.ast.PyExpr):
            callback(self.target)

        if self.block is not None:
            self.block.used_screens(callback)

    def has_transclude(self):
        if self.block:
            return self.block.has_transclude()
        else:
            return False

    def dump_const(self, prefix):
        self.dc(prefix, "use", self.target)

        for i in self.ast.children:
            if self.block:
                i.dump_const(prefix + "│ ")
            else:
                i.dump_const(prefix + "  ")

        if self.block:
            self.dc(prefix, "└ (transclude block)")
            for i in self.block.children:
                i.dump_const(prefix + "  ")

class SLTransclude(SLNode):

    def __init__(self, loc):
        SLNode.__init__(self, loc)

    def copy(self, transclude):
        rv = self.instantiate(transclude)
        rv.constant = transclude
        return rv

    def execute(self, context):

        if not context.transclude:
            return

        parent = context.parent
        if parent is not None:
            parent = parent()

        ctx = SLContext(parent)
        ctx.new_cache = context.new_cache[self.serial] = { }
        ctx.old_cache = context.old_cache.get(self.serial, None) or { }
        ctx.miss_cache = context.miss_cache.get(self.serial, None) or { }
        ctx.uses_scope = context.uses_scope

        if not isinstance(ctx.old_cache, dict):
            ctx.old_cache = { }
        if not isinstance(ctx.miss_cache, dict):
            ctx.miss_cache = { }

        ctx.new_cache["transclude"] = context.transclude

        ctx.children = context.children
        ctx.showif = context.showif

        try:
            renpy.ui.stack.append(ctx) # type: ignore
            context.transclude.keywords(ctx)
            context.transclude.execute(ctx)
        finally:
            renpy.ui.stack.pop()

        if ctx.fail:
            context.fail = True

    def copy_on_change(self, cache):

        c = cache.get(self.serial, None)

        if c is None or "transclude" not in c:
            return

        SLBlock.copy_on_change(c["transclude"], c)

    def has_transclude(self):
        return True

    def dump_const(self, prefix):
        self.dc(prefix, "transclude")

class SLCustomUse(SLNode):
    """This represents special use screen statement defined
    by renpy.register_sl_statement.
    """

    def __init__(self, loc, target, positional, block):

        SLNode.__init__(self, loc)

        # The name of the screen we're accessing.
        self.target = target

        # The SL2 SLScreen node at the root of the ast for that screen.
        self.ast = None

        # Positional argument expressions.
        self.positional = positional

        # A block for transclusion, from which we also take kwargs.
        self.block = block

    def copy(self, transclude):

        rv = self.instantiate(transclude)

        rv.target = self.target
        rv.ast = None

        rv.positional = self.positional
        rv.block = self.block.copy(transclude)

        return rv

    def analyze(self, analysis):

        self.last_keyword = True

        self.block.analyze(analysis)

    def prepare(self, analysis):

        block = self.block

        block.prepare(analysis)

        # Figure out the ast we want to use.
        target = renpy.display.screen.get_screen_variant(self.target)

        if target is None:
            self.constant = NOT_CONST

            if renpy.config.developer:
                raise Exception("A screen named {} does not exist.".format(self.target))
            else:
                return

        if target.ast is None:
            self.constant = NOT_CONST

            if renpy.config.developer:
                raise Exception("A screen used in CD SLS should be a SL-based screen.")
            else:
                return

        # If we have the id property, we're not constant - since we may get
        # our state via other screen on replace.
        if block.keyword_exist("id"):
            self.constant = NOT_CONST
            self.ast = target.ast.not_const_ast

        elif block.constant == GLOBAL_CONST:
            self.ast = target.ast.const_ast
        else:
            self.ast = target.ast.not_const_ast

        self.constant = min(self.constant, self.ast.constant)

    def execute(self, context):

        # Figure out the cache to use.
        ctx = SLContext(context)
        ctx.new_cache = context.new_cache[self.serial] = { }
        ctx.miss_cache = context.miss_cache.get(self.serial, None) or { }

        # Evaluate the arguments to use in screen.
        try:
            args = [eval(i, context.globals, context.scope) for i in self.positional]

            kwargs = ctx.keywords = {}

            self.block.keywords(ctx)

            arguments = kwargs.pop("arguments", None)
            if arguments:
                args += arguments

            properties = kwargs.pop("properties", None)
            if properties:
                kwargs.update(properties)

            # If we don't know the style, figure it out.
            style_suffix = kwargs.pop("style_suffix", None)
            if ("style" not in kwargs) and style_suffix:
                if ctx.style_prefix is None:
                    kwargs["style"] = style_suffix
                else:
                    kwargs["style"] = ctx.style_prefix + "_" + style_suffix

        except Exception:
            if not context.predicting:
                raise

            args = [ ]
            kwargs = { }

        # Get the id and deal with replacement algorithm.
        id = kwargs.pop("id", None)
        if id is not None:

            use_id = (self.target, id)

            ctx.old_cache = context.old_use_cache.get(use_id, None) or context.old_cache.get(self.serial, None) or { }

            ctx.new_use_cache[use_id] = ctx.new_cache

        else:

            ctx.old_cache = context.old_cache.get(self.serial, None) or { }

        if not isinstance(ctx.old_cache, dict):
            ctx.old_cache = { }
        if not isinstance(ctx.miss_cache, dict):
            ctx.miss_cache = { }

        ast = self.ast

        scope = ctx.old_cache.get("scope", None) or ctx.miss_cache.get("scope", None) or { }
        if not ctx.updating:
            scope.clear()

        # Apply the arguments to the parameters (if present) or to the scope of the used screen.
        if ast.parameters is not None:
            new_scope = ast.parameters.apply(args, kwargs, ignore_errors=context.predicting)

            scope.update(new_scope)

        else:

            if args:
                raise Exception("Screen {} does not take positional arguments. ({} given)".format(self.target, len(args)))

            scope.clear()
            scope.update(context.scope)
            scope.update(kwargs)

        scope["_scope"] = scope
        ctx.new_cache["scope"] = scope

        # Run the child screen.
        ctx.scope = scope
        ctx.parent = weakref.ref(context)

        # If we have any children, pass them to (possible) transclude
        if self.block.children:
            ctx.transclude = self.block

        try:
            ast.execute(ctx)
        finally:
            del scope["_scope"]

        if ctx.fail:
            context.fail = True

    def copy_on_change(self, cache):

        c = cache.get(self.serial, None)
        if c is None:
            return

        self.ast.copy_on_change(c)

    def used_screens(self, callback):
        callback(self.target)

        if self.block is not None:
            self.block.used_screens(callback)


    def has_transclude(self):
        return self.block.has_transclude()


    def dump_const(self, prefix):
        self.dc(prefix, "custom-use", self.target)

        for i in self.ast.children:
            if self.block:
                i.dump_const(prefix + "│ ")
            else:
                i.dump_const(prefix + "  ")

        if self.block:
            self.dc("prefix", "└ (transclude block)")
            for i in self.block.children:
                i.dump_const(prefix + "  ")


class SLScreen(SLBlock):
    """
    This represents a screen defined in the screen language 2.
    """

    version = 0

    # This screen's AST when the transcluded block is entirely
    # constant (or there is no transcluded block at all). This may be
    # the actual AST, or a copy.
    const_ast = None

    # A copy of this screen's AST when the transcluded block is not
    # constant.
    not_const_ast = None

    # The analysis
    analysis = None

    layer = "'screens'"
    sensitive = "True"
    roll_forward = "None"

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

        # Should this screen be sensitive.
        self.sensitive = "True"

        # The parameters this screen takes.
        self.parameters = None

        # The analysis object used for this screen, if the screen has
        # already been analyzed.
        self.analysis = None

        # True if this screen has been prepared.
        self.prepared = False

    def copy(self, transclude):
        rv = self.instantiate(transclude) # type: ignore

        rv.name = self.name # type: ignore
        rv.modal = self.modal # type: ignore
        rv.zorder = self.zorder # type: ignore
        rv.tag = self.tag # type: ignore
        rv.variant = self.variant # type: ignore
        rv.predict = self.predict # type: ignore
        rv.parameters = self.parameters # type: ignore
        rv.sensitive = self.sensitive # type: ignore

        rv.prepared = False # type: ignore
        rv.analysis = None # type: ignore

        return rv

    def define(self, location):
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
            location=self.location,
            layer=renpy.python.py_eval(self.layer),
            sensitive=self.sensitive,
            roll_forward=renpy.python.py_eval(self.roll_forward),
            )

    def analyze(self, analysis):

        SLBlock.analyze(self, analysis)

    def analyze_screen(self):

        # Have we already been analyzed?
        if self.const_ast:
            return

        key = (self.name, self.variant, self.location)

        if key in scache.const_analyzed:
            self.const_ast = scache.const_analyzed[key]
            self.not_const_ast = scache.not_const_analyzed[key]
            return

        self.const_ast = self

        if self.has_transclude():
            self.not_const_ast = self.copy(NOT_CONST)
            self.not_const_ast.const_ast = self.not_const_ast # type: ignore
            targets = [ self.const_ast, self.not_const_ast ]
        else:
            self.not_const_ast = self.const_ast
            targets = [ self.const_ast ]

        for ast in targets:
            analysis = ast.analysis = Analysis(None)

            if ast.parameters:
                analysis.parameters(ast.parameters)

            ast.analyze(analysis)

            while not analysis.at_fixed_point():
                ast.analyze(analysis)

        scache.const_analyzed[key] = self.const_ast
        scache.not_const_analyzed[key] = self.not_const_ast
        scache.updated = True

    def unprepare_screen(self):
        self.prepared = False

    def prepare_screen(self):

        if self.prepared:
            return

        self.analyze_screen()

        # This version ensures we're not using the cache from an old
        # version of the screen.
        self.version += 1

        self.const_ast.prepare(self.const_ast.analysis)

        if self.not_const_ast is not self.const_ast:
            self.not_const_ast.prepare(self.not_const_ast.analysis) # type: ignore

        self.prepared = True

        if renpy.display.screen.get_profile(self.name).const:
            profile_log.write("CONST ANALYSIS %s", self.name)

            new_constants = [ i for i in self.const_ast.analysis.global_constant if i not in renpy.pyanalysis.constants ]
            new_constants.sort()
            profile_log.write('    global_const: %s', " ".join(new_constants))

            local_constants = list(self.const_ast.analysis.local_constant)
            local_constants.sort()
            profile_log.write('    local_const: %s', " ".join(local_constants))

            not_constants = list(self.const_ast.analysis.not_constant)
            not_constants.sort()
            profile_log.write('    not_const: %s', " ".join(not_constants))

            profile_log.write('')

            self.const_ast.dump_const("")

            profile_log.write('')

    def execute(self, context):
        self.const_ast.keywords(context)
        SLBlock.execute(self.const_ast, context) # type: ignore

    def report_traceback(self, name, last):
        if last:
            return None

        if name == "__call__":
            return [ ]

        return SLBlock.report_traceback(self, name, last)

    def copy_on_change(self, cache):
        SLBlock.copy_on_change(self.const_ast, cache) # type: ignore

    def __call__(self, *args, **kwargs):
        scope = kwargs["_scope"]
        debug = kwargs.get("_debug", False)

        if self.parameters:

            args = scope.get("_args", ())
            kwargs = scope.get("_kwargs", { })

            values = renpy.ast.apply_arguments(self.parameters, args, kwargs, ignore_errors=renpy.display.predict.predicting)
            scope.update(values)

        if not self.prepared:
            self.prepare_screen()

        current_screen = renpy.display.screen.current_screen()

        if current_screen.screen_name[0] in renpy.config.profile_screens:
            debug = True

        context = SLContext()

        context.scope = scope
        context.root_scope = scope
        context.globals = renpy.python.store_dicts["store"]
        context.debug = debug
        context.predicting = renpy.display.predict.predicting
        context.updating = (current_screen.phase == renpy.display.screen.UPDATE)

        name = scope["_name"]

        def get_cache(d):
            rv = d.get(name, None)

            if (not isinstance(rv, dict)) or (rv.get("version", None) != self.version):
                rv = { "version" : self.version }
                d[name] = rv

            return rv

        context.old_cache = get_cache(current_screen.cache)
        context.miss_cache = get_cache(current_screen.miss_cache)
        context.new_cache = { "version" : self.version }

        context.old_use_cache = current_screen.use_cache
        context.new_use_cache = { }

        # This really executes self.const_ast.
        self.execute(context)

        for i in context.children:
            renpy.ui.implicit_add(i)

        current_screen.cache[name] = context.new_cache
        current_screen.use_cache = context.new_use_cache


class ScreenCache(object):

    def __init__(self):
        self.version = 1

        self.const_analyzed = { }
        self.not_const_analyzed = { }

        self.updated = False


scache = ScreenCache()

CACHE_FILENAME = "cache/screens.rpyb"


def load_cache():
    if renpy.game.args.compile: # type: ignore
        return

    try:
        with renpy.loader.load(CACHE_FILENAME) as f:
            digest = f.read(hashlib.md5().digest_size)
            if digest != renpy.game.script.digest.digest():
                return

            s = loads(zlib.decompress(f.read()))

        if s.version == scache.version:
            renpy.game.script.update_bytecode()
            scache.const_analyzed.update(s.const_analyzed)
            scache.not_const_analyzed.update(s.not_const_analyzed)

    except Exception:
        pass


def save_cache():
    if not scache.updated:
        return

    if renpy.macapp:
        return

    try:
        data = zlib.compress(dumps(scache), 3)

        with open(renpy.loader.get_path(CACHE_FILENAME), "wb") as f:
            f.write(renpy.game.script.digest.digest())
            f.write(data)
    except Exception:
        pass
