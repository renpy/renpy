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

from __future__ import (
    division,
    absolute_import,
    with_statement,
    print_function,
    unicode_literals,
    annotations,
)
from collections.abc import Callable, Iterable
from types import CodeType
from typing import Any, cast, override
from renpy.compat import (
    PY2,
    basestring,
    bchr,
    bord,
    chr,
    open,
    pystr,
    range,
    round,
    str,
    tobytes,
    unicode,
)  # *


import builtins

import renpy  # @UnusedImport
from renpy.python import py_compile

# Import the Python AST module, instead of the Ren'Py ast module.
import ast

import zlib

from renpy.compat.pickle import loads, dumps

# The set of names that should be treated as constants.
always_constants = {"True", "False", "None"}

# fmt: off
# The set of names that should be treated as pure functions.
pure_functions = {
    # Python 3 builtins.
    'abs', 'all', 'any', 'ascii', 'bin', 'bool', 'bytes', 'callable',
    'chr', 'complex', 'dict', 'dir', 'divmod', 'enumerate', 'filter', 'float',
    'format', 'frozenset', 'getattr', 'hasattr', 'hash', 'hex', 'int',
    'isinstance', 'issubclass', 'len', 'list', 'map', 'max', 'min', 'oct',
    'ord', 'pow', 'range', 'repr', 'reversed', 'round', 'set', 'slice', 'sorted',
    'str', 'sum', 'tuple', 'type', 'zip',

    # minstore.py
    "_",
    "_p",
    "absolute",
    "position",
    "__renpy__list__",
    "__renpy__dict__",
    "__renpy__set__",

    # defaultstore.py
    "ImageReference", "Image", "Frame", "Solid", "LiveComposite", "LiveCrop",
    "LiveTile", "Flatten", "Null", "Window", "Viewport", "DynamicDisplayable",
    "ConditionSwitch", "ShowingSwitch", "Transform", "Animation", "Movie",
    "Particles", "SnowBlossom", "Text", "ParameterizedText", "FontGroup",
    "Drag", "Alpha", "AlphaMask", "Position", "Pan", "Move", "Motion", "Revolve", "Zoom",
    "RotoZoom", "FactorZoom", "SizeZoom", "Fade", "Dissolve", "ImageDissolve",
    "AlphaDissolve", "CropMove", "PushMove", "Pixellate", "OldMoveTransition",
    "MoveTransition", "MoveFactory", "MoveIn", "MoveOut", "ZoomInOut",
    "RevolveInOut", "MultipleTransition", "ComposeTransition", "Pause",
    "SubTransition", "ADVSpeaker", "ADVCharacter", "Speaker", "Character",
    "DynamicCharacter", "Fixed", "HBox", "VBox", "Grid", "AlphaBlend", "At",
    "color", "Color",

    # ui.py

    "ui.returns",
    "ui.jumps",
    "ui.jumpsoutofcontext",
    "ui.callsinnewcontext",
    "ui.invokesinnewcontext",
    "ui.gamemenus",

    # renpy.py

    "renpy.version_string",
    "renpy.version_only",
    "renpy.version_tuple",
    "renpy.version_name",
    "renpy.license",
}
# fmt: on

constants = {"config", "style"} | always_constants | pure_functions

# A set of names that should not be treated as global constants.
not_constants: set[str] = set()

# The base set for the local constants.
local_constants: set[str] = set()


def const(name: str):
    """
    :doc: const

    Declares a variable in the store to be constant.

    A variable is constant if nothing can change its value, or any value
    reached by indexing it or accessing its attributes. Variables must
    remain constant out of define, init, and translate python blocks.

    `name`
        A string giving the name of the variable to declare constant.
    """

    if name not in not_constants:
        constants.add(name)


def not_const(name: str):
    """
    :doc: const

    Declares a name in the store to be not constant.

    This undoes the effect of calls to :func:`renpy.const` and
    :func:`renpy.pure`.

    `name`
        The name to declare not constant.
    """

    constants.discard(name)
    pure_functions.discard(name)
    not_constants.add(name)


def pure(fn: str | Callable[..., Any]):
    """
    :doc: const

    Declares a function as pure. A pure function must always return the
    same value when it is called with the same arguments, outside of
    define, init, and translate python blocks.

    `fn`
        The name of the function to declare pure. This may either be a string
        containing the name of the function, or the function itself.
        If a string is passed and the function is inside a module,
        this string should contain the module name with the dot.

    Returns `fn`, allowing this function to be used as a decorator.
    """

    name = fn

    if isinstance(name, Callable):
        name = cast(str, fn.__name__)

        module = fn.__module__
        name = f"{module}.{name}"

    if name.startswith("store."):
        name = name[6:]

    if name not in not_constants:
        pure_functions.add(name)
        constants.add(name)

    return fn


