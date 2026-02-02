# Copyright 2014-2026 Tom Rothamel <pytom@bishoujo.us>
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

from .sdl cimport *
from cpython.ref cimport Py_INCREF, Py_DECREF
from cpython.buffer cimport PyObject_CheckBuffer, PyObject_GetBuffer, PyBuffer_Release, PyBUF_CONTIG, PyBUF_CONTIG_RO
from libc.string cimport memcpy
from libc.stdio cimport FILE, fopen, fclose, fseek, ftell, fread, SEEK_SET, SEEK_CUR, SEEK_END
from libc.stdlib cimport calloc, free
from libc.stdint cimport uintptr_t
from libcpp cimport bool

import sys
import io

cdef extern from "SDL3/SDL.h":
    cdef struct SDL_IOStreamInterface:
        Uint32 version
        Sint64 (*size)(void *userdata) noexcept nogil
        Sint64 (*seek)(void *userdata, Sint64 offset, SDL_IOWhence whence) noexcept nogil
        size_t (*read)(void *userdata, void *ptr, size_t size, SDL_IOStatus *status) noexcept nogil
        size_t (*write)(void *userdata, const void *ptr, size_t size, SDL_IOStatus *status) noexcept nogil
        bool (*flush)(void *userdata, SDL_IOStatus *status) noexcept nogil
        bool (*close)(void *userdata) noexcept nogil

# The fsencoding.
fsencoding = sys.getfilesystemencoding() or "utf-8"

cdef extern from "pygame/python_threads.h":
    void init_python_threads()

cdef set_error(e):
    cdef char *msg
    e = str(e)
    msg = <char *> e
    SDL_SetError("%s", msg)

cdef Sint64 python_size(void *userdata) noexcept with gil:
    f = <object> userdata

    try:
        cur = f.tell()
        f.seek(0, 2)
        rv = f.tell()
        f.seek(cur, 0)
    except Exception as e:
        return -1

    return rv

cdef Sint64 python_seek(void *userdata, Sint64 seek, SDL_IOWhence whence) noexcept with gil:
    f = <object> userdata

    try:
        f.seek(seek, whence)
        rv = f.tell()
    except Exception as e:
        set_error(e)
        return -1

    return rv

cdef size_t python_read(void *userdata, void *ptr, size_t size, SDL_IOStatus *status) noexcept with gil:
    f = <object> userdata

    try:
        data = f.read(size)
    except Exception as e:
        status[0] = SDL_IO_STATUS_ERROR
        set_error(e)
        return -1

    memcpy(ptr, <void *><char *> data, len(data))
    return len(data)

cdef size_t python_write(void *userdata, const void *ptr, size_t size, SDL_IOStatus *status) noexcept with gil:
    f = <object> userdata
    data = (<char *> ptr)[:size]

    try:
        f.write(data)
    except Exception as e:
        status[0] = SDL_IO_STATUS_ERROR
        set_error(e)
        return -1

    return len(data)

cdef bool python_flush(void *userdata, SDL_IOStatus *status) noexcept with gil:
    f = <object> userdata

    try:
        f.flush()
    except Exception as e:
        status[0] = SDL_IO_STATUS_ERROR
        set_error(e)
        return False

    return True

cdef bool python_close(void *userdata) noexcept with gil:
    if userdata != NULL:
        f = <object> userdata

        try:
            f.close()
        except Exception as e:
            set_error(e)
            return False

        Py_DECREF(f)

        userdata = NULL
    return True

cdef SDL_IOStreamInterface python_iointerface
python_iointerface.version = sizeof(SDL_IOStreamInterface)
python_iointerface.size = python_size
python_iointerface.seek = python_seek
python_iointerface.read = python_read
python_iointerface.write = python_write
python_iointerface.flush = python_flush
python_iointerface.close = python_close


cdef struct SubFile:
    SDL_IOStream *rw
    Sint64 base
    Sint64 length
    Sint64 tell


