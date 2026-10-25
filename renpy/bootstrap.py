# Copyright 2004-2026 Tom Rothamel <pytom@bishoujo.us>
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

import os
import io
import importlib.abc
import importlib.util
import sys
import subprocess
import textwrap

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
    trace_file.write("{} {} {} {}\n".format(fn, frame.f_lineno, frame.f_code.co_name, event))  # type: ignore
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
    import shlex

    os.system("open " + shlex.quote(fn))  # type: ignore


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
        from pyobjus import autoclass  # type: ignore
        from pyobjus.objc_py_types import enum  # type: ignore

        NSSearchPathDirectory = enum("NSSearchPathDirectory", NSApplicationSupportDirectory=14)
        NSSearchPathDomainMask = enum("NSSearchPathDomainMask", NSUserDomainMask=1)

        NSFileManager = autoclass("NSFileManager")
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


def excepthook(type, value, traceback):
    # In rare cases, the exception value can be None,
    # In which case, we create a new exception object.
    # We can't just instantiate it, but because error handling
    # code uses only BaseException fields, we can create an empty instance.
    if value is None:
        value = BaseException.__new__(type)
        value.__traceback__ = traceback

    te = renpy.error.TracebackException(value)
    te.format(renpy.error.MaybeColoredExceptionPrintContext(sys.stderr))


def relaunch():
    """
    Call this to launch a new copy of the same game.
    """

    if hasattr(sys, "renpy_executable"):
        subprocess.Popen([sys.renpy_executable] + sys.argv[1:])  # type: ignore
    else:
        subprocess.Popen([sys.executable] + sys.argv)


def disable_requests_ca_bundle(adapters) -> None:
    """
    Stops requests from loading its default (certifi) CA bundle when `verify` is True, so that
    urllib3 loads the default certificates, which truststore provides from the system store. An
    explicit CA bundle path passed as `verify` (or via REQUESTS_CA_BUNDLE) is still honored.

    `adapters` is the requests.adapters module.
    """

    original_cert_verify = adapters.HTTPAdapter.cert_verify

    def cert_verify(self, conn, url, verify, cert):
        if verify is True and url.lower().startswith("https"):
            # Clears ca_certs and ca_cert_dir, then requires verification against the defaults.
            original_cert_verify(self, conn, url, False, cert)
            conn.cert_reqs = "CERT_REQUIRED"
        else:
            original_cert_verify(self, conn, url, verify, cert)

    adapters.HTTPAdapter.cert_verify = cert_verify


class RequestsAdaptersLoader(importlib.abc.Loader):
    """
    Wraps the loader of requests.adapters, calling disable_requests_ca_bundle once the module
    has been executed. Other attributes are delegated to the wrapped loader.
    """

    def __init__(self, loader):
        self.loader = loader

    def __getattr__(self, name):
        return getattr(self.loader, name)

    def create_module(self, spec):
        return self.loader.create_module(spec)

    def exec_module(self, module):
        self.loader.exec_module(module)
        disable_requests_ca_bundle(module)


class RequestsAdaptersFinder(importlib.abc.MetaPathFinder):
    """
    A one-shot meta path finder that arranges for requests.adapters to be patched when it is
    first imported, so requests need not be imported at startup.
    """

    def find_spec(self, fullname, path, target=None):
        if fullname != "requests.adapters":
            return None

        if self in sys.meta_path:
            sys.meta_path.remove(self)

        spec = importlib.util.find_spec(fullname)

        if spec is None or spec.loader is None:
            return spec

        spec.loader = RequestsAdaptersLoader(spec.loader)
        return spec


def use_system_certificates() -> None:
    """
    Make ssl and requests verify TLS certificates against the operating system's trust store,
    rather than certifi's CA bundle.
    """

    import truststore

    if "urllib3" in sys.modules or "requests" in sys.modules:
        truststore.inject_into_ssl()
    else:
        # inject_into_ssl() imports urllib3 and requests to patch them. They have not been
        # imported yet, so replacing ssl.SSLContext is enough for them to use truststore.
        import ssl

        ssl.SSLContext = truststore.SSLContext  # type: ignore

    if "requests.adapters" in sys.modules:
        disable_requests_ca_bundle(sys.modules["requests.adapters"])
    else:
        sys.meta_path.insert(0, RequestsAdaptersFinder())


