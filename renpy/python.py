# Copyright 2004-2024 Tom Rothamel <pytom@bishoujo.us>
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
from renpy.compat import PY2, basestring, bchr, bord, chr, open, pystr, range, round, str, tobytes, unicode # *

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

# Import these for pickle-compatibility.
from renpy.revertable import (
    CompressedList, DetRandom, RevertableDict,
    RevertableList, RevertableObject, RevertableSet, RollbackRandom,
    revertable_range, revertable_sorted,
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
        return (get_store_module, (self.__name__,)) # type: ignore

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
store_dicts = { }

# Same, for module objects.
store_modules = { }

# The store dicts that have been cleared and initialized during the current
# run.
initialized_store_dicts = set()


def create_store(name):
    """
    Creates the store with `name`.
    """

    if name == "store.store":
        raise NameError('Namespaces may not begin with "store".')

    parent, _, var = name.rpartition('.')

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
        if (k not in d) and k != "__all__":
            d[k] = v

    # Create or reuse the corresponding module.
    if name in store_modules:
        sys.modules[pyname] = store_modules[name]
    else:
        store_modules[name] = sys.modules[pyname] = StoreModule(d) # type: ignore

    if parent:
        store_dicts[parent][var] = sys.modules[pyname]


class StoreBackup():
    """
    This creates a copy of the current store, as it was at the start of
    the current statement.
    """

    def __init__(self):

        # The contents of the store for each store.
        self.store = { }

        # The contents of old for each store.
        self.old = { }

        # The contents of ever_been_changed for each store.
        self.ever_been_changed = { }

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


clean_store_backup = None # type: Optional[StoreBackup]


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

    clean_store_backup.restore() # type: ignore


def clean_store(name):
    """
    Reverts the named store to its clean copy.
    """

    if not name.startswith("store."):
        name = "store." + name

    clean_store_backup.restore_one(name) # type: ignore


def reset_store_changes(name):

    if not name.startswith("store."):
        name = "store." + name

    sd = store_dicts[name]
    sd.begin()

# Code that replaces literals will calls to magic constructors.


def b(s):
    if PY2:
        return s.encode("utf-8")
    else:
        return s


class LoadedVariables(ast.NodeVisitor):
    """
    This is used to implement find_loaded_variables.
    """

    def visit_Name(self, node):
        if isinstance(node.ctx, ast.Load):
            self.loaded.add(node.id)
        elif isinstance(node.ctx, ast.Store):
            self.stored.add(node.id)
        elif PY2 and isinstance(node.ctx, ast.Param):
            # there's no guarantee that ast.Param will keep existing in future versions of python3
            # it's only present in asts made in py2
            self.stored.add(node.id)

    if not PY2:
        # we could remove this if, but the method wouldn't be called in py2 anyway
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

class WrapFormattedValue(ast.NodeTransformer):
    """
    This walks through the children of a FormattedValue, to look for
    nodes with the __name syntax, and format those nodes.
    """

    def visit_Name(self, node):

        name = node.id

        if not name.startswith("__"):
            return node

        name = name[2:]

        if (not name) or ("__" in name):
            return node

        prefix = renpy.lexer.munge_filename(compile_filename)

        name = prefix + name

        return ast.Name(id=name, ctx=node.ctx, lineno=node.lineno, col_offset=node.col_offset, end_lineno=node.end_lineno, end_col_offset=node.end_col_offset)

wrap_formatted_value = WrapFormattedValue().visit


class WrapNode(ast.NodeTransformer):


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

        lambda_args = [ ]
        call_args =[ ]

        for var in variables:
            if PY2:
                lambda_args.append(ast.Name(id=var, ctx=ast.Param()))
            else:
                lambda_args.append(ast.arg(arg=var))

            call_args.append(ast.Name(id=var, ctx=ast.Load()))

        if PY2:

            return ast.Call(
                func=ast.Lambda(
                    args=ast.arguments(
                        args=lambda_args,
                        vararg=None,
                        kwarg=None,
                        defaults=[]
                    ),
                    body=node,
                ),
                args=call_args,
                keywords=[ ],
                starargs=None,
                kwargs=None,
            )

        else:

            return ast.Call(
                func=ast.Lambda(
                    args=ast.arguments(
                        posonlyargs=[ ],
                        args=lambda_args,
                        kwonlyargs=[ ],
                        kw_defaults=[ ],
                        defaults=[ ],
                    ),
                    body=node,
                ),
                args=call_args,
                keywords=[ ],
            )

    def wrap_starred_assign(self, n, targets):

        if PY2:
            return n

        starred = find_starred_variables(targets)

        if not starred:
            return n

        list_stmts = [ ]

        for var in starred:

            call = ast.Call(
                func=ast.Name(
                    id=b("__renpy__list__"),
                    ctx=ast.Load()
                    ),
                args=[
                    ast.Name(id=var, ctx=ast.Load())
                ],
                keywords=[ ],
                starargs=None,
                kwargs=None)

            assign = ast.Assign(
                targets=[ ast.Name(id=var, ctx=ast.Store()) ],
                value=call,
            )

            list_stmts.append(assign)

        return ast.Try(
            body=[ n ],
            handlers=[ ],
            orelse=[ ],
            finalbody=list_stmts,
            )

    def wrap_starred_for(self, node):

        if PY2:
            return node

        starred = find_starred_variables([ node.target ])

        if not starred:
            return node

        for var in starred:

            call = ast.Call(
                func=ast.Name(
                    id=b("__renpy__list__"),
                    ctx=ast.Load()
                    ),
                args=[
                    ast.Name(id=var, ctx=ast.Load())
                ],
                keywords=[ ],
                starargs=None,
                kwargs=None)

            assign = ast.Assign(
                targets=[ ast.Name(id=var, ctx=ast.Store()) ],
                value=call,
            )

            node.body.insert(0, assign)

        return node


    def wrap_starred_with(self, node):

        if PY2:
            return node

        optional_vars = [ ]

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
                func=ast.Name(
                    id=b("__renpy__list__"),
                    ctx=ast.Load()
                    ),
                args=[
                    ast.Name(id=var, ctx=ast.Load())
                ],
                keywords=[ ],
                starargs=None,
                kwargs=None)

            assign = ast.Assign(
                targets=[ ast.Name(id=var, ctx=ast.Store()) ],
                value=call,
            )

            node.body.insert(0, assign)

        return node

    def visit_Assign(self, n):
        n = self.generic_visit(n)
        return self.wrap_starred_assign(n, n.targets) # type: ignore

    def visit_AnnAssign(self, n):
        n = self.generic_visit(n)
        return self.wrap_starred_assign(n, [ n.target ]) # type: ignore

    def visit_For(self, n):
        n = self.generic_visit(n)
        return self.wrap_starred_for(n)

    def visit_AsyncFor(self, n):
        n = self.generic_visit(n)
        return self.wrap_starred_for(n)

    def visit_With(self, n):
        n = self.generic_visit(n)
        return self.wrap_starred_with(n)

    def visit_AsyncWith(self, n):
        n = self.generic_visit(n)
        return self.wrap_starred_with(n)

    def visit_ClassDef(self, n):
        n = self.generic_visit(n)

        if not n.bases: # type: ignore
            n.bases.append(ast.Name(id=b("object"), ctx=ast.Load())) # type: ignore

        return n

    def visit_GeneratorExp(self, node):
        return self.wrap_generator(node)

    def visit_SetComp(self, n):
        return ast.Call(
            func=ast.Name(
                id=b("__renpy__set__"),
                ctx=ast.Load()
                ),
            args=[ self.wrap_generator(n) ],
            keywords=[ ],
            starargs=None,
            kwargs=None)

    def visit_Set(self, n):

        return ast.Call(
            func=ast.Name(
                id=b("__renpy__set__"),
                ctx=ast.Load()
                ),
            args=[ self.generic_visit(n) ],
            keywords=[ ],
            starargs=None,
            kwargs=None)

    def visit_ListComp(self, n):

        return ast.Call(
            func=ast.Name(
                id=b("__renpy__list__"),
                ctx=ast.Load()
                ),
            args=[ self.wrap_generator(n) ],
            keywords=[ ],
            starargs=None,
            kwargs=None)

    def visit_List(self, n):
        if not isinstance(n.ctx, ast.Load):
            return self.generic_visit(n)

        return ast.Call(
            func=ast.Name(
                id=b("__renpy__list__"),
                ctx=ast.Load()
                ),
            args=[ self.generic_visit(n) ],
            keywords=[ ],
            starargs=None,
            kwargs=None)

    def visit_DictComp(self, n):
        return ast.Call(
            func=ast.Name(
                id=b("__renpy__dict__"),
                ctx=ast.Load()
                ),
            args=[ self.wrap_generator(n) ],
            keywords=[ ],
            starargs=None,
            kwargs=None)

    def visit_Dict(self, n):

        return ast.Call(
            func=ast.Name(
                id=b("__renpy__dict__"),
                ctx=ast.Load()
                ),
            args=[ self.generic_visit(n) ],
            keywords=[ ],
            starargs=None,
            kwargs=None)


    def visit_FormattedValue(self, n):
        n = wrap_formatted_value(n)
        return self.generic_visit(n)

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

    hide.body[0].body = tree.body # type: ignore
    tree.body = hide.body


