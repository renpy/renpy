# Copyright 2004-2024 Tom Rothamel <pytom@bishoujo.us>
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

from __future__ import division, absolute_import, with_statement, print_function, unicode_literals
from renpy.compat import PY2, basestring, bchr, bord, chr, open, pystr, range, round, str, tobytes, unicode # *

from typing import Optional

import os
import sys
import subprocess
import io

# Encoding and sys.stderr/stdout handling ######################################

FSENCODING = sys.getfilesystemencoding() or "utf-8"

# Sets the default encoding to utf-8.
old_stdout = sys.stdout
old_stderr = sys.stderr

if PY2:
    sys_executable = sys.executable
    reload(sys) # type: ignore
    sys.setdefaultencoding("utf-8") # type: ignore
    sys.executable = sys_executable

def _setdefaultencoding(name):
    """
    This is install in sys to prevent games from trying to change the default
    encoding.
    """

sys.setdefaultencoding = _setdefaultencoding # type: ignore


sys.stdout = old_stdout
sys.stderr = old_stderr

import renpy.error


class NullFile(io.IOBase):
    """
    This file raises an error on input, and IOError on read.
    """

    def write(self, s):
        return

    def read(self, length=None):
        raise IOError("Not implemented.")

    def flush(self):
        return


def null_files():
    try:
        if (sys.stderr is None) or sys.stderr.fileno() < 0:
            sys.stderr = NullFile()

        if (sys.stdout is None) or sys.stdout.fileno() < 0:
            sys.stdout = NullFile()
    except Exception:
        pass


null_files()

# Tracing ######################################################################

trace_file = None
trace_local = None


def trace_function(frame, event, arg):
    fn = os.path.basename(frame.f_code.co_filename)
    trace_file.write("{} {} {} {}\n".format(fn, frame.f_lineno, frame.f_code.co_name, event)) # type: ignore
    return trace_local


def enable_trace(level):
    global trace_file
    global trace_local

    trace_file = open("trace.txt", "w", buffering=1, encoding="utf-8")

    if level > 1:
        trace_local = trace_function
    else:
        trace_local = None

    sys.settrace(trace_function)


def mac_start(fn):
    """
    os.start compatibility for mac.
    """

    os.system("open " + fn) # type: ignore

def popen_del(self, *args, **kwargs):
    """
    Fix an issue where the __del__ method of popen doesn't work.
    """

    return

def get_alternate_base(basedir, always=False):
    """
    :undocumented:

    Tries to find an alternate base directory. This exists in a writable
    location, and is intended for use by a game that downloads its assets
    to the device (generally for ios or android, where the assets may be
    too big for the app store).
    """

    # Determine the alternate base directory location.

    if renpy.android:
        altbase = os.path.join(os.environ["ANDROID_PRIVATE"], "base")

    elif renpy.ios:
        from pyobjus import autoclass # type: ignore
        from pyobjus.objc_py_types import enum # type: ignore

        NSSearchPathDirectory = enum("NSSearchPathDirectory", NSApplicationSupportDirectory=14)
        NSSearchPathDomainMask = enum("NSSearchPathDomainMask", NSUserDomainMask=1)

        NSFileManager = autoclass('NSFileManager')
        manager = NSFileManager.defaultManager()
        url = manager.URLsForDirectory_inDomains_(
            NSSearchPathDirectory.NSApplicationSupportDirectory,
            NSSearchPathDomainMask.NSUserDomainMask,
            ).lastObject()

        # url.path seems to change type based on iOS version, for some reason.
        try:
            altbase = url.path().UTF8String()
        except Exception:
            altbase = url.path.UTF8String()

        if isinstance(altbase, bytes):
            altbase = altbase.decode("utf-8")

    else:
        altbase = os.path.join(basedir, "base")

    if always:
        return altbase

    # Check to see if there's a game in there created with the
    # current version of Ren'Py.

    def ver(s):
        """
        Returns the first three components of a version string.
        """

        return tuple(int(i) for i in s.split(".")[:3])

    import json

    version_json = os.path.join(altbase, "update", "version.json")

    if not os.path.exists(version_json):
        return basedir

    with open(version_json, "r") as f:
        modules = json.load(f)

        for v in modules.values():
            if ver(v["renpy_version"]) != ver(renpy.version_only):
                return basedir

    return altbase


