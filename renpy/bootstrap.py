# Copyright 2004-2018 Tom Rothamel <pytom@bishoujo.us>
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

from __future__ import print_function
import os.path
import sys
import subprocess
import io

FSENCODING = sys.getfilesystemencoding() or "utf-8"

# Sets the default encoding to the filesystem encoding.
old_stdout = sys.stdout
old_stderr = sys.stderr

reload(sys)
sys.setdefaultencoding(FSENCODING)  # @UndefinedVariable

sys.stdout = old_stdout
sys.stderr = old_stderr

import renpy.error


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
    import encodings.idna; encodings.idna
    import math; math
    import glob; glob
    import pickle; pickle
    import difflib; difflib
    import shutil; shutil
    import tarfile; tarfile
    import bz2; bz2  # @UnresolvedImport
    import webbrowser; webbrowser
    import posixpath; posixpath
    import ctypes; ctypes
    import ctypes.wintypes; ctypes.wintypes
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
    import _renpysteam; _renpysteam
    import compileall; compileall
    import cProfile; cProfile
    import pstats; pstats
    import _ssl; _ssl

    # Used by requests.
    import cgi; cgi
    import Cookie; Cookie
    import hmac; hmac
    import Queue; Queue
    import uuid; uuid


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
    print(fn, frame.f_lineno, frame.f_code.co_name, event, file=trace_file)
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

    global renpy  # W0602

    import renpy.log  # @UnusedImport

    # Remove a legacy environment setting.
    if os.environ.get(b"SDL_VIDEODRIVER", "") == "windib":
        del os.environ[b"SDL_VIDEODRIVER"]

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

    if args.trace:
        enable_trace(args.trace)

    if args.basedir:
        basedir = os.path.abspath(args.basedir).decode(FSENCODING)
    else:
        basedir = renpy_base

    if not os.path.exists(basedir):
        sys.stderr.write("Base directory %r does not exist. Giving up.\n" % (basedir,))
        sys.exit(1)

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

    if renpy.macintosh:
        # If we're on a mac, install our own os.start.
        os.startfile = mac_start

        # Are we starting from inside a mac app resources directory?
        if basedir.endswith("Contents/Resources/autorun"):
            renpy.macapp = True

    # Check that we have installed pygame properly. This also deals with
    # weird cases on Windows and Linux where we can't import modules. (On
    # windows ";" is a directory separator in PATH, so if it's in a parent
    # directory, we won't get the libraries in the PATH, and hence pygame
    # won't import.)
    try:
        import pygame_sdl2
        if not ("pygame" in sys.modules):
            pygame_sdl2.import_as_pygame()
    except:
        print("""\
Could not import pygame_sdl2. Please ensure that this program has been built
and unpacked properly. Also, make sure that the directories containing
this program do not contain : or ; in their names.

You may be using a system install of python. Please run {0}.sh,
{0}.exe, or {0}.app instead.
""".format(name), file=sys.stderr)

        raise

    # If we're not given a command, show the presplash.
    if args.command == "run" and not renpy.mobile:
        import renpy.display.presplash  # @Reimport
        renpy.display.presplash.start(basedir, gamedir)

    # Ditto for the Ren'Py module.
    try:
        import _renpy; _renpy
    except:
        print("""\
Could not import _renpy. Please ensure that this program has been built
and unpacked properly.

You may be using a system install of python. Please run {0}.sh,
{0}.exe, or {0}.app instead.
""".format(name), file=sys.stderr)
        raise

    # Load up all of Ren'Py, in the right order.

    import renpy  # @Reimport
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
                    os.makedirs(renpy.config.logdir, 0o777)

                renpy.main.main()

                exit_status = 0

            except KeyboardInterrupt:
                raise

            except renpy.game.UtterRestartException:

                # On an UtterRestart, reload Ren'Py.
                renpy.reload_all()

                exit_status = None

            except renpy.game.QuitException as e:
                exit_status = e.status

                if e.relaunch:
                    if hasattr(sys, "renpy_executable"):
                        subprocess.Popen([sys.renpy_executable] + sys.argv[1:])
                    else:
                        subprocess.Popen([sys.executable, "-EO"] + sys.argv)

            except renpy.game.ParseErrorException:
                pass

            except Exception as e:
                renpy.error.report_exception(e)
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
