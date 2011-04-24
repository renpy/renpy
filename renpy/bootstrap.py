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
import os.path
import sys
import cStringIO
import platform

# Extra things used for distribution.
def extra_imports():
    import datetime; datetime
    import encodings.ascii; encodings.ascii
    import encodings.utf_8; encodings.utf_8
    import encodings.zlib_codec; encodings.zlib_codec
    import encodings.unicode_escape; encodings.unicode_escape
    import encodings.string_escape; encodings.string_escape
    import encodings.raw_unicode_escape; encodings.raw_unicode_escape
    import encodings.mbcs; encodings.mbcs
    import encodings.utf_16; encodings.utf_16
    import encodings.utf_16_be; encodings.utf_16_be
    import encodings.utf_16_le; encodings.utf_16_le
    import math; math
    import glob; glob
    import pickle; pickle
    import pysdlsound; pysdlsound
    import pysdlsound.sound; pysdlsound.sound
    import pysdlsound.winmixer; pysdlsound.winmixer
    import pysdlsound.linmixer; pysdlsound.linmixer
    import difflib; difflib
    import shutil; shutil
    import renpy.tools.archiver; renpy.tools.archiver
    import renpy.tools.add_from; renpy.tools.add_from
    import tarfile; tarfile
    import bz2; bz2
    import webbrowser; webbrowser
    import pygame.locals; pygame.locals
    import pygame.color; pygame.color
    import pygame.colordict; pygame.colordict
    import posixpath; posixpath # W0403
    import ctypes; ctypes
    import ctypes.wintypes; ctypes.wintypes
    import EasyDialogs; EasyDialogs #@UnresolvedImport
    import argparse; argparse
    import compiler; compiler
    import textwrap; textwrap
    import copy; copy
    import urllib; urllib
    import urllib2; urllib2
    
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
def popen_del(self, *args, **kwargs):
    return

def bootstrap(renpy_base):

    global renpy # W0602

    import renpy.log #@UnusedImport

    os.environ["RENPY_BASE"] = os.path.abspath(renpy_base)
    
    # If environment.txt exists, load it into the os.environ dictionary.
    if os.path.exists(renpy_base + "/environment.txt"):
        evars = { }
        execfile(renpy_base + "/environment.txt", evars)
        for k, v in evars.iteritems():
            if k not in os.environ:
                os.environ[k] = str(v)

    # Also look for it in an alternate path (the path that contains the
    # .app file.), if on a mac.
    alt_path = os.path.abspath("renpy_base")
    if ".app" in alt_path:
        alt_path = alt_path[:alt_path.find(".app")+4]
        
        if os.path.exists(alt_path + "/environment.txt"):
            evars = { }
            execfile(alt_path + "/environment.txt", evars)
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

    op.add_option('--log-startup', dest='log_startup', action='store_true', default=os.environ.get("RENPY_LOG_STARTUP", None),
                  help="Causes Ren'Py to log startup timings to its log.")

    op.add_option('--debug-image-cache', dest='debug_image_cache', action='store_true', default=False,
                  help="Causes Ren'Py to log startup timings to its log.")
                  
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
        import renpy.display.presplash #@Reimport
        renpy.display.presplash.start(gamedir)

    # If we're on a mac, install our own os.start.
    if sys.platform == "darwin":
        os.startfile = mac_start
        
    # Load up all of Ren'Py, in the right order.
    import renpy #@Reimport
    renpy.import_all()

    if options.version:
        print renpy.version
        sys.exit(0)

    keep_running = True

    try:
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

                if renpy.display.draw:
                    renpy.display.draw.deinit()
                    renpy.display.draw.quit()
                    
                # On an UtterRestart, reload Ren'Py.
                renpy.reload_all()
                continue

            except renpy.game.QuitException:
                keep_running = False

            except renpy.game.ParseErrorException:
                keep_running = False

            except Exception, e:
                report_exception(e)
                keep_running = False

        sys.exit(0)

    finally:
        
        if "RENPY_SHUTDOWN_TRACE" in os.environ:
            enable_trace(int(os.environ["RENPY_SHUTDOWN_TRACE"]))

        renpy.display.im.cache.quit()

        if renpy.display.draw:
            renpy.display.draw.quit()

        # Prevent subprocess from throwing errors while trying to run it's
        # __del__ method during shutdown.
        import subprocess # W0403
        subprocess.Popen.__del__ = popen_del # E1101

        if options.leak:
            memory_profile()

def report_line(out, filename, line, what):
    out.write('  File "%s", line %d, in %s\n' % (filename, line, what))
    try:
        fn = renpy.parser.unelide_filename(filename)
        f = file(fn, "rb")            
        lines = f.read().decode("utf-8").replace("\r", "").split("\n")
        out.write("    " + lines[line - 1].encode("utf-8") + "\n")
    except:
        pass
         

def report_tb(out, tb):

    while tb:
        f = tb.tb_frame
        line = tb.tb_lineno
        co = f.f_code
        filename = co.co_filename
        
        if filename.endswith(".rpy") and not filename.replace("\\", "/").startswith("common/"):
            report_line(out, filename, line, "python")

        elif 'self' in f.f_locals:
            obj = f.f_locals['self']
 
            import renpy
            
            if isinstance(obj, renpy.execution.Context):
                obj.report_tb(out)

        tb = tb.tb_next

def report_exception(e, editor=True):
    """
    Reports an exception by writing it to standard error and 
    traceback.txt. If `editor` is True, opens the traceback 
    up in a text editor.
    
    Returns a two-unicode tuple, with the first item being 
    a simple message, and the second being a full traceback.
    """
    
    import codecs
    import traceback

    type, _value, tb = sys.exc_info()

    def safe_utf8(e):
        try:
            m = unicode(e)
        except:
            m = str(e)
            
        if isinstance(m, unicode):
            return m.encode("utf-8")
        else:
            return m
    
    # Return values - which can be displayed to the user.
    simple = cStringIO.StringIO()
    full = cStringIO.StringIO()
    
    print >>simple, renpy.game.exception_info
    report_tb(simple, tb)
    print >>simple, type.__name__ + ":", 
    print >>simple, safe_utf8(e)

    print >>full, "Full traceback:"
    traceback.print_tb(tb, None, full)
    print >>full, type.__name__ + ":", 
    print >>full, safe_utf8(e)
    
    # Write to stdout/stderr.
    sys.stdout.write("\n")
    sys.stdout.write(full.getvalue())
    sys.stdout.write("\n")
    sys.stdout.write(simple.getvalue())

    print >>full
    try:
        print >>full, platform.platform()
        print >>full, renpy.version
        print >>full, renpy.config.name + " " + renpy.config.version
    except:
        pass

    
    simple = simple.getvalue()
    full = full.getvalue()
 
    # Inside of the file, which may not be openable.
    try:

        f = file("traceback.txt", "w")

        f.write(codecs.BOM_UTF8)

        print >>f, "I'm sorry, but an uncaught exception occurred."
        print >>f

        f.write(simple)
        
        print >>f
        print >>f, "-- Full Traceback ------------------------------------------------------------"
        print >>f  

        f.write(full)
        f.close()
        
        try:
            if editor:
                if renpy.config.editor:
                    renpy.exports.launch_editor([ 'traceback.txt' ], 1, transient=1)
                else:
                    os.startfile('traceback.txt') #@UndefinedVariable
        except:
            pass

    except:
        pass

    try:
        renpy.display.log.exception() #@UndefinedVariable
    except:
        pass

    return simple.decode("utf-8"), full.decode("utf-8")


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

