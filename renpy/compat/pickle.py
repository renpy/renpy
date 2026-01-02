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

from typing import Any, BinaryIO

import types
import pickle
import io
import functools
import datetime
import ast
import renpy

PROTOCOL = pickle.HIGHEST_PROTOCOL


def dump_paths(filename: str, **roots: object):
    """
    Dumps information about the `roots` to `filename`. We dump the size
    of the object (including unique children), the path to the object,
    and the type or repr of the object.
    """

    o_repr_cache = {}

    def visit_seq(o: tuple | list, path: str) -> int:
        size = 1
        for i, oo in enumerate(o):
            size += 1
            size += visit(oo, f"{path}[{i!r}]")

        return size

    def visit_map(o: dict, path: str) -> int:
        size = 2
        for k, v in o.items():
            size += 2
            if isinstance(k, str):
                size += len(k) // 40 + 1
            else:
                size += visit(v, f"key {k!r} of {path}")
            size += visit(v, f"{path}[{k!r}]")

        return size

    def visit(o: object, path: str) -> int:
        ido = id(o)

        if ido in o_repr_cache:
            f.write(f"{0: 7d} {path} = alias {o_repr_cache[ido]}\n")
            return 0

        if isinstance(o, (int, float, complex, types.NoneType, types.ModuleType, type)):
            o_repr = repr(o)

        elif isinstance(o, str):
            if len(o) <= 80:
                o_repr = repr(o)
            else:
                o_repr = repr(o[:40] + "..." + o[-40:])

        elif isinstance(o, bytes):
            if len(o) <= 80:
                o_repr = repr(o)
            else:
                o_repr = repr(o[:40] + b"..." + o[-40:])

        elif isinstance(o, (tuple, list, dict)):
            o_repr = f"<{o.__class__.__name__}>"

        elif isinstance(o, types.MethodType):
            o_repr = f"<method {o.__self__.__class__}.{o.__name__}>"

        elif isinstance(o, types.FunctionType):
            name = o.__qualname__ or o.__name__

            o_repr = f"{o.__module__}.{name}"

        elif isinstance(o, object):
            o_repr = f"<{type(o).__name__}>"

        else:
            o_repr = f"BAD TYPE <{type(o).__name__}>"

        o_repr_cache[ido] = o_repr

        if isinstance(o, (int, float, complex, types.NoneType, types.ModuleType, type)):
            size = 1

        elif isinstance(o, (bytes, str)):
            size = len(o) // 40 + 1

        elif isinstance(o, (tuple, list)):
            size = visit_seq(o, path)

        elif isinstance(o, dict):
            size = visit_map(o, path)

        elif isinstance(o, types.MethodType):
            size = 1 + visit(o.__self__, f"{path}.__self__")

        elif isinstance(o, types.FunctionType):
            size = 1

        else:
            try:
                reduction = o.__reduce_ex__(PROTOCOL)
            except Exception:
                reduction = ()
                o_repr_cache[ido] = "BAD REDUCTION " + o_repr

            if isinstance(reduction, str):
                o_repr_cache[ido] = f"{o.__module__}.{reduction}"
                size = 1

            else:
                reduction = [*reduction] + [None] * (5 - len(reduction))
                _, _, state, seq, map, *_ = reduction

                # An estimate of the size of the object, in arbitrary units.
                # (These units are about 20-25 bytes on my computer.)
                size = 1

                if isinstance(state, tuple):
                    state, slots = state
                    for k, v in slots.items():
                        size += 1
                        size += visit(v, f"{path}.{k}")

                if state is not None:
                    size += visit(state, f"{path}.__getstate__()")

                if seq is not None:
                    visit(seq, path)

                if map is not None:
                    visit(map, path)

        f.write(f"{size: 7d} {path} = {o_repr_cache[ido]}\n")

        return size

    f, _ = renpy.error.open_error_file(filename, "w")

    with f:
        for k, v in roots.items():
            visit(v, k)


