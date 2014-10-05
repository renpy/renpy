# Copyright 2004-2014 Tom Rothamel <pytom@bishoujo.us>
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

import time
import weakref
import types
import sys
import collections
import pygame
import gc

import renpy

memory_log = renpy.log.open("memory")

def write(s):
    sys.stdout.write(s + "\n")
    memory_log.write("%s", s)

def walk_memory(roots):
    """
    Walks over memory, trying to account it to the objects in `roots`. Each
    object in memory is attributed to at most one of the roots. We use a
    breadth-first search to try to come up with the most accurate
    attribution possible.

    `roots`
        A list of (name, object) tuples.

    Returns a dictionary mapping names from roots to the number of bytes
    reachable from that name.
    """

    # The set of ids we've seen.
    seen = set()

    # A list of (name, object) pairs.
    worklist = [ ]

    # A map from root_name to total_size.
    size = collections.defaultdict(int)

    # Empty objects we can reuse.
    empty_list = [ ]
    empty_dict = { }

    def add(name, o):
        """
        Adds o to the worklist if it's not in seen.
        """

        id_o = id(o)
        if id_o in seen:
            return

        seen.add(id_o)
        worklist.append((name, o))

    for name, o in roots:
        add(name, o)

    while worklist:
        name, o = worklist.pop(0)

        if isinstance(o, (int, float, types.NoneType, types.ModuleType, types.ClassType, types.FunctionType)):
            continue

        size[name] += sys.getsizeof(o)

        if isinstance(o, pygame.Surface):
            w, h = o.get_size()
            size[name] += w * h * o.get_bytesize()

        for v in gc.get_referents(o):
            add(name, v)

    return size

def profile_memory_common():
    """
    Profiles object, surface, and texture memory used in the renpy and store
    packages.

    Returns a map from name to the number of bytes accounted for by that
    name.
    """

    roots = [ ]

    for mod_name, mod in sorted(sys.modules.items()):

        if mod is None:
            continue

        if not (mod_name.startswith("renpy") or mod_name.startswith("store")):
            continue

        for name, o in mod.__dict__.items():
            roots.append((mod_name + "." + name, o))

    return walk_memory(roots)


def profile_memory(fraction=1.0, minimum=0):
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
    """

    usage = [ (v, k) for (k, v) in profile_memory_common().items() ]
    usage.sort()

    # The total number of bytes allocated.
    total = sum(i[0] for i in usage)

    # The number of bytes we have yet to process.
    remaining = total

    write("=" * 78)
    write("")
    write("Memory profile at " + time.ctime() + ":")
    write("")

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

def diff_memory(update=True):
    """
    :doc: memory

    Profiles objects, surface, and texture memory use by Ren'Py and the game.
    Writes (to memory.txt and stdout) the difference in memory usage from the
    last time this function was called with `update` true.

    The accounting is by names in the store and in the Ren'Py implementation
    that the memory is reachable from. If an object is reachable from more
    than one name, it's assigned to the name it's most directly reachable
    from.
    """

    global old_usage
    global old_total

    usage = profile_memory_common()
    total = sum(usage.values())

    diff = [ ]

    for k, v in usage.iteritems():
        diff.append((
            v - old_usage.get(k, 0),
            k))

    diff.sort()

    write("=" * 78)
    write("")
    write("Memory profile at " + time.ctime() + ":")
    write("")

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


################################################################################
# Legacy memory debug functions
################################################################################

def find_parents(cls):
    """
    Finds the parents of every object of type `cls`.
    """

    # GC to save memory.
    gc.collect()

    objs = gc.get_objects()

    def print_path(o):

        prefix = ""

        seen = set()
        queue = [ ]
        objects = [ ]

        for _i in range(30):

            objects.append(o)

            print prefix + str(id(o)), type(o),

            try:
                if isinstance(o, dict) and "__name__" in o:
                    print "with name", o["__name__"]
                else:
                    print repr(o)#[:1000]
            except:
                print "Bad repr."

            found = False

            if isinstance(o, types.ModuleType):
                if not queue:
                    break

                o, prefix = queue.pop()
                continue

            if isinstance(o, weakref.WeakKeyDictionary):
                for k, v in o.data.items():
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
                print "<no parent, popping>"

            o, prefix = queue.pop()

    for o in objs:
        if isinstance(o, cls):
            import random
            if random.random() < .1:

                print
                print "==================================================="
                print

                print_path(o)
