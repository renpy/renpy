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

# This file contains code that handles the execution of python code
# contained within the script file. It also handles rolling back the
# game state to some time in the past.

from __future__ import division, absolute_import, with_statement, print_function, unicode_literals
from renpy.compat import PY2, basestring, bchr, bord, chr, open, pystr, range, round, str, tobytes, unicode  # *

from typing import Optional, Any
import contextlib

# Import the python ast module, not ours.
import ast

# Import the future module itself.
import __future__

import collections
import marshal
import random
import weakref
import re
import sys
import time
import io
import types
import copyreg
import functools
import warnings

import renpy

from renpy.astsupport import hash32

# Import these for pickle-compatibility.
from renpy.revertable import (
    CompressedList,
    DetRandom,
    RevertableDict,
    RevertableList,
    RevertableObject,
    RevertableSet,
    RollbackRandom,
    revertable_range,
    revertable_sorted,
)

from renpy.rollback import (
    deleted,
    StoreDeleted,
    AlwaysRollback,
    NoRollback,
    SlottedNoRollback,
    rng,
    reached,
    reached_vars,
    Rollback,
    RollbackLog,
)


##############################################################################
# Code that implements the store.


class StoreModule(object):
    """
    This class represents one of the modules containing the store of data.
    """

    # Set our dict to be the StoreDict. Then proxy over setattr and delattr,
    # since Python won't call them by default.

    def __reduce__(self):
        return (get_store_module, (self.__name__,))  # type: ignore

    def __init__(self, d):
        object.__setattr__(self, "__dict__", d)

    def __setattr__(self, key, value):
        self.__dict__[key] = value

    def __delattr__(self, key):
        del self.__dict__[key]


# Used to unpickle a store module.


def get_store_module(name):
    return sys.modules[name]


from renpy.pydict import DictItems, find_changes


class StoreDict(dict):
    """
    This class represents the dictionary of a store module. It logs
    sets and deletes.
    """

    def __reduce__(self):
        raise Exception("Cannot pickle a reference to a store dictionary.")

    def __init__(self):
        # The value of this dictionary at the start of the current
        # rollback period (when begin() was last called).
        self.old = DictItems(self)

        # The set of variables in this StoreDict that changed since the
        # end of the init phase.
        self.ever_been_changed = set()

    def reset(self):
        """
        Called to reset this to its initial conditions.
        """

        self.ever_been_changed = set()
        self.clear()
        self.old = DictItems(self)

    def begin(self):
        """
        Called to mark the start of a rollback period.
        """

        if self.get("_constant", False):
            return

        self.old = DictItems(self)

    def get_changes(self, cycle, previous):
        """
        For every key that has changed since begin() was called, returns a
        dictionary mapping the key to its value when begin was called, or
        deleted if it did not exist when begin was called.

        As a side-effect, updates self.ever_been_changed, and returns the
        changes to ever_been_changed as well.

        `cycle`
            If true, this cycles the old changes to the new changes. If
            False, does not.

        `previous`
            The result of a call to this from a previous cycle. The result
            from a previous run take precedence over the current run. None
            if this is the first run.
        """

        if self.get("_constant", False):
            return

        new = DictItems(self)
        rv = find_changes(self.old, new, deleted)

        if rv is None:
            return None

        if cycle:
            self.old = new

        if previous is not None:
            rv.update(previous)

        delta_ebc = set()

        if cycle:
            for k in rv:
                if k not in self.ever_been_changed:
                    self.ever_been_changed.add(k)
                    delta_ebc.add(k)

        return rv, delta_ebc


def begin_stores():
    """
    Calls .begin on every store dict.
    """

    for sd in store_dicts.values():
        sd.begin()


# A map from the name of a store dict to the corresponding StoreDict object.
# This isn't reset during a reload, so store objects stay the same in modules.
store_dicts = {}

# Same, for module objects.
store_modules = {}

# The store dicts that have been cleared and initialized during the current
# run.
initialized_store_dicts = set()