class Control(object):
    """
    Represents control flow.

    `const`
        True if this statement always executes.

    `loop`
        True if this corresponds to a loop.

    `imagemap`
        True if this control is in a non-constant imagemap.
    """

    def __init__(self, const: bool, loop: bool, imagemap: bool):
        self.const: bool = const
        self.loop: bool = loop
        self.imagemap: bool = imagemap

    @override
    def __repr__(self):
        return "<Control const={0} loop={1} imagemap={2}>".format(
            self.const, self.loop, self.imagemap
        )


# Three levels of constness.

# An expression is globally constant if it will evaluate to the same value
# whenever it is run.
GLOBAL_CONST = 2

# An expression is locally const if it will evaluate to the same value when
# run in the same place - the same screen, with the same parameters, the same
# statement, and the same iteration of a for loop.
LOCAL_CONST = 1

# An expression is not const if it wilk change it's value.
NOT_CONST = 0


class DeltaSet[T](object):

    def __init__(self, base: set[T], copy: DeltaSet[T] | None = None):
        """
        Represents a set that stores its contents as differences from a base
        set.
        """

        self.base: set[T] = base

        if copy is not None:
            self.added: set[T] = set(copy.added)
            self.removed: set[T] = set(copy.removed)
        else:
            self.added = set()
            self.removed = set()

        self.changed: bool = False

    def add(self, v: T):

        if v in self.removed:
            self.removed.discard(v)
            self.changed = True
        elif v not in self.base and v not in self.added:
            self.added.add(v)
            self.changed = True

    def discard(self, v: T):

        if v in self.added:
            self.added.discard(v)
            self.changed = True
        elif v in self.base and v not in self.removed:
            self.removed.add(v)
            self.changed = True

    def __contains__(self, v: T):
        return (v in self.added) or ((v in self.base) and (v not in self.removed))

    def copy(self):
        return DeltaSet(self.base, self)

    def __iter__(self):

        for i in self.base:
            if i not in self.removed:
                yield i

        for i in self.added:
            yield i


