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


import inspect
import json
import sys
import os
from typing import Callable

import renpy
from renpy.test import testexecution, testast

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

    result["test"] = get_test_hierarchy_metadata(name_filter)

    filename = renpy.exports.fsdecode(args.json_dump)  # type: ignore

    if filename != "-":
        new = filename + ".new"

        with open(new, "w") as f:
            json.dump(result, f)

        if os.path.exists(filename):
            os.unlink(filename)

        os.rename(new, filename)
    else:
        json.dump(result, sys.stdout, indent=2)


def get_test_hierarchy_metadata(name_filter: Callable[[str, str], bool]) -> dict:
    """
    Returns metadata for testsuite/testcase declarations and parameterized display names.
    """

    rv = {
        "items": [],
    }

    try:
        root = testexecution.setup_global_test_suite()
    except Exception:
        return rv

    def get_kind(block: testast.TestCase) -> str:
        if isinstance(block, testast.TestSuite):
            return "testsuite"
        return "testcase"

    def get_parameterized(block: testast.TestCase) -> list[dict]:
        items = []

        count = len(block.parameters)
        for i in range(count):
            items.append({
                "index": i,
                "display_name": block.get_parameterized_name(i),
            })

        return items

    def append_block(block: testast.TestCase):
        filename = block.filename
        if not name_filter(block.name, filename):
            return

        parent_full_path = None
        if block.parent is not None:
            parent_full_path = block.parent.full_path

        rv["items"].append({
            "full_path": block.full_path,
            "name": block.name,
            "kind": get_kind(block),
            "file": filename,
            "line": block.linenumber,
            "parent_full_path": parent_full_path,
            "parameterized": get_parameterized(block),
            "description": block.description,
        })

        if isinstance(block, testast.TestSuite):
            for subtest in block.subtests:
                append_block(subtest)

    append_block(root)
    return rv
