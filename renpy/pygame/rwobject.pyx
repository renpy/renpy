# Copyright 2014 Tom Rothamel <tom@rothamel.us>
#
# This software is provided 'as-is', without any express or implied
# warranty.  In no event will the authors be held liable for any damages
# arising from the use of this software.
#
# Permission is granted to anyone to use this software for any purpose,
# including commercial applications, and to alter it and redistribute it
# freely, subject to the following restrictions:
#
# 1. The origin of this software must not be misrepresented; you must not
#    claim that you wrote the original software. If you use this software
#    in a product, an acknowledgment in the product documentation would be
#    appreciated but is not required.
# 2. Altered source versions must be plainly marked as such, and must not be
#    misrepresented as being the original software.
# 3. This notice may not be removed or altered from any source distribution.

from sdl2 cimport *
from cpython.ref cimport Py_INCREF, Py_DECREF
from cpython.buffer cimport PyObject_CheckBuffer, PyObject_GetBuffer, PyBuffer_Release, PyBUF_CONTIG, PyBUF_CONTIG_RO
from libc.string cimport memcpy
from libc.stdio cimport FILE, fopen, fclose, fseek, ftell, fread, SEEK_SET, SEEK_CUR, SEEK_END
from libc.stdlib cimport calloc, free
from libc.stdint cimport uintptr_t

from renpy.pygame.compat import file_type, bytes_, unicode_

import sys
import io

# The fsencoding.
fsencoding = sys.getfilesystemencoding() or "utf-8"

cdef extern from "SDL.h" nogil:
    Sint64 SDL_RWtell(SDL_RWops* context)

    Sint64 SDL_RWseek(SDL_RWops* context,
                      Sint64     offset,
                      int        whence)

    size_t SDL_RWread(SDL_RWops* context,
                  void*             ptr,
                  size_t            size,
                  size_t            maxnum)

    size_t SDL_RWwrite(SDL_RWops* context,
                       const void*       ptr,
                       size_t            size,
                       size_t            num)

    int SDL_RWclose(SDL_RWops* context)

    SDL_RWops* SDL_RWFromFile(const char *file,
                              const char *mode)

cdef extern from "pygame/python_threads.h":
    void init_python_threads()

cdef set_error(e):
    cdef char *msg
    e = str(e)
    msg = <char *> e
    SDL_SetError("%s", msg)

cdef Sint64 python_size(SDL_RWops *context) noexcept with gil:
    f = <object> context.hidden.unknown.data1

    try:
        cur = f.tell()
        f.seek(0, 2)
        rv = f.tell()
        f.seek(cur, 0)
    except Exception as e:
        return -1

    return rv

cdef Sint64 python_seek(SDL_RWops *context, Sint64 seek, int whence) noexcept with gil:
    f = <object> context.hidden.unknown.data1

    try:
        f.seek(seek, whence)
        rv = f.tell()
    except Exception as e:
        set_error(e)
        return -1

    return rv

cdef size_t python_read(SDL_RWops *context, void *ptr, size_t size, size_t maxnum) noexcept with gil:
    f = <object> context.hidden.unknown.data1

    try:
        data = f.read(size * maxnum)
    except Exception as e:
        set_error(e)
        return -1

    memcpy(ptr, <void *><char *> data, len(data))
    return len(data)

cdef size_t python_write(SDL_RWops *context, const void *ptr, size_t size, size_t maxnum) noexcept with gil:
    f = <object> context.hidden.unknown.data1
    data = (<char *> ptr)[:size * maxnum]

    try:
        f.write(data)
    except Exception as e:
        set_error(e)
        return -1

    return len(data)

cdef int python_close(SDL_RWops *context) noexcept with gil:
    if context != NULL:
        if context.hidden.unknown.data1 != NULL:
            f = <object> context.hidden.unknown.data1

            try:
                f.close()
            except Exception as e:
                set_error(e)
                return -1

            Py_DECREF(f)

            context.hidden.unknown.data1 = NULL
        SDL_FreeRW(context)
    return 0

cdef struct SubFile:
    SDL_RWops *rw
    Sint64 base
    Sint64 length
    Sint64 tell

cdef Sint64 subfile_size(SDL_RWops *context) noexcept nogil:
    cdef SubFile *sf = <SubFile *> context.hidden.unknown.data1
    return sf.length

