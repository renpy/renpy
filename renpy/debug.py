# Copyright 2004-2023 Tom Rothamel <pytom@bishoujo.us>
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

from __future__ import division, absolute_import, with_statement, print_function, unicode_literals
from renpy.compat import PY2, basestring, bchr, bord, chr, open, pystr, range, round, str, tobytes, unicode # *



import renpy
import threading
import datetime
import traceback
import os
import builtins
import io

if PY2:
    real_open = io.open
else:
    real_open = builtins.open

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

    builtins.open = replacement_open
