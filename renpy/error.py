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

# This file contains code for formatting tracebacks.

from __future__ import print_function
import traceback
import sys
import cStringIO
import platform
import linecache
import time
import os

import renpy

FSENCODING = sys.getfilesystemencoding() or "utf-8"


def write_utf8_traceback_list(out, l):
    """
    Given the traceback list l, writes it to out as utf-8.
    """

    ul = [ ]

    for filename, line, what, text in l:

        # Filename is either unicode or an fsecoded string.
        if not isinstance(filename, unicode):
            filename = unicode(filename, FSENCODING, "replace")

        # Line is a number.

        # Assume what is in a unicode encoding, since it is either python,
        # or comes from inside Ren'Py.

        if isinstance(text, str):
            text = text.decode("utf-8", "replace")

        ul.append((filename, line, what, text))

    for t in traceback.format_list(ul):
        out.write(t.encode("utf-8", "replace"))


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
            except:
                pass

        l.append((filename, line_number, name, None))

    rv = [ ]

    for filename, line_number, name, line in l:
        if line is None:
            try:
                line = linecache.getline(filename, line_number)
            except:
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
        new_fn = os.path.join(renpy.config.logdir, fn)
        f = file(new_fn, mode)
        return f, new_fn
    except:
        pass

    try:
        f = file(fn, mode)
        return f, fn
    except:
        pass

    import tempfile

    new_fn = os.path.join(tempfile.gettempdir(), "renpy-" + fn)
    return file(new_fn, mode), new_fn


def report_exception(e, editor=True):
    """
    Reports an exception by writing it to standard error and
    traceback.txt. If `editor` is True, opens the traceback
    up in a text editor.

    Returns a two-unicode tuple, with the first item being
    a simple message, and the second being a full traceback.
    """

    # Note: Doki Doki Literature club calls this as ("Words...", False).
    # For what it's worth.

    import codecs

    type, _value, tb = sys.exc_info()  # @ReservedAssignment

    def safe_utf8(e):
        try:
            m = unicode(e)
        except:
            try:
                if len(e.args) == 0:
                    m = ""
                elif len(e.args) == 1:
                    m = e.args[0]
                else:
                    m = " ".join(e.args)
            except:
                try:
                    m = repr(e)
                except:
                    m = "<Could not encode exception.>"

        if isinstance(m, unicode):
            return m.encode("utf-8", "replace")
        else:
            return m

    # Return values - which can be displayed to the user.
    simple = cStringIO.StringIO()
    full = cStringIO.StringIO()

    full_tl = traceback_list(tb)
    simple_tl = filter_traceback_list(full_tl)

    print(renpy.game.exception_info, file=simple)
    write_utf8_traceback_list(simple, simple_tl)
    print(type.__name__ + ":", end=' ', file=simple)
    print(safe_utf8(e), file=simple)

    print("Full traceback:", file=full)
    write_utf8_traceback_list(full, full_tl)
    print(type.__name__ + ":", end=' ', file=full)
    print(safe_utf8(e), file=full)

    # Write to stdout/stderr.
    try:
        sys.stdout.write("\n")
        sys.stdout.write(full.getvalue())
        sys.stdout.write("\n")
        sys.stdout.write(simple.getvalue())
    except:
        pass

    print(file=full)
    try:
        print(platform.platform(), file=full)
        print(renpy.version, file=full)
        print(safe_utf8(renpy.config.name + " " + renpy.config.version), file=full)
        print(time.ctime(), file=full)
    except:
        pass

    simple = simple.getvalue()
    full = full.getvalue()

    # Inside of the file, which may not be openable.
    try:

        f, traceback_fn = open_error_file("traceback.txt", "w")

        f.write(codecs.BOM_UTF8)

        print("I'm sorry, but an uncaught exception occurred.", file=f)
        print(file=f)

        f.write(simple)

        print(file=f)
        print("-- Full Traceback ------------------------------------------------------------", file=f)
        print(file=f)

        f.write(full)
        f.close()

        try:
            if editor and renpy.game.args.command == "run":  # @UndefinedVariable
                renpy.exports.launch_editor([ traceback_fn ], 1, transient=1)
        except:
            pass

    except:
        pass

    return simple.decode("utf-8", "replace"), full.decode("utf-8", "replace"), traceback_fn