def set_utf8_locale() -> None:
    """
    Align the native character locale and inherited subprocess environment with UTF-8.

    Run only during desktop POSIX startup, before engine threads are started.
    Other locale categories are preserved, including those overridden by LC_ALL.
    If no usable UTF-8 locale is available, warn and retain the original settings.
    """
    if os.name != "posix" or renpy.android or renpy.ios or renpy.emscripten:
        return

    import locale

    original = locale.setlocale(locale.LC_CTYPE)
    configured = False

    try:
        # Python's UTF-8 mode can mask a non-UTF-8 environment inherited by native children.
        locale.setlocale(locale.LC_CTYPE, "")
        if locale.getencoding().lower().replace("-", "") == "utf8":
            configured = True
            return

        for candidate in ("C.UTF-8", "C.utf8", "UTF-8"):
            try:
                locale.setlocale(locale.LC_CTYPE, candidate)
            except locale.Error:
                continue

            if locale.getencoding().lower().replace("-", "") == "utf8":
                break
        else:
            raise locale.Error("none of C.UTF-8, C.utf8, or UTF-8 is available with a UTF-8 encoding")

        override = os.environ.get("LC_ALL")
        if override:
            categories = ["LC_COLLATE", "LC_MESSAGES", "LC_MONETARY", "LC_NUMERIC", "LC_TIME"]
            if sys.platform.startswith("linux"):
                categories.extend(
                    ["LC_PAPER", "LC_NAME", "LC_ADDRESS", "LC_TELEPHONE", "LC_MEASUREMENT", "LC_IDENTIFICATION"]
                )

            for category in categories:
                os.environ[category] = override

            del os.environ["LC_ALL"]

        os.environ["LC_CTYPE"] = candidate
        configured = True
    except locale.Error as e:
        sys.stderr.write(
            f"Warning: Could not configure a UTF-8 character locale: {e}. "
            "Keeping the original locale; native dialogs and other external tools may not handle non-ASCII text.\n"
        )
    finally:
        if not configured:
            locale.setlocale(locale.LC_CTYPE, original)