def create_store(name):
    """
    Creates the store with `name`.
    """

    if name == "store.store":
        raise NameError('Namespaces may not begin with "store".')

    parent, _, var = name.rpartition(".")

    if parent:
        create_store(parent)

    name = str(name)

    if name in initialized_store_dicts:
        return

    initialized_store_dicts.add(name)

    # Create the dict.
    d = store_dicts.setdefault(name, StoreDict())
    d.reset()

    pyname = pystr(name)

    # Set the name.
    d.update(__name__=pyname, __package__=pyname)

    # Set up the default contents of the store.
    eval("1", d)

    for k, v in renpy.minstore.__dict__.items():
        if k in ("__all__", "__name__", "__doc__", "__package__", "__loader__", "__spec__", "__file__", "__cached__"):
            continue

        if k in d:
            continue

        d[k] = v

    # Create or reuse the corresponding module.
    if name in store_modules:
        sys.modules[pyname] = store_modules[name]
    else:
        store_modules[name] = sys.modules[pyname] = StoreModule(d)  # type: ignore

    if parent:
        store_dicts[parent][var] = sys.modules[pyname]


class StoreBackup:
    """
    This creates a copy of the current store, as it was at the start of
    the current statement.
    """

    def __init__(self):
        # The contents of the store for each store.
        self.store = {}

        # The contents of old for each store.
        self.old = {}

        # The contents of ever_been_changed for each store.
        self.ever_been_changed = {}

        for k, v in store_dicts.items():
            if not v.get("_constant", False):
                self.backup_one(k)

    def backup_one(self, name):
        d = store_dicts[name]

        self.store[name] = dict(d)
        self.old[name] = d.old.as_dict()
        self.ever_been_changed[name] = set(d.ever_been_changed)

    def restore_one(self, name):
        sd = store_dicts[name]

        sd.clear()
        sd.update(self.store[name])

        sd.old = DictItems(self.old[name])

        sd.ever_been_changed.clear()
        sd.ever_been_changed.update(self.ever_been_changed[name])

    def restore(self):
        for k in self.store:
            self.restore_one(k)


clean_store_backup = None  # type: Optional[StoreBackup]


def make_clean_stores():
    """
    Copy the clean stores.
    """

    global clean_store_backup

    for _k, v in store_dicts.items():
        v.ever_been_changed.clear()
        v.begin()

    clean_store_backup = StoreBackup()


def clean_stores():
    """
    Revert the store to the clean copy.
    """

    clean_store_backup.restore()  # type: ignore


def clean_store(name):
    """
    Reverts the named store to its clean copy.
    """

    if not name.startswith("store."):
        name = "store." + name

    clean_store_backup.restore_one(name)  # type: ignore


def reset_store_changes(name):
    if not name.startswith("store."):
        name = "store." + name

    sd = store_dicts[name]
    sd.begin()


def mark_changed(name: str, variable: str):
    """
    :undocumented:

    Marks `variable` in the store with `name` as changed, causing it to be saved/loaded.
    """

    if not name.startswith("store."):
        name = "store." + name

    sd = store_dicts[name]
    sd.ever_been_changed.add(variable)


# Code that replaces literals will calls to magic constructors.

class LoadedVariables(ast.NodeVisitor):
    """
    This is used to implement find_loaded_variables.
    """

    def visit_Name(self, node):
        if isinstance(node.ctx, ast.Load):
            self.loaded.add(node.id)
        elif isinstance(node.ctx, ast.Store):
            self.stored.add(node.id)

    def visit_MatchMapping(self, node):
        if node.rest:
            self.stored.add(node.rest)

    def visit_MatchStar(self, node):
        if node.name is not None:
            self.stored.add(node.name)

    def visit_MatchAs(self, node):
        if node.name is not None:
            self.stored.add(node.name)

    def visit_arg(self, node):
        self.stored.add(node.arg)

    def find(self, node):
        self.loaded = set()
        self.stored = set()

        self.visit(node)

        return self.loaded - self.stored