class Analysis(object):
    """
    Represents the result of code analysis, and provides tools to perform
    code analysis.
    """

    def __init__(self, parent: Analysis | None = None):

        # The parent context transcludes run in, or None if there is no parent
        # context.
        self.parent: Analysis | None = parent

        # Analyses of children, such a screens we use.
        self.children: dict[str, Analysis] = {}

        # The variables we consider to be not-constant.
        self.not_constant: DeltaSet[str] = DeltaSet(not_constants)

        # Variables we consider to be locally constant.
        self.local_constant: DeltaSet[str] = DeltaSet(local_constants)

        # Variables we consider to be globally constant.
        self.global_constant: DeltaSet[str] = DeltaSet(always_constants)

        # The functions we consider to be pure.
        self.pure_functions: DeltaSet[str] = DeltaSet(pure_functions)

        # Represents what we know about the current control.
        self.control: Control = Control(True, False, False)

        # The stack of const_flow values.
        self.control_stack: list[Control] = [self.control]

    def get_child(self, identifier: str):
        if identifier in self.children:
            return self.children[identifier]

        rv = Analysis(self)
        self.children[identifier] = rv

        return rv

    def push_control(
        self, const: bool = True, loop: bool = False, imagemap: bool = False
    ):
        self.control = Control(
            self.control.const and const,
            loop,
            self.control.imagemap or imagemap,
        )
        self.control_stack.append(self.control)  # type: ignore

    def pop_control(self):
        rv = self.control_stack.pop()
        self.control = self.control_stack[-1]
        return rv

    def imagemap(self):
        """
        Returns NOT_CONST if we're in a non-constant imagemap.
        """

        if self.control.imagemap:
            return NOT_CONST
        else:
            return GLOBAL_CONST

    def exit_loop(self):
        """
        Call this to indicate the current loop is being exited by the
        continue or break statements.
        """

        l = list(self.control_stack)
        l.reverse()

        for i in l:
            i.const = False

            if i.loop:
                break

    def at_fixed_point(self):
        """
        Returns True if we've reached a fixed point, where the analysis has
        not changed since the last time we called this function.
        """

        for i in self.children.values():
            if not i.at_fixed_point():
                return False

        if (
            self.not_constant.changed
            or self.global_constant.changed
            or self.local_constant.changed
            or self.pure_functions.changed
        ):

            self.not_constant.changed = False
            self.global_constant.changed = False
            self.local_constant.changed = False
            self.pure_functions.changed = False

            return False

        return True

    def mark_constant(self, name: str):
        """
        Marks `name` as a potential local constant.
        """

        if not name in self.not_constant:
            self.local_constant.add(name)
            self.global_constant.discard(name)
            self.pure_functions.discard(name)

    def mark_not_constant(self, name: str):
        """
        Marks `name` as definitely not-constant.
        """

        self.not_constant.add(name)

        self.pure_functions.discard(name)
        self.local_constant.discard(name)
        self.global_constant.discard(name)

    def _check_name(self, node: ast.AST) -> tuple[int, str | None]:
        """
        Check nodes that make up a name. This returns a pair:

        * The first element is True if the node is constant, and False
            otherwise.
        * The second element is None if the node is constant or the name is
            not known, and the name otherwise.
        """

        if isinstance(node, ast.Name):
            const = NOT_CONST
            name = node.id

        elif isinstance(node, ast.Attribute):
            const, name = self._check_name(node.value)

            if name is not None:
                name = f"{name}.{node.attr}"

        else:
            return self._check_node(node), None

        if name in self.not_constant:
            return NOT_CONST, name
        elif name in self.global_constant:
            return GLOBAL_CONST, name
        elif name in self.local_constant:
            return LOCAL_CONST, name
        else:
            return const, name

    def _check_nodes(self, nodes: Iterable[ast.AST | None]):
        """
        Checks a list of nodes for constness.
        """

        nodes = list(nodes)

        if not nodes:
            return GLOBAL_CONST

        return min(self._check_node(i) for i in nodes)

    def _check_node(self, node: ast.AST | None) -> int:
        """
        When given `node`, part of a Python expression, returns how
        const the expression is.
        """

        # This handles children that do not exist.
        if node is None:
            return GLOBAL_CONST

        # PY3: see if there are new node types.

        if isinstance(node, ast.Constant):
            return GLOBAL_CONST

        elif isinstance(node, ast.BoolOp):
            return self._check_nodes(node.values)

        elif isinstance(node, ast.NamedExpr):
            return self._check_node(node.value)

        elif isinstance(node, ast.BinOp):
            return min(
                self._check_node(node.left),
                self._check_node(node.right),
            )

        elif isinstance(node, ast.UnaryOp):
            return self._check_node(node.operand)

        # ast.Lambda is NOT_CONST.

        elif isinstance(node, ast.IfExp):
            return min(
                self._check_node(node.test),
                self._check_node(node.body),
                self._check_node(node.orelse),
            )

        elif isinstance(node, ast.Dict):
            return min(self._check_nodes(node.keys), self._check_nodes(node.values))

        elif isinstance(node, ast.Set):
            return self._check_nodes(node.elts)

        # ast.ListComp is NOT_CONST.
        # ast.SetComp is NOT_CONST.
        # ast.DictComp is NOT_CONST.

        # ast.GeneratorExp is NOT_CONST.

        # ast.Await is NOT_CONST.
        # ast.Yield is NOT_CONST.
        # ast.YieldFrom is NOT_CONST.

        elif isinstance(node, ast.Compare):
            return min(
                self._check_node(node.left),
                self._check_nodes(node.comparators),
            )

        elif isinstance(node, ast.Call):
            const, name = self._check_name(node.func)

            # The function must have a name, and must be declared pure.
            if (const != GLOBAL_CONST) or (name not in self.pure_functions):
                return NOT_CONST

            return min(
                self._check_nodes(node.args),
                self._check_nodes(i.value for i in node.keywords),
            )

        elif isinstance(node, ast.FormattedValue):
            return min(
                self._check_node(node.value),
                self._check_node(node.format_spec),
            )

        elif isinstance(node, ast.JoinedStr):
            return self._check_nodes(node.values)

        elif isinstance(node, (ast.Attribute, ast.Name)):
            return self._check_name(node)[0]

        elif isinstance(node, ast.Subscript):
            return min(
                self._check_node(node.value),
                self._check_node(node.slice),
            )

        elif isinstance(node, ast.Starred):
            return self._check_node(node.value)

        elif isinstance(node, (ast.List, ast.Tuple)):
            return self._check_nodes(node.elts)

        elif isinstance(node, ast.Slice):
            return min(
                self._check_node(node.lower),
                self._check_node(node.upper),
                self._check_node(node.step),
            )

        return NOT_CONST

    def is_constant(self, node: ast.AST):
        """
        Returns true if `node` is constant for the purpose of screen
        language. Node should be a python AST node.

        Screen language ignores object identity for the purposes of
        object equality.
        """

        return self._check_node(node) != NOT_CONST

    def is_constant_expr(self, expr: str | renpy.ast.PyExpr | ast.Module):
        """
        Compiles `expr` into an AST node, then returns the result of
        self.is_constant called on that node.
        """

        node, literal = cast(tuple[ast.AST, bool], ccache.ast_eval_literal(expr))

        if literal:
            return GLOBAL_CONST
        else:
            return self.is_constant(node)

    def python(self, code: str):
        """
        Performs analysis on a block of python code.
        """

        nodes = ccache.ast_exec(code)

        a = PyAnalysis(self)

        for i in nodes:  # pyright: ignore[reportGeneralTypeIssues]
            a.visit(cast(ast.AST, i))

    def parameters(self, parameters):
        """
        Analyzes the parameters to the screen.
        """

        self.global_constant = DeltaSet(constants)

        # As we have parameters, analyze with those parameters.

        for name in parameters.parameters:
            self.mark_not_constant(name)