cdef Sint64 subfile_seek(SDL_RWops *context, Sint64 seek, int whence) noexcept nogil:
    cdef SubFile *sf = <SubFile *> context.hidden.unknown.data1

    if whence == RW_SEEK_SET:
        sf.tell = SDL_RWseek(sf.rw, seek + sf.base, RW_SEEK_SET) - sf.base
    elif whence == RW_SEEK_CUR:
        sf.tell = SDL_RWseek(sf.rw, seek, RW_SEEK_CUR) - sf.base
    elif whence == RW_SEEK_END:
        sf.tell = SDL_RWseek(sf.rw, sf.base + sf.length + seek, RW_SEEK_SET) - sf.base

    return sf.tell

cdef size_t subfile_read(SDL_RWops *context, void *ptr, size_t size, size_t maxnum) noexcept nogil:
    cdef SubFile *sf = <SubFile *> context.hidden.unknown.data1

    cdef Sint64 left = sf.length - sf.tell
    cdef size_t rv

    if size * maxnum > left:
        maxnum = left // size

    if maxnum == 0:
        return 0

    rv = SDL_RWread(sf.rw, ptr, size, maxnum)

    if rv > 0:
        sf.tell += size * rv

    return rv

cdef int subfile_close(SDL_RWops *context) noexcept nogil:
    cdef SubFile *sf

    if context != NULL:
        sf = <SubFile *> context.hidden.unknown.data1
        if sf.rw != NULL:
            SDL_RWclose(sf.rw)
        if sf != NULL:
            free(sf)
            context.hidden.unknown.data1 = NULL
        SDL_FreeRW(context)

    return 0


cdef struct SplitFile:
    SDL_RWops *a
    SDL_RWops *b
    Sint64 split
    Sint64 tell

cdef Sint64 splitfile_size(SDL_RWops *context) noexcept nogil:
    cdef SplitFile *sf = <SplitFile *> context.hidden.unknown.data1
    cdef Sint64 rv

    return SDL_RWsize(sf.a) + SDL_RWsize(sf.b)

cdef Sint64 splitfile_seek(SDL_RWops *context, Sint64 seek, int whence) noexcept nogil:
    cdef SplitFile *sf = <SplitFile *> context.hidden.unknown.data1
    cdef Sint64 rv

    if whence == RW_SEEK_SET:
        sf.tell = seek
    elif whence == RW_SEEK_CUR:
        sf.tell += seek
    elif whence == RW_SEEK_END:
        sf.tell = splitfile_size(context) + seek

    if sf.tell < sf.split:
        rv = SDL_RWseek(sf.a, sf.tell, RW_SEEK_SET)
        SDL_RWseek(sf.b, 0, RW_SEEK_SET)
    else:
        SDL_RWseek(sf.a, sf.split, RW_SEEK_SET)
        rv = SDL_RWseek(sf.b, sf.tell - sf.split, RW_SEEK_SET)

    if rv < 0:
        return rv
    else:
        return sf.tell

cdef size_t splitfile_read(SDL_RWops *context, void *ptr, size_t size, size_t maxnum) noexcept nogil:
    cdef SplitFile *sf = <SplitFile *> context.hidden.unknown.data1
    cdef Sint64 left = splitfile_size(context) - sf.tell
    cdef size_t rv

    cdef size_t total_read
    cdef size_t left_read
    cdef size_t right_read
    cdef size_t ret

    total_read = size * maxnum

    left_read = min(total_read, sf.split - sf.tell)
    left_read = max(left_read, 0)

    if left_read > 0:
        left_read = SDL_RWread(sf.a, ptr, 1, left_read)
        if left_read < 0:
            return left_read

    right_read = total_read - left_read

    if right_read > 0:
        right_read = SDL_RWread(sf.b, <char *> ptr + left_read, 1, right_read)
        if right_read < 0:
            return right_read

    sf.tell += left_read + right_read

    return (left_read + right_read) // size

cdef int splitfile_close(SDL_RWops *context) noexcept nogil:
    cdef SplitFile *sf

    if context != NULL:
        sf = <SplitFile *> context.hidden.unknown.data1
        if sf.a != NULL:
            SDL_RWclose(sf.a)
        if sf.b != NULL:
            SDL_RWclose(sf.b)
        if sf != NULL:
            free(sf)
            context.hidden.unknown.data1 = NULL
        SDL_FreeRW(context)

    return 0