cdef Sint64 subfile_size(void *userdata) noexcept nogil:
    cdef SubFile *sf = <SubFile *> userdata
    return sf.length

cdef Sint64 subfile_seek(void *userdata, Sint64 offset, SDL_IOWhence whence) noexcept nogil:
    cdef SubFile *sf = <SubFile *> userdata

    if whence == SDL_IO_SEEK_SET:
        sf.tell = SDL_SeekIO(sf.rw, offset + sf.base, SDL_IO_SEEK_SET) - sf.base
    elif whence == SDL_IO_SEEK_CUR:
        sf.tell = SDL_SeekIO(sf.rw, offset, SDL_IO_SEEK_CUR) - sf.base
    elif whence == SDL_IO_SEEK_END:
        sf.tell = SDL_SeekIO(sf.rw, sf.base + sf.length + offset, SDL_IO_SEEK_SET) - sf.base

    return sf.tell

cdef size_t subfile_read(void *userdata, void *ptr, size_t size, SDL_IOStatus *status) noexcept nogil:
    cdef SubFile *sf = <SubFile *> userdata

    cdef Sint64 left = sf.length - sf.tell
    cdef size_t rv

    if size > left:
        size = left

    if size == 0:
        status[0] = SDL_IO_STATUS_EOF
        return 0

    rv = SDL_ReadIO(sf.rw, ptr, size)

    if rv > 0:
        sf.tell += rv
        status[0] = SDL_IO_STATUS_READY
    else:
        status[0] = SDL_IO_STATUS_ERROR

    return rv

cdef size_t subfile_write(void *userdata, const void *ptr, size_t size, SDL_IOStatus *status) noexcept nogil:
    status[0] = SDL_IO_STATUS_READONLY
    return 0

cdef bool subfile_flush(void *userdata, SDL_IOStatus *status) noexcept nogil:
    status[0] = SDL_IO_STATUS_READY
    return True

cdef bool subfile_close(void *userdata) noexcept nogil:
    cdef SubFile *sf = <SubFile *> userdata

    if sf != NULL:
        if sf.rw != NULL:
            SDL_CloseIO(sf.rw)
        free(sf)

    return True

cdef SDL_IOStreamInterface subfile_iointerface
subfile_iointerface.version = sizeof(SDL_IOStreamInterface)
subfile_iointerface.size = subfile_size
subfile_iointerface.seek = subfile_seek
subfile_iointerface.read = subfile_read
subfile_iointerface.write = subfile_write
subfile_iointerface.flush = subfile_flush
subfile_iointerface.close = subfile_close


cdef struct SplitFile:
    SDL_IOStream *a
    SDL_IOStream *b
    Sint64 split
    Sint64 tell

cdef Sint64 splitfile_size(void *userdata) noexcept nogil:
    cdef SplitFile *sf = <SplitFile *> userdata
    cdef Sint64 rv

    return SDL_GetIOSize(sf.a) + SDL_GetIOSize(sf.b)

cdef Sint64 splitfile_seek(void *userdata, Sint64 offset, SDL_IOWhence whence) noexcept nogil:
    cdef SplitFile *sf = <SplitFile *> userdata
    cdef Sint64 rv

    if whence == SDL_IO_SEEK_SET:
        sf.tell = offset
    elif whence == SDL_IO_SEEK_CUR:
        sf.tell += offset
    elif whence == SDL_IO_SEEK_END:
        sf.tell = splitfile_size(userdata) + offset

    if sf.tell < sf.split:
        rv = SDL_SeekIO(sf.a, sf.tell, SDL_IO_SEEK_SET)
        SDL_SeekIO(sf.b, 0, SDL_IO_SEEK_SET)
    else:
        SDL_SeekIO(sf.a, sf.split, SDL_IO_SEEK_SET)
        rv = SDL_SeekIO(sf.b, sf.tell - sf.split, SDL_IO_SEEK_SET)

    if rv < 0:
        return rv
    else:
        return sf.tell

