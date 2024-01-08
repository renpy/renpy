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

# This file contains functions used to help debug memory leaks. They aren't
# called by default, but can be used when problems occur.

from __future__ import division, absolute_import, with_statement, print_function, unicode_literals
from renpy.compat import PY2, basestring, bchr, bord, chr, open, pystr, range, round, str, tobytes, unicode # *


import time
import weakref
import types
import sys
import collections
import gc
import inspect

import renpy

memory_log = renpy.log.open("memory")

# Names that are intended to be constant containers and may be skipped during profiling.
constant_containers = {
    "renpy.game.script",
    "renpy.display.image.images",
    "renpy.display.image.image_attributes",
    "renpy.python.py_compile_cache",
    "renpy.python.old_py_compile_cache",
    "renpy.python.store_dicts",
    "renpy.python.store_modules",
    "renpy.pyanalysis.ccache",
    "renpy.gl2.live2d.common_cache",
    "renpy.sl2.slast.scache",
    "renpy.sl2.slast.ccache",
    "renpy.sl2.slparser.all_statements",
    "renpy.screenlang.all_statements",
    "renpy.display.screen.screens_at_sort",
    "renpy.display.screen.screens",
    "renpy.display.screen.screens_by_name",
}


def print_garbage(gen):
    """
    Prints out the garbage after collecting a generation of memory.
    """

    print()
    print("Garbage after collecting generation {}:".format(gen))

    for i in gc.garbage:
        prefix = ""
        suffix = ""

        if hasattr(i, "cell_contents"):
            i = i.cell_contents
            prefix = "cell: "

        try:
            suffix = " (" + inspect.getfile(i) + ")"
        except Exception:
            pass

        print(" -", prefix + repr(i)[:160] + suffix)


def write(s):
    sys.stdout.write(s + "\n")
    memory_log.write("%s", s)


def cycle_finder(o, name):
    o_repr_cache = { }
    paths = { }

    edges = set()

    def visit(old_ido, o, path):
        ido = id(o)

        if old_ido is not None:
            edges.add((old_ido, ido, path))

        if ido in o_repr_cache:
            return

        paths[ido] = path

        if isinstance(o, (int, float, type(None), types.ModuleType, type)):
            o_repr = repr(o)

        elif isinstance(o, basestring):
            if len(o) <= 80:
                o_repr = repr(o).encode("utf-8")
            else:
                o_repr = repr(o[:80] + "...").encode("utf-8")

        elif isinstance(o, (tuple, list)):
            o_repr = "<" + o.__class__.__name__ + ">"

        elif isinstance(o, dict):
            o_repr = "<" + o.__class__.__name__ + ">"

        elif isinstance(o, types.MethodType):
            if PY2:
                o_repr = "<method {0}.{1}>".format(o.__self__.__class__.__name__, o.__func__.__name__) # type: ignore
            else:
                o_repr = "<method {0}.{1}>".format(o.__self__.__class__.__name__, o.__name__)

        elif isinstance(o, object):
            o_repr = "<{0}>".format(type(o).__name__)

        else:
            o_repr = "BAD TYPE <{0}>".format(type(o).__name__)

        o_repr_cache[ido] = o_repr

        if isinstance(o, (tuple, list)):
            for i, oo in enumerate(o):
                visit(ido, oo, "{0}[{1!r}]".format(path, i))

        if isinstance(o, dict):
            for k, v in o.items():
                visit(ido, v, "{0}[{1!r}]".format(path, k))

        elif isinstance(o, types.MethodType):
            visit(ido, o.__self__, path + ".im_self")

        else:

            try:
                reduction = o.__reduce_ex__(2) # type: ignore
            except Exception:
                reduction = [ ]

            # Gets an element from the reduction, or o if we don't have
            # such an element.
            def get(idx, default):
                if idx < len(reduction) and reduction[idx] is not None:
                    return reduction[idx]
                else:
                    return default

            state = get(2, { })
            if isinstance(state, dict):
                for k, v in state.items():
                    visit(ido, v, path + "." + k)
            else:
                visit(ido, state, path + ".__getstate__()")

            for i, oo in enumerate(get(3, [])): # type: ignore
                visit(ido, oo, "{0}[{1}]".format(path, i))

            for i in get(4, []): # type: ignore

                if len(i) != 2:
                    continue

                k, v = i

                visit(ido, v, "{0}[{1!r}]".format(path, k))

    visit(None, o, name)

    while True:
        left = set(i[0] for i in edges)
        right = set(i[1] for i in edges)

        leaves = right - left
        roots = left - right

        if (not leaves) and (not roots):
            break

        edges = set(i for i in edges if (i[1] not in leaves) if (i[0] not in roots))

    while edges:
        print()
        print("Cycle:")

        edge = list(edges)[0]

        while edge in edges:
            edges.remove(edge)
            print("  ", edge)
            print(" -", edge[2], "=", o_repr_cache[edge[1]])

            relevant = [ i for i in edges if i[0] == edge[1] ]
            if not relevant:
                break

            edge = relevant[0]


