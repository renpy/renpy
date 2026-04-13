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

from __future__ import print_function

cdef extern from "rpa_archive.h":
    ctypedef struct RPAArchive:
        pass

    ctypedef enum RPAError:
        RPA_OK = 0
        RPA_ERROR_FILE_NOT_FOUND = -1
        RPA_ERROR_INVALID_HEADER = -2
        RPA_ERROR_INDEX_CORRUPT = -3
        RPA_ERROR_ENTRY_NOT_FOUND = -4
        RPA_ERROR_READ_ERROR = -5
        RPA_ERROR_ZLIB_ERROR = -6
        RPA_ERROR_OUT_OF_MEMORY = -7

    int rpa_archive_open(const char* path, RPAArchive** out_archive)
    void rpa_archive_close(RPAArchive* archive)
    int rpa_archive_read_entry(RPAArchive* archive, const char* name, uint8_t** out_data, size_t* out_len)
    int rpa_archive_has_entry(RPAArchive* archive, const char* name)
    int rpa_archive_get_entry_count(RPAArchive* archive)
    const char* rpa_archive_get_entry_name(RPAArchive* archive, int index)
    const char* rpa_archive_error_string(int error)

cdef class RPAFile:
    cdef RPAArchive* archive
    cdef bytes _name

    def __init__(self, name):
        self._name = name.encode('utf-8') if isinstance(name, str) else name

    def __enter__(self):
        cdef RPAArchive* archive
        cdef int result

        result = rpa_archive_open(<const char*>self._name, &archive)
        if result != RPA_OK:
            raise Exception("Failed to open RPA archive: %s" % rpa_archive_error_string(result).decode('utf-8'))

        self.archive = archive
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        if self.archive != NULL:
            rpa_archive_close(self.archive)
            self.archive = NULL

    def read_entry(self, name):
        cdef uint8_t* data
        cdef size_t length
        cdef int result
        cdef bytes py_name

        if self.archive == NULL:
            raise Exception("Archive not opened")

        py_name = name.encode('utf-8') if isinstance(name, str) else name

        result = rpa_archive_read_entry(self.archive, <const char*>py_name, &data, &length)
        if result != RPA_OK:
            return None

        try:
            return bytes(data[:length])
        finally:
            free(data)

    def has_entry(self, name):
        cdef int result
        cdef bytes py_name

        if self.archive == NULL:
            raise Exception("Archive not opened")

        py_name = name.encode('utf-8') if isinstance(name, str) else name

        result = rpa_archive_has_entry(self.archive, <const char*>py_name)
        return result != 0

    def get_entry_count(self):
        if self.archive == NULL:
            raise Exception("Archive not opened")
        return rpa_archive_get_entry_count(self.archive)

    def get_entry_name(self, int index):
        cdef const char* name

        if self.archive == NULL:
            raise Exception("Archive not opened")

        name = rpa_archive_get_entry_name(self.archive, index)
        if name == NULL:
            return None

        return name.decode('utf-8')

    def get_all_entries(self):
        cdef int count
        cdef const char* name
        cdef bytes py_name

        if self.archive == NULL:
            raise Exception("Archive not opened")

        count = rpa_archive_get_entry_count(self.archive)
        entries = []

        for i in range(count):
            name = rpa_archive_get_entry_name(self.archive, i)
            if name != NULL:
                entries.append(name.decode('utf-8'))

        return entries

def open_rpa_archive(name):
    return RPAFile(name)