def bootstrap(renpy_base):

    global renpy

    import renpy.config
    import renpy.log

    # Remove a legacy environment setting.
    if os.environ.get("SDL_VIDEODRIVER", "") == "windib":
        del os.environ["SDL_VIDEODRIVER"]

    if not isinstance(renpy_base, str):
        renpy_base = str(renpy_base, FSENCODING)

    # If environment.txt exists, load it into the os.environ dictionary.
    if os.path.exists(renpy_base + "/environment.txt"):
        evars = { }
        with open(renpy_base + "/environment.txt", "r") as f:
            code = compile(f.read(), renpy_base + "/environment.txt", 'exec')
            exec(code, evars)
        for k, v in evars.items():
            if k not in os.environ:
                os.environ[k] = str(v)

    # Also look for it in an alternate path (the path that contains the
    # .app file.), if on a mac.
    alt_path = os.path.abspath("renpy_base")
    if ".app" in alt_path:
        alt_path = alt_path[:alt_path.find(".app") + 4]

        if os.path.exists(alt_path + "/environment.txt"):
            evars = { }
            with open(alt_path + "/environment.txt", "rb") as f:
                code = compile(f.read(), alt_path + "/environment.txt", 'exec')
                exec(code, evars)
            for k, v in evars.items():
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
        basedir = os.path.abspath(args.basedir)
        if not isinstance(basedir, str):
            basedir = basedir.decode(FSENCODING)
    else:
        basedir = renpy_base

    if not os.path.exists(basedir):
        sys.stderr.write("Base directory %r does not exist. Giving up.\n" % (basedir,))
        sys.exit(1)

    # Make game/ on Android.
    if renpy.android:
        if not os.path.exists(basedir + "/game"):
            os.mkdir(basedir + "/game", 0o777)

    sys.path.insert(0, basedir)

    if renpy.macintosh:
        # If we're on a mac, install our own os.start.
        os.startfile = mac_start # type: ignore

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
    except Exception:
        print("""\
Could not import pygame_sdl2. Please ensure that this program has been built
and unpacked properly. Also, make sure that the directories containing
this program do not contain : or ; in their names.

You may be using a system install of python. Please run {0}.sh,
{0}.exe, or {0}.app instead.
""".format(name), file=sys.stderr)

        raise

    gamedir = renpy.__main__.path_to_gamedir(basedir, name)

    # If we're not given a command, show the presplash.
    if args.command == "run" and not renpy.mobile:
        import renpy.display.presplash # @Reimport
        renpy.display.presplash.start(basedir, gamedir)

    # Ditto for the Ren'Py module.
    try:
        import _renpy
    except Exception:
        print("""\
Could not import _renpy. Please ensure that this program has been built
and unpacked properly.

You may be using a system install of python. Please run {0}.sh,
{0}.exe, or {0}.app instead.
""".format(name), file=sys.stderr)
        raise

    # Load the rest of Ren'Py.
    import renpy
    renpy.import_all()

    renpy.loader.init_importer()

    exit_status = None
    original_basedir = basedir
    original_sys_path = list(sys.path)

    try:
        while exit_status is None:
            exit_status = 1

            try:

                # Potentially use an alternate base directory.
                try:
                    basedir = get_alternate_base(original_basedir)
                except Exception:
                    import traceback
                    traceback.print_exc()

                gamedir = renpy.__main__.path_to_gamedir(basedir, name)

                sys.path = list(original_sys_path)
                if basedir not in sys.path:
                    sys.path.insert(0, basedir)

                renpy.game.args = args
                renpy.config.renpy_base = renpy_base
                renpy.config.basedir = basedir
                renpy.config.gamedir = gamedir
                renpy.config.args = [ ] # type: ignore

                renpy.config.logdir = renpy.__main__.path_to_logdir(basedir)

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
                        subprocess.Popen([sys.renpy_executable] + sys.argv[1:]) # type: ignore
                    else:
                        if PY2:
                            subprocess.Popen([sys.executable, "-EO"] + sys.argv)
                        else:
                            subprocess.Popen([sys.executable] + sys.argv)

            except renpy.game.ParseErrorException:
                pass

            except Exception as e:
                renpy.error.report_exception(e)

        sys.exit(exit_status)

    finally:

        if "RENPY_SHUTDOWN_TRACE" in os.environ:
            enable_trace(int(os.environ["RENPY_SHUTDOWN_TRACE"]))

        renpy.display.tts.tts(None) # type: ignore

        renpy.display.im.cache.quit() # type: ignore

        if renpy.display.draw: # type: ignore
            renpy.display.draw.quit() # type: ignore

        renpy.audio.audio.quit()

        # Prevent subprocess from throwing errors while trying to run it's
        # __del__ method during shutdown.
        if not renpy.emscripten:
            subprocess.Popen.__del__ = popen_del # type: ignore

        if renpy.android:
            from jnius import autoclass # type: ignore

            import android
            android.activity.finishAndRemoveTask()

            # Avoid running Python shutdown, which can cause more harm than good. (#5280)
            System = autoclass("java.lang.System")
            System.exit(0)