unicode_re = re.compile(r'[\u0080-\uffff]')


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
        prefix = 'u' + prefix

    rv = prefix + sep + body + sep

    return rv


string_re = re.compile(r'([uU]?[rR]?)("""|"|\'\'\'|\')((\\.|.)*?)\2')


def escape_unicode(s):
    if unicode_re.search(s):
        s = string_re.sub(unicode_sub, s)

    return s

# A list of warnings that were issued during compilation.
compile_warnings = [ ]

@contextlib.contextmanager
def save_warnings():
    """
    A context manager that captures warnings issued during compilation.
    """

    pending_warnings = [ ]

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
old_compile_flags = (__future__.nested_scopes.compiler_flag
                      | __future__.with_statement.compiler_flag
                      )

new_compile_flags = (old_compile_flags
                      | __future__.absolute_import.compiler_flag
                      | __future__.print_function.compiler_flag
                      | __future__.unicode_literals.compiler_flag
                      )

# A set of __future__ flag overrides for each file.
file_compiler_flags = collections.defaultdict(int)

# A cache for the results of py_compile.
py_compile_cache = { }

# An old version of the same, that's preserved across reloads.
old_py_compile_cache = { }


def fix_locations(node, lineno, col_offset):
    """
    Assigns locations to the given node, and all of its children, adding
    any missing line numbers and column offsets.
    """

    start = max(
        (lineno, col_offset),
        (getattr(node, "lineno", None) or 1, getattr(node, "col_offset", None) or 0)
    )

    lineno, col_offset = start

    node.lineno = lineno
    node.col_offset = col_offset

    ends = [ start, (getattr(node, "end_lineno", None) or 1, getattr(node, "end_col_offset", None) or 0) ]

    for child in ast.iter_child_nodes(node):
        fix_locations(child, lineno, col_offset)
        ends.append((child.end_lineno, child.end_col_offset))

    end = max(ends)

    node.end_lineno = end[0]
    node.end_col_offset = end[1]


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
    rv = [ ]

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
        if c == '\0':
            rv.append(c)
            i += 1
            continue

        # Any escaped character passes.
        if c == '\\':
            rv.append(s[i:i + 2])
            i += 2
            continue

        # String delimiters.
        if c in '\'"':

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
                rv.append('\\')

            rv.append("\n")
            i += 1
            continue

        raise Exception("Unknown character {} (can't happen)".format(c))

    # Since the last 2 characters are \0, those characters need to be stripped.
    return "".join(rv[:-2])


