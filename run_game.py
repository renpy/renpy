#!/usr/bin/env python

# Go psyco! (Compile where we can.)
try:
    import psyco
    psyco.full()
except ImportError:
    pass

import codecs
import optparse
import traceback
import os
import os.path
import re
import sys

# Extra things used for distribution.
import encodings.utf_8
import encodings.zlib_codec

# Load up all of Ren'Py, in the right order.
import renpy

if __name__ == "__main__":


    # Stdout should be a utf-8 stream, so print works nicely.
    # utf8writer = codecs.getwriter("utf-8")
    # sys.stdout = utf8writer(sys.stdout)

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

        traceback.print_tb(tb, None, sys.stdout)
        traceback.print_tb(tb, None, f)

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
        
    sys.exit(0)
        

    
