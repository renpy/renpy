# Copyright 2004-2007 PyTom <pytom@bishoujo.us>
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

import optparse
import os
import os.path
import sys

# Extra things used for distribution.
def extra_imports():
    import datetime
    import encodings.ascii
    import encodings.utf_8
    import encodings.zlib_codec
    import encodings.unicode_escape
    import encodings.string_escape
    import encodings.raw_unicode_escape
    import encodings.mbcs
    import math
    import glob
    import platform
    import pysdlsound
    import pysdlsound.sound
    import pysdlsound.nativemidi
    import pysdlsound.winmixer
    import pysdlsound.linmixer
    import difflib
    import shutil
    import renpy.tools.archiver
    import renpy.tools.add_from
    import tarfile
    import bz2
    import webbrowser
    
def bootstrap(renpy_base):

    # Get a working name for the game.
    name = os.path.basename(sys.argv[0])

    if name.find(".") != -1:
        name = name[:name.find(".")]

    op = optparse.OptionParser()
    op.add_option('--version', dest='version', default=False, action='store_true',
                  help="Display the version of Ren'Py")

    op.add_option('--game', dest='game', default=None,
                  help='The directory the game is in.')

    op.add_option("--savedir", dest='savedir', default=None, action='store',
                  help='The directory in which to save data. Defaults to the saves directory under the game directory.')

    op.add_option('--lock', dest='lock', default=None, action='store',
                  help=optparse.SUPPRESS_HELP)

    op.add_option('--python', dest='python', default=None,
                  help=optparse.SUPPRESS_HELP)

    op.add_option('--compile', dest='compile', default=False, action='store_true',
                  help="Causes Ren'Py to compile all .rpy files to .rpyc files, and then quit.")

    op.add_option('--lint', dest='lint', default=False, action='store_true',
                  help='Run a number of expensive tests, to try to detect errors in the script.')

    op.add_option('--profile', dest='profile', action='store_true', default=False,
                  help='Causes the amount of time it takes to draw the screen to be profiled.')

    op.add_option('--leak', dest='leak', action='store_true', default=False,
                  help=optparse.SUPPRESS_HELP)

    op.add_option('--warp', dest='warp', default=None,
                  help='This takes as an argument a filename:linenumber pair, and tries to warp to the statement before that line number.')

    options, args = op.parse_args()

    if options.python:
        import __main__
        sys.argv = [ options.python ] + args
        execfile(options.python, __main__.__dict__, __main__.__dict__)
        sys.exit(0)

    if len(args) >= 1:
        basedir = os.path.abspath(args[0])
    else:
        basedir = renpy_base

    # If we made it this far, we will be running the game, or at least
    # doing a lint.

    # os.chdir(renpy_base)

    # Look for the game directory.
    if options.game:
        gamedir = options.game

    else:
        gamedirs = [ name ]
        game_name = name

        while game_name:
            prefix = game_name[0]
            game_name = game_name[1:]

            if prefix == ' ' or prefix == '_':
                gamedirs.append(game_name)

        gamedirs.extend([ 'game', 'data',])

        for i in gamedirs:

            if i == "renpy":
                continue

            gamedir = basedir + "/" + i
            if os.path.isdir(gamedir):
                break
        else:
            gamedir = basedir
    
    # Force windib on windows, unless the user explicitly overrides.
    if hasattr(sys, 'winver') and not 'SDL_VIDEODRIVER' in os.environ:
        os.environ['SDL_VIDEODRIVER'] = 'windib'

    # Show the presplash.
    if not options.lint and not options.compile and not options.version:
        import renpy.display.presplash
        renpy.display.presplash.start(gamedir)

    # Load up all of Ren'Py, in the right order.
    import renpy
    renpy.import_all()

    if options.version:
        print renpy.version
        sys.exit(0)

    try:

        keep_running = True
        while keep_running:
            try:
                renpy.game.options = options

                renpy.config.renpy_base = renpy_base
                renpy.config.basedir = basedir
                renpy.config.gamedir = gamedir

                renpy.main.main()
                keep_running = False

            except renpy.game.UtterRestartException:

                # On an UtterRestart, reload Ren'Py.
                renpy.reload_all()
                continue
            
    except Exception, e:
        import codecs
        import traceback

        type, value, tb = sys.exc_info()

        def safe_utf8(e):
            try:
                return unicode(e).encode("utf-8")
            except:
                return str(e)

        # Outside of the file.
        traceback.print_tb(tb, None, sys.stdout)
        print type.__name__ + ":", 
        print safe_utf8(e)
        print
        print renpy.game.exception_info

        # Inside of the file, which may not be openable.
        try:

            f = file("traceback.txt", "w")

            f.write(codecs.BOM_UTF8)

            print >>f, "I'm sorry, but an exception occured while executing your Ren'Py"
            print >>f, "script."
            print >>f

            print >>f, type.__name__ + ":", 
            print >>f, safe_utf8(e)
            print >>f
            print >>f, renpy.game.exception_info

            print >>f
            print >>f, "-- Full Traceback ------------------------------------------------------------"
            print >>f  

            traceback.print_tb(tb, None, f)
            print >>f, type.__name__ + ":", 
            print >>f, safe_utf8(e)

            print >>f

            print >>f, renpy.game.exception_info

            print >>f
            print >>f, "Ren'Py Version:", renpy.version

            f.close()

            try:
                if renpy.config.editor:
                    renpy.exports.launch_editor([ 'traceback.txt' ], 1)
                else:
                    os.startfile('traceback.txt')
            except:
                pass

        except:
            pass


    if options.leak:
        memory_profile()

    sys.exit(0)

def memory_profile():

    import renpy

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
