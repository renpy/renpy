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
import threading
import weakref
import types
import sys
import collections
import pygame

import renpy.gl.gltexture

def memory_profile(minimum=10000):

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

    for mod_name, mod in sorted(sys.modules.items()):

        if mod is None:
            continue

        if not (mod_name.startswith("renpy") or mod_name.startswith("store")):
            continue

        for name, o in mod.__dict__.items():
            add(mod_name + "." + name, o)

    while worklist:
        name, o = worklist.pop(0)

        size[name] += sys.getsizeof(o)

        if isinstance(o, pygame.Surface):
            w, h = o.get_size()
            size[name] += w * h * o.get_bytesize()
        elif isinstance(o, renpy.gl.gltexture.Texture):
            print sys.getsizeof(o), o

        if isinstance(o, (int, float, types.NoneType, types.ModuleType, types.ClassType)):
            continue

        elif isinstance(o, (str, unicode)):
            continue

        elif isinstance(o, (tuple, list, set, frozenset)):
            for i in o:
                add(name, i)

            continue

        elif isinstance(o, dict):
            for k, v in o.iteritems():
                add(name, k)
                add(name, v)

            continue

        elif isinstance(o, types.MethodType):
            add(name, o.im_self)

        else:
            try:
                slots = getattr(o, "__slots__", empty_list)
            except:
                slots = empty_list

            if slots is not None:
                for f in slots:
                    try:
                        v = getattr(o, f, None)
                    except:
                        v = None

                    add(name, v)

            try:
                d = getattr(o, "__dict__", empty_dict)
            except:
                d = empty_dict

            add(name, d)

    total = 0

    for k, v in sorted(size.items(), key=lambda a : a[1]):
        total += v

        if v > minimum:
            print v / 1024, k

    print "Total python memory used:", total



def find_parents(cls):
    """
    Finds the parents of every object of type `cls`.
    """

    # GC to save memory.
    import gc
    import types
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

def memory_thread():

    import sys
    TextureGrid = sys.modules['renpy.gl.gltexture'].TextureGrid

    while True:
        print "==================================================="
        print "==================================================="
        find_parents(TextureGrid)
        sys.stderr.write("Wrote textures.\n")
        time.sleep(5)

def start_memory_thread():
    t = threading.Thread(target=memory_thread)
    t.daemon = True
    t.start()
