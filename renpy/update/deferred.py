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

# A directory containing files to be deleted on next startup.
DELETED_DIRECTORY: str

# True if this is the first delete operation to need to be deferred.
first_deferred_delete = False


def delete(fn: str):
    """
    Deletes the file `fn`. If deletion fails, renames the file into the
    deleted directory, to be deleted on next startup.
    """

    global first_deferred_delete

    if not os.path.exists(fn):
        return

    try:
        os.unlink(fn)
    except Exception:

        if first_deferred_delete:
            attempts = 5
            delay = 1
            first_deferred_delete = False
        else:
            attempts = 1
            delay = 0

        for i in range(attempts):

            try:
                if not os.path.exists(DELETED_DIRECTORY):
                    os.makedirs(DELETED_DIRECTORY, exist_ok=True)
                os.rename(fn, os.path.join(DELETED_DIRECTORY, os.path.basename(fn)))

                return

            except Exception:
                pass

            time.sleep(delay)


def process_deferred_line(l):
    cmd, _, fn = l.partition(" ")

    if cmd == "R":
        newfn = fn + ".new.rpu"

        if not os.path.exists(newfn):
            newfn = fn + ".new"

        if not os.path.exists(newfn):
            return False

        if os.path.exists(fn):
            delete(fn)

        os.rename(newfn, fn)
        return True

    elif cmd == "D":
        if os.path.exists(fn):
            delete(fn)
            return True

    elif cmd == "":
        pass

    else:
        raise Exception("Bad command. %r (%r %r)" % (l, cmd, fn))

    return False


def process_deferred():
    """
    Process the deferred update file.

    Returns True if a change was made, False otherwise.
    """

    global first_deferred_delete
    first_deferred_delete = True


    DEFERRED_UPDATE_LOG = os.path.join(renpy.config.renpy_base, "update", "log.txt")

    if not os.path.exists(DEFERRED_UPDATE_FILE):
        return False

    # Give a previous process time to quit (and let go of the
    # open files.)
    time.sleep(3)

    try:
        log = open(DEFERRED_UPDATE_LOG, "a")
    except Exception:
        log = io.StringIO()

    rv = False

    with open(DEFERRED_UPDATE_FILE, "r") as f:
        for l in f:
            l = l.rstrip("\r\n")

            log.write(l)

            try:
                if process_deferred_line(l):
                    rv = True

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

    return rv


def process_deleted():
    """
    Delete files in the update/deleted directory.
    """


    if not os.path.exists(DELETED_DIRECTORY):
        return

    import shutil

    try:
        shutil.rmtree(DELETED_DIRECTORY)
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
    global DELETED_DIRECTORY
    DEFERRED_UPDATE_FILE = os.path.join(renpy.config.renpy_base, "update", "deferred.txt")
    DELETED_DIRECTORY = os.path.join(renpy.config.renpy_base, "update", "deleted")

    rv = process_deferred()
    process_deleted()

    return rv