# Given a comprehension or generator expression, returns the list of variables
# that are loaded from external scopes.
find_loaded_variables = LoadedVariables().find


class StarredVariables(ast.NodeVisitor):
    """
    Return a list of variables that are set using starred assignment, and hence
    need to be wrapped in RevertableList.
    """

    def visit_Starred(self, node):
        if isinstance(node.value, ast.Name) and isinstance(node.value.ctx, ast.Store):
            self.starred.add(node.value.id)

    def visit_Name(self, node):
        if isinstance(node.ctx, ast.Store):
            self.starred.discard(node.id)

    def find(self, targets):
        self.starred = set()

        for i in targets:
            self.visit(i)

        return self.starred


# Given an assignment target list, return a list of variables that are set using
# starred assignment.
find_starred_variables = StarredVariables().find


class FindStarredMatchPatterns(ast.NodeVisitor):
    """
    Given a match patten, return a list of (name, type) tuples, where type is "dict" or "list".
    """

    def __init__(self):
        self.vars = []

    def visit_MatchStar(self, node: ast.MatchStar) -> Any:
        self.generic_visit(node)
        if node.name is not None:
            self.vars.append((node.name, "list"))

    def visit_MatchMapping(self, node: ast.MatchMapping) -> Any:
        self.generic_visit(node)
        if node.rest is not None:
            self.vars.append((node.rest, "dict"))


def find_starred_match_patterns(node):
    """
    Given a match pattern, return a list of (name, type) tuples, where type is "dict" or "list".
    """

    visitor = FindStarredMatchPatterns()
    visitor.visit(node)
    return visitor.vars