def find_bad_reduction(**roots: object) -> str | None:
    """
    Finds objects that can't be reduced properly.
    """

    seen = set()

    def visit_seq(o: tuple | list, path: str):
        for i, oo in enumerate(o):
            if rv := visit(oo, f"{path}[{i!r}]"):
                return rv

    def visit_map(o: dict, path: str):
        for k, v in o.items():
            if rv := visit(k, f"key {k!r} of {path}"):
                return rv

            if rv := visit(v, f"{path}[{k!r}]"):
                return rv

    def visit(o: object, path: str) -> str | None:
        ido = id(o)

        if ido in seen:
            return None

        seen.add(ido)

        if isinstance(o, (int, float, complex, str, bytes, types.NoneType, types.ModuleType, type)):
            return None

        if isinstance(o, (tuple, list)):
            if rv := visit_seq(o, path):
                return rv

        elif isinstance(o, dict):
            if rv := visit_map(o, path):
                return rv

        elif isinstance(o, types.MethodType):
            return visit(o.__self__, f"{path}.__self__")

        else:
            try:
                reduction = o.__reduce_ex__(PROTOCOL)
            except Exception:
                return f"{path} = {repr(o)[:160]}"

            if isinstance(reduction, str):
                return None

            reduction = [*reduction] + [None] * (5 - len(reduction))
            _, _, state, seq, map, *_ = reduction

            if isinstance(state, tuple):
                state, slots = state
                for k, v in slots.items():
                    if rv := visit(v, f"{path}.{k}"):
                        return rv

            if state is not None:
                if rv := visit(state, f"{path}.__getstate__()"):
                    return rv

            if seq is not None:
                if rv := visit(seq, path):
                    return rv

            if map is not None:
                if rv := visit(map, path):
                    return rv

        return None

    for k, v in roots.items():
        if rv := visit(v, k):
            return rv

    return None


def make_datetime(cls, *args, **kwargs):
    """
    Makes a datetime.date, datetime.time, or datetime.datetime object
    from a surrogateescaped str. This is used when unpickling a datetime
    object that was first created in Python 2.
    """

    if (len(args) == 1) and isinstance(args[0], str):
        data = args[0].encode("utf-8", "surrogateescape")
        return cls.__new__(cls, data.decode("latin-1"))

    return cls.__new__(cls, *args, **kwargs)


class Unpickler(pickle.Unpickler):
    date = functools.partial(make_datetime, datetime.date)
    time = functools.partial(make_datetime, datetime.time)
    datetime = functools.partial(make_datetime, datetime.datetime)

    def find_class(self, module, name):
        if module == "datetime":
            if name == "date":
                return self.date
            elif name == "time":
                return self.time
            elif name == "datetime":
                return self.datetime

        if module == "_ast" and name in REWRITE_NODES:
            return REWRITE_NODES[name]

        return super().find_class(module, name)


def load(f) -> Any:
    """
    Read and return an object from the pickle data stored in a file.
    """

    return Unpickler(f, fix_imports=True, encoding="utf-8", errors="surrogateescape").load()


def loads(s) -> Any:
    """
    Read and return an object from the given pickle data.
    """

    return load(io.BytesIO(s))


def dump(o: object, f: BinaryIO, highest=False):
    """
    Write a pickled representation of `o` to the open file object `f`.

    `highest`
        If true, use the highest protocol version available.
        Otherwise, use the default protocol version.
    """

    pickle.dump(o, f, pickle.HIGHEST_PROTOCOL if highest else PROTOCOL)


def dumps(o: object, highest=False, bad_reduction_name: str | None = None) -> bytes:
    """
    Return the pickled representation of the object as a bytes object.

    `highest`
        If true, use the highest protocol version available.
        Otherwise, use the default protocol version.

    `bad_reduction_name`
        If provided, this parameter name is used to help diagnose pickle errors
        caused by problematic object reduction. When pickling fails, it attempts
        to find path to the specific reduction that caused the error using this name.
    """

    try:
        return pickle.dumps(o, pickle.HIGHEST_PROTOCOL if highest else PROTOCOL)
    except Exception as e:
        if bad_reduction_name is not None:
            try:
                if bad := find_bad_reduction(**{bad_reduction_name: o}):
                    e.add_note(f"Perhaps unpickleable object in {bad}")
            except Exception:
                pass

        raise


# The python AST module changed significantly between python 2 and 3. Old-style
# screenlang support records raw python ast nodes into the rpyc data, making these
# impossible to load normally. This dict contains mappings of nodes that need to be
# modified to wrapper classes with a custom __setstate__ implementation that will
# cause the pickle machinery to do the right thing.
# There are some things that cannot be handled by this
# (as the type of the node to be emitted is not fixed at that point), so those
# are handled by a NodeTransformer in the ast.Module replacement.
# Note: this isn't a complete python 2 -> python 3 ast conversion, we just convert
# what is needed to still support old-style screens (Ren'py 6.17 and below)
# mapping of "classname": WrapperClass
REWRITE_NODES = {}


# NodeTransformer that runs after the ast has been instantiated in the ast.Module
# handler, and allows us to fix some more difficult issues. Currently only
# handles converting ast.Name nodes that contain True/False/None into the appropriate
# ast.Constant nodes.
class AstFixupTransformer(ast.NodeTransformer):
    def visit_Name(self, node):
        # in python 2 True, False, None are keywords, and get parsed as such.
        if node.id == "True":
            alt_node = ast.Constant(True)

        elif node.id == "False":
            alt_node = ast.Constant(False)

        elif node.id == "None":
            alt_node = ast.Constant(None)

        else:
            return node

        alt_node.lineno = node.lineno
        alt_node.col_offset = node.col_offset
        return alt_node


