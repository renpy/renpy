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

from __future__ import division, absolute_import, with_statement, print_function, unicode_literals # type: ignore
from renpy.compat import PY2, basestring, bchr, bord, chr, open, pystr, range, round, str, tobytes, unicode # *

import os
import sys
import threading

import renpy
import pygame_sdl2

from renpy.exports.commonexports import renpy_pure

@renpy_pure
def variant(name):
    """
    :doc: screens

    Returns true if `name` is a screen variant that corresponds to the
    context in which Ren'Py is currently executing. See :ref:`screen-variants`
    for more details. This function can be used as the condition in an
    if statement to switch behavior based on the selected screen variant.

    `name` can also be a list of variants, in which case this function
    returns True if any of the variants would.
    """

    if isinstance(name, basestring):
        return name in renpy.config.variants
    else:
        for n in name:
            if n in renpy.config.variants:
                return True

        return False


def vibrate(duration):
    """
    :doc: other

    Causes the device to vibrate for `duration` seconds. Currently, this
    is only supported on Android.
    """

    if duration < 0.01:
        duration = 0.01

    if renpy.android:
        import android # @UnresolvedImport
        android.vibrate(duration)


def invoke_in_thread(fn, *args, **kwargs):
    """
    :doc: other

    Invokes the function `fn` in a background thread, passing it the
    provided arguments and keyword arguments. Restarts the interaction
    once the thread returns.

    This function creates a daemon thread, which will be automatically
    stopped when Ren'Py is shutting down.

    This thread is very limited in what it can do with the Ren'Py API.
    Changing store variables is allowed, as are calling calling the following
    functions:

    * :func:`renpy.restart_interaction`
    * :func:`renpy.invoke_in_main_thread`
    * :func:`renpy.queue_event`

    Most other portions of the Ren'Py API are expected to be called from
    the main thread.

    This does not work on the web platform, except for immediately returning
    without an error.
    """

    if renpy.emscripten:
        return

    def run():
        try:
            fn(*args, **kwargs)
        except Exception:
            import traceback
            traceback.print_exc()

        renpy.exports.restart_interaction()

    t = threading.Thread(target=run)
    t.daemon = True
    t.start()


def invoke_in_main_thread(fn, *args, **kwargs):
    """
    :doc: other

    This runs the given function with the given arguments in the main
    thread. The function runs in an interaction context similar to an
    event handler. This is meant to be called from a separate thread,
    whose creation is handled by :func:`renpy.invoke_in_thread`.

    If a single thread schedules multiple functions to be invoked, it is guaranteed
    that they will be run in the order in which they have been scheduled::

        def ran_in_a_thread():
            renpy.invoke_in_main_thread(a)
            renpy.invoke_in_main_thread(b)

    In this example, it is guaranteed that ``a`` will return before
    ``b`` is called. The order of calls made from different threads is not
    guaranteed.

    This may not be called during the init phase.
    """

    if renpy.game.context().init_phase:
        raise Exception("invoke_in_main_thread may not be called during the init phase.")

    renpy.display.interface.invoke_queue.append((fn, args, kwargs))


old_battery = False


def get_on_battery():
    """
    :doc: other

    Returns True if Ren'Py is running on a device that is powered by an internal
    battery, or False if the device is being charged by some external source.
    """

    global old_battery

    pi = pygame_sdl2.power.get_power_info() # @UndefinedVariable

    if pi.state == pygame_sdl2.POWERSTATE_UNKNOWN: # @UndefinedVariable
        return old_battery
    elif pi.state == pygame_sdl2.POWERSTATE_ON_BATTERY: # @UndefinedVariable
        old_battery = True
        return True
    else:
        old_battery = False
        return False


sdl_dll = False

def get_sdl_dll():
    """
    :doc: sdl

    Returns a ctypes.cdll object that refers to the library that contains
    the instance of SDL2 that Ren'Py is using. If this fails, None is returned.
    """

    global sdl_dll

    if sdl_dll is not False:
        return sdl_dll

    try:

        lib = os.path.dirname(sys.executable) + "/"

        DLLS = [ None, lib + "librenpython.dll", lib + "librenpython.dylib", lib + "librenpython.so", "librenpython.so", "SDL2.dll", "libSDL2.dylib", "libSDL2-2.0.so.0" ]

        import ctypes

        for i in DLLS:
            try:
                # Look for the DLL.
                dll = ctypes.cdll[i]
                # See if it has SDL_GetError..
                dll.SDL_GetError
            except Exception as e:
                continue

            sdl_dll = dll
            return dll

    except Exception:
        pass

    sdl_dll = None
    return None


def get_sdl_window_pointer():
    """
    :doc: sdl

    :rtype: ctypes.c_void_p | None

    Returns a pointer to the main window, or None if the main window is not
    displayed (or some other problem occurs).
    """

    try:
        window = pygame_sdl2.display.get_window()

        if window is None:
            return None

        return window.get_sdl_window_pointer()

    except Exception:
        return None


def check_permission(permission):
    """
    :doc: android_permission

    Checks to see if an Android permission has been granted to this application.

    `permission`
        A string giving the name of the permission, for example, "android.permission.WRITE_EXTERNAL_STORAGE".

    Returns true if the permission has been granted, false if it has not or if called on
    a non-Android platform.
    """

    if not renpy.android:
        return False

    from jnius import autoclass
    PythonSDLActivity = autoclass("org.renpy.android.PythonSDLActivity")
    activity = PythonSDLActivity.mActivity

    try:
        return activity.checkSelfPermission(permission) == 0 # PackageManager.PERMISSION_GRANTED
    except Exception:
        return False


def request_permission(permission):
    """
    :doc: android_permission

    Asks Android to grant a permission to this application. The user may be
    prompted to grant the permission.

    `permission`
        A string giving the name of the permission, for example, "android.permission.WRITE_EXTERNAL_STORAGE".

    Returns true if the permission has been granted, false if not or if called on a
    non-Android platform.
    """

    if not renpy.android:
        return False

    return get_sdl_dll().SDL_AndroidRequestPermission(permission.encode("utf-8")) # type: ignore

def open_url(url):
    """
    :doc: other

    Opens a URL in the system's web browser, if possible.
    """

    if not renpy.mobile:
        renpy.game.preferences.fullscreen = False

    try:
        import webbrowser
        webbrowser.open_new(url)
    except Exception:
        pass