cdef size_t splitfile_read(void *userdata, void *ptr, size_t size, SDL_IOStatus *status) noexcept nogil:
    cdef SplitFile *sf = <SplitFile *> userdata
    cdef Sint64 left = splitfile_size(userdata) - sf.tell
    cdef size_t rv

    cdef size_t total_read
    cdef size_t left_read
    cdef size_t right_read

    if size > left:
        size = left

    if size == 0:
        status[0] = SDL_IO_STATUS_EOF
        return 0

    left_read = min(size, sf.split - sf.tell)
    left_read = max(left_read, 0)

    if left_read > 0:
        left_read = SDL_ReadIO(sf.a, ptr, left_read)
        if left_read < 0:
            status[0] = SDL_IO_STATUS_ERROR
            return 0

    right_read = size - left_read

    if right_read > 0:
        right_read = SDL_ReadIO(sf.b, <char *> ptr + left_read, right_read)
        if right_read < 0:
            status[0] = SDL_IO_STATUS_ERROR
            return 0

    sf.tell += left_read + right_read

    status[0] = SDL_IO_STATUS_READY
    return left_read + right_read

cdef size_t splitfile_write(void *userdata, const void *ptr, size_t size, SDL_IOStatus *status) noexcept nogil:
    status[0] = SDL_IO_STATUS_READONLY
    return 0

cdef bool splitfile_flush(void *userdata, SDL_IOStatus *status) noexcept nogil:
    status[0] = SDL_IO_STATUS_READY
    return True

cdef bool splitfile_close(void *userdata) noexcept nogil:
    cdef SplitFile *sf = <SplitFile *> userdata

    if sf != NULL:
        if sf.a != NULL:
            SDL_CloseIO(sf.a)
        if sf.b != NULL:
            SDL_CloseIO(sf.b)
        free(sf)

    return True

cdef SDL_IOStreamInterface splitfile_iointerface
splitfile_iointerface.version = sizeof(SDL_IOStreamInterface)
splitfile_iointerface.size = splitfile_size
splitfile_iointerface.seek = splitfile_seek
splitfile_iointerface.read = splitfile_read
splitfile_iointerface.write = splitfile_write
splitfile_iointerface.flush = splitfile_flush
splitfile_iointerface.close = splitfile_close


cdef struct BufFile:
    Py_buffer view
    Uint8 *base
    Uint8 *here
    Uint8 *stop

cdef Sint64 buffile_size(void *userdata) noexcept nogil:
    cdef BufFile *bf = <BufFile *> userdata

    return bf.stop - bf.base

cdef Sint64 buffile_seek(void *userdata, Sint64 offset, SDL_IOWhence whence) noexcept nogil:
    cdef BufFile *bf = <BufFile *> userdata

    cdef Uint8 *newpos

    if whence == SDL_IO_SEEK_SET:
        newpos = bf.base + offset
    elif whence == SDL_IO_SEEK_CUR:
        newpos = bf.here + offset
    elif whence == SDL_IO_SEEK_END:
        newpos = bf.stop + offset
    else:
        return -1
    if newpos < bf.base:
        newpos = bf.base
    if newpos > bf.stop:
        newpos = bf.stop
    bf.here = newpos

    return bf.here - bf.base

cdef size_t buffile_read(void *userdata, void *ptr, size_t size, SDL_IOStatus *status) noexcept nogil:
    cdef BufFile *bf = <BufFile *> userdata
    cdef size_t mem_available = 0

    mem_available = bf.stop - bf.here
    if size > mem_available:
        size = mem_available

    if size == 0:
        status[0] = SDL_IO_STATUS_EOF
        return 0

    memcpy(ptr, bf.here, size)
    bf.here += size

    status[0] = SDL_IO_STATUS_READY
    return size

