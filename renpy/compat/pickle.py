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

from __future__ import division, absolute_import, with_statement, print_function, unicode_literals
from renpy.compat import PY2, basestring, bchr, bord, chr, open, pystr, range, round, str, tobytes, unicode # *


import renpy
import pickle
import io

# Protocol 2 can be loaded on Python 2 and Python 3.
PROTOCOL = 2

if PY2:

    import cPickle # type: ignore

    def load(f): # type: ignore
        if renpy.config.use_cpickle:
            return cPickle.load(f)
        else:
            return pickle.load(f)

    def loads(s): # type: ignore
        if renpy.config.use_cpickle:
            return cPickle.loads(s)
        else:
            return pickle.loads(s)

    def dump(o, f, highest=False):
        if renpy.config.use_cpickle:
            cPickle.dump(o, f, PROTOCOL)
        else:
            pickle.dump(o, f,PROTOCOL)

    def dumps(o, highest=False): # type: ignore
        if renpy.config.use_cpickle:
            return cPickle.dumps(o, PROTOCOL)
        else:
            return pickle.dumps(o, PROTOCOL)

else:

    import functools
    import datetime
    import ast

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

    def load(f):
        up = Unpickler(f, fix_imports=True, encoding="utf-8", errors="surrogateescape")
        return up.load()

    def loads(s):
        return load(io.BytesIO(s))

    def dump(o, f, highest=False):
        pickle.dump(o, f, pickle.HIGHEST_PROTOCOL if highest else PROTOCOL)

    def dumps(o, highest=False):
        return pickle.dumps(o, pickle.HIGHEST_PROTOCOL if highest else PROTOCOL)

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
            self.defaults =  state["defaults"]

    REWRITE_NODES["arguments"] = ArgumentsWrapper

    class ParamWrapper(ast.Load):
        def __reduce__(self):
            _, args, attrs = super().__reduce__()
            return ast.Load, args, attrs

    REWRITE_NODES["Param"] = ParamWrapper