# The filename being compiled.
compile_filename = ""


def py_compile(source, mode, filename='<none>', lineno=1, ast_node=False, cache=True, py=None):
    """
    Compiles the given source code using the supplied codegenerator.
    Lists, List Comprehensions, and Dictionaries are wrapped when
    appropriate.

    `source`
        The source code, as a either a string, pyexpr, or ast module
        node.

    `mode`
        One of "exec" or "eval".

    `filename`
        The filename the source comes from. If a pyexpr is given, the
        filename embedded in the pyexpr is used.

    `lineno`
        The line number of the first line of source code. If a pyexpr is
        given, the filename embedded in the pyexpr is used.

    `ast_node`
        Rather than returning compiled bytecode, returns the AST object
        that would be used.
    """

    global compile_filename
    global compile_warnings

    if ast_node:
        cache = False

    if isinstance(source, ast.Module):
        return compile(source, filename, mode)

    if isinstance(source, renpy.ast.PyExpr):
        filename = source.filename
        lineno = source.linenumber

        if py is None:
            py = source.py

    if py is None:
        if PY2:
            py = 2
        else:
            py = 3

    if cache:
        key = (lineno, filename, str(source), mode, renpy.script.MAGIC)
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

            renpy.game.script.bytecode_newcache[key] = bytecode

            if warnings_key in renpy.game.script.bytecode_oldcache:
                renpy.game.script.bytecode_newcache[warnings_key] = renpy.game.script.bytecode_oldcache[warnings_key]

            rv = marshal.loads(bytecode)
            py_compile_cache[key] = rv
            return rv

    else:
        warnings_key = None
        key = None

    source = str(source)
    source = source.replace("\r", "")

    if mode == "eval":
        source = quote_eval(source)

    line_offset = lineno - 1
    compile_filename = filename

    try:

        if mode == "hide":
            py_mode = "exec"
        else:
            py_mode = mode

        flags = file_compiler_flags.get(filename, 0)

        if (not PY2) or flags:

            flags |= new_compile_flags

            try:
                with save_warnings():
                    tree = compile(source, filename, py_mode, ast.PyCF_ONLY_AST | flags, 1)
            except SyntaxError as orig_e:

                try:
                    fixed_source = renpy.compat.fixes.fix_tokens(source)
                    with save_warnings():
                        tree = compile(fixed_source, filename, py_mode, ast.PyCF_ONLY_AST | flags, 1)
                except Exception:
                    raise orig_e

        else:

            try:
                flags = new_compile_flags
                with save_warnings():
                    tree = compile(source, filename, py_mode, ast.PyCF_ONLY_AST | flags, 1)
            except Exception:
                flags = old_compile_flags
                source = escape_unicode(source)
                with save_warnings():
                    tree = compile(source, filename, py_mode, ast.PyCF_ONLY_AST | flags, 1)

        tree = wrap_node.visit(tree)

        if mode == "hide":
            wrap_hide(tree)

        fix_locations(tree, 1, 0)
        ast.increment_lineno(tree, lineno - 1)

        line_offset = 0

        if ast_node:
            return tree.body

        try:
            with save_warnings():
                rv = compile(tree, filename, py_mode, flags, 1)
        except SyntaxError as orig_e:
            try:
                tree = renpy.compat.fixes.fix_ast(tree)
                fix_locations(tree, 1, 0)
                with save_warnings():
                    rv = compile(tree, filename, py_mode, flags, 1)
            except Exception:
                raise orig_e

        if cache:
            py_compile_cache[key] = rv

            renpy.game.script.bytecode_newcache[key] = marshal.dumps(rv)

            if compile_warnings:
                renpy.game.script.bytecode_newcache[warnings_key] = compile_warnings
                compile_warnings = [ ]

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