cdef size_t buffile_write(void *userdata, const void *ptr, size_t size, SDL_IOStatus *status) noexcept nogil:
    cdef BufFile *bf = <BufFile *> userdata

    if bf.view.readonly != 0:
        status[0] = SDL_IO_STATUS_READONLY
        return 0

    if (bf.here + size) > bf.stop:
        size = bf.stop - bf.here

    memcpy(bf.here, ptr, size)
    bf.here += size

    status[0] = SDL_IO_STATUS_READY
    return size

cdef bool buffile_flush(void *userdata, SDL_IOStatus *status) noexcept nogil:
    status[0] = SDL_IO_STATUS_READY
    return True

cdef bool buffile_close(void *userdata) noexcept with gil:
    cdef BufFile *bf = <BufFile *> userdata

    if bf != NULL:
        PyBuffer_Release(&bf.view)
        free(bf)

    return True

cdef SDL_IOStreamInterface buffile_iointerface
buffile_iointerface.version = sizeof(SDL_IOStreamInterface)
buffile_iointerface.size = buffile_size
buffile_iointerface.seek = buffile_seek
buffile_iointerface.read = buffile_read
buffile_iointerface.write = buffile_write
buffile_iointerface.flush = buffile_flush
buffile_iointerface.close = buffile_close


cdef SDL_IOStream *to_sdl_iostream(filelike, mode="rb", base=None, length=None) except NULL:
    """
    This accepts, in order:

    * An io.BufferedIOBase object, which is unwrapped to get the
      underlying file object. (Which is then processed as below.)

    * An IOStream object, which is closed and the underlying SDL_IOStream
      object is returned.

    * A filename, which is opened.

    * An object with the name, base, and length attributes. The name is
      interpreted as a filename, and the base and length are used to
      create a subfile.

    * An object with a name fileld. The name is interpreted as a filename.
      and opened. The object will be closed.

    * An object that supports the buffer protocol.

    * A file-like object, which is wrapped in a Python file-like object

    It returns an SDL_IOStream object, or NULL on error.
    """

    cdef FILE *f
    cdef SubFile *sf
    cdef SDL_IOStream *rv
    cdef SDL_IOStream *rw
    cdef char *cname
    cdef char *cmode

    cdef IOStreamImpl iostream

    if not isinstance(mode, bytes):
        mode = mode.encode("ascii")

    name = filelike

    # Handle turning BufferedIOBase and IOStream objects into their underlying
    # objects.
    try:
        while True:
            filelike = filelike.raw
    except AttributeError:
        pass

    if isinstance(filelike, IOStreamImpl):
        iostream = <IOStreamImpl> filelike
        if not iostream.ops:
            raise ValueError("I/O on closed file.")

        rv = iostream.ops
        iostream.ops = NULL
        return rv

    if isinstance(filelike, (io.FileIO, io.IOBase)) and mode == "rb":
        name = getattr(filelike, "name", None)

    # Try to open as a file.
    if isinstance(name, bytes):
        name = name.decode(fsencoding)
    elif isinstance(name, str):
        pass
    else:
        name = None

    if (mode == b"rb") and (name is not None):

        dname = name.encode("utf-8")
        cname = dname
        cmode = mode

        with nogil:
            rv = SDL_IOFromFile(cname, cmode)

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

            SDL_SeekIO(rw, base, SDL_IO_SEEK_SET);

            sf = <SubFile *> calloc(sizeof(SubFile), 1)
            sf.rw = rw
            sf.base = base
            sf.length = length
            sf.tell = 0

            rv = SDL_OpenIO(&subfile_iointerface, <void *> sf)

        try:
            filelike.close()
        except:
            pass

        return rv

    if not (hasattr(filelike, "read") or hasattr(filelike, "write")):
        raise IOError("{!r} is not a filename or file-like object.".format(filelike))

    Py_INCREF(filelike)

    rv = SDL_OpenIO(&python_iointerface, <void *> filelike)

    return rv


