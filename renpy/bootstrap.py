# 2004-2008 PyTom <pytom@bishoujo.us>
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
    import datetime; datetime
    import encodings.ascii
    import encodings.utf_8
    import encodings.zlib_codec
    import encodings.unicode_escape
    import encodings.string_escape
    import encodings.raw_unicode_escape
    import encodings.mbcs
    import encodings.utf_16_be
    import encodings.utf_16_le; encodings.utf_16_le
    import math; math
    import glob; glob
    import pickle; pickle
    import platform; platform
    import pysdlsound
    import pysdlsound.sound
    import pysdlsound.winmixer
    import pysdlsound.linmixer; pysdlsound.linmixer
    import difflib; difflib
    import shutil; shutil
    import renpy.tools.archiver
    import renpy.tools.add_from; renpy.tools.add_from
    import tarfile; tarfile
    import bz2; bz2
    import webbrowser; webbrowser
    import pygame.locals
    import pygame.color
    import pygame.colordict; pygame.colordict
    import posixpath; posixpath # W0403
    import ctypes
    import ctypes.wintypes; ctypes.wintypes
    import EasyDialogs; EasyDialogs
    
trace_file = None
trace_local = None

def trace_function(frame, event, arg):
    fn = os.path.basename(frame.f_code.co_filename)
    print >>trace_file, fn, frame.f_lineno, frame.f_code.co_name, event
    return trace_local
    
def enable_trace(level):
    global trace_file
    global trace_local

    trace_file = file("trace.txt", "w", 1)

    if level > 1:
        trace_local = trace_function
    else:
        trace_local = None
 
    sys.settrace(trace_function)

def mac_start(fn):
    os.system("open " + fn)

# This code fixes a bug in subprocess.Popen.__del__
def popen_del(self, _deadstate=sys.maxint):
    if not self._child_created:
        return
    self.poll(_deadstate=_deadstate)

    try:
        import subprocess # W0403
        if self.returncode is None and subprocess._active is not None: # E1101
            subprocess._active.append(self) # E1101
    except:
        pass
            
def bootstrap(renpy_base):

    global renpy # W0602

    os.environ["RENPY_BASE"] = os.path.abspath(renpy_base)
    
    # If environment.txt exists, load it into the os.environ dictionary.
    if os.path.exists(renpy_base + "/environment.txt"):
        evars = { }
        execfile(renpy_base + "/environment.txt", evars)
        for k, v in evars.iteritems():
            if k not in os.environ:
                os.environ[k] = str(v)
    
    # Get a working name for the game.
    name = os.path.basename(sys.argv[0])

    if name.find(".") != -1:
        name = name[:name.find(".")]

    op = optparse.OptionParser()

    op.add_option('--arg', dest='args', default=[], action='append',
                  help='Append an argument to a list that can be accessed as config.args.')

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

    op.add_option('--trace', dest='trace', action='count', default=0,
                  help='Dump internal trace data to trace.txt. Use twice to dump in absurd detail.')
    
    op.add_option('--leak', dest='leak', action='store_true', default=False,
                  help=optparse.SUPPRESS_HELP)

    op.add_option('--warp', dest='warp', default=None,
                  help='This takes as an argument a filename:linenumber pair, and tries to warp to the statement before that line number.')

    op.add_option('--remote', dest='remote', action='store_true',
                  help="Allows Ren'Py to be fed commands on stdin.")

    op.add_option('--rmpersistent', dest='rmpersistent', action='store_true',
                  help="Deletes the persistent data, and exits.")

    op.add_option('--presplash', dest='presplash', default=None,
                  help="Used internally to display the presplash screen.")
                  
    options, args = op.parse_args()

    if options.presplash:
        import renpy.display.presplash
        renpy.display.presplash.show(options.presplash)
    
    if options.trace:
        enable_trace(options.trace)
    
    if options.python:
        import __main__
        sys.argv = [ options.python ] + args
        execfile(options.python, __main__.__dict__, __main__.__dict__)
        sys.exit(0)

    args = list(args)
            
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

        gamedirs.extend([ 'game', 'data', 'launcher'])

        for i in gamedirs:

            if i == "renpy":
                continue

            gamedir = basedir + "/" + i
            if os.path.isdir(gamedir):
                break
        else:
            gamedir = basedir

    sys.path.insert(0, basedir)
            
    # Force windib on windows, unless the user explicitly overrides.
    if hasattr(sys, 'winver') and not 'SDL_VIDEODRIVER' in os.environ:
        os.environ['SDL_VIDEODRIVER'] = 'windib'

    # Show the presplash.
    if not options.lint and not options.compile and not options.version and not options.rmpersistent:
        import renpy.display.presplash # W0404
        renpy.display.presplash.start(gamedir)

    # Fix an exception thrown by garbage collection.
    import subprocess # W0403
    subprocess.Popen.__del__ = popen_del # E1101

    # If we're on a mac, install our own os.start.
    if sys.platform == "darwin":
        os.startfile = mac_start
        
    # Load up all of Ren'Py, in the right order.
    import renpy
    renpy.import_all()

    if options.version:
        print renpy.version
        sys.exit(0)

    keep_running = True
    report_error = None

    while keep_running:
        try:
            renpy.game.options = options

            renpy.config.renpy_base = renpy_base
            renpy.config.basedir = basedir
            renpy.config.gamedir = gamedir
            renpy.config.args = options.args
            
            renpy.main.main()
            keep_running = False

        except KeyboardInterrupt:
            import traceback
            traceback.print_exc()
            break
            
        except renpy.game.UtterRestartException:
            
            # Only works after a full restart.
            report_error = renpy.display.error.ReportError()
            
            # On an UtterRestart, reload Ren'Py.
            renpy.reload_all()
            continue

        except renpy.game.ParseErrorException:
            
            if report_error and report_error.report('a parse error'):
                renpy.reload_all()
                keep_running = True
            else:
                keep_running = False
        
        except Exception, e:
            report_exception(e)

            if report_error and report_error.report('an exception'):
                renpy.reload_all()
                keep_running = True
            else:
                keep_running = False
            
    if options.leak:
        memory_profile()

    renpy.display.im.cache.quit()
    
    sys.exit(0)