def py_compile_exec_bytecode(source, **kwargs):
    code = py_compile(source, 'exec', cache=False, **kwargs)
    return marshal.dumps(code)


def py_compile_hide_bytecode(source, **kwargs):
    code = py_compile(source, 'hide', cache=False, **kwargs)
    return marshal.dumps(code)


def py_compile_eval_bytecode(source, **kwargs):
    source = source.strip()
    code = py_compile(source, 'eval', cache=False, **kwargs)
    return marshal.dumps(code)

# Classes that are exported in place of the normal list, dict, and
# object.



def py_exec_bytecode(bytecode, hide=False, globals=None, locals=None, store="store"): # @ReservedAssignment

    if hide:
        locals = { } # @ReservedAssignment

    if globals is None:
        globals = store_dicts[store] # @ReservedAssignment

    if locals is None:
        locals = globals # @ReservedAssignment

    exec(bytecode, globals, locals)


def py_exec(source, hide=False, store=None):

    if store is None:
        store = store_dicts["store"]

    if hide:
        locals = { } # @ReservedAssignment
    else:
        locals = store # @ReservedAssignment

    exec(py_compile(source, 'exec'), store, locals)


def py_eval_bytecode(bytecode, globals=None, locals=None): # @ReservedAssignment

    if globals is None:
        globals = store_dicts["store"] # @ReservedAssignment

    if locals is None:
        locals = globals # @ReservedAssignment

    return eval(bytecode, globals, locals)


def py_eval(code, globals=None, locals=None): # @ReservedAssignment
    if isinstance(code, basestring):
        code = py_compile(code, 'eval')

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
    code = compile(node, filename, 'exec') #type: ignore

    # PY3 - need to change to exec().
    exec(code, { "e" : e })


# This was used to proxy accesses to the store. Now it's kept around to deal
# with cases where it might have leaked into a pickle.
class StoreProxy(object):

    def __getattr__(self, k):
        return getattr(renpy.store, k) # @UndefinedVariable

    def __setattr__(self, k, v):
        setattr(renpy.store, k, v) # @UndefinedVariable

    def __delattr__(self, k):
        delattr(renpy.store, k) # @UndefinedVariable

# This needs to exist even after PY2 support is dropped, to load older saves.
def method_unpickle(obj, name):
    return getattr(obj, name)

if PY2:

    # Code for pickling bound methods.
    def method_pickle(method):
        name = method.im_func.__name__

        obj = method.im_self

        if obj is None:
            obj = method.im_class

        return method_unpickle, (obj, name)

    copyreg.pickle(types.MethodType, method_pickle)

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
copyreg.pickle(weakref.ReferenceType, lambda r : (type(None), tuple()))
