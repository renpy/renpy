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

import io
import sys

import renpy
from renpy.exports.commonexports import renpy_pure


@renpy_pure
def loadable(filename, directory=None, tl=True):
    """
    :doc: file

    Returns True if the given filename is loadable, meaning that it
    can be loaded from the disk or from inside an archive. Returns
    False if this is not the case.

    `directory`
        If not None, a directory to search in if the file is not found
        in the game directory. This will be prepended to filename, and
        the search tried again.
    `tl`
        If True, a translation subdirectory will be considered as well.
    """

    return renpy.loader.loadable(filename, tl=tl, directory=directory)


@renpy_pure
def exists(filename):
    """
    :doc: file_rare

    Returns true if the given filename can be found in the
    searchpath. This only works if a physical file exists on disk. It
    won't find the file if it's inside of an archive.

    You almost certainly want to use :func:`renpy.loadable` in preference
    to this function.
    """

    try:
        renpy.loader.transfn(filename)
        return True
    except Exception:
        return False


def open_file(fn, encoding=None, directory=None): # @ReservedAssignment
    """
    :doc: file

    Returns a read-only file-like object that accesses the file named `fn`. The file is
    accessed using Ren'Py's standard search method, and may reside in the game directory,
    in an RPA archive, or as an Android asset.

    The object supports a wide subset of the fields and methods found on Python's
    standard file object, opened in binary mode. (Basically, all of the methods that
    are sensible for a read-only file.)

    `encoding`
        If given, the file is open in text mode with the given encoding.
        If False, the file is opened in binary mode.
        If None, the default, the encoding is taken from :var:`config.open_file_encoding`.
        In most cases, None will open a file in binary mode.

    `directory`
        If not None, a directory to search in if the file is not found
        in the game directory. This will be prepended to filename, and
        the search tried again.

    This returns an io.BufferedReader object if encoding is None, and an
    io.TextIOWrapper object if encoding is not None.
    """

    rv = renpy.loader.load(fn, directory=directory)

    if encoding is None:
        encoding = renpy.config.open_file_encoding

    rv = io.BufferedReader(rv)

    if encoding:
        rv = io.TextIOWrapper(rv, encoding=encoding, errors="surrogateescape") # type: ignore

    return rv


def file(fn, encoding=None):
    """
    :doc: file

    An alias for :func:`renpy.open_file`, for compatibility with older
    versions of Ren'Py.
    """

    return open_file(fn, encoding=encoding)


def notl_file(fn): # @ReservedAssignment
    """
    :undocumented:

    Like file, but doesn't search the translation prefix.
    """
    return renpy.loader.load(fn, tl=False)


@renpy_pure
def list_files(common=False):
    """
    :doc: file

    Lists the files in the game directory and archive files. Returns
    a list of files, with / as the directory separator.

    `common`
        If true, files in the common directory are included in the
        listing.
    """

    rv = [ ]

    for _dir, fn in renpy.loader.listdirfiles(common):
        if fn.startswith("saves/"):
            continue

        rv.append(fn)

    rv.sort()

    return rv


@renpy_pure
def fsencode(s, force=False): # type: (str, bool) -> str
    """
    :doc: file_rare
    :name: renpy.fsencode

    Converts s from unicode to the filesystem encoding.
    """

    if (not PY2) and (not force):
        return s

    if not isinstance(s, str):
        return s

    fsencoding = sys.getfilesystemencoding() or "utf-8"
    return s.encode(fsencoding) # type: ignore


@renpy_pure
def fsdecode(s): # type: (bytes|str) -> str
    """
    :doc: file_rare
    :name: renpy.fsdecode

    Converts s from filesystem encoding to unicode.
    """

    if isinstance(s, str):
        return s

    fsencoding = sys.getfilesystemencoding() or "utf-8"
    return s.decode(fsencoding) # type: ignore


def munge(name, filename=None):
    """
    :doc: other

    Munges `name`, which must begin with __.

    `filename`
        The filename the name is munged into. If None, the name is munged
        into the filename containing the call to this function.
    """

    if not name.startswith("__"):
        return name

    if name.endswith("__"):
        return name

    if filename is None:
        filename = sys._getframe(1).f_code.co_filename

    return renpy.lexer.munge_filename(filename) + name[2:]