class PyAnalysis(ast.NodeVisitor):
    """
    This analyzes Python code to determine which variables should be
    marked const, and which should be marked non-const.
    """

    def __init__(self, analysis: Analysis):
        self.analysis: Analysis = analysis

    # Expressions that assign names
    @override
    def visit_Name(self, node: ast.Name):
        if isinstance(node.ctx, ast.AugStore):
            self.analysis.mark_not_constant(node.id)

        elif isinstance(node.ctx, ast.Store):
            if self.analysis.control.const:
                self.analysis.mark_constant(node.id)
            else:
                self.analysis.mark_not_constant(node.id)

    @override
    def visit_NamedExpr(self, node: ast.NamedExpr):

        const = self.analysis.is_constant(node.value)
        self.analysis.push_control(const, False)

        self.generic_visit(node)

        self.analysis.pop_control()

    # Statements that assign names or control constness.
    @override
    def visit_FunctionDef(self, node: ast.FunctionDef):
        self.analysis.mark_constant(node.name)

    @override
    def visit_AsyncFunctionDef(self, node: ast.AsyncFunctionDef):
        self.analysis.mark_constant(node.name)

    @override
    def visit_ClassDef(self, node: ast.ClassDef):
        self.analysis.mark_constant(node.name)

    # Return can't assign a name.

    # Delete doesn't assign a name - so it would be something else making
    # the name non-const, not delete.

    @override
    def visit_Assign(self, node: ast.Assign):
        const = self.analysis.is_constant(node.value)
        self.analysis.push_control(const, False)

        self.generic_visit(node)

        self.analysis.pop_control()

    @override
    def visit_AugAssign(self, node: ast.AugAssign):

        self.analysis.push_control(False, False)

        self.generic_visit(node)

        self.analysis.pop_control()

    @override
    def visit_AnnAssign(self, node: ast.AnnAssign):
        const = self.analysis.is_constant(cast(ast.AST, node.value))
        self.analysis.push_control(const, False)

        self.generic_visit(node)

        self.analysis.pop_control()

    @override
    def visit_For(self, node: ast.For | ast.AsyncFor):
        const = self.analysis.is_constant(node.iter)

        self.analysis.push_control(const=const, loop=True)
        old_const = self.analysis.control.const

        self.generic_visit(node)  # All nodes in the loop depend on node.test.

        if self.analysis.control.const != old_const:
            self.generic_visit(node)

        self.analysis.pop_control()

    @override
    def visit_AsyncFor(self, node: ast.AsyncFor):
        return self.visit_For(node)

    @override
    def visit_While(self, node: ast.While):
        const = self.analysis.is_constant(node.test)

        self.analysis.push_control(const=const, loop=True)
        old_const = self.analysis.control.const

        self.generic_visit(node)  # All nodes in the loop depend on node.test.

        if self.analysis.control.const != old_const:
            self.generic_visit(node)

        self.analysis.pop_control()

    @override
    def visit_If(self, node: ast.If):
        const = self.analysis.is_constant(node.test)
        self.analysis.push_control(const, False)

        self.generic_visit(node)

        self.analysis.pop_control()

    # Nothing special for visit_With or visit_AsyncWith, when withitem is
    # defined as below.

    @override
    def visit_withitem(self, node: ast.withitem):

        const = self.analysis.is_constant(node.context_expr)
        self.visit(node.context_expr)

        self.analysis.push_control(const, False)

        if node.optional_vars is not None:
            self.visit(node.optional_vars)

        self.analysis.pop_control()

    # Match is barely implemented. We assume that it's always going to be
    # performed on something non-constant, which means that every variable
    # assigned inside the match is also non-constant. This is probably a
    # reasonable assumption.
    @override
    def visit_MatchMapping(self, node: ast.MatchMapping):
        if node.rest:
            self.analysis.mark_not_constant(node.rest)

    @override
    def visit_MatchStar(self, node: ast.MatchStar):
        if node.name is not None:
            self.analysis.mark_not_constant(node.name)

    @override
    def visit_MatchAs(self, node: ast.MatchAs):
        if node.name is not None:
            self.analysis.mark_not_constant(node.name)

    @override
    def visit_Try(self, node: ast.Try):
        for i in node.handlers:
            if i.name:
                self.analysis.mark_not_constant(i.name)

        self.generic_visit(node)

    # Import and Import from can only assign to a variable in a way that
    # keeps it constant.

    # Global and NonLocal only make sense inside Python functions, and we don't
    # analyze Python functions.

    # Expr can be ignored, as it can't assign.

    # The continue and break statements should be pretty rare, so if they
    # occur, we mark everything later in the loop as non-const.
    @override
    def visit_Break(self, node: ast.Break):
        self.analysis.exit_loop()

    @override
    def visit_Continue(self, node: ast.Continue):
        self.analysis.exit_loop()