# wrapper classes. They all have __setstate__ defined to handle converting from the
# py2 class, and __reduce__ implemented to convert to the underlying py3 class
# if it gets repickled. Note that py3 ast classes will not hit the REWRITE_NODES check
# as py3 classes report to be from "ast" instead of "_ast"
class CallWrapper(ast.Call):
    def __reduce__(self):
        _, args, attrs = super().__reduce__()
        return ast.Call, args, attrs

    def __setstate__(self, state):
        # source info
        self.lineno = state["lineno"]
        self.col_offset = state["col_offset"]

        # contents
        self.func = state["func"]
        self.args = state["args"]
        self.keywords = state["keywords"]

        # these gained some extra info
        for keyword in self.keywords:
            keyword.lineno = self.lineno
            keyword.col_offset = self.col_offset

        # these are no longer an extra field, they're just part of args and keywords
        # as you can now supply multiple of them.
        if state["starargs"]:
            node = ast.Starred(value=state["starargs"], ctx=ast.Load())
            node.lineno = self.lineno
            node.col_offset = self.col_offset
            self.args.append(node)

        if state["kwargs"]:
            node = ast.keyword(None, state["kwargs"])
            node.lineno = self.lineno
            node.col_offset = self.col_offset
            self.keywords.append(node)


REWRITE_NODES["Call"] = CallWrapper


class NumWrapper(ast.Constant):
    def __reduce__(self):
        _, args, attrs = super().__reduce__()
        return ast.Constant, args, attrs

    def __setstate__(self, state):
        # source info
        self.lineno = state["lineno"]
        self.col_offset = state["col_offset"]

        # contents
        self.value = state["n"]


REWRITE_NODES["Num"] = NumWrapper


class StrWrapper(ast.Constant):
    def __reduce__(self):
        _, args, attrs = super().__reduce__()
        return ast.Constant, args, attrs

    def __setstate__(self, state):
        # source info
        self.lineno = state["lineno"]
        self.col_offset = state["col_offset"]

        # contents
        self.value = state["s"]


REWRITE_NODES["Str"] = StrWrapper


class ModuleWrapper(ast.Module):
    def __reduce__(self):
        _, args, attrs = super().__reduce__()
        return ast.Module, args, attrs

    def __setstate__(self, state):
        # contents
        self.body = state["body"]
        self.type_ignores = []

        # this is the root node, so now is a good moment do do some transforms we couldn't
        # do earlier because we weren't sure of the node type to be created.

        transformer = AstFixupTransformer()
        transformer.visit(self)


REWRITE_NODES["Module"] = ModuleWrapper


class ReprWrapper(ast.Call):
    def __reduce__(self):
        _, args, attrs = super().__reduce__()
        return ast.Call, args, attrs

    def __setstate__(self, state):
        # we need to transform `thing` into repr(thing)
        # source info
        self.lineno = state["lineno"]
        self.col_offset = state["col_offset"]

        # contents
        self.func = ast.Name("repr", ast.Load(), lineno=self.lineno, col_offset=self.col_offset)
        self.args = [state["value"]]
        self.keywords = []


REWRITE_NODES["Repr"] = ReprWrapper


class ArgumentsWrapper(ast.arguments):
    def __reduce__(self):
        _, args, attrs = super().__reduce__()
        return ast.arguments, args, attrs

    def __setstate__(self, state):
        # source info: this node doesn't get source info

        def make_arg(name):
            # python 2 just uses bare ast.Name nodes as arguments
            # technically it also can support more complex tuple destructuring
            # expressions in here, but python 3 just doesn't support that,
            # and there's really no good way of exactly handling that crazyness.
            assert isinstance(name, ast.Name)
            return ast.arg(name.id, lineno=name.lineno, col_offset=name.col_offset)

        # contents. source doesn't record lineno/col_offset for vararg/kwarg
        self.posonlyargs = []
        self.args = [make_arg(i) for i in state["args"]]
        self.vararg = ast.arg(state["vararg"], lineno=1, col_offset=0)
        self.kwonlyargs = []
        self.kw_defaults = []
        self.kwarg = ast.arg(state["kwarg"], lineno=1, col_offset=0)
        self.defaults = state["defaults"]


REWRITE_NODES["arguments"] = ArgumentsWrapper


class ParamWrapper(ast.Load):
    def __reduce__(self):
        _, args, attrs = super().__reduce__()
        return ast.Load, args, attrs


REWRITE_NODES["Param"] = ParamWrapper
