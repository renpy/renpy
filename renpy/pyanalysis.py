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

from __future__ import division, absolute_import, with_statement, print_function, unicode_literals
from renpy.compat import PY2, basestring, bchr, bord, chr, open, pystr, range, round, str, tobytes, unicode  # *


import builtins

import renpy
from renpy.python import py_compile

# Import the Python AST module, instead of the Ren'Py ast module.
import ast

import operator
import zlib

from renpy.compat.pickle import loads, dumps

# The set of names that should be treated as constants.
always_constants = {"True", "False", "None"}

# The set of names that should be treated as pure functions.
pure_functions = {
    # Python 3 builtins.
    "abs",
    "all",
    "any",
    "ascii",
    "bin",
    "bool",
    "bytes",
    "callable",
    "chr",
    "complex",
    "dict",
    "dir",
    "divmod",
    "enumerate",
    "filter",
    "float",
    "format",
    "frozenset",
    "getattr",
    "hasattr",
    "hash",
    "hex",
    "int",
    "isinstance",
    "issubclass",
    "len",
    "list",
    "map",
    "max",
    "min",
    "oct",
    "ord",
    "pow",
    "range",
    "repr",
    "reversed",
    "round",
    "set",
    "slice",
    "sorted",
    "str",
    "sum",
    "tuple",
    "type",
    "zip",
    # minstore.py
    "_",
    "_p",
    "absolute",
    "position",
    "__renpy__list__",
    "__renpy__dict__",
    "__renpy__set__",
    # defaultstore.py
    "ImageReference",
    "Image",
    "Frame",
    "Solid",
    "LiveComposite",
    "LiveCrop",
    "LiveTile",
    "Flatten",
    "Null",
    "Window",
    "Viewport",
    "DynamicDisplayable",
    "ConditionSwitch",
    "ShowingSwitch",
    "Transform",
    "Animation",
    "Movie",
    "Particles",
    "SnowBlossom",
    "Text",
    "ParameterizedText",
    "FontGroup",
    "Drag",
    "Alpha",
    "AlphaMask",
    "Position",
    "Pan",
    "Move",
    "Motion",
    "Revolve",
    "Zoom",
    "RotoZoom",
    "FactorZoom",
    "SizeZoom",
    "Fade",
    "Dissolve",
    "ImageDissolve",
    "AlphaDissolve",
    "CropMove",
    "PushMove",
    "Pixellate",
    "OldMoveTransition",
    "MoveTransition",
    "MoveFactory",
    "MoveIn",
    "MoveOut",
    "ZoomInOut",
    "RevolveInOut",
    "MultipleTransition",
    "ComposeTransition",
    "Pause",
    "SubTransition",
    "ADVSpeaker",
    "ADVCharacter",
    "Speaker",
    "Character",
    "DynamicCharacter",
    "Fixed",
    "HBox",
    "VBox",
    "Grid",
    "AlphaBlend",
    "At",
    "color",
    "Color",
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

constants = {"config", "style"} | always_constants | pure_functions

# A set of names that should not be treated as global constants.
not_constants = set()

# The base set for the local constants.
local_constants = set()


def const(name):
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


def not_const(name):
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


def pure(fn):
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

    if not isinstance(name, str):
        name = fn.__qualname__

        module = fn.__module__
        name = module + "." + name

    if name.startswith("store."):
        name = name[6:]

    if name not in not_constants:
        pure_functions.add(name)
        constants.add(name)

    return fn


def import_from(from_module_name, in_module_name, *names):
    """
    This function is called after each `from from_module import name` statement,
    to make sure that if `from_module.name` is a const / pure value, `in_module.name` is marked const / pure as well.

    Also, if `name.subname` is const / pure, we also need to make sure that `in_module.name.subname` is correctly marked.

    `names` are 2-tuples of `(original name, imported as name)`.
    """
    if from_module_name.startswith("store."):
        from_module_name = from_module_name[6:]

    if in_module_name.startswith("store."):
        in_module_name = in_module_name[6:]

    for name, asname in names:
        from_fullname = f"{from_module_name}.{name}"

        if from_fullname in not_constants:
            continue

        imported_fullname = f"{in_module_name}.{asname}"

        if from_fullname in pure_functions:
            pure(imported_fullname)
        elif from_fullname in constants:
            const(imported_fullname)

        else:
            from_fullname_dot = f"{from_fullname}."
            prefix_size = len(from_fullname_dot)

            for subname in tuple(filter(lambda c: c.startswith(from_fullname_dot), constants)):
                imported_subname = f"{imported_fullname}.{subname[prefix_size:]}"

                if subname in pure_functions:
                    pure(imported_subname)
                else:
                    const(imported_subname)


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

    def __init__(self, const, loop, imagemap):
        self.const = const
        self.loop = loop
        self.imagemap = imagemap

    def __repr__(self):
        return "<Control const={0} loop={1} imagemap={2}>".format(self.const, self.loop, self.imagemap)


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


class DeltaSet(object):
    def __init__(self, base, copy=None):
        """
        Represents a set that stores its contents as differences from a base
        set.
        """

        self.base = base

        if copy is not None:
            self.added = set(copy.added)
            self.removed = set(copy.removed)
        else:
            self.added = set()
            self.removed = set()

        self.changed = False

    def add(self, v):
        if v in self.removed:
            self.removed.discard(v)
            self.changed = True
        elif v not in self.base and v not in self.added:
            self.added.add(v)
            self.changed = True

    def discard(self, v):
        if v in self.added:
            self.added.discard(v)
            self.changed = True
        elif v in self.base and v not in self.removed:
            self.removed.add(v)
            self.changed = True

    def __contains__(self, v):
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

    def __init__(self, parent=None):
        # The parent context transcludes run in, or None if there is no parent
        # context.
        self.parent = parent

        # Analyses of children, such a screens we use.
        self.children = {}

        # The variables we consider to be not-constant.
        self.not_constant = DeltaSet(not_constants)

        # Variables we consider to be locally constant.
        self.local_constant = DeltaSet(local_constants)

        # Variables we consider to be globally constant.
        self.global_constant = DeltaSet(always_constants)

        # The functions we consider to be pure.
        self.pure_functions = DeltaSet(pure_functions)

        # Represents what we know about the current control.
        self.control = Control(True, False, False)

        # The stack of const_flow values.
        self.control_stack = [self.control]

    def get_child(self, identifier):
        if identifier in self.children:
            return self.children[identifier]

        rv = Analysis(self)
        self.children[identifier] = rv

        return rv

    def push_control(self, const=True, loop=False, imagemap=False):
        self.control = Control(self.control.const and const, loop, self.control.imagemap or imagemap)
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

    def mark_constant(self, name):
        """
        Marks `name` as a potential local constant.
        """

        if not name in self.not_constant:
            self.local_constant.add(name)
            self.global_constant.discard(name)
            self.pure_functions.discard(name)

    def mark_not_constant(self, name):
        """
        Marks `name` as definitely not-constant.
        """

        self.not_constant.add(name)

        self.pure_functions.discard(name)
        self.local_constant.discard(name)
        self.global_constant.discard(name)

    def _check_name(self, node):
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
                name = name + "." + node.attr

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

    def _check_nodes(self, nodes):
        """
        Checks a list of nodes for constness.
        """

        nodes = list(nodes)

        if not nodes:
            return GLOBAL_CONST

        return min(self._check_node(i) for i in nodes)

    def _check_node(self, node):
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

    def is_constant(self, node):
        """
        Returns true if `node` is constant for the purpose of screen
        language. Node should be a python AST node.

        Screen language ignores object identity for the purposes of
        object equality.
        """

        return self._check_node(node)

    def is_constant_expr(self, expr):
        """
        Compiles `expr` into an AST node, then returns the result of
        self.is_constant called on that node.
        """

        node, literal = ccache.ast_eval_literal(expr)

        if literal:
            return GLOBAL_CONST
        else:
            return self.is_constant(node)

    def python(self, code):
        """
        Performs analysis on a block of python code.
        """

        nodes = ccache.ast_exec(code)

        a = PyAnalysis(self)

        for i in nodes:
            a.visit(i)

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

    def __init__(self, analysis):
        self.analysis = analysis

    # Expressions that assign names.
    def visit_Name(self, node):
        if isinstance(node.ctx, ast.AugStore):
            self.analysis.mark_not_constant(node.id)

        elif isinstance(node.ctx, ast.Store):
            if self.analysis.control.const:
                self.analysis.mark_constant(node.id)
            else:
                self.analysis.mark_not_constant(node.id)

    def visit_NamedExpr(self, node):
        const = self.analysis.is_constant(node.value)
        self.analysis.push_control(const, False)

        self.generic_visit(node)

        self.analysis.pop_control()

    # Statements that assign names or control constness.
    def visit_FunctionDef(self, node):
        self.analysis.mark_constant(node.name)

    def visit_AsyncFunctionDef(self, node):
        self.analysis.mark_constant(node.name)

    def visit_ClassDef(self, node):
        self.analysis.mark_constant(node.name)

    # Return can't assign a name.

    # Delete doesn't assign a name - so it would be something else making
    # the name non-const, not delete.

    def visit_Assign(self, node):
        const = self.analysis.is_constant(node.value)
        self.analysis.push_control(const, False)

        self.generic_visit(node)

        self.analysis.pop_control()

    def visit_AugAssign(self, node):
        self.analysis.push_control(False, False)

        self.generic_visit(node)

        self.analysis.pop_control()

    def visit_AnnAssign(self, node):
        const = self.analysis.is_constant(node.value)
        self.analysis.push_control(const, False)

        self.generic_visit(node)

        self.analysis.pop_control()

    def visit_For(self, node):  # type: (ast.For|ast.AsyncFor) -> None
        const = self.analysis.is_constant(node.iter)

        self.analysis.push_control(const=const, loop=True)
        old_const = self.analysis.control.const

        self.generic_visit(node)  # All nodes in the loop depend on node.test.

        if self.analysis.control.const != old_const:
            self.generic_visit(node)

        self.analysis.pop_control()

    def visit_AsyncFor(self, node):
        return self.visit_For(node)

    def visit_While(self, node):
        const = self.analysis.is_constant(node.test)

        self.analysis.push_control(const=const, loop=True)
        old_const = self.analysis.control.const

        self.generic_visit(node)  # All nodes in the loop depend on node.test.

        if self.analysis.control.const != old_const:
            self.generic_visit(node)

        self.analysis.pop_control()

    def visit_If(self, node):
        const = self.analysis.is_constant(node.test)
        self.analysis.push_control(const, False)

        self.generic_visit(node)

        self.analysis.pop_control()

    # Nothing special for visit_With or visit_AsyncWith, when withitem is
    # defined as below.

    def visit_withitem(self, node):
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
    def visit_MatchMapping(self, node):
        if node.rest:
            self.analysis.mark_not_constant(node.rest)

    def visit_MatchStar(self, node):
        if node.name is not None:
            self.analysis.mark_not_constant(node.name)

    def visit_MatchAs(self, node):
        if node.name is not None:
            self.analysis.mark_not_constant(node.name)

    def visit_Try(self, node):
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
    def visit_Break(self, node):
        self.analysis.exit_loop()

    def visit_Continue(self, node):
        self.analysis.exit_loop()


class CompilerCache(object):
    """
    Objects of this class are used to cache the compilation of Python code.
    """

    def __init__(self):
        self.ast_eval_cache = {}
        self.ast_exec_cache = {}

        # True if we've changed the caches.
        self.updated = False

        # The version of this object.
        self.version = 1

    def ast_eval_literal(self, expr):
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
            expr = py_compile(expr, "eval", ast_node=True)

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

    def ast_eval(self, expr):
        return self.ast_eval_literal(expr)[0]

    def ast_exec(self, code):
        """
        Compiles a block into an AST.
        """

        if isinstance(code, renpy.ast.PyExpr):
            key = (code, code.filename, code.linenumber)
        else:
            key = (code, None, None)

        rv = self.ast_exec_cache.get(key, None)

        if rv is None:
            rv = py_compile(code, "exec", ast_node=True)
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


# A cache mapping python source to the result of analyze_assignments for that
# source.
assignment_cache: "dict[str, list | None]" = {}

# A cache mapping a condition string to its parsed expression or None if it
# could not be parsed.
predict_expression_cache: "dict[str, ast.expr | None]" = {}


def is_immutable_literal(value):
    """
    Returns true if `value` is immutable data, so prediction can bind it into
    per-path variable state and share it safely.
    """

    if value is None or value is True or value is False:
        return True

    if isinstance(value, (int, float, complex, str, bytes)):
        return True

    if isinstance(value, (tuple, frozenset)):
        return all(is_immutable_literal(i) for i in value)

    return False


class PredictRefused(Exception):
    """
    Raised during prediction expression evaluation when evaluating further
    might run creator-supplied code or needs a value prediction doesn't
    know.
    """


_predict_binary_ops = {
    ast.Add: operator.add,
    ast.Sub: operator.sub,
    ast.Mult: operator.mul,
    ast.Div: operator.truediv,
    ast.FloorDiv: operator.floordiv,
    ast.Mod: operator.mod,
    ast.Pow: operator.pow,
    ast.LShift: operator.lshift,
    ast.RShift: operator.rshift,
    ast.BitOr: operator.or_,
    ast.BitXor: operator.xor,
    ast.BitAnd: operator.and_,
}

_predict_unary_ops = {
    ast.Not: operator.not_,
    ast.USub: operator.neg,
    ast.UAdd: operator.pos,
    ast.Invert: operator.invert,
}

_predict_compare_ops = {
    ast.Eq: operator.eq,
    ast.NotEq: operator.ne,
    ast.Lt: operator.lt,
    ast.LtE: operator.le,
    ast.Gt: operator.gt,
    ast.GtE: operator.ge,
    ast.Is: operator.is_,
    ast.IsNot: operator.is_not,
    ast.In: lambda a, b: a in b,
    ast.NotIn: lambda a, b: a not in b,
}


# A bound on the size, in bits or items, of values prediction is willing to
# compute.
PREDICT_SIZE_LIMIT = 65536


def predict_binop_allowed(op_type, left, right):
    """
    Returns false when applying the binary operator `op_type` to `left` and
    `right` could produce a value so large that computing it during
    prediction would be noticed.
    """

    if op_type is ast.Pow:
        if isinstance(left, int) and isinstance(right, int) and abs(left) > 1:
            return abs(right) * abs(left).bit_length() <= PREDICT_SIZE_LIMIT
    elif op_type is ast.LShift:
        if isinstance(left, int) and isinstance(right, int) and left != 0:
            return right <= PREDICT_SIZE_LIMIT
    elif op_type is ast.Mult:
        if isinstance(left, int) and isinstance(right, int):
            return abs(left).bit_length() + abs(right).bit_length() <= PREDICT_SIZE_LIMIT

        for count, seq in ((left, right), (right, left)):
            if isinstance(count, int) and isinstance(seq, (str, bytes, tuple, list)):
                return count * len(seq) <= PREDICT_SIZE_LIMIT

    return True


def resolve_predicted_name(name, state):
    """
    Returns the value prediction knows `name` to have, raising PredictRefused
    if it doesn't know one.
    """

    if name in state:
        return state[name]

    raise PredictRefused(name)


def eval_predicted_expression(node, state):
    """
    Evaluates the expression `node` using only values prediction has proven,
    raising PredictRefused otherwise.
    """

    if isinstance(node, ast.Constant):
        return node.value

    if isinstance(node, ast.Name):
        return resolve_predicted_name(node.id, state)

    # An attribute of `store` is the same variable a bare name is.
    if (
        isinstance(node, ast.Attribute)
        and isinstance(node.value, ast.Name)
        and node.value.id == "store"
        and "store" not in state
    ):
        return resolve_predicted_name(node.attr, state)

    if isinstance(node, ast.Tuple):
        return tuple(eval_predicted_expression(i, state) for i in node.elts)

    if isinstance(node, ast.List):
        return [eval_predicted_expression(i, state) for i in node.elts]

    if isinstance(node, ast.Set):
        return {eval_predicted_expression(i, state) for i in node.elts}

    if isinstance(node, ast.Dict):
        rv = {}

        for k, v in zip(node.keys, node.values):
            if k is None: # A None key is a ** unpacking.
                raise PredictRefused(node)

            rv[eval_predicted_expression(k, state)] = eval_predicted_expression(v, state)

        return rv

    if isinstance(node, ast.UnaryOp):
        op = _predict_unary_ops.get(type(node.op))

        if op is None:
            raise PredictRefused(node)

        return op(eval_predicted_expression(node.operand, state))

    if isinstance(node, ast.BinOp):
        op_type = type(node.op)
        op = _predict_binary_ops.get(op_type)

        if op is None:
            raise PredictRefused(node)

        left = eval_predicted_expression(node.left, state)
        right = eval_predicted_expression(node.right, state)

        if not predict_binop_allowed(op_type, left, right):
            raise PredictRefused(node)

        return op(left, right)

    if isinstance(node, ast.BoolOp):
        value = None

        for i in node.values:
            value = eval_predicted_expression(i, state)

            if isinstance(node.op, ast.And):
                if not value:
                    return value
            else:
                if value:
                    return value

        return value

    if isinstance(node, ast.Compare):
        left = eval_predicted_expression(node.left, state)

        for op_node, comparator in zip(node.ops, node.comparators):
            op_type = type(op_node)
            op = _predict_compare_ops.get(op_type)

            if op is None:
                raise PredictRefused(node)

            right = eval_predicted_expression(comparator, state)

            # Identity of anything but the singletons None, True, and False
            # isn't preserved between prediction and runtime.
            if op_type in (ast.Is, ast.IsNot):
                if not any(i is None or i is True or i is False for i in (left, right)):
                    raise PredictRefused(node)

            if not op(left, right):
                return False

            left = right

        return True

    if isinstance(node, ast.IfExp):
        if eval_predicted_expression(node.test, state):
            return eval_predicted_expression(node.body, state)

        return eval_predicted_expression(node.orelse, state)

    if isinstance(node, ast.Subscript):
        value = eval_predicted_expression(node.value, state)

        if isinstance(node.slice, ast.Slice):
            def bound(b):
                return None if b is None else eval_predicted_expression(b, state)

            index = slice(bound(node.slice.lower), bound(node.slice.upper), bound(node.slice.step))
        else:
            index = eval_predicted_expression(node.slice, state)

        return value[index]

    raise PredictRefused(node)


def eval_predicted_condition(condition, state):
    """
    Tries to evaluate `condition` using only the variable values in `state`.

    Returns True or False if the condition could be evaluated or None if it
    could not be.
    """

    tree = predict_expression_cache.get(condition, False)

    if tree is False:
        try:
            tree = ast.parse(condition, mode="eval").body
        except Exception:
            tree = None

        predict_expression_cache[condition] = tree

    if tree is None:
        return None

    try:
        return bool(eval_predicted_expression(tree, state))
    except PredictRefused:
        return None
    except Exception:
        return None


def assignment_target_names(target):
    """
    Returns (names, simple) for an assignment target, where `names` are the
    variables the target stores to, and `simple` is true if the assigned
    value binds to a single name. Returns None if the target can't be
    analyzed or if storing to it could run creator-supplied code.
    """

    if isinstance(target, ast.Name):
        # Rebinding store would change the meaning of store.x elsewhere.
        if target.id == "store":
            return None

        return [target.id], True

    # StoreModule.__setattr__ only writes to the store's dict.
    if isinstance(target, ast.Attribute) and isinstance(target.value, ast.Name) and target.value.id == "store":
        return [target.attr], True

    if isinstance(target, (ast.Tuple, ast.List)):
        names = []

        for i in target.elts:
            sub = assignment_target_names(i)

            if sub is None:
                return None

            names.extend(sub[0])

        return names, False

    if isinstance(target, ast.Starred):
        sub = assignment_target_names(target.value)

        if sub is None:
            return None

        return sub[0], False

    # Attribute and subscript targets run __setattr__ or __setitem__.
    return None


def expression_is_inert(node):
    """
    Returns true if evaluating `node` at runtime can't run creator-supplied
    code no matter what its names hold - it only reads names and builds
    containers, with no operators, calls, or subscripts.
    """

    if isinstance(node, (ast.Constant, ast.Name)):
        return True

    if isinstance(node, (ast.Tuple, ast.List)):
        return all(expression_is_inert(i) for i in node.elts)

    if isinstance(node, ast.Starred):
        return expression_is_inert(node.value)

    return False


def analyze_assignments(code):
    """
    Analyzes a PyCode object into a list of assignment effects that
    apply_assignments can replay against prediction variable state. Returns
    None if executing the code may change variables in a way that can't be
    followed.
    """

    rv = assignment_cache.get(code.source, False)

    if rv is False:
        rv = analyze_assignments_core(code.source)
        assignment_cache[code.source] = rv

    return rv


def analyze_assignments_core(source):
    """
    Implements analyze_assignments without caching.
    """

    try:
        tree = ast.parse(source)
    except Exception:
        return None

    ops = []

    for stmt in tree.body:
        if isinstance(stmt, ast.Pass):
            continue

        if isinstance(stmt, ast.Expr):
            # A docstring or other constant does nothing.
            if isinstance(stmt.value, ast.Constant):
                continue

            # Anything else is checked when the effects are applied.
            ops.append(((), stmt.value, False))

            continue

        if isinstance(stmt, ast.Delete):
            names = []

            for i in stmt.targets:
                sub = assignment_target_names(i)

                if sub is None or not sub[1]:
                    return None

                names.extend(sub[0])

            ops.append((tuple(names), None, False))

            continue

        if isinstance(stmt, ast.Assign):
            targets = stmt.targets
        elif isinstance(stmt, ast.AnnAssign):
            if stmt.value is None:
                continue

            targets = [stmt.target]
        elif isinstance(stmt, ast.AugAssign):
            sub = assignment_target_names(stmt.target)

            if sub is None or not sub[1]:
                return None

            name = sub[0][0]

            # x += y has the effect of x = x + y when x is an immutable
            # literal, which is the only case a result is bound in.
            expr = ast.BinOp(left=ast.Name(id=name, ctx=ast.Load()), op=stmt.op, right=stmt.value)

            ops.append(((name,), expr, True))

            continue
        else:
            return None

        names = []
        bind = True

        for target in targets:
            sub = assignment_target_names(target)

            if sub is None:
                return None

            names.extend(sub[0])

            # When a target unpacks, which name takes what isn't tracked.
            if not sub[1]:
                bind = False

        ops.append((tuple(names), stmt.value, bind))

    return ops


def apply_assignments(ops, state):
    """
    Applies the effects returned by analyze_assignments to `state`, returning
    the new state, or None if variables may have changed in ways prediction
    can't follow.
    """

    state = dict(state)

    for names, expr, bind in ops:
        if expr is None:
            for name in names:
                state.pop(name, None)

            continue

        try:
            value = eval_predicted_expression(expr, state)
        except PredictRefused:
            # The expression couldn't be evaluated. If evaluating it at
            # runtime can't touch other variables either, only the assigned
            # names are lost.
            if not expression_is_inert(expr):
                return None

            for name in names:
                state.pop(name, None)

            continue
        except Exception:
            return None

        if bind and is_immutable_literal(value):
            for name in names:
                state[name] = value
        else:
            for name in names:
                state.pop(name, None)

    return state


def assignments_are_inert(ops):
    """
    Returns true if replaying the effects returned by analyze_assignments at
    runtime can't run creator-supplied code, no matter what values the names
    involved hold.
    """

    return all((expr is None or expression_is_inert(expr)) for _names, expr, _bind in ops)


def assigned_names(ops):
    """
    Returns the set of every name the effects returned by analyze_assignments
    may store to.
    """

    rv = set()

    for names, _expr, _bind in ops:
        rv.update(names)

    return rv


def merge_predicted_states(a, b):
    """
    Returns the variable state holding what the states `a` and `b` agree on,
    for when two prediction paths reach the same node.
    """

    rv = {}

    for name, value in a.items():
        if name in b:
            other = b[name]

            if (value is other) or (type(value) is type(other) and value == other):
                rv[name] = value

    return rv
