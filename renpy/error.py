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

# This file contains code for formatting tracebacks.

from __future__ import division, absolute_import, with_statement, print_function, unicode_literals
from renpy.compat import PY2, basestring, bchr, bord, chr, open, pystr, range, round, str, tobytes, unicode # *



import traceback
import sys
import io
import platform
import linecache
import time
import os

import renpy

FSENCODING = sys.getfilesystemencoding() or "utf-8"


def write_traceback_list(out, l):
    """
    Given the traceback list, writes it to out as unicode.
    """

    ul = [ ]

    for filename, line, what, text in l:

        # Filename is either unicode or fsecoded bytes.
        if isinstance(filename, bytes):
            filename = filename.decode(FSENCODING)

        # Line is a number.

        # Assume what is in a unicode encoding, since it is either python,
        # or comes from inside Ren'Py.

        if isinstance(text, bytes):
            text = text.decode("utf-8")

        ul.append((filename, line, what, text))

    for t in traceback.format_list(ul):
        out.write(t)


def traceback_list(tb):
    """
    Given `tb`, returns a list of (filename, line_number, function, line_text)
    tuples.
    """

    l = [ ]

    while tb:
        frame = tb.tb_frame
        line_number = tb.tb_lineno
        code = frame.f_code
        filename = code.co_filename
        name = code.co_name

        tb = tb.tb_next

        if ('self' in frame.f_locals) and (not renpy.config.raw_tracebacks):
            obj = frame.f_locals['self']

            last = (tb is None)

            try:
                report = obj.report_traceback(name, last)

                if report is not None:
                    l.extend(report)
                    continue
            except Exception:
                pass

        l.append((filename, line_number, name, None))

    rv = [ ]

    for filename, line_number, name, line in l:
        if line is None:
            try:
                line = linecache.getline(filename, line_number)
            except Exception:
                line = ''

        rv.append((filename, line_number, name, line))

    return rv


def filter_traceback_list(tl):
    """
    Returns the subset of `tl` that originates in creator-written files, as
    opposed to those portions that come from Ren'Py itself.
    """

    rv = [ ]

    for t in tl:
        filename = t[0]
        if filename.endswith(".rpy") and not filename.replace("\\", "/").startswith("common/"):
            rv.append(t)

    return rv


def open_error_file(fn, mode):
    """
    Opens an error/log/file. Returns the open file, and the filename that
    was opened.
    """

    try:
        new_fn = os.path.join(renpy.config.logdir, fn) # type: ignore
        f = open(new_fn, mode)
        return f, new_fn
    except Exception:
        pass

    try:
        f = open(fn, mode)
        return f, fn
    except Exception:
        pass

    import tempfile

    new_fn = os.path.join(tempfile.gettempdir(), "renpy-" + fn)
    return open(new_fn, mode), new_fn


def report_exception(e, editor=True):
    """
    Reports an exception by writing it to standard error and
    traceback.txt. If `editor` is True, opens the traceback
    up in a text editor.

    Returns a three-item tuple, with the first item being
    a simplified traceback, the second being a full traceback,
    and the third being the traceback filename.
    """

    # Note: Doki Doki Literature club calls this as ("Words...", False).
    # For what it's worth.

    if not int(os.environ.get("RENPY_REPORT_EXCEPTIONS", "1")):
        raise

    # The sound system may not be ready during exception handling.
    renpy.config.debug_sound = False

    import codecs

    type, _value, tb = sys.exc_info() # @ReservedAssignment

    # Return values - which can be displayed to the user.
    simple = io.StringIO()
    full = io.StringIO()

    full_tl = traceback_list(tb)
    simple_tl = filter_traceback_list(full_tl)

    print(str(renpy.game.exception_info), file=simple)
    write_traceback_list(simple, simple_tl)
    print(type.__name__ + ":", end=' ', file=simple)
    print(str(e), file=simple)

    print("Full traceback:", file=full)
    write_traceback_list(full, full_tl)
    print(type.__name__ + ":", end=' ', file=full)
    print(str(e), file=full)

    # Write to stdout/stderr.
    try:
        sys.stdout.write("\n")
        sys.stdout.write(full.getvalue())
        sys.stdout.write("\n")
        sys.stdout.write(simple.getvalue())
    except Exception:
        pass

    print('', file=full)

    try:
        print(str(platform.platform()), str(platform.machine()), file=full)
        print(renpy.version, file=full)
        print(renpy.config.name + " " + renpy.config.version, file=full)
        print(str(time.ctime()), file=full)
    except Exception:
        pass

    simple = simple.getvalue()
    full = full.getvalue()

    # Inside of the file, which may not be openable.
    try:

        f, traceback_fn = open_error_file("traceback.txt", "w")

        with f:
            f.write("\ufeff") # BOM

            print("I'm sorry, but an uncaught exception occurred.", file=f)
            print('', file=f)

            f.write(simple)

            print('', file=f)
            print("-- Full Traceback ------------------------------------------------------------", file=f)
            print('', file=f)

            f.write(full)

        try:
            renpy.util.expose_file(traceback_fn)
        except Exception:
            pass

        try:
            if editor and ((renpy.game.args.command == "run") or (renpy.game.args.errors_in_editor)): # type: ignore
                renpy.exports.launch_editor([ traceback_fn ], 1, transient=True)
        except Exception:
            pass

    except Exception:
        traceback_fn = os.path.join(renpy.config.basedir, "traceback.txt") # type: ignore

    return simple, full, traceback_fn