class WrapNode(ast.NodeTransformer):
    def __init__(self):
        # Do we call `renpy.pyanalysis.import_from` when importing stuff?
        self.call_import_from = True

    def wrap_generator(self, node):
        """
        This wraps generators in lambdas, such that:

            (i for i in l if i == b)

        becomes:

            (lambda l, b : (i for i in l if i == b))(l, b)

        Why do this? It's because if b is a local, it's not present inside
        the generator expression scope, and when compiled independently of
        a larger scope, no cell is generated.
        """

        variables = list(sorted(find_loaded_variables(node)))

        node = self.generic_visit(node)

        lambda_args = []
        call_args = []

        for var in variables:
            lambda_args.append(ast.arg(arg=var))
            call_args.append(ast.Name(id=var, ctx=ast.Load()))

        return ast.Call(
            func=ast.Lambda(
                args=ast.arguments(
                    posonlyargs=[],
                    args=lambda_args,
                    kwonlyargs=[],
                    kw_defaults=[],
                    defaults=[],
                ),
                body=node,  # type: ignore
            ),
            args=call_args,
            keywords=[],
        )

    def wrap_starred_assign(self, n, targets):
        starred = find_starred_variables(targets)

        if not starred:
            return n

        list_stmts = []

        for var in starred:
            call = ast.Call(
                func=ast.Name(id="__renpy__list__", ctx=ast.Load()),
                args=[ast.Name(id=var, ctx=ast.Load())],
                keywords=[],
            )

            assign = ast.Assign(
                targets=[ast.Name(id=var, ctx=ast.Store())],
                value=call,
            )

            list_stmts.append(assign)

        return ast.Try(
            body=[n],
            handlers=[],
            orelse=[],
            finalbody=list_stmts,
        )

    def wrap_starred_for(self, node):
        starred = find_starred_variables([node.target])

        if not starred:
            return node

        for var in starred:
            call = ast.Call(
                func=ast.Name(id="__renpy__list__", ctx=ast.Load()),
                args=[ast.Name(id=var, ctx=ast.Load())],
                keywords=[],
            )

            assign = ast.Assign(
                targets=[ast.Name(id=var, ctx=ast.Store())],
                value=call,
            )

            node.body.insert(0, assign)

        return node

    def wrap_starred_with(self, node):
        optional_vars = []

        for i in node.items:
            if i.optional_vars is not None:
                optional_vars.append(i.optional_vars)

        if not optional_vars:
            return node

        starred = find_starred_variables(optional_vars)

        if not starred:
            return node

        for var in starred:
            call = ast.Call(
                func=ast.Name(id="__renpy__list__", ctx=ast.Load()),
                args=[ast.Name(id=var, ctx=ast.Load())],
                keywords=[],
            )

            assign = ast.Assign(
                targets=[ast.Name(id=var, ctx=ast.Store())],
                value=call,
            )

            node.body.insert(0, assign)

        return node

    def wrap_match_case(self, node):
        starred = find_starred_match_patterns(node.pattern)
        if not starred:
            return node

        for var, kind in reversed(starred):
            if kind == "list":
                call = ast.Call(
                    func=ast.Name(id="__renpy__list__", ctx=ast.Load()),
                    args=[ast.Name(id=var, ctx=ast.Load())],
                    keywords=[],
                )

                assign = ast.Assign(
                    targets=[ast.Name(id=var, ctx=ast.Store())],
                    value=call,
                )

                node.body.insert(0, assign)

            elif kind == "dict":
                call = ast.Call(
                    func=ast.Name(id="__renpy__dict__", ctx=ast.Load()),
                    args=[ast.Name(id=var, ctx=ast.Load())],
                    keywords=[],
                )

                assign = ast.Assign(
                    targets=[ast.Name(id=var, ctx=ast.Store())],
                    value=call,
                )

                node.body.insert(0, assign)

        return node

    def visit_Assign(self, node: ast.Assign):
        node = self.generic_visit(node)  # type: ignore
        return self.wrap_starred_assign(node, node.targets)

    def visit_AnnAssign(self, node: ast.AnnAssign):
        node = self.generic_visit(node)  # type: ignore
        return self.wrap_starred_assign(node, [node.target])

    def visit_For(self, node):
        node = self.generic_visit(node)
        return self.wrap_starred_for(node)

    def visit_AsyncFor(self, node):
        node = self.generic_visit(node)
        return self.wrap_starred_for(node)

    def visit_With(self, node):
        node = self.generic_visit(node)
        return self.wrap_starred_with(node)

    def visit_AsyncWith(self, node):
        node = self.generic_visit(node)
        return self.wrap_starred_with(node)

    def visit_ClassDef(self, node: ast.ClassDef):
        old = self.call_import_from
        self.call_import_from = False
        node = self.generic_visit(node)  # type: ignore
        self.call_import_from = old

        # This will force the class to inherit from RevertableObject.
        if not node.bases:
            node.bases.append(ast.Name(id="object", ctx=ast.Load()))

        return node

    def visit_GeneratorExp(self, node):
        return self.wrap_generator(node)

    def visit_SetComp(self, node):
        return ast.Call(
            func=ast.Name(id="__renpy__set__", ctx=ast.Load()), args=[self.wrap_generator(node)], keywords=[]
        )

    def visit_Set(self, node):
        return ast.Call(
            func=ast.Name(id="__renpy__set__", ctx=ast.Load()),
            args=[self.generic_visit(node)],  # type: ignore
            keywords=[],
        )

    def visit_ListComp(self, node):
        return ast.Call(
            func=ast.Name(id="__renpy__list__", ctx=ast.Load()), args=[self.wrap_generator(node)], keywords=[]
        )

    def visit_List(self, node):
        if not isinstance(node.ctx, ast.Load):
            return self.generic_visit(node)

        return ast.Call(
            func=ast.Name(id="__renpy__list__", ctx=ast.Load()),
            args=[self.generic_visit(node)],  # type: ignore
            keywords=[],
        )

    def visit_DictComp(self, node):
        return ast.Call(
            func=ast.Name(id="__renpy__dict__", ctx=ast.Load()), args=[self.wrap_generator(node)], keywords=[]
        )

    def visit_Dict(self, node):
        return ast.Call(
            func=ast.Name(id="__renpy__dict__", ctx=ast.Load()),
            args=[self.generic_visit(node)],  # type: ignore
            keywords=[],
        )

    def visit_Match(self, node: ast.Match):
        node = self.generic_visit(node)  # type: ignore
        node.cases = [self.wrap_match_case(i) for i in node.cases]
        return node

    def visit_FunctionDef(self, node):
        old = self.call_import_from
        self.call_import_from = False
        node = self.generic_visit(node)
        self.call_import_from = old

        return node

    def visit_ImportFrom(self, node):
        if not self.call_import_from:
            return node

        namespace = node.module
        if namespace.startswith("store"):
            namespace = namespace[6:]

        names = [(alias.name, alias.asname or alias.name) for alias in node.names]

        if not names:
            return node

        rv = [node]

        args = []

        # name of the module we're importing from
        args.append(ast.Constant(namespace))

        # name of the module we're importing into
        args.append(ast.Name(id="__name__", ctx=ast.Load()))

        # what we are importing
        args.extend([ast.Tuple([ast.Constant(name), ast.Constant(asname)], ctx=ast.Load()) for name, asname in names])

        renpy_pyanalysis_import_from = ast.Attribute(
            value=ast.Attribute(value=ast.Name(id="_renpy_exports", ctx=ast.Load()), attr="pyanalysis", ctx=ast.Load()),
            attr="import_from",
            ctx=ast.Load(),
        )

        rv.append(ast.Expr(value=ast.Call(func=renpy_pyanalysis_import_from, args=args, keywords=[])))

        return rv


