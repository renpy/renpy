#!/usr/bin/env python

import os.path

# Enable psyco. Warning: Check for memory leaks!

try:
    if not os.path.exists("nopsyco"):
        import psyco
        psyco.full()
except ImportError:
    pass

import codecs
import optparse
import traceback
import os
import re
import sys

# Extra things used for distribution.
import encodings.utf_8
import encodings.zlib_codec

# Load up all of Ren'Py, in the right order.
import renpy

def main():

    name = os.path.basename(sys.argv[0])

    if name.find(".") != -1:
        name = name[:name.find(".")]

    if name.find("_") != -1:
        name = name[name.find("_") + 1:]

    if os.path.isdir(name):
        game = name
    else:
        game = "game"

    op = optparse.OptionParser()
    op.add_option('--game', dest='game', default=game,
                  help='The directory the game is in.')

    op.add_option('--python', dest='python', default=None,
                  help='Run the argument in the python interpreter.')

    op.add_option('--leak', dest='leak', action='store_true', default=False,
                  help='When the game exits, dumps a profile of memory usage.')

    options, args = op.parse_args()

    if options.python:
        execfile(options.python)
        sys.exit(0)

    try:
        renpy.main.main(options.game)
            
    except Exception, e:

        f = file("traceback.txt", "wU")

        f.write(codecs.BOM_UTF8)

        print >>f, "I'm sorry, but an exception occured while executing your Ren'Py"
        print >>f, "script."
        print >>f

        type, value, tb = sys.exc_info()


        print >>f, type.__name__ + ":", 
        print >>f, unicode(e).encode('utf-8')
        print >>f
        print >>f, renpy.game.exception_info

        print >>f
        print >>f, "-- Full Traceback ------------------------------------------------------------"
        print >>f  

        traceback.print_tb(tb, None, sys.stdout)
        traceback.print_tb(tb, None, f)

        print >>f, type.__name__ + ":", 
        print type.__name__ + ":", 

        print >>f, unicode(e).encode('utf-8')
        print unicode(e).encode('utf-8')

        print
        print >>f

        print renpy.game.exception_info
        print >>f, renpy.game.exception_info

        print >>f
        print >>f, "Ren'Py Version:", renpy.version

        f.close()

        try:
            os.startfile('traceback.txt')
        except:
            pass

    if options.leak:
        memory_profile()

    sys.exit(0)

def memory_profile():

    print "Memory Profile"
    print
    print "Showing all objects in memory at program termination."
    print

    import gc
    gc.collect()

    objs = gc.get_objects()

    c = { } # count
    dead_renders = 0

    for i in objs:
        t = type(i)
        c[t] = c.get(t, 0) + 1

        if isinstance(i, renpy.display.render.Render):
            if i.dead:
                dead_renders += 1
            

    results = [ (count, ty) for ty, count in c.iteritems() ]
    results.sort()

    for count, ty in results:
        print count, str(ty)

    if dead_renders:
        print
        print "*** found", dead_renders, "dead Renders. ***"
    
if __name__ == "__main__":
    main()
