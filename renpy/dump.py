# Copyright 2004-2018 Tom Rothamel <pytom@bishoujo.us>
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

from __future__ import print_function

import inspect
import json
import sys
import os

import renpy


# A list of (name, filename, linenumber) tuples, for various types of
# name. These are added to as the definitions occur.
definitions = [ ]
transforms = [ ]
screens = [ ]


# Does a file exist? We cache the result here.
file_exists_cache = { }


def file_exists(fn):
    rv = file_exists_cache.get(fn, None)

    if rv is None:
        fullfn = renpy.parser.unelide_filename(fn)

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

    if not args.json_dump:
        return

    def filter(name, filename):  # @ReservedAssignment
        """
        Returns true if the name is included by the filter, or false if it is excluded.
        """

        filename = filename.replace("\\", "/")

        if name.startswith("_") and not args.json_dump_private:
            if name.startswith("__") and name.endswith("__"):
                pass
            else:
                return False

        if not file_exists(filename):
            return False

        if filename.startswith("common/") or filename.startswith("renpy/common/"):
            return args.json_dump_common

        if not filename.startswith("game/"):
            return False

        return True

    result = { }

    # Error flag.
    result["error"] = error

    # The size.
    result["size"] = [ renpy.config.screen_width, renpy.config.screen_height ]

    # The name and version.
    result["name"] = renpy.config.name
    result["version"] = renpy.config.version

    # The JSON object we return.
    location = { }
    result["location"] = location

    # Labels.
    label = location["label"] = { }

    for name, n in renpy.game.script.namemap.iteritems():
        filename = n.filename
        line = n.linenumber

        if not isinstance(name, basestring):
            continue

        if not filter(name, filename):
            continue

        label[name] = [ filename, line ]

    # Definitions.
    define = location["define"] = { }

    for name, filename, line in definitions:
        if not filter(name, filename):
            continue

        define[name] = [ filename, line ]

    # Screens.
    screen = location["screen"] = { }

    for name, filename, line in screens:
        if not filter(name, filename):
            continue

        screen[name] = [ filename, line ]

    # Transforms.
    transform = location["transform"] = { }

    for name, filename, line in transforms:
        if not filter(name, filename):
            continue

        transform[name] = [ filename, line ]

    # Code.

    def get_line(o):
        """
        Returns the filename and the first line number of the class or function o. Returns
        None, None if unknown.

        For a class, this doesn't return the first line number of the class, but rather
        the line number of the first method in the class - hopefully.
        """

        if inspect.isfunction(o):
            return inspect.getfile(o), o.func_code.co_firstlineno

        if inspect.ismethod(o):
            return get_line(o.im_func)

        return None, None

    code = location["callable"] = { }

    for modname, mod in sys.modules.items():

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

                    if not filter(name, filename):
                        continue

                    code[prefix + name] = [ filename, line ]
                except:
                    continue

            if inspect.isclass(o):

                for methname, method in o.__dict__.iteritems():

                    try:
                        if inspect.getmodule(method) != mod:
                            continue

                        filename, line = get_line(method)

                        if filename is None:
                            continue

                        if not filter(name, filename):
                            continue

                        if not filter(methname, filename):
                            continue

                        code[prefix + name + "." + methname] = [ filename, line ]
                    except:
                        continue

    # Add the build info from 00build.rpy, if it's available.
    try:
        result["build"] = renpy.store.build.dump()  # @UndefinedVariable
    except:
        pass

    if args.json_dump != "-":
        new = args.json_dump + ".new"

        with file(new, "w") as f:
            json.dump(result, f)

        if os.path.exists(args.json_dump):
            os.unlink(args.json_dump)

        os.rename(new, args.json_dump)
    else:
        json.dump(result, sys.stdout, indent=2)
