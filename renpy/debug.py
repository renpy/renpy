# Copyright 2004-2019 Tom Rothamel <pytom@bishoujo.us>
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

# This file contains debugging code that isn't enabled in normal Ren'Py
# operation.

from __future__ import print_function

import renpy
import __builtin__
import threading
import datetime
import traceback
import os

real_open = __builtin__.open
__builtin__.real_file = __builtin__.file

report = True


def replacement_open(*args, **kwargs):

    global report

    rv = real_open(*args, **kwargs)

    if not renpy.game.contexts:
        return rv

    if renpy.game.context().init_phase:
        return rv

    if threading.current_thread().name != "MainThread":
        return rv

    if not report:
        return rv

    if os.environ["RENPY_DEBUG_MAIN_THREAD_OPEN"] == "stack":
        report = False
        print()
        traceback.print_stack()
        report = True

    print(datetime.datetime.now().strftime("%H:%M:%S"), "In main thread: open" + repr(args))
    return rv


def init_main_thread_open():
    if not "RENPY_DEBUG_MAIN_THREAD_OPEN" in os.environ:
        return

    __builtin__.open = replacement_open
    __builtin__.file = replacement_open