whence_mapping = {
    io.SEEK_SET : SDL_IO_SEEK_SET,
    io.SEEK_CUR : SDL_IO_SEEK_CUR,
    io.SEEK_END : SDL_IO_SEEK_END,
}

cdef class IOStreamImpl:
    """
    This wraps an SDL_IOStream object in a Python file-like object.
    """

    cdef SDL_IOStream *ops
    cdef public object name
    cdef public object base
    cdef public object length

    def __dealloc__(self):
        if self.ops != NULL:
            SDL_CloseIO(self.ops)
            self.ops = NULL

    def __init__(self, filelike, mode="rb", base=None, length=None, name=None):
        """
        Creates a new IOStreamImpl object. All parameter are passed to to_sdl_iostream
        to create the SDL_IOstream object.
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
            self.ops = to_sdl_iostream(filelike, mode, base, length)
        else:
            self.ops = NULL

    def close(self):

        # A closed file may be closed again.

        if self.ops:
            SDL_CloseIO(self.ops)
            self.ops = NULL

    def is_closed(self):
        return not self.ops

    def seek(self, long long offset, whence=0):
        cdef SDL_IOWhence whence_io
        cdef long long rv

        if not self.ops:
            raise ValueError("I/O operation on closed file.")

        whence_io = whence_mapping.get(whence, SDL_IO_SEEK_SET)

        with nogil:
            rv = SDL_SeekIO(self.ops, offset, whence_io)

        if rv < 0:
            raise IOError("Could not seek: {}".format(SDL_GetError()))

        return rv

    def tell(self):
        cdef long long rv

        with nogil:
            rv = SDL_TellIO(self.ops)

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
                rv = SDL_WriteIO(self.ops, view.buf, view.len)
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
                rv = SDL_WriteIO(self.ops, view.buf, view.len)
        finally:
            PyBuffer_Release(&view)

        if rv < 0:
            raise IOError("Could not write: {}".format(SDL_GetError()))

        return rv


cdef SDL_IOStream *SDLIOStreamFromPython(filelike) except NULL:
    return to_sdl_iostream(filelike, "rb", None, None)


class IOStream(io.RawIOBase):

    def __init__(self, filelike, mode='rb', base=None, length=None, name=None):
        """
        Creates a new IOStream object.
        """

        io.RawIOBase.__init__(self)

        self.raw = IOStreamImpl(filelike, mode=mode, base=base, length=length, name=name)

        self.close = self.raw.close
        self.seek = self.raw.seek
        self.tell = self.raw.tell
        self.write = self.raw.write
        self.readinto = self.raw.readinto

    def __repr__(self):
        if self.raw.base is not None:
            return "<SDLIOStreamIO {!r} base={!r} length={!r}>".format(self.raw.name, self.raw.base, self.raw.length)
        else:
            return "<SDLIOStreamIO {!r}>".format(self.raw.name)

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
        cdef SDL_IOStream *stream

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

        stream = SDL_OpenIO(&buffile_iointerface, <void *> bf)

        rv = IOStream(None, name=name)
        (<IOStreamImpl> rv.raw).ops = stream
        return rv

    @staticmethod
    def from_split(a, b, name=None):
        """
        Creates a new RWopsIO object from two other RWopsIO objects,
        representing the concatenation of the two.
        """

        cdef SplitFile *sf
        cdef SDL_IOStream *rw

        sf = <SplitFile *> calloc(sizeof(SplitFile), 1)
        if sf == NULL:
            raise MemoryError()

        sf.a = to_sdl_iostream(a)
        sf.b = to_sdl_iostream(b)
        sf.split = SDL_GetIOSize(sf.a)
        sf.tell = 0

        rw = SDL_OpenIO(&splitfile_iointerface, <void *> sf)

        rv = IOStream(None, name=name)
        (<IOStreamImpl> rv.raw).ops = rw
        return rv



init_python_threads()
