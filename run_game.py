#!/usr/bin/env python

# Go psyco! (Compile where we can.)
try:
    import psyco
    psyco.full()
except ImportError:
    pass

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

        print >>f, "I'm sorry, but an exception occured while executing your Ren'Py"
        print >>f, "script."
        print >>f

        traceback.print_exc(None, sys.stdout)
        traceback.print_exc(None, f)

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
        

    