wrap_node = WrapNode()


def wrap_hide(tree):
    """
    Wraps code inside a python hide or python early hide block inside a
    function, so it gets its own scope that works the way Python expects
    it to.
    """

    hide = ast.parse("""\
def _execute_python_hide(): pass;
_execute_python_hide()
""")

    for i in ast.walk(hide):
        ast.copy_location(i, hide.body[0])

    hide.body[0].body = tree.body  # type: ignore
    tree.body = hide.body


unicode_re = re.compile(r"[\u0080-\uffff]")


def unicode_sub(m):
    """
    If the string s contains a unicode character, make it into a
    unicode string.
    """

    s = m.group(0)

    if not unicode_re.search(s):
        return s

    prefix = m.group(1)
    sep = m.group(2)
    body = m.group(3)

    if "u" not in prefix and "U" not in prefix:
        prefix = "u" + prefix

    rv = prefix + sep + body + sep

    return rv


string_re = re.compile(r'([uU]?[rR]?)("""|"|\'\'\'|\')((\\.|.)*?)\2')


def escape_unicode(s):
    if unicode_re.search(s):
        s = string_re.sub(unicode_sub, s)

    return s


# A list of warnings that were issued during compilation.
compile_warnings = []


@contextlib.contextmanager
def save_warnings():
    """
    A context manager that captures warnings issued during compilation.
    """

    pending_warnings = []

    def showwarning(message, category, filename, lineno, file=None, line=None):
        pending_warnings.append((filename, lineno, warnings.formatwarning(message, category, filename, lineno, line)))

    old = warnings.showwarning

    try:
        warnings.showwarning = showwarning

        yield

        compile_warnings.extend(pending_warnings)

    finally:
        warnings.showwarning = old


# Flags used by py_compile.
old_compile_flags = __future__.nested_scopes.compiler_flag | __future__.with_statement.compiler_flag

new_compile_flags = (
    old_compile_flags
    | __future__.absolute_import.compiler_flag
    | __future__.print_function.compiler_flag
    | __future__.unicode_literals.compiler_flag
)

# A set of __future__ flag overrides for each file.
file_compiler_flags = collections.defaultdict(int)

# A cache for the results of py_compile.
py_compile_cache = {}

# An old version of the same, that's preserved across reloads.
old_py_compile_cache = {}


