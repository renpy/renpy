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

import os.path
import sys
import cStringIO
import platform
import traceback
import subprocess
import io

FSENCODING = sys.getfilesystemencoding() or "utf-8"

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
    import encodings.utf_32_be; encodings.utf_32_be
    import encodings.latin_1; encodings.latin_1
    import encodings.hex_codec; encodings.hex_codec
    import encodings.base64_codec; encodings.base64_codec
    import math; math
    import glob; glob
    import pickle; pickle
    import pysdlsound; pysdlsound #@UnresolvedImport
    import pysdlsound.sound; pysdlsound.sound #@UnresolvedImport
    import pysdlsound.winmixer; pysdlsound.winmixer #@UnresolvedImport
    import pysdlsound.linmixer; pysdlsound.linmixer #@UnresolvedImport
    import difflib; difflib
    import shutil; shutil
    import tarfile; tarfile
    import bz2; bz2  # @UnresolvedImport
    import webbrowser; webbrowser
    import pygame.locals; pygame.locals
    import pygame.color; pygame.color
    import pygame.colordict; pygame.colordict
    import posixpath; posixpath
    import ctypes; ctypes
    import ctypes.wintypes; ctypes.wintypes
    import EasyDialogs; EasyDialogs #@UnresolvedImport
    import argparse; argparse
    import compiler; compiler
    import textwrap; textwrap
    import copy; copy
    import urllib; urllib
    import urllib2; urllib2
    import codecs; codecs
    import rsa; rsa
    import decimal; decimal
    import plistlib; plistlib

class NullFile(io.IOBase):
    """
    This file raises an error on input, and IOError on read.
    """

    def write(self, s):
        return

    def read(self, length=None):
        raise IOError("Not implemented.")

def null_files():
    try:
        if sys.stderr.fileno() < 0:
            sys.stderr = NullFile()

        if sys.stdout.fileno() < 0:
            sys.stdout = NullFile()
    except:
        pass

null_files()


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

    renpy_base = unicode(renpy_base, FSENCODING, "replace")

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

    # Parse the arguments.
    import renpy.arguments
    args = renpy.arguments.bootstrap()

    # Since we don't have time to fully initialize before running the presplash
    # command, handle it specially.
    if args.command == "presplash":
        import renpy.display.presplash
        renpy.display.presplash.show(sys.argv[3])

    if args.trace:
        enable_trace(args.trace)

    if args.basedir:
        basedir = os.path.abspath(args.basedir).decode(FSENCODING)
    else:
        basedir = renpy_base


    gamedirs = [ name ]
    game_name = name

    while game_name:
        prefix = game_name[0]
        game_name = game_name[1:]

        if prefix == ' ' or prefix == '_':
            gamedirs.append(game_name)

    gamedirs.extend([ 'game', 'data', 'launcher/game' ])

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
    if renpy.windows and not 'SDL_VIDEODRIVER' in os.environ:
        os.environ['SDL_VIDEODRIVER'] = 'windib'

    # If we're not given a command, show the presplash.
    if args.command == "run":
        import renpy.display.presplash #@Reimport
        renpy.display.presplash.start(basedir, gamedir)

    # If we're on a mac, install our own os.start.
    if renpy.macintosh:
        os.startfile = mac_start


    # Check that we have installed pygame properly. This also deals with
    # weird cases on Windows and Linux where we can't import modules. (On
    # windows ";" is a directory separator in PATH, so if it's in a parent
    # directory, we won't get the libraries in the PATH, and hence pygame
    # won't import.)
    try:
        import pygame; pygame
    except:
        print >>sys.stderr, """\
Could not import pygame. Please ensure that this program has been built
and unpacked properly. Also, make sure that the directories containing
this program do not contain : or ; in their names.

You may be using a system install of python. Please run {0}.sh,
{0}.exe, or {0}.app instead.
""".format(name)

        raise

    # Ditto for the Ren'Py module.
    try:
        import _renpy; _renpy
    except:
        print >>sys.stderr, """\
Could not import _renpy. Please ensure that this program has been built
and unpacked properly.

You may be using a system install of python. Please run {0}.sh,
{0}.exe, or {0}.app instead.
""".format(name)
        raise

    # Load up all of Ren'Py, in the right order.

    import renpy #@Reimport
    renpy.import_all()

    renpy.loader.init_importer()

    exit_status = None

    try:
        while exit_status is None:
            exit_status = 1

            try:
                renpy.game.args = args
                renpy.config.renpy_base = renpy_base
                renpy.config.basedir = basedir
                renpy.config.gamedir = gamedir
                renpy.config.args = [ ]

                if renpy.android:
                    renpy.config.logdir = os.environ['ANDROID_PUBLIC']
                else:
                    renpy.config.logdir = basedir

                if not os.path.exists(renpy.config.logdir):
                    os.makedirs(renpy.config.logdir, 0777)

                renpy.main.main()

                exit_status = 0

            except KeyboardInterrupt:
                raise

            except renpy.game.UtterRestartException:

                if renpy.display.draw:
                    renpy.display.draw.deinit()
                    renpy.display.draw.quit()

                # On an UtterRestart, reload Ren'Py.
                renpy.reload_all()

                exit_status = None

            except renpy.game.QuitException as e:
                exit_status = e.status

                if e.relaunch:
                    subprocess.Popen([sys.executable, "-EO"] + sys.argv)

            except renpy.game.ParseErrorException:
                pass

            except Exception, e:
                report_exception(e)
                pass

        sys.exit(exit_status)

    finally:

        if "RENPY_SHUTDOWN_TRACE" in os.environ:
            enable_trace(int(os.environ["RENPY_SHUTDOWN_TRACE"]))

        renpy.display.im.cache.quit()

        if renpy.display.draw:
            renpy.display.draw.quit()

        # Prevent subprocess from throwing errors while trying to run it's
        # __del__ method during shutdown.
        subprocess.Popen.__del__ = popen_del

