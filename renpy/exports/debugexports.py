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

import renpy
from renpy.exports.commonexports import renpy_pure

def warp_to_line(warp_spec):
    """
    :doc: debug

    This takes as an argument a filename:linenumber pair, and tries to warp to
    the statement before that line number.

    This works samely as the `--warp` command.
    """

    renpy.warp.warp_spec = warp_spec
    renpy.exports.full_restart()


def get_filename_line():
    """
    :doc: debug

    Returns a pair giving the filename and line number of the current
    statement.
    """

    n = renpy.game.script.namemap.get(renpy.game.context().current, None)

    if n is None:
        return "unknown", 0
    else:
        return n.filename, n.linenumber


# A file that log logs to.
logfile = None


def log(msg):
    """
    :doc: debug

    If :var:`config.log` is not set, this does nothing. Otherwise, it opens
    the logfile (if not already open), formats the message to :var:`config.log_width`
    columns, and prints it to the logfile.
    """

    global logfile

    if not renpy.config.log:
        return

    if msg is None:
        return

    try:
        msg = unicode(msg)
    except Exception:
        pass

    try:

        if not logfile:
            import os
            if renpy.config.clear_log:
                file_mode = "w"
            else:
                file_mode = "a"
            logfile = open(os.path.join(renpy.config.basedir, renpy.config.log), file_mode)

            if not logfile.tell():
                logfile.write("\ufeff")

        import textwrap

        wrapped = [ ]

        for line in msg.split('\n'):
            line = textwrap.fill(line, renpy.config.log_width)
            line = unicode(line)
            wrapped.append(line)

        wrapped = '\n'.join(wrapped)

        logfile.write(wrapped + "\n")
        logfile.flush()

    except Exception:
        renpy.config.log = None


# Error handling stuff.
def _error(msg):
    raise Exception(msg)

_error_handlers = [ _error ]

def push_error_handler(eh):
    _error_handlers.append(eh)


def pop_error_handler():
    _error_handlers.pop()


def error(msg):
    """
    :doc: lint

    Reports `msg`, a string, as as error for the user. This is logged as a
    parse or lint error when approprate, and otherwise it is raised as an
    exception.
    """

    _error_handlers[-1](msg)


def write_log(s, *args):
    """
    :undocumented:

    Writes to log.txt.
    """

    renpy.display.log.write(s, *args)
