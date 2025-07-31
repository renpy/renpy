# Copyright 2004-2025 Tom Rothamel <pytom@bishoujo.us>
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
from renpy.compat import PY2, basestring, bchr, bord, chr, open, pystr, range, round, str, tobytes, unicode  # *

import os

import renpy
import io
import time
import traceback

# The deferred update file is used to store commands that are to be executed
# when Ren'Py starts up. This is used to handle updates that cannot be
# performed while Ren'Py is running, such as renaming or deleting files.
#
# It is a file containing deferred update commands, one per line. Right now,
# there are two commands:
#
# R <path>
#     Rename <path>.new to <path>.
# D <path>
#     Delete <path>.
#
# Deferred commands that cannot be accomplished on start are ignored.
DEFERRED_UPDATE_FILE: str


def process_deferred_line(l):
    cmd, _, fn = l.partition(" ")

    if cmd == "R":
        newfn = fn + ".new.rpu"

        if not os.path.exists(newfn):
            newfn = fn + ".new"

        if not os.path.exists(newfn):
            return

        if os.path.exists(fn):
            os.unlink(fn)

        os.rename(newfn, fn)

    elif cmd == "D":
        if os.path.exists(fn):
            os.unlink(fn)

    elif cmd == "":
        pass

    else:
        raise Exception("Bad command. %r (%r %r)" % (l, cmd, fn))


def process_deferred():
    DEFERRED_UPDATE_LOG = os.path.join(renpy.config.renpy_base, "update", "log.txt")

    if not os.path.exists(DEFERRED_UPDATE_FILE):
        return

    # Give a previous process time to quit (and let go of the
    # open files.)
    time.sleep(3)

    try:
        log = open(DEFERRED_UPDATE_LOG, "a")
    except Exception:
        log = io.StringIO()

    with open(DEFERRED_UPDATE_FILE, "r") as f:
        for l in f:
            l = l.rstrip("\r\n")

            log.write(l)

            try:
                process_deferred_line(l)
            except Exception:
                traceback.print_exc(file=log)

    try:
        os.unlink(DEFERRED_UPDATE_FILE + ".old")
    except Exception:
        pass

    try:
        os.rename(DEFERRED_UPDATE_FILE, DEFERRED_UPDATE_FILE + ".old")
    except Exception:
        traceback.print_exc(file=log)

    log.close()


def process_deleted():
    """
    Delete files in the update/deleted directory. This stopped being created in
    Ren'Py 8.4, and so can be removed in Ren'Py 8.6.
    """

    DELETED = os.path.join(renpy.config.renpy_base, "update", "deleted")

    if not os.path.exists(DELETED):
        return

    import shutil

    try:
        shutil.rmtree(DELETED)
    except Exception as e:
        pass


def defer_rename(fn):
    """
    Defers the rename of `fn`.rpu.new or `fn`.new to `fn`.
    """

    with open(DEFERRED_UPDATE_FILE, "a") as f:
        f.write("R %s\n" % fn)


def defer_delete(fn):
    """
    Defers the deletion of `fn`.
    """

    with open(DEFERRED_UPDATE_FILE, "a") as f:
        f.write("D %s\n" % fn)


def init():
    """
    Initialize deferred updates.
    """

    global DEFERRED_UPDATE_FILE
    DEFERRED_UPDATE_FILE = os.path.join(renpy.config.renpy_base, "update", "deferred.txt")

    process_deferred()
    process_deleted()