class LocationFixer:
    """
    This class is responsible for fixing the locations of nodes in the AST. First,
    it will adjust the line numbers and column offsets, and then it will use this
    information to fill in missing attributes.

    `line_delta`
        The number of lines to add to the line numbers of the nodes.

    `first_line_col_delta`
        The number of columns to add to the column offsets of the first line.

    `rest_line_col_delta`
        The number of columns to add to the column offsets of the rest of the lines.
    """

    line_delta: int
    first_line_col_delta: int
    rest_line_col_delta: int

    def __init__(
        self,
        node: ast.Module | ast.Expression,
        line_delta: int = 0,
        first_line_col_delta: int = 0,
        rest_line_col_delta: int = 0,
    ):
        self.line_delta = line_delta
        self.first_line_col_delta = first_line_col_delta
        self.rest_line_col_delta = rest_line_col_delta

        self.fix(node, 1 + line_delta, first_line_col_delta)

    def fix(self, node: ast.stmt, lineno: int, col_offset: int):
        # Not all nodes have location attributes, e.g. expr_context.
        # But it's either none of them, or all 4 of them.
        if "lineno" not in node._attributes:
            for c in ast.iter_child_nodes(node):
                self.fix(c, lineno, col_offset)

            return

        # This finds missing attributes by triggering AttributeErrors if an attribute is missing.
        try:
            if node.lineno == 1:
                node.col_offset += self.first_line_col_delta
            else:
                node.col_offset += self.rest_line_col_delta

            node.lineno += self.line_delta
            lineno, col_offset = node.lineno, node.col_offset

        except (AttributeError, TypeError):
            node.lineno = lineno
            node.col_offset = col_offset

        try:
            if node.end_lineno == 1:
                node.end_col_offset += self.first_line_col_delta
            else:
                node.end_col_offset += self.rest_line_col_delta

            node.end_lineno += self.line_delta

        except (AttributeError, TypeError):
            node.end_lineno = node.lineno
            node.end_col_offset = node.col_offset

        end = (node.end_lineno, node.end_col_offset)
        for c in ast.iter_child_nodes(node):
            self.fix(c, lineno, col_offset)

            # Not all children may have end location attributes.
            if "lineno" in c._attributes:
                if end < (c_end := (c.end_lineno, c.end_col_offset)):
                    end = c_end

        node.end_lineno, node.end_col_offset = end


def quote_eval(s):
    """
    Quotes a string for `eval`. This is necessary when it's in certain places,
    like as part of an argument string. We need to stick a single backslash
    at the end of lines that don't have it already, and that aren't in triple-quoted strings.
    """

    # No newlines! No problem.
    if "\n" not in s:
        return s

    # Characters being added to the string.
    rv = []

    # Pad out the string, so we don't have to deal with quotes at the end.
    s += "\0\0"

    len_s = len(s)

    # The index into the string.
    i = 0

    # Special characters, that aren't just copied into the string.
    special = "\0\\'\"\n"

    # The string currently being processed.
    string = None

    while i < len_s:
        c = s[i]

        # Non-special characters.
        if c not in special:
            start = i

            while True:
                i += 1
                if s[i] in special:
                    break

            rv.append(s[start:i])
            continue

        # Null.
        if c == "\0":
            rv.append(c)
            i += 1
            continue

        # Any escaped character passes.
        if c == "\\":
            rv.append(s[i : i + 2])
            i += 2
            continue

        # String delimiters.
        if c in "'\"":
            if ((string is None) or (len(string) == 3)) and (s[i + 1] == c) and (s[i + 2] == c):
                delim = c + c + c
            else:
                delim = c

            if (string is not None) and (delim == string):
                string = None
            elif string is None:
                string = delim

            rv.append(delim)
            i += len(delim)

            continue

        # Newline.
        if c == "\n":
            if string is None:
                rv.append("\\")

            rv.append("\n")
            i += 1
            continue

        raise Exception("Unknown character {} (can't happen)".format(c))

    # Since the last 2 characters are \0, those characters need to be stripped.
    return "".join(rv[:-2])