def report_tb(out, tb):

    while tb:
        f = tb.tb_frame
        line = tb.tb_lineno
        co = f.f_code
        filename = co.co_filename
        
        if filename.endswith(".rpy") and not filename.startswith("common"):
            print >>out, " - python at line %d of %s." % (line, filename)

        elif 'self' in f.f_locals:
            obj = f.f_locals['self']

            import renpy
            
            if isinstance(obj, renpy.execution.Context):
                obj.report_tb(out)

        tb = tb.tb_next

def report_exception(e):
    import renpy

    import codecs
    import traceback

    type, value, tb = sys.exc_info()

    def safe_utf8(e):
        try:
            m = unicode(e)
        except:
            m = str(e)
            
        if isinstance(m, unicode):
            return m.encode("utf-8")
        else:
            return m

    # Outside of the file.
    traceback.print_tb(tb, None, sys.stdout)
    print type.__name__ + ":", 
    print safe_utf8(e)
    print
    print renpy.game.exception_info
    report_tb(sys.stdout, tb)
    
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
        report_tb(f, tb)
        
        print >>f
        print >>f, "-- Full Traceback ------------------------------------------------------------"
        print >>f  

        traceback.print_tb(tb, None, f)
        print >>f, type.__name__ + ":", 
        print >>f, safe_utf8(e)

        print >>f

        print >>f, renpy.game.exception_info
        report_tb(f, tb)

        print >>f
        print >>f, "Ren'Py Version:", renpy.version

        f.close()

        try:
            if renpy.config.editor:
                renpy.exports.launch_editor([ 'traceback.txt' ], 1, transient=1)
            else:
                os.startfile('traceback.txt')
        except:
            pass

    except:
        pass


def memory_profile():

    print "Memory Profile"
    print
    print "Showing all objects in memory at program termination."
    print

    import gc
    gc.collect()

    objs = gc.get_objects()

    c = { } # count

    for i in objs:
        t = type(i)
        c[t] = c.get(t, 0) + 1

    results = [ (count, ty) for ty, count in c.iteritems() ]
    results.sort()

    for count, ty in results:
        print count, str(ty)