class CompilerCache(object):
    """
    Objects of this class are used to cache the compilation of Python code.
    """

    def __init__(self):
        self.ast_eval_cache: dict[
            tuple[str | renpy.ast.PyExpr | ast.Module, str | None, int | None],
            tuple[str | renpy.ast.PyExpr | ast.Module, bool],
        ] = {}
        self.ast_exec_cache: dict[
            tuple[str | renpy.ast.PyExpr | ast.Module, str | None, int | None],
            ast.AST | None,
        ] = {}

        # True if we've changed the caches.
        self.updated: bool = False

        # The version of this object.
        self.version: int = 1

    def ast_eval_literal(self, expr: str | renpy.ast.PyExpr | ast.Module):
        """
        Compiles an expression into an AST.
        """

        if isinstance(expr, renpy.ast.PyExpr):
            filename = expr.filename
            linenumber = expr.linenumber
        else:
            filename = None
            linenumber = None

        key = (expr, filename, linenumber)

        rv = self.ast_eval_cache.get(key, None)

        if rv is None:
            expr = py_compile(
                expr, "eval", ast_node=True
            )  # pyright: ignore[reportAssignmentType]

            try:
                ast.literal_eval(expr)
                literal = True
            except Exception:
                literal = False

            rv = (expr, literal)

            self.ast_eval_cache[key] = rv
            self.updated = True

        new_ccache.ast_eval_cache[key] = rv

        return rv

    def ast_eval(self, expr: str | renpy.ast.PyExpr | ast.Module):
        return self.ast_eval_literal(expr)[0]

    def ast_exec(self, code: str | renpy.ast.PyExpr | ast.Module):
        """
        Compiles a block into an AST.
        """

        if isinstance(code, renpy.ast.PyExpr):
            key = (code, code.filename, code.linenumber)
        else:
            key = (code, None, None)

        rv: ast.AST | None = self.ast_exec_cache.get(key, None)

        if rv is None:
            rv = cast(ast.AST, py_compile(code, "exec", ast_node=True))
            self.ast_exec_cache[key] = rv
            self.updated = True

        new_ccache.ast_exec_cache[key] = rv

        return rv


ccache = CompilerCache()
new_ccache = CompilerCache()

CACHE_FILENAME = "cache/py3analysis.rpyb"


def load_cache():
    if renpy.game.args.compile:  # type: ignore
        return

    try:
        with renpy.loader.load(CACHE_FILENAME) as f:
            c = loads(zlib.decompress(f.read()))

        if c.version == ccache.version:
            ccache.ast_eval_cache.update(c.ast_eval_cache)
            ccache.ast_exec_cache.update(c.ast_exec_cache)
    except Exception:
        pass


def save_cache():
    if not ccache.updated:
        return

    if renpy.macapp:
        return

    try:
        data = zlib.compress(dumps(new_ccache, True), 3)

        with open(renpy.loader.get_path(CACHE_FILENAME), "wb") as f:
            f.write(data)
    except Exception:
        pass