IMMUTABLE_TYPES = (int, float, str, bool, bytes, type(None), complex)


def is_immutable_value(v):
    """
    Returns True if v is an immutable value, and False if it is not.
    """

    if isinstance(v, IMMUTABLE_TYPES):
        return True

    if isinstance(v, tuple):
        return all(is_immutable_value(i) for i in v)

    return False


def py_compile(source, mode, filename="<none>", lineno=1, ast_node=False, cache=True, py=None, hashcode=None, column=0):
    """
    Compiles the given source code using the supplied codegenerator.
    Lists, List Comprehensions, and Dictionaries are wrapped when
    appropriate.

    `source`
        The source code, as a either a string, pyexpr, or ast module
        node.

    `mode`
        One of "eval", "exec", or "hide".

    `filename`
        The filename the source comes from. If a pyexpr is given, the
        filename embedded in the pyexpr is used.

    `lineno`
        The line number of the first line of source code. If a pyexpr is
        given, the filename embedded in the pyexpr is used.

    `ast_node`
        Rather than returning compiled bytecode, returns the AST object
        that would be used.

    `column`
        A column offset to add to the column numbers of the source.
    """
    global compile_warnings

    first_line_column_delta = column
    rest_line_column_delta = column

    if ast_node:
        cache = False

    if isinstance(source, ast.Module):
        return compile(source, filename, mode)

    elif isinstance(source, renpy.ast.PyExpr):
        filename = source.filename
        lineno = source.linenumber
        hashcode = source.hashcode

        first_line_column_delta = source.column
        rest_line_column_delta = 0

        if py is None:
            py = source.py

    elif hashcode is None:
        hashcode = hash32(source)

    if py is None:
        py = 3

    # This determines if the lines are indented. If so, we adjust the
    # ast to match.
    indented = source and (source[0] == " ") and (mode != "eval")

    if indented:
        lineno -= 1
        source = "if True:\n" + source

    flags = file_compiler_flags.get(filename, 0)

    if renpy.config.future_annotations:
        flags |= __future__.annotations.compiler_flag

    if cache:
        key = (hashcode, lineno, filename, mode, renpy.script.PYC_MAGIC, flags, column)
        warnings_key = ("warnings", key)

        rv = py_compile_cache.get(key, None)
        if rv is not None:
            return rv

        rv = old_py_compile_cache.get(key, None)
        if rv is not None:
            py_compile_cache[key] = rv

            return rv

        bytecode = renpy.game.script.bytecode_oldcache.get(key, None)

        if bytecode is not None:
            try:
                rv = marshal.loads(bytecode)
                py_compile_cache[key] = rv

                renpy.game.script.bytecode_newcache[key] = bytecode

                if warnings_key in renpy.game.script.bytecode_oldcache:
                    renpy.game.script.bytecode_newcache[warnings_key] = renpy.game.script.bytecode_oldcache[
                        warnings_key
                    ]

                return rv

            except Exception:
                pass

    else:
        warnings_key = None
        key = None

    source = str(source)
    source = source.replace("\r", "")

    if mode == "eval" and not ast_node:
        # If possible, compute the value of immutable literals.
        try:
            rv = ast.literal_eval(source)
            if is_immutable_value(rv):
                rv = ("literal", rv)
                py_compile_cache[key] = rv
                renpy.game.script.bytecode_newcache[key] = marshal.dumps(rv)

                return rv

        except Exception:
            pass

        source = quote_eval(source)

    line_offset = lineno - 1

    try:
        if mode == "hide":
            py_mode = "exec"
        else:
            py_mode = mode

        tree: Any = None

        with save_warnings():
            try:
                tree = compile(source, filename, py_mode, ast.PyCF_ONLY_AST | flags, True)

            except SyntaxError:
                handled = False
                try:
                    fixed_source = renpy.compat.fixes.fix_tokens(source)
                    tree = compile(fixed_source, filename, py_mode, ast.PyCF_ONLY_AST | flags, True)
                    handled = True
                except Exception:
                    pass

                if not handled:
                    raise

        # If the body is indented, it's wrapped in an "if True:" statement, which needs to be eliminated.
        if indented:
            tree.body = tree.body[0].body

        tree = wrap_node.visit(tree)

        if mode == "hide":
            wrap_hide(tree)

        LocationFixer(tree, lineno - 1, first_line_column_delta, rest_line_column_delta)

        line_offset = 0

        if ast_node:
            return tree.body

        rv: Any = None
        with save_warnings():
            try:
                rv = compile(tree, filename, py_mode, flags, True)
            except SyntaxError:
                handled = False
                try:
                    tree = renpy.compat.fixes.fix_ast(tree)
                    LocationFixer(tree, 0, 0, 0)
                    rv = compile(tree, filename, py_mode, flags, True)
                    handled = True
                except Exception:
                    pass

                if not handled:
                    raise

        if cache:
            py_compile_cache[key] = rv

            renpy.game.script.bytecode_newcache[key] = marshal.dumps(rv)

            if compile_warnings:
                renpy.game.script.bytecode_newcache[warnings_key] = compile_warnings
                compile_warnings = []

            renpy.game.script.bytecode_dirty = True

        return rv

    except SyntaxError as e:
        try:
            # e.text = # renpy.lexer.get_line_text(e.filename, e.lineno)
            e.text = source.splitlines()[e.lineno - 1]
        except Exception:
            pass

        if e.lineno is not None:
            e.lineno += line_offset

        raise e