def report_line(out, filename, line, what):
    out.write('  File "%s", line %d, in %s\n' % (filename, line, what))
    try:
        fn = renpy.parser.unelide_filename(filename)
        f = file(fn, "rb")
        lines = f.read().decode("utf-8").replace("\r", "").split("\n")
        out.write("    " + lines[line - 1].encode("utf-8") + "\n")
    except:
        pass


def write_utf8_traceback_list(out, l):
    """
    Given the traceback list l, writes it to out as utf-8.
    """

    ul = [ ]

    for filename, line, what, text in l:

        # Filename is either unicode or an fsecoded string.
        if not isinstance(filename, unicode):
            filename = unicode(filename, FSENCODING, "replace")

        # Line is a number.

        # Assume what is in a unicode encoding, since it is either python,
        # or comes from inside Ren'Py.

        if isinstance(text, str):
            text = text.decode("utf-8", "replace")

        ul.append((filename, line, what, text))

    for t in traceback.format_list(ul):
        out.write(t.encode("utf-8", "replace"))


def script_level_traceback(out, tb):
    """
    Writes a script-level traceback to out, based on the traceback
    object tb.
    """

    tbl = [ ]

    while tb:
        f = tb.tb_frame
        line = tb.tb_lineno
        co = f.f_code
        filename = co.co_filename

        if filename.endswith(".rpy") and not filename.replace("\\", "/").startswith("common/"):
            tbl.append((filename, line, "python", None))

        elif 'self' in f.f_locals:
            obj = f.f_locals['self']

            import renpy

            if isinstance(obj, renpy.execution.Context):
                tbl.extend(obj.report_tb(out))

        tb = tb.tb_next

    write_utf8_traceback_list(out, tbl)

def open_error_file(fn, mode):
    """
    Opens an error/log/file. Returns the open file, and the filename that
    was opened.
    """

    try:
        f = file(os.path.join(renpy.config.logdir, fn), mode)
        return f, fn
    except:
        pass

    try:
        f = file(fn, mode)
        return f, fn
    except:
        pass

    import tempfile

    fn = os.path.join(tempfile.gettempdir(), "renpy-" + fn)
    return file(fn, mode), fn

def report_exception(e, editor=True):
    """
    Reports an exception by writing it to standard error and
    traceback.txt. If `editor` is True, opens the traceback
    up in a text editor.

    Returns a two-unicode tuple, with the first item being
    a simple message, and the second being a full traceback.
    """

    import codecs

    type, _value, tb = sys.exc_info() #@ReservedAssignment

    def safe_utf8(e):
        try:
            m = unicode(e)
        except:
            m = str(e)

        if isinstance(m, unicode):
            return m.encode("utf-8", "replace")
        else:
            return m

    # Return values - which can be displayed to the user.
    simple = cStringIO.StringIO()
    full = cStringIO.StringIO()

    print >>simple, renpy.game.exception_info
    script_level_traceback(simple, tb)
    print >>simple, type.__name__ + ":",
    print >>simple, safe_utf8(e)

    print >>full, "Full traceback:"
    tbl = traceback.extract_tb(tb)
    write_utf8_traceback_list(full, tbl)
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

        f, traceback_fn = open_error_file("traceback.txt", "w")

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
            if editor and renpy.game.args.command == "run": #@UndefinedVariable
                renpy.exports.launch_editor([ traceback_fn ], 1, transient=1)
        except:
            pass

    except:
        pass

    try:
        renpy.display.log.exception() #@UndefinedVariable
    except:
        pass

    return simple.decode("utf-8", "replace"), full.decode("utf-8", "replace"), traceback_fn


old_memory = { }

def memory_profile():
    """
    Calling this function displays the change in the number of instances of
    each type of object.
    """

    print "- Memory Profile ---------------------------------------------------"

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
        diff = count - old_memory.get(ty, 0)
        old_memory[ty] = count
        if diff:
            print diff, ty