def bootstrap(renpy_base: str):
    global renpy

    import renpy.config
    import renpy.log

    # In case of invocation with system python, check that it's run with -X utf8
    if not sys.flags.utf8_mode:
        import locale
        if locale.getpreferredencoding(False).lower() != "utf-8":
            raise Exception("Ren'Py requires Python to be run with -X utf8.")

    if not isinstance(renpy_base, str):
        raise TypeError("renpy_base must be a string.")

    # Remove a legacy environment setting.
    if os.environ.get("SDL_VIDEODRIVER", "") == "windib":
        del os.environ["SDL_VIDEODRIVER"]

    renpy.config.renpy_base = renpy_base

    # Handle any file deletions or renamed that were deferred from a previous update.

    import renpy.update.deferred

    if renpy.update.deferred.init() and renpy.windows:
        relaunch()
        sys.exit(0)

    # If environment.txt exists, load it into the os.environ dictionary.
    if os.path.exists(renpy_base + "/environment.txt"):
        evars = {}
        with open(renpy_base + "/environment.txt", "r") as f:
            code = compile(f.read(), renpy_base + "/environment.txt", "exec")
            exec(code, evars)
        for k, v in evars.items():
            if k not in os.environ:
                os.environ[k] = str(v)

    # Also look for it in an alternate path (the path that contains the
    # .app file.), if on a mac.
    alt_path = os.path.abspath("renpy_base")
    if ".app" in alt_path:
        alt_path = alt_path[: alt_path.find(".app") + 4]

        if os.path.exists(alt_path + "/environment.txt"):
            evars = {}
            with open(alt_path + "/environment.txt", "rb") as f:
                code = compile(f.read(), alt_path + "/environment.txt", "exec")
                exec(code, evars)
            for k, v in evars.items():
                if k not in os.environ:
                    os.environ[k] = str(v)

    set_utf8_locale()

    # Get a working name for the game.
    name = os.path.basename(sys.argv[0])

    if name.find(".") != -1:
        name = name[: name.find(".")]

    # Parse the arguments.
    import renpy.arguments

    args = renpy.arguments.bootstrap()

    if args.trace:
        enable_trace(args.trace)

    if args.basedir:
        basedir = os.path.abspath(args.basedir)
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
        os.startfile = mac_start  # type: ignore

        # Are we starting from inside a mac app resources directory?
        if basedir.endswith("Contents/Resources/autorun"):
            renpy.macapp = True

    # Set up Ren'Py specific exception handling.
    sys.excepthook = excepthook

    # Check that we have installed pygame properly. This also deals with
    # weird cases on Windows and Linux where we can't import modules. (On
    # windows ";" is a directory separator in PATH, so if it's in a parent
    # directory, we won't get the libraries in the PATH, and hence pygame
    # won't import.)
    try:
        import renpy.pygame

        renpy.pygame.import_as_pygame()
    except Exception as e:
        e.add_note(
            textwrap.dedent(f"""
        Could not import renpy.pygame. Please ensure that this program has been built
        and unpacked properly. Also, make sure that the directories containing this
        program do not contain : or ; in their names.

        You may be using a system install of python. Please run {name}.sh,
        {name}.exe, or {name}.app instead.
        """)
        )

        raise

    gamedir = renpy.__main__.path_to_gamedir(basedir, name)

    # If we're not given a command, show the presplash.
    if args.command == "run" and not renpy.mobile:
        import renpy.display.presplash

        renpy.display.presplash.start(basedir, gamedir)

    # Ditto for the Ren'Py module.
    try:
        import _renpy  # type: ignore
    except Exception as e:
        e.add_note(
            textwrap.dedent(f"""
        Could not import _renpy. Please ensure that this program has been built
        and unpacked properly.

        You may be using a system install of python. Please run {name}.sh,
        {name}.exe, or {name}.app instead.
        """)
        )
        raise

    # Load the rest of Ren'Py.
    import renpy

    renpy.import_all()

    # This must run before init_importer, as importing truststore through the Ren'Py importer
    # would cache the game's Python files before the game directory is known.
    if not renpy.emscripten:
        use_system_certificates()

    renpy.importer.init_importer()

    if renpy.emscripten:
        import renpy.gl2.live2d

        renpy.gl2.live2d.web_init()

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
                renpy.config.basedir = basedir
                renpy.config.gamedir = gamedir
                renpy.config.args = []  # type: ignore

                renpy.config.logdir = renpy.__main__.path_to_logdir(basedir)

                if not os.path.exists(renpy.config.logdir):
                    os.makedirs(renpy.config.logdir, 0o777)

                renpy.main.main()

                exit_status = 0

            except renpy.game.UtterRestartException:
                # On an UtterRestart, reload Ren'Py.
                renpy.reload_all()

                exit_status = None

            except renpy.game.QuitException as e:
                exit_status = e.status

                if e.relaunch:
                    relaunch()

            except renpy.game.ParseErrorException:
                pass

            except Exception as e:
                # If exception was raised outside of Ren'Py execution context,
                # or context was unable to handle it, report it here.
                renpy.error.report_exception(e, editor=True)

        sys.exit(exit_status)

    finally:
        if "RENPY_SHUTDOWN_TRACE" in os.environ:
            enable_trace(int(os.environ["RENPY_SHUTDOWN_TRACE"]))

        renpy.display.tts.tts(None)  # type: ignore

        if renpy.display.draw:  # type: ignore
            renpy.display.im.cache.quit()  # type: ignore
            renpy.display.draw.quit()  # type: ignore

        renpy.audio.audio.quit()

        for cb in renpy.config.python_exit_callbacks:
            cb()

        renpy.pygame.surface._quit_surface_deallocation()

        # Prevent subprocess from throwing errors while trying to run it's
        # __del__ method during shutdown.
        if not renpy.emscripten:
            subprocess.Popen.__del__ = popen_del  # type: ignore

        if renpy.android:
            from jnius import autoclass  # type: ignore

            import android

            android.activity.finishAndRemoveTask()

            # Avoid running Python shutdown, which can cause more harm than good.
            # For more details, see https://github.com/renpy/renpy/issues/5280.
            System = autoclass("java.lang.System")
            System.exit(0)