def py_exec_bytecode(bytecode, hide=False, globals=None, locals=None, store="store"):
    if hide:
        locals = {}

    if globals is None:
        globals = store_dicts[store]

    if locals is None:
        locals = globals

    exec(bytecode, globals, locals)


def py_exec(source, hide=False, store=None):
    if store is None:
        store = store_dicts["store"]

    if hide:
        locals = {}
    else:
        locals = store

    exec(py_compile(source, "exec"), store, locals)


def py_eval_bytecode(bytecode, globals=None, locals=None):
    if bytecode.__class__ is tuple:
        return bytecode[1]

    if globals is None:
        globals = store_dicts["store"]

    if locals is None:
        locals = globals

    return eval(bytecode, globals, locals)


def py_eval(code, globals=None, locals=None):
    if isinstance(code, str):
        code = py_compile(code, "eval")

    return py_eval_bytecode(code, globals, locals)


def store_eval(code, globals=None, locals=None):
    if globals is None:
        globals = sys._getframe(1).f_globals

    return py_eval(code, globals, locals)


def raise_at_location(e, loc):
    """
    Raises `e` (which must be an Exception object) at location `loc`.

    `loc`
        A location, which should be a (filename, line_number) tuple.
    """

    filename, line = loc

    node = ast.parse("raise e", filename)
    ast.increment_lineno(node, line - 1)
    code = compile(node, filename, "exec")

    exec(code, {"e": e})


# This was used to proxy accesses to the store. Now it's kept around to deal
# with cases where it might have leaked into a pickle.
class StoreProxy(object):
    def __getattr__(self, k):
        return getattr(renpy.store, k)

    def __setattr__(self, k, v):
        setattr(renpy.store, k, v)

    def __delattr__(self, k):
        delattr(renpy.store, k)


# This needs to exist even after PY2 support is dropped, to load older saves.
def method_unpickle(obj, name):
    return getattr(obj, name)


# Code for pickling modules.


def module_pickle(module):
    if renpy.config.developer:
        raise Exception("Could not pickle {!r}.".format(module))

    return module_unpickle, (module.__name__,)


def module_unpickle(name):
    return __import__(name)


copyreg.pickle(types.ModuleType, module_pickle)

# Allow weakrefs to be pickled, with the reference being broken during
# unpickling.


def construct_None(*args):
    return None


copyreg.pickle(weakref.ReferenceType, lambda r: (construct_None, tuple()))
