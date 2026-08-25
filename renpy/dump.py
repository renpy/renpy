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

# This file contains code to write the reflect.json file. This file contains
# information about the game that's used to reflect on the contents,
# including how to navigate around the game.

from __future__ import division, absolute_import, with_statement, print_function, unicode_literals
from renpy.compat import PY2, basestring, bchr, bord, chr, open, pystr, range, round, str, tobytes, unicode  # *


import ast as python_ast
import inspect
import json
import sys
import os

import renpy

# A list of (name, filename, linenumber) tuples, for various types of
# name. These are added to as the definitions occur.
definitions = []
transforms = []
screens = []

# Does a file exist? We cache the result here.
file_exists_cache = {}


def file_exists(fn):
    rv = file_exists_cache.get(fn, None)

    if rv is None:
        fullfn = renpy.lexer.unelide_filename(fn)

        rv = os.path.exists(fullfn)
        file_exists_cache[fn] = rv

    return rv


python_flow_functions = {
    "jump",
    "call",
    "jump_out_of_context",
    "call_in_new_context",
    "invoke_in_new_context",
}


def new_flow():
    """
    Returns a new, empty, flow record.
    """

    return {"jumps": [], "calls": [], "menus": [], "dynamic": False}


def add_target(targets, name):
    if name not in targets:
        targets.append(name)


def flow_python(source, into):
    """
    Records the flow found in the Python `source` in `into`.
    """

    try:
        tree = python_ast.parse(source)
    except SyntaxError:
        into["dynamic"] = True
        return

    class FlowVisitor(python_ast.NodeVisitor):
        def visit_Call(self, node):
            function = node.func

            if not (
                isinstance(function, python_ast.Attribute)
                and isinstance(function.value, python_ast.Name)
                and function.value.id == "renpy"
                and function.attr in python_flow_functions
            ):
                self.generic_visit(node)
                return

            if function.attr in ("jump", "call") and node.args:
                target = node.args[0]

                if isinstance(target, python_ast.Constant) and isinstance(target.value, str):
                    if function.attr == "jump":
                        add_target(into["jumps"], target.value)
                    else:
                        add_target(into["calls"], target.value)

                    self.generic_visit(node)
                    return

            into["dynamic"] = True
            self.generic_visit(node)

        # Calls inside a function declared by this block do not transfer
        # control when the label itself runs.
        def visit_FunctionDef(self, node):
            return

        def visit_AsyncFunctionDef(self, node):
            return

        def visit_Lambda(self, node):
            return

    FlowVisitor().visit(tree)


def flow_block(block, into):
    """
    Walks `block`, a list of nodes, and records the jumps, calls, and menus
    found in it (and in the blocks nested inside it) in `into`, a flow record
    created by new_flow. Labels nested inside the block are skipped, as they
    get their own records.
    """

    for n in block:
        if isinstance(n, renpy.ast.Label):
            continue

        if isinstance(n, renpy.ast.Jump):
            if n.expression:
                into["dynamic"] = True
            else:
                add_target(into["jumps"], n.target)

        elif isinstance(n, renpy.ast.Call):
            if n.expression:
                into["dynamic"] = True
            else:
                add_target(into["calls"], n.label)

        elif isinstance(n, renpy.ast.Menu):
            choices = []

            for label, condition, choice_block in n.items:
                # Captions have no block.
                if choice_block is None:
                    continue

                choice = new_flow()
                choice["label"] = label

                if condition != "True":
                    choice["condition"] = condition

                flow_block(choice_block, choice)
                choices.append(choice)

            into["menus"].append({"line": n.linenumber, "choices": choices})

        elif isinstance(n, renpy.ast.If):
            for _condition, entry_block in n.entries:
                flow_block(entry_block, into)

        elif isinstance(n, (renpy.ast.While, renpy.ast.Translate, renpy.ast.TranslateBlock)):
            flow_block(n.block, into)

        elif isinstance(n, renpy.ast.Python):
            flow_python(n.code.source, into)

        elif isinstance(n, renpy.ast.UserStatement):
            # Creator-defined statements can declare the labels they transfer
            # control to. Their sub-blocks are walked like any other block.
            try:
                reachable = n.reachable(True)
            except Exception:
                reachable = set()

            for i in reachable:
                if isinstance(i, str):
                    add_target(into["jumps"], i)

            for i in n.subparses:
                flow_block(i.block, into)


def label_flow(label):
    """
    Returns the flow record for `label`, a Label node.
    """

    rv = new_flow()

    flow_block(label.block, rv)

    # The statement control reaches when it runs off the end of the block.
    if label.block:
        after = label.block[-1].next
    else:
        after = label.next

    if isinstance(after, renpy.ast.Label) and isinstance(after.name, str):
        rv["falls_through"] = after.name
    else:
        rv["falls_through"] = None

    return rv