def walk_memory(roots, seen=None):
    """
    Walks over memory, trying to account it to the objects in `roots`. Each
    object in memory is attributed to at most one of the roots. We use a
    breadth-first search to try to come up with the most accurate
    attribution possible.

    `roots`
        A list of (name, object) tuples.

    Returns a dictionary mapping names to the number of bytes
    reachable from that name, and a dictionary mapping object ids to
    names.
    """

    # A map from id(o) to the name o is accounted under.
    if seen is None:
        seen = { }

    # A deque of (name, object) pairs.
    # We use a deque because we want to pop from the left.
    worklist = collections.deque()

    # A map from root_name to total_size.
    size = collections.defaultdict(int)

    for name, o in roots:
        id_o = id(o)

        if id_o in seen:
            continue

        seen[id_o] = name
        worklist.append((name, o))

    # For speed, cache name lookups.
    getsizeof = sys.getsizeof
    get_referents = gc.get_referents
    worklist_append = worklist.append

    ignore_types = (types.ModuleType, type, types.FunctionType)

    while worklist:
        name, o = worklist.popleft()

        if isinstance(o, ignore_types):
            continue

        size[name] += getsizeof(o)

        for v in get_referents(o):
            id_v = id(v)

            if id_v in seen:
                continue

            seen[id_v] = name
            worklist_append((name, v))

    return size, seen


def profile_memory_common(packages=[ "renpy", "store" ], skip_constants=False):
    """
    Profiles object, surface, and texture memory used in the renpy and store
    packages.

    Returns a map from name to the number of bytes accounted for by that
    name, and a dictionary mapping object ids to
    names.
    """

    roots = [ ]

    for mod_name, mod in sorted(sys.modules.items()):

        if mod is None:
            continue

        for p in packages:
            if mod_name.startswith(p):
                break
        else:
            continue

        if not (mod_name.startswith("renpy") or mod_name.startswith("store")):
            continue

        if mod_name.startswith("renpy.store"):
            continue

        for name, o in mod.__dict__.items():
            name = mod_name + "." + name

            if skip_constants and name in constant_containers:
                continue

            roots.append((name, o))

    return walk_memory(roots)


def profile_memory(fraction=1.0, minimum=0, skip_constants=False):
    """
    :doc: memory

    Profiles object, surface, and texture memory use by Ren'Py and the
    game. Writes an accounting of memory use by to the memory.txt file and
    stdout.

    The accounting is by names in the store and in the Ren'Py implementation
    that the memory is reachable from. If an object is reachable from more
    than one name, it's assigned to the name it's most directly reachable
    from.

    `fraction`
        The fraction of the total memory usage to show. 1.0 will show all
        memory usage, .9 will show the top 90%.

    `minimum`
        If a name is accounted less than `minimum` bytes of memory, it will
        not be printed.

    `skip_constants`
        If True, the profiler will skip scanning of large Ren'Py's containers,
        that are intended to be immutable after startup.

    As it has to scan all memory used by Ren'Py, this function may take a
    long time to complete.
    """

    write("=" * 78)
    write("")
    write("Memory profile at " + time.ctime() + ":")
    write("")

    usage = [ (v, k) for (k, v) in profile_memory_common(skip_constants=skip_constants)[0].items() ]
    usage.sort()

    # The total number of bytes allocated.
    total = sum(i[0] for i in usage)

    # The number of bytes we have yet to process.
    remaining = total

    for size, name in usage:

        if (remaining - size) < total * fraction:
            if size > minimum:
                write("{:13,d} {}".format(size, name))

        remaining -= size

    write("-" * 13)
    write("{:13,d} Total object, surface, and texture memory usage (in bytes).".format(total))
    write("")


old_usage = { }
old_total = 0


