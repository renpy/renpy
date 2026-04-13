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

"""
C++ optimized RPA archive reader.
"""

import io
from renpy.pygame.rwobject import RWopsIO

try:
    from renpy.loader.rpa_archive import RPAFile
    _HAS_CXX_READER = True
except ImportError:
    _HAS_CXX_READER = False


class CachedRPAFile:
    """
    A cached RPA file reader that provides fast random access to entries.
    """

    def __init__(self, path):
        self.path = path
        self.archive = None
        self._entries = None

    def open(self):
        if self.archive is None:
            self.archive = RPAFile(self.path)
            self.archive.__enter__()
        return self

    def close(self):
        if self.archive is not None:
            self.archive.__exit__(None, None, None)
            self.archive = None

    def read_entry(self, name):
        if self.archive is None:
            self.open()
        return self.archive.read_entry(name)

    def has_entry(self, name):
        if self.archive is None:
            self.open()
        return self.archive.has_entry(name)

    def entries(self):
        if self._entries is None and self.archive is not None:
            self._entries = self.archive.get_all_entries()
        return self._entries

    def __enter__(self):
        self.open()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.close()


_rpa_cache = {}


def get_rpa_reader(path):
    """
    Get a cached RPA file reader for the given path.
    """
    if path not in _rpa_cache:
        _rpa_cache[path] = CachedRPAFile(path)
    return _rpa_cache[path]


def read_from_rpa(archive_path, entry_name):
    """
    Read a single entry from an RPA archive using the C++ reader.

    Returns bytes or None if the entry doesn't exist.
    """
    if not _HAS_CXX_READER:
        return None

    reader = get_rpa_reader(archive_path)
    return reader.read_entry(entry_name)


def has_in_rpa(archive_path, entry_name):
    """
    Check if an entry exists in an RPA archive using the C++ reader.
    """
    if not _HAS_CXX_READER:
        return False

    reader = get_rpa_reader(archive_path)
    return reader.has_entry(entry_name)


def preload_rpa_index(archive_path):
    """
    Preload the index of an RPA archive for faster later access.
    """
    if not _HAS_CXX_READER:
        return False

    reader = get_rpa_reader(archive_path)
    reader.open()
    return True