cdef struct BufFile:
    Py_buffer view
    Uint8 *base
    Uint8 *here
    Uint8 *stop

cdef Sint64 buffile_size(SDL_RWops *context) noexcept nogil:
    cdef BufFile *bf = <BufFile *> context.hidden.unknown.data1

    return bf.stop - bf.base

cdef Sint64 buffile_seek(SDL_RWops *context, Sint64 offset, int whence) noexcept nogil:
    cdef BufFile *bf = <BufFile *> context.hidden.unknown.data1

    cdef Uint8 *newpos

    if whence == RW_SEEK_SET:
        newpos = bf.base + offset
    elif whence == RW_SEEK_CUR:
        newpos = bf.here + offset
    elif whence == RW_SEEK_END:
        newpos = bf.stop + offset
    else:
        with gil:
            set_error("Unknown value for 'whence'")
        return -1
    if newpos < bf.base:
        newpos = bf.base
    if newpos > bf.stop:
        newpos = bf.stop
    bf.here = newpos

    return bf.here - bf.base

cdef size_t buffile_read(SDL_RWops *context, void *ptr, size_t size, size_t maxnum) noexcept nogil:
    cdef BufFile *bf = <BufFile *> context.hidden.unknown.data1
    cdef size_t total_bytes = 0
    cdef size_t mem_available = 0

    total_bytes = maxnum * size
    if (maxnum == 0) or (size == 0) or ((total_bytes // maxnum) != size):
        return 0

    mem_available = bf.stop - bf.here
    if total_bytes > mem_available:
        total_bytes = mem_available

    SDL_memcpy(ptr, bf.here, total_bytes)
    bf.here += total_bytes

    return (total_bytes // size)

cdef size_t buffile_write(SDL_RWops *context, const void *ptr, size_t size, size_t num) noexcept nogil:
    cdef BufFile *bf = <BufFile *> context.hidden.unknown.data1

    if bf.view.readonly != 0:
        return 0

    if (bf.here + (num * size)) > bf.stop:
        num = (bf.stop - bf.here) // size
    SDL_memcpy(bf.here, ptr, num * size)
    bf.here += num * size

    return num

cdef int buffile_close(SDL_RWops *context) noexcept with gil:
    cdef BufFile *bf

    if context != NULL:
        bf = <BufFile *> context.hidden.unknown.data1
        if bf != NULL:
            PyBuffer_Release(&bf.view)
            free(bf)
            bf = NULL
        SDL_FreeRW(context)

    return 0


cdef SDL_RWops *to_rwops(filelike, mode="rb", base=None, length=None) except NULL:
    """
    This accepts, in order:

    * An io.BufferedIOBase object, which is unwrapped to get the
      underlying file object. (Which is then processed as below.)

    * A RWopsIO object, which is closed and the underlying SDL_RWops
      object is returned.

    * A filename, which is opened.

    * An object with the name, base, and length attributes. The name is
      interpreted as a filename, and the base and length are used to
      create a subfile.

    * An object with a name fileld. The name is interpreted as a filename.
      and opened. The object will be closed.

    * An object that supports the buffer protocol.

    * A file-like object, which is wrapped in a Python file-like object

    It returns an SDL_RWops object, or NULL on error.
    """

    cdef FILE *f
    cdef SubFile *sf
    cdef SDL_RWops *rv
    cdef SDL_RWops *rw
    cdef char *cname
    cdef char *cmode

    cdef RWopsIOImpl rwopsio

    if not isinstance(mode, bytes_):
        mode = mode.encode("ascii")

    name = filelike

    # Handle turning BufferedIOBase and RWopsIO objects into their underlying
    # objects.
    try:
        while True:
            filelike = filelike.raw
    except AttributeError:
        pass

    if isinstance(filelike, RWopsIOImpl):
        rwopsio = <RWopsIOImpl> filelike
        if not rwopsio.ops:
            raise ValueError("I/O on closed file.")

        rv = rwopsio.ops
        rwopsio.ops = NULL
        return rv

    if isinstance(filelike, (file_type, io.IOBase)) and mode == "rb":
        name = getattr(filelike, "name", None)

    # Try to open as a file.
    if isinstance(name, bytes_):
        name = name.decode(fsencoding)
    elif isinstance(name, unicode_):
        pass
    else:
        name = None

    if (mode == b"rb") and (name is not None):

        dname = name.encode("utf-8")
        cname = dname
        cmode = mode

        with nogil:
            rv = SDL_RWFromFile(cname, cmode)

        if rv == NULL:
            raise IOError("Could not open {!r}: {}".format(name, SDL_GetError()))

        if base is None and length is None:
            try:
                base = filelike.base
                length = filelike.length
            except AttributeError:
                pass

        if base is not None and length is not None:

            # If we have these properties, we're either an APK asset or a Ren'Py-style
            # subfile, so use an optimized path.

            rw = rv

            SDL_RWseek(rw, base, RW_SEEK_SET);

            sf = <SubFile *> calloc(sizeof(SubFile), 1)
            sf.rw = rw
            sf.base = base
            sf.length = length
            sf.tell = 0

            rv = SDL_AllocRW()
            rv.size = subfile_size
            rv.seek = subfile_seek
            rv.read = subfile_read
            rv.write = NULL
            rv.close = subfile_close
            rv.type = 0
            rv.hidden.unknown.data1 = <void *> sf

        try:
            filelike.close()
        except:
            pass

        return rv

    if not (hasattr(filelike, "read") or hasattr(filelike, "write")):
        raise IOError("{!r} is not a filename or file-like object.".format(filelike))

    Py_INCREF(filelike)

    rv = SDL_AllocRW()
    rv.size = python_size
    rv.seek = python_seek
    rv.read = python_read
    rv.write = python_write
    rv.close = python_close
    rv.type = 0
    rv.hidden.unknown.data1 = <void *> filelike

    return rv


whence_mapping = {
    io.SEEK_SET : RW_SEEK_SET,
    io.SEEK_CUR : RW_SEEK_CUR,
    io.SEEK_END : RW_SEEK_END,
}

cdef class RWopsIOImpl:
    """
    This wraps an SDL_RWops object in a Python file-like object.
    """

    cdef SDL_RWops *ops
    cdef public object name
    cdef public object base
    cdef public object length

    def __dealloc__(self):
        if self.ops != NULL:
            SDL_RWclose(self.ops)
            self.ops = NULL

    def __init__(self, filelike, mode="rb", base=None, length=None, name=None):
        """
        Creates a new RWopsIO object. All parameter are passed to to_rwops
        to create the SDL_RWops object.
        """

        if name is not None:
            self.name = name
        elif isinstance(filelike, basestring):
            self.name = filelike
        else:
            self.name = getattr(filelike, "name", name)

        self.base = base
        self.length = length

        if filelike is not None:
            self.ops = to_rwops(filelike, mode, base, length)
        else:
            self.ops = NULL

    def close(self):

        # A closed file may be closed again.

        if self.ops:
            SDL_RWclose(self.ops)
            self.ops = NULL

    def is_closed(self):
        return not self.ops

    def seek(self, long long offset, whence=0):
        cdef int whence_rw
        cdef long long rv

        if not self.ops:
            raise ValueError("I/O operation on closed file.")

        whence_rw = whence_mapping.get(whence, RW_SEEK_SET)

        with nogil:
            rv = SDL_RWseek(self.ops, offset, whence_rw)

        if rv < 0:
            raise IOError("Could not seek: {}".format(SDL_GetError()))

        return rv

    def tell(self):
        cdef long long rv

        with nogil:
          rv = SDL_RWtell(self.ops)

        return rv

    def readinto(self, b):
        cdef Py_buffer view
        cdef long long rv = 0

        if not self.ops:
            raise ValueError("I/O operation on closed file.")

        if not PyObject_CheckBuffer(b):
            raise ValueError("Passed in object does not support buffer protocol")

        try:
            PyObject_GetBuffer(b, &view, PyBUF_CONTIG)

            with nogil:
                rv = SDL_RWread(self.ops, view.buf, 1, view.len)
        finally:
            PyBuffer_Release(&view)

        if rv < 0:
            raise IOError("Could not read: {}".format(SDL_GetError()))

        return rv

    def write(self, b):
        cdef Py_buffer view
        cdef long long rv = 0

        if not self.ops:
            raise ValueError("I/O operation on closed file.")

        if not PyObject_CheckBuffer(b):
            raise ValueError("Passed in object does not support buffer protocol")

        try:
            PyObject_GetBuffer(b, &view, PyBUF_CONTIG_RO)
            with nogil:
                rv = SDL_RWwrite(self.ops, view.buf, 1, view.len)
        finally:
            PyBuffer_Release(&view)

        if rv < 0:
            raise IOError("Could not write: {}".format(SDL_GetError()))

        return rv


cdef SDL_RWops *RWopsFromPython(filelike) except NULL:
    return to_rwops(filelike, "rb", None, None)


class RWopsIO(io.RawIOBase):

    def __init__(self, filelike, mode='rb', base=None, length=None, name=None):
        """
        Creates a new RWopsIO object. All parameter are passed to to_rwops
        to create the SDL_RWops object.
        """

        io.RawIOBase.__init__(self)

        self.raw = RWopsIOImpl(filelike, mode=mode, base=base, length=length, name=name)

        self.close = self.raw.close
        self.seek = self.raw.seek
        self.tell = self.raw.tell
        self.write = self.raw.write
        self.readinto = self.raw.readinto

    def __repr__(self):
        if self.raw.base is not None:
            return "<RWopsIO {!r} base={!r} length={!r}>".format(self.raw.name, self.raw.base, self.raw.length)
        else:
            return "<RWopsIO {!r}>".format(self.raw.name)

    # Implemented class: io.IOBase

    # close is taken from RWopsIOImpl.

    @property
    def closed(self):
        return self.raw.is_closed()

    def fileno(self):
        raise OSError()

    # inherited flush is used

    # inherited isatty is used

    def readable(self):
        return True

    # inherited readline is used

    # inherited readlines is used

    # seek is taken from RWopsIOImpl.

    def seekable(self):
        return True

    # tell is taken from RWopsIOImpl.

    def truncate(self, size=None):
        raise OSError()

    def writable(self):
        return True

    # inherited writelines is used

    # inherited __del__ is used

    # Implemented class: io.RawIOBase

    # inherited read is used

    # inherited readall is used

    # readinto is taken from RWopsIOImpl.

    # write is taken from RWopsIOImpl.

    @staticmethod
    def from_buffer(buffer, mode="rb", name=None):
        """
        Creates a new RWopsIO object from a buffer.
        """

        cdef BufFile *bf
        cdef SDL_RWops *rw

        if not PyObject_CheckBuffer(buffer):
            raise ValueError("Passed in object does not support buffer protocol")

        bf = <BufFile *> calloc(sizeof(BufFile), 1)
        if bf == NULL:
            raise MemoryError()

        if PyObject_GetBuffer(buffer, &bf.view, PyBUF_CONTIG_RO) < 0:
            free(bf)
            raise ValueError("Could not get buffer.")

        bf.base = <Uint8 *> bf.view.buf
        bf.here = bf.base
        bf.stop = bf.base + bf.view.len

        rw = SDL_AllocRW()
        rw.size = buffile_size
        rw.seek = buffile_seek
        rw.read = buffile_read
        rw.write = buffile_write
        rw.close = buffile_close
        rw.type = 0
        rw.hidden.unknown.data1 = <void *> bf

        rv = RWopsIO(None, name=name)
        (<RWopsIOImpl> rv.raw).ops = rw
        return rv

    @staticmethod
    def from_split(a, b, name=None):
        """
        Creates a new RWopsIO object from two other RWopsIO objects,
        representing the concatenation of the two.
        """

        cdef SplitFile *sf
        cdef SDL_RWops *rw

        sf = <SplitFile *> calloc(sizeof(SplitFile), 1)
        if sf == NULL:
            raise MemoryError()

        sf.a = to_rwops(a)
        sf.b = to_rwops(b)
        sf.split = SDL_RWsize(sf.a)
        sf.tell = 0

        rw = SDL_AllocRW()
        rw.size = splitfile_size
        rw.seek = splitfile_seek
        rw.read = splitfile_read
        rw.write = NULL
        rw.close = splitfile_close
        rw.type = 0
        rw.hidden.unknown.data1 = <void *> sf

        rv = RWopsIO(None, name=name)
        (<RWopsIOImpl> rv.raw).ops = rw
        return rv



init_python_threads()