def diff_memory(update=True, skip_constants=False):
    """
    :doc: memory

    Profiles objects, surface, and texture memory use by Ren'Py and the game.
    Writes (to memory.txt and stdout) the difference in memory usage from the
    last time this function was called with `update` true.

    The accounting is by names in the store and in the Ren'Py implementation
    that the memory is reachable from. If an object is reachable from more
    than one name, it's assigned to the name it's most directly reachable
    from.

    `skip_constants`
        If True, the profiler will skip scanning of large Ren'Py's containers,
        that are intended to be immutable after startup.

    As it has to scan all memory used by Ren'Py, this function may take a
    long time to complete.
    """

    global old_usage
    global old_total

    write("=" * 78)
    write("")
    write("Memory diff at " + time.ctime() + ":")
    write("")

    usage = profile_memory_common(skip_constants=skip_constants)[0]
    total = sum(usage.values())

    diff = [ ]

    for k, v in usage.items():
        diff.append((
            v - old_usage.get(k, 0),
            k))

    diff.sort()

    for change, name in diff:
        if name == "renpy.memory.old_usage":
            continue

        if change:
            write("{:+14,d} {:13,d} {}".format(change, usage[name], name))

    write("-" * 14 + " " + "-" * 13)
    write("{:+14,d} {:13,d} {}".format(total - old_total, total, "Total memory usage (in bytes)."))
    write("")

    if update:
        old_usage = usage
        old_total = total


def profile_rollback():
    """
    :doc: memory

    Profiles memory used by the rollback system. Writes (to memory.txt and
    stdout) the memory used by the rollback system. This tries to account
    for rollback memory used by various store variables, as well as by
    internal aspects of the rollback system.
    """

    write("=" * 78)
    write("")
    write("Rollback profile at " + time.ctime() + ":")
    write("")

    # Profile live memory.
    seen = profile_memory_common([ "store", "renpy.display" ])[1]

    # Like seen, but for objects found in rollback.
    new_seen = { }

    log = list(renpy.game.log.log)
    log.reverse()

    roots = [ ]

    # Walk the log, finding new roots and rollback information.
    for rb in log:

        for store_name, store in rb.stores.items():
            for var_name, o in store.items():
                name = store_name + "." + var_name
                id_o = id(o)

                if (id_o not in seen) and (id_o not in new_seen):
                    new_seen[id_o] = name

                roots.append((name, o))

        for o, roll in rb.objects:

            id_o = id(o)

            name = "<unknown>"
            name = new_seen.get(id_o, name)
            name = seen.get(id_o, name)

            roots.append((name, roll))

        roots.append(("<scene lists>", rb.context.scene_lists))
        roots.append(("<context>", rb.context))

    sizes = walk_memory(roots, seen)[0]

    usage = [ (v, k) for (k, v) in sizes.items() ]
    usage.sort()

    write("Total Bytes".rjust(13) + " " + "Per Rollback".rjust(13))
    write("-" * 13 + " " + "-" * 13 + " " + "-" * 50)

    for size, name in usage:
        if name.startswith("renpy"):
            continue

        if size:
            write("{:13,d} {:13,d} {}".format(size, size // len(log), name))

    write("")
    write("{} Rollback objects exist.".format(len(log)))
    write("")


def find_parents(cls):
    """
    Finds the parents of every object of type `cls`.
    """

    if gc.garbage:
        del gc.garbage[:]

    objs = gc.get_objects()

    def print_path(o, objs):

        prefix = ""

        seen = set()
        queue = [ ]
        objects = [ ]

        last = None

        for _i in range(30):

            objects.append(o)
            last = o

            print(prefix + "%x" % id(o), "(%d referrers)" % len(gc.get_referrers(o)), type(o), end=' ')

            try:
                if isinstance(o, dict) and "__name__" in o:
                    print("with name", o["__name__"])
                else:
                    print(repr(o))
            except Exception:
                print("Bad repr.")

            found = False

            if isinstance(o, types.ModuleType):
                if not queue:
                    break

                o, prefix = queue.pop()
                continue

            if isinstance(o, weakref.WeakKeyDictionary):
                for k, v in o.items():
                    if v is objects[-4]:
                        k = k()
                        seen.add(id(k))
                        queue.append((k, prefix + " (key) "))

            for i in gc.get_referrers(o):

                if i is objs or i is objects:
                    continue

                if id(i) in seen:
                    continue

                if isinstance(i, types.FrameType):
                    continue

                seen.add(id(i))
                queue.append((i, prefix + "  "))
                found = True
                break

            if not queue:
                break

            if not found:
                print("<no parent, popping>")

            o, prefix = queue.pop()

        for i in gc.get_referrers(last):
            print(prefix + "<- %x" % id(i), type(i))

        del objects[:]

    for o in objs:
        if isinstance(o, cls):

            print()
            print("===================================================")
            print()

            print_path(o, objs)

    del objs[:]