# Did we do a dump?
completed_dump = False


def dump(error):
    """
    Causes a JSON dump file to be written, if the user has requested it.

    `error`
        An error flag that is added to the written file.
    """

    global completed_dump

    args = renpy.game.args

    if completed_dump:
        return

    completed_dump = True

    if not args.json_dump:  # type: ignore
        return

    def name_filter(name, filename):
        """
        Returns true if the name is included by the name_filter, or false if it is excluded.
        """

        filename = filename.replace("\\", "/")

        if name.startswith("_") and not args.json_dump_private:  # type: ignore
            if name.startswith("__") and name.endswith("__"):
                pass
            else:
                return False

        if not file_exists(filename):
            return False

        if filename.startswith("common/") or filename.startswith("renpy/common/"):
            return args.json_dump_common  # type: ignore

        if not filename.startswith("game/"):
            return False

        return True

    result = {}

    # Error flag.
    result["error"] = error

    # The size.
    result["size"] = [renpy.config.screen_width, renpy.config.screen_height]

    # The name and version.
    result["name"] = renpy.config.name
    result["version"] = renpy.config.version

    # The JSON object we return.
    location = {}
    result["location"] = location

    # Labels.
    label = location["label"] = {}

    for name, n in renpy.game.script.namemap.items():
        filename = n.filename
        line = n.linenumber

        if isinstance(name, renpy.ast.Node):
            name = name.name

        if not isinstance(name, str):
            continue

        if not name_filter(name, filename):
            continue

        label[name] = [filename, line]

    # Flow - the jumps, calls, and menus in each label, and the label control
    # falls through to at the end of it.
    flow = result["flow"] = {}

    for n in renpy.game.script.namemap.values():
        if not isinstance(n, renpy.ast.Label):
            continue

        name = n.name

        if not isinstance(name, str):
            continue

        if not name_filter(name, n.filename):
            continue

        record = label_flow(n)
        record["file"] = n.filename
        record["line"] = n.linenumber

        flow[name] = record

    # Definitions.
    define = location["define"] = {}

    for name, filename, line in definitions:
        if not name_filter(name, filename):
            continue

        define[name] = [filename, line]

    # Screens.
    screen = location["screen"] = {}

    for name, filename, line in screens:
        if not name_filter(name, filename):
            continue

        screen[name] = [filename, line]

    # Transforms.
    transform = location["transform"] = {}

    for name, filename, line in transforms:
        if not name_filter(name, filename):
            continue

        transform[name] = [filename, line]

    # Code.

    def get_line(o):
        """
        Returns the filename and the first line number of the class or function o. Returns
        None, None if unknown.

        For a class, this doesn't return the first line number of the class, but rather
        the line number of the first method in the class - hopefully.
        """

        if inspect.isfunction(o):
            return inspect.getfile(o), o.__code__.co_firstlineno

        if inspect.ismethod(o):
            return get_line(o.__func__)

        return None, None

    code = location["callable"] = {}

    for modname, mod in sys.modules.copy().items():
        if mod is None:
            continue

        if modname == "store":
            prefix = ""
        elif modname.startswith("store."):
            prefix = modname[6:] + "."
        else:
            continue

        for name, o in mod.__dict__.items():
            if inspect.isfunction(o):
                try:
                    if inspect.getmodule(o) != mod:
                        continue

                    filename, line = get_line(o)

                    if filename is None:
                        continue

                    if not name_filter(name, filename):
                        continue

                    code[prefix + name] = [filename, line]
                except Exception:
                    continue

            if inspect.isclass(o):
                for methname, method in o.__dict__.items():
                    try:
                        if inspect.getmodule(method) != mod:
                            continue

                        filename, line = get_line(method)

                        if filename is None:
                            continue

                        if not name_filter(name, filename):
                            continue

                        if not name_filter(methname, filename):
                            continue

                        code[prefix + name + "." + methname] = [filename, line]
                    except Exception:
                        continue

    # Add the build info from 00build.rpy, if it's available.
    try:
        result["build"] = renpy.store.build.dump()  # type: ignore
    except Exception:
        pass

    result["test"] = {
        "has_default_testcase": renpy.test.testexecution.has_default_testcase(),
    }

    filename = args.json_dump

    if filename != "-":
        new = filename + ".new"

        with open(new, "w", encoding="utf-8") as f:
            json.dump(result, f)

        if os.path.exists(filename):
            os.unlink(filename)

        os.rename(new, filename)
    else:
        json.dump(result, sys.stdout, indent=2)
