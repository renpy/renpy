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

"""
SDL_IOStream-backed file objects.

This module provides a single family of file objects that are simultaneously:

* Usable from Python as raw binary files (registered with io.RawIOBase, so
  they can be wrapped in io.BufferedReader or io.TextIOWrapper).

* Usable from Cython as SDL_IOStream pointers, via IOStream.borrow(), with
  no conversion cost.

Choosing a kind
---------------

IOPath, IOSubFile and IOBuffer are GIL-free on the read path. IOFileLike
reacquires the GIL for every operation, so prefer the others when the data
is reachable another way:

* A path on disk                                         IOPath
* A region inside another IOStream, e.g. an archive      IOSubFile
* bytes, bytearray, memoryview, mmap, array              IOBuffer
* A BytesIO you own and will not resize                  IOBuffer(b.getbuffer())
* Anything computed: gzip, zipfile, network              IOFileLike

Thread safety
-------------

It is unsafe to read or write the same IOStream from different threads at the
same time.

SDL_Quit must be called before interpreter shutdown, or the program may hang,
unable to deallocate Python objects owned by stream userdata.
"""

from .sdl cimport *

from cpython.object cimport PyObject
from cpython.ref cimport Py_INCREF, Py_DECREF
from cpython.buffer cimport (
    PyObject_CheckBuffer,
    PyObject_GetBuffer,
    PyBuffer_Release,
    PyBUF_CONTIG,
    PyBUF_CONTIG_RO,
)
from cpython.exc cimport PyErr_WriteUnraisable
from libc.string cimport memcpy

import io
import os

cdef extern from "SDL3/SDL.h":
    cdef struct SDL_IOStreamInterface:
        Uint32 version
        Sint64 (*size)(void *userdata) noexcept nogil
        Sint64 (*seek)(void *userdata, Sint64 offset, SDL_IOWhence whence) noexcept nogil
        size_t (*read)(void *userdata, void *ptr, size_t size, SDL_IOStatus *status) noexcept nogil
        size_t (*write)(void *userdata, const void *ptr, size_t size, SDL_IOStatus *status) noexcept nogil
        cbool (*flush)(void *userdata, SDL_IOStatus *status) noexcept nogil
        cbool (*close)(void *userdata) noexcept nogil


cdef str get_error():
    cdef const char *message = SDL_GetError()
    return message.decode("utf-8", "replace")


cdef void set_error(object obj):
    cdef bytes msg = str(obj).encode("utf-8", "replace")
    SDL_SetError("%s", <const char *> msg)


################################################################################
# Base class.

cdef class IOStream:
    """
    Abstract base class wrapping an SDL_IOStream. Implements the io.RawIOBase
    interface on top of the SDL_* IO functions.
    """

    def __cinit__(IOStream self not None, *args, **kwargs):
        self._stream = NULL
        self._closed = False

    def __init__(IOStream self not None):
        if type(self) is IOStream:
            raise TypeError("IOStream is abstract, use one of its subclasses.")

    def __del__(IOStream self not None, /):
        # Subclasses can overwrite IOStream.close and using __del__ guards
        # against resurrection.
        if not self.closed:
            try:
                self.close()
            except Exception:
                pass

    def __dealloc__(IOStream self not None, /):
        # Guard against close that didn't closed SDL stream.
        cdef SDL_IOStream *stream = self._stream
        if stream != NULL:
            self._stream = NULL
            SDL_CloseIO(stream)

    # IOBase implements them and others use it, ugly.
    def _checkClosed(IOStream self not None, /):
        if self.closed:
            raise ValueError("I/O operation on closed file.")

    def _checkReadable(IOStream self not None, /):
        if not self.readable():
            raise io.UnsupportedOperation("This stream does not support read.")

    def _checkWritable(IOStream self not None, /):
        if not self.writable():
            raise io.UnsupportedOperation("This stream does not support write.")

    def _checkSeekable(IOStream self not None, /):
        if not self.seekable():
            raise io.UnsupportedOperation("This stream does not support seek.")

    cdef SDL_IOStream *borrow(self) except NULL:
        """
        Borrow the reference to the underlying SDL_IOStream.

        Caller must make sure this object is kept alive while the stream
        is used by SDL. To transfer ownership use IOStream.take().
        """

        self._checkClosed()

        # Protection against improper subclass overrides.
        if self._stream == NULL:
            raise RuntimeError("SDL stream was closed unexpectedly.")

        return self._stream

    def on_take(IOStream self not None, /):
        """
        Called before SDL stream is detached from the object, including when
        the stream is about to be closed.

        This function should clean any references to the objects that
        will be owned by it.
        """

    cdef SDL_IOStream *take(self) except NULL:
        """
        Transfers ownership of the underlying SDL_IOStream to the caller, and
        caller is responsible to call SDL_CloseIO on it.

        This object is closed from Python's point of view after the call.
        """

        self._checkClosed()

        self.on_take()

        # Protection against improper subclass overrides.
        cdef SDL_IOStream *stream = self.borrow()

        self._stream = NULL
        self._closed = True
        return stream

    # io.IOBase interface.
    def __iter__(IOStream self not None, /):
        self._checkClosed()
        return self

    def __next__(IOStream self not None, /):
        line = self.readline()

        if not line:
            raise StopIteration()

        return line

    def __enter__(IOStream self not None, /):
        self._checkClosed()
        return self

    def __exit__(IOStream self not None, /, *exc):
        self.close()
        return False

    def __getstate__(self):
        raise TypeError(f"cannot pickle {type(self).__name__!r} object")

    def close(IOStream self not None, /):
        # A closed file may be closed again.
        if self.closed:
            return

        # Mimic io.IOBase.close behavior.
        cdef cbool rv
        cdef SDL_IOStream *stream
        try:
            self.flush()
        finally:
            stream = self.take()
            with nogil:
                rv = SDL_CloseIO(stream)

            if not rv:
                raise IOError(f"Could not close: {get_error()}")

    @property
    def closed(IOStream self not None, /):
        return self._closed

    def fileno(IOStream self not None, /):
        raise io.UnsupportedOperation("This stream is not backed by a file descriptor.")

    def flush(IOStream self not None, /):
        self._checkClosed()

        if not self.writable():
            return

        cdef SDL_IOStream *stream = self.borrow()
        with nogil:
            rv = SDL_FlushIO(stream)

        if not rv:
            raise IOError(f"Could not flush: {get_error()}")

    def isatty(IOStream self not None, /):
        self._checkClosed()
        return False

    def readable(IOStream self not None, /):
        self._checkClosed()
        return False

    def readline(IOStream self not None, object size=None, /):
        cdef Py_ssize_t c_size = -1 if size is None else size
        cdef list chunks = []
        cdef bytes c

        while c_size < 0 or len(chunks) < c_size:
            c = self.read(1)

            if not c:
                break

            chunks.append(c)

            if c == b"\n":
                break

        return b"".join(chunks)

    def readlines(IOStream self not None, object hint=None, /):
        cdef Py_ssize_t c_hint = -1 if hint is None else hint
        cdef Py_ssize_t total = 0
        rv = []

        while True:
            line = self.readline()

            if not line:
                break

            rv.append(line)
            total += len(line)

            if c_hint > 0 and total >= c_hint:
                break

        return rv

    def seek(IOStream self not None, Sint64 offset, int whence=io.SEEK_SET, /):
        self._checkClosed()
        self._checkSeekable()

        cdef SDL_IOStream *s = self.borrow()
        cdef SDL_IOWhence w
        cdef Sint64 rv

        if whence == io.SEEK_SET:
            w = SDL_IO_SEEK_SET
        elif whence == io.SEEK_CUR:
            w = SDL_IO_SEEK_CUR
        elif whence == io.SEEK_END:
            w = SDL_IO_SEEK_END
        else:
            raise ValueError(f"Invalid whence: {whence!r}")

        with nogil:
            rv = SDL_SeekIO(s, offset, w)

        if rv < 0:
            raise IOError(f"Could not seek: {get_error()}")

        return rv

    def seekable(IOStream self not None, /):
        self._checkClosed()
        return False

    def tell(IOStream self not None, /):
        self._checkClosed()
        self._checkSeekable()

        cdef SDL_IOStream *s = self.borrow()
        cdef Sint64 rv

        with nogil:
            rv = SDL_TellIO(s)

        if rv < 0:
            raise IOError(f"Could not tell: {get_error()}")

        return rv

    def truncate(IOStream self not None, object size=None, /):
        raise io.UnsupportedOperation("This stream does not support truncate.")

    def writable(IOStream self not None, /):
        self._checkClosed()
        return False

    def writelines(IOStream self not None, object lines, /):
        self._checkClosed()
        self._checkWritable()

        for l in lines:
            self.write(l)

    # io.RawIOBase interface.
    def read(IOStream self not None, Py_ssize_t size=-1, /):
        self._checkClosed()
        self._checkReadable()

        cdef bytearray buf
        cdef object got

        if size < 0:
            return self.readall()

        if size == 0:
            return b""

        buf = bytearray(size)
        got = self.readinto(buf)

        if got is None:
            return None

        cdef Py_ssize_t n = <Py_ssize_t>got

        if n == size:
            return bytes(buf)

        return bytes(memoryview(buf)[:n])

    def readall(IOStream self not None, /):
        self._checkClosed()
        self._checkReadable()

        cdef list chunks = []

        while True:
            chunk = self.read(io.DEFAULT_BUFFER_SIZE)

            if chunk is None:
                return b"".join(chunks) if chunks else None

            if not chunk:
                break

            chunks.append(chunk)

        return b"".join(chunks)

    def readinto(IOStream self not None, object b, /):
        self._checkClosed()
        self._checkReadable()

        cdef SDL_IOStream *s = self.borrow()
        cdef Py_buffer view
        cdef size_t rv
        cdef SDL_IOStatus status

        PyObject_GetBuffer(b, &view, PyBUF_CONTIG)

        try:
            if view.len == 0:
                return 0

            with nogil:
                rv = SDL_ReadIO(s, view.buf, <size_t> view.len)
        finally:
            PyBuffer_Release(&view)

        if rv == 0:
            status = SDL_GetIOStatus(s)

            if status == SDL_IO_STATUS_ERROR:
                raise IOError(f"Could not read: {get_error()}")
            elif status == SDL_IO_STATUS_WRITEONLY:
                raise io.UnsupportedOperation("not readable")
            elif status == SDL_IO_STATUS_NOT_READY:
                return None

        return rv

    def write(IOStream self not None, object b, /):
        self._checkClosed()
        self._checkWritable()

        cdef SDL_IOStream *s = self.borrow()
        cdef Py_buffer view
        cdef size_t rv
        cdef Py_ssize_t length
        cdef SDL_IOStatus status

        PyObject_GetBuffer(b, &view, PyBUF_CONTIG_RO)
        length = view.len

        try:
            if length == 0:
                return 0

            with nogil:
                rv = SDL_WriteIO(s, view.buf, <size_t> length)
        finally:
            PyBuffer_Release(&view)

        if rv == 0 and length:
            status = SDL_GetIOStatus(s)

            if status == SDL_IO_STATUS_READONLY:
                raise io.UnsupportedOperation("not writable")
            elif status == SDL_IO_STATUS_NOT_READY:
                return None

            raise IOError(f"Could not write: {get_error()}")

        return rv


# Make isinstance(x, io.RawIOBase) and io.BufferedReader(x) work. The protocol
# above is implemented by hand, since Cython cannot inherit from _io._RawIOBase.
io.RawIOBase.register(IOStream)


# IOPath - a file on disk.
cdef class IOPath(IOStream):
    """
    An IOStream backed by a file on disk, opened by SDL. All operations are
    GIL-free.

    `path`
        The file to open, as a str or os.PathLike[str].

    `mode`
        A string, "rb" to open file for reading, "wb" to open file for writing.

    `name`
        If given, a string with a file name this stream represents.
    """

    def __init__(IOPath self not None, object path, /, str mode="rb", str name=None):
        cdef bytes path_bytes = os.fsencode(path)
        cdef const char* c_path = path_bytes
        path = os.fsdecode(path)

        if mode not in ("rb", "wb"):
            raise ValueError(f"invalid mode: {mode!r}")
        cdef bytes mode_bytes = mode.encode("utf-8")
        cdef const char* c_mode = mode_bytes

        cdef SDL_IOStream *s
        with nogil:
            s = SDL_IOFromFile(c_path, c_mode)

        if s == NULL:
            raise IOError(f"Could not open {path!r}: {get_error()}")

        self._stream = s
        self.path = path
        self.mode = mode
        self.name = path if name is None else name

    def __repr__(IOPath self not None, /):
        class_name = f"{type(self).__module__}.{type(self).__qualname__}"
        name = "" if self.name is None else f", name={self.name!r}"
        return f"{class_name}({self.path!r}, mode={self.mode!r}{name})"

    def readable(IOPath self not None, /):
        self._checkClosed()
        return self.mode == "rb"

    def writable(IOPath self not None, /):
        self._checkClosed()
        return self.mode == "wb"

    def seekable(IOPath self not None, /):
        self._checkClosed()
        return True


# IOSubFile - a read-only window into a file.
cdef struct SubFileData:
    SDL_IOStream *parent
    Sint64 base
    Sint64 length
    Sint64 pos


cdef Sint64 sub_size(void *userdata) noexcept nogil:
    return (<SubFileData *> userdata).length


cdef Sint64 sub_seek(void *userdata, Sint64 offset, SDL_IOWhence whence) noexcept nogil:
    cdef SubFileData *d = <SubFileData *> userdata
    cdef Sint64 target

    if whence == SDL_IO_SEEK_SET:
        target = offset
    elif whence == SDL_IO_SEEK_CUR:
        target = d.pos + offset
    elif whence == SDL_IO_SEEK_END:
        target = d.length + offset
    else:
        return -1

    if target < 0:
        target = 0
    elif target > d.length:
        target = d.length

    if SDL_SeekIO(d.parent, d.base + target, SDL_IO_SEEK_SET) < 0:
        return -1

    d.pos = target
    return target


cdef size_t sub_read(void *userdata, void *ptr, size_t size, SDL_IOStatus *status) noexcept nogil:
    cdef SubFileData *d = <SubFileData *> userdata
    cdef size_t left = <size_t> (d.length - d.pos)
    cdef size_t rv

    if size > left:
        size = left

    if size == 0:
        status[0] = SDL_IO_STATUS_EOF
        return 0

    rv = SDL_ReadIO(d.parent, ptr, size)

    if rv == 0:
        status[0] = SDL_GetIOStatus(d.parent)
        return 0

    d.pos += rv
    return rv


cdef size_t sub_write(void *userdata, const void *ptr, size_t size, SDL_IOStatus *status) noexcept nogil:
    status[0] = SDL_IO_STATUS_READONLY
    return 0


cdef cbool sub_flush(void *userdata, SDL_IOStatus *status) noexcept nogil:
    return True


cdef cbool sub_close(void *userdata) noexcept nogil:
    cdef SubFileData *d = <SubFileData *> userdata

    if d.parent != NULL:
        SDL_CloseIO(d.parent)

    SDL_free(d)
    return True


cdef SDL_IOStreamInterface sub_interface
sub_interface.version = <Uint32> sizeof(SDL_IOStreamInterface)
sub_interface.size = sub_size
sub_interface.seek = sub_seek
sub_interface.read = sub_read
sub_interface.write = sub_write
sub_interface.flush = sub_flush
sub_interface.close = sub_close


cdef class IOSubFile(IOStream):
    """
    A read-only window into a file on disk, of `length` bytes starting at
    `base`. Used for files stored inside Ren'Py archives and Android assets.

    The window opens and exclusively owns its own handle on the underlying
    file, so distinct IOSubFile objects over the same path are independent and
    each read is a single SDL_ReadIO with no redundant seek.

    `path`
        The file to open, as a str, or os.PathLike[str]. An IOStream may
        also be given, in which case its SDL stream is taken and this
        object assumes exclusive ownership of it.

    `base`
        Non-negative offset into `path` where sub-file starts.

    `length`
        Non-negative length of the sub-file.

    `name`
        If given, a string with a file name this stream represents.
    """

    def __init__(IOSubFile self not None, object path, /, Sint64 base, Sint64 length, str name=None):
        cdef SDL_IOStream *p
        cdef bytes path_bytes
        cdef const char* c_path

        if base < 0:
            raise ValueError(f"base must be non-negative, not {base}")

        if length < 0:
            raise ValueError(f"length must be non-negative, not {length}")

        if isinstance(path, IOStream):
            p = (<IOStream> path).take()
            if name is None:
                name = path.name

            if path.name is None:
                path = "<file-like>"
            else:
                path = path.name

        else:
            path_bytes = os.fsencode(path)
            c_path = path_bytes
            path = os.fsdecode(path)
            with nogil:
                p = SDL_IOFromFile(c_path, b"rb")

            if p == NULL:
                raise IOError(f"Could not open {path!r}: {get_error()}")

        cdef Sint64 rv
        with nogil:
            rv = SDL_SeekIO(p, base, SDL_IO_SEEK_SET)

        if rv < 0:
            SDL_CloseIO(p)
            raise IOError(f"Could not seek to {base} in {path!r}: {get_error()}")

        cdef SubFileData *userdata = <SubFileData *>SDL_malloc(sizeof(SubFileData))
        if userdata == NULL:
            SDL_CloseIO(p)
            raise MemoryError("Could not allocate SubFileData.")

        userdata.parent = p
        userdata.base = base
        userdata.length = length
        userdata.pos = 0
        cdef SDL_IOStream *s = SDL_OpenIO(&sub_interface, userdata)
        if s == NULL:
            SDL_CloseIO(p)
            SDL_free(userdata)
            raise MemoryError(f"Could not create SDL_IOStream: {get_error()}")

        self._stream = s
        self.path = path
        self.base = base
        self.length = length
        self.mode = "rb"
        self.name = name

    def __repr__(IOSubFile self not None, /):
        class_name = f"{type(self).__module__}.{type(self).__qualname__}"
        name = "" if self.name is None else f", name={self.name!r}"
        return f"{class_name}({self.path!r}, base={self.base}, length={self.length}{name})"

    def readable(IOSubFile self not None, /):
        self._checkClosed()
        return True

    def seekable(IOSubFile self not None, /):
        self._checkClosed()
        return True


# IOBuffer - an object supporting the buffer protocol.
cdef struct BufferData:
    Py_buffer view
    Sint64 pos


cdef Sint64 buf_size(void *userdata) noexcept nogil:
    return (<BufferData *> userdata).view.len


cdef Sint64 buf_seek(void *userdata, Sint64 offset, SDL_IOWhence whence) noexcept nogil:
    cdef BufferData *d = <BufferData *> userdata
    cdef Sint64 length = d.view.len
    cdef Sint64 target

    if whence == SDL_IO_SEEK_SET:
        target = offset
    elif whence == SDL_IO_SEEK_CUR:
        target = d.pos + offset
    elif whence == SDL_IO_SEEK_END:
        target = length + offset
    else:
        return -1

    if target < 0:
        target = 0
    elif target > length:
        target = length

    d.pos = target
    return target


cdef size_t buf_read(void *userdata, void *ptr, size_t size, SDL_IOStatus *status) noexcept nogil:
    cdef BufferData *d = <BufferData *> userdata
    cdef size_t available = <size_t> (d.view.len - d.pos)

    if size > available:
        size = available

    if size == 0:
        status[0] = SDL_IO_STATUS_EOF
        return 0

    memcpy(ptr, <char *>d.view.buf + d.pos, size)
    d.pos += size
    return size


cdef size_t buf_write(void *userdata, const void *ptr, size_t size, SDL_IOStatus *status) noexcept nogil:
    cdef BufferData *d = <BufferData *> userdata

    if d.view.readonly:
        status[0] = SDL_IO_STATUS_READONLY
        return 0

    cdef size_t available = <size_t> (d.view.len - d.pos)

    if size > available:
        size = available

    if size == 0:
        status[0] = SDL_IO_STATUS_ERROR
        SDL_SetError("%s", <const char *> b"Buffer is full.")
        return 0

    memcpy(<char *>d.view.buf + d.pos, ptr, size)
    d.pos += size
    return size


cdef cbool buf_flush(void *userdata, SDL_IOStatus *status) noexcept nogil:
    return True


cdef cbool buf_close(void *userdata) noexcept nogil:
    cdef BufferData *d = <BufferData *> userdata

    with gil:
        PyBuffer_Release(&d.view)

    SDL_free(d)
    return True


cdef SDL_IOStreamInterface buf_interface
buf_interface.version = <Uint32> sizeof(SDL_IOStreamInterface)
buf_interface.size = buf_size
buf_interface.seek = buf_seek
buf_interface.read = buf_read
buf_interface.write = buf_write
buf_interface.flush = buf_flush
buf_interface.close = buf_close


cdef class IOBuffer(IOStream):
    """
    An IOStream over any object supporting the buffer protocol. The buffer view
    is held for as long as the underlying SDL_IOStream is open, independent of
    this Python object's lifetime.

    `buffer`
        An object supporting the buffer protocol that provides contiguous memory.
        Set to None when this stream is closed.

    `writable`
        If True, `buffer` must allow requesting writable buffer.

    `name`
        If given, a string with a file name this stream represents.
    """

    def __init__(IOBuffer self not None, object buffer, /, bint writable=False, str name=None):
        if not PyObject_CheckBuffer(buffer):
            raise TypeError(f"{type(buffer).__qualname__} does not support the buffer protocol.")

        cdef Py_buffer view
        cdef int flags = PyBUF_CONTIG if writable else PyBUF_CONTIG_RO
        PyObject_GetBuffer(buffer, &view, flags)

        cdef BufferData *userdata = <BufferData *>SDL_malloc(sizeof(BufferData))
        if userdata == NULL:
            PyBuffer_Release(&view)
            raise MemoryError("Could not allocate BufferData.")

        userdata.view = view
        userdata.pos = 0
        cdef SDL_IOStream *s = SDL_OpenIO(&buf_interface, userdata)
        if s == NULL:
            PyBuffer_Release(&view)
            SDL_free(userdata)
            raise MemoryError(f"Could not create SDL_IOStream: {get_error()}")

        self._stream = s
        self.buffer = buffer
        self.mode = "rb" if view.readonly else "rb+"
        self.name = name

    def __repr__(IOBuffer self not None, /):
        class_name = f"{type(self).__module__}.{type(self).__qualname__}"
        name = "" if self.name is None else f", name={self.name!r}"
        return f"{class_name}({self.buffer!r}, writable={self.writable()}{name})"

    def on_take(IOBuffer self not None, /):
        self.buffer = None

    def readable(IOBuffer self not None, /):
        self._checkClosed()
        return True

    def writable(IOBuffer self not None, /):
        self._checkClosed()
        return self.mode == "rb+"

    def seekable(IOBuffer self not None, /):
        self._checkClosed()
        return True


# IOFileLike - an arbitrary Python file-like object.
cdef struct FileLikeData:
    PyObject *filelike
    bint close_filelike
    bint has_readinto
    bint readable
    bint writable
    bint seekable


cdef Sint64 py_size(void *userdata) noexcept with gil:
    cdef FileLikeData *d = <FileLikeData *>userdata
    cdef object f = <object>d.filelike

    if not d.seekable:
        set_error(f"{f} is not seekable.")
        return -1

    try:
        cur = f.tell()

        try:
            f.seek(0, io.SEEK_END)
            return f.tell()
        finally:
            try:
                f.seek(cur, io.SEEK_SET)
            except Exception:
                pass

    except Exception as e:
        set_error(e)
        return -1


cdef Sint64 py_seek(void *userdata, Sint64 offset, SDL_IOWhence whence) noexcept with gil:
    cdef FileLikeData *d = <FileLikeData *>userdata
    cdef object f = <object>d.filelike
    cdef int w

    if not d.seekable:
        set_error(f"{f} is not seekable.")
        return -1

    try:
        if whence == SDL_IO_SEEK_SET:
            w = io.SEEK_SET
        elif whence == SDL_IO_SEEK_CUR:
            w = io.SEEK_CUR
        elif whence == SDL_IO_SEEK_END:
            w = io.SEEK_END
        else:
            raise ValueError(f"Invalid whence: {whence!r}")

        return <Sint64> f.seek(offset, w)

    except Exception as e:
        set_error(e)
        return -1


cdef size_t py_read(void *userdata, void *ptr, size_t size, SDL_IOStatus *status) noexcept with gil:
    cdef FileLikeData *d = <FileLikeData *>userdata
    cdef object f = <object>d.filelike

    cdef char[:] cv = None
    cdef object mv = None
    cdef Py_buffer view
    cdef Py_ssize_t n

    if size == 0:
        return 0

    if not d.readable:
        status[0] = SDL_IO_STATUS_WRITEONLY
        return 0

    try:
        if d.has_readinto:
            # Zero-copy: let the object fill SDL's buffer directly.
            cv = <char[:<Py_ssize_t> size]><char *> ptr
            mv = memoryview(cv)

            try:
                got = f.readinto(mv)
            finally:
                mv.release()

            if got is None:
                status[0] = SDL_IO_STATUS_NOT_READY
                return 0

            n = <Py_ssize_t> got

            if n < 0 or n > <Py_ssize_t> size:
                raise ValueError(f"readinto() reported {n} bytes for a {size}-byte buffer.")

        else:
            data = f.read(size)

            if data is None:
                status[0] = SDL_IO_STATUS_NOT_READY
                return 0

            PyObject_GetBuffer(data, &view, PyBUF_CONTIG_RO)
            try:
                n = view.len
                if n > <Py_ssize_t> size:
                    raise ValueError(f"read({size}) returned {n} bytes.")

                if n:
                    memcpy(ptr, <char *>view.buf, n)

            finally:
                PyBuffer_Release(&view)

        if n == 0:
            status[0] = SDL_IO_STATUS_EOF

        return <size_t> n

    except Exception as e:
        status[0] = SDL_IO_STATUS_ERROR
        set_error(e)
        return 0


cdef size_t py_write(void *userdata, const void *ptr, size_t size, SDL_IOStatus *status) noexcept with gil:
    cdef FileLikeData *d = <FileLikeData *>userdata
    cdef object f = <object>d.filelike

    cdef const char[:] cv = None
    cdef object mv = None
    cdef object got
    cdef Py_ssize_t n

    if size == 0:
        return 0

    if not d.writable:
        status[0] = SDL_IO_STATUS_READONLY
        return 0

    try:
        cv = <char[:<Py_ssize_t> size]><char *> ptr
        mv = memoryview(cv)

        try:
            got = f.write(mv)
        finally:
            mv.release()

        if got is None:
            status[0] = SDL_IO_STATUS_NOT_READY
            return 0

        n = <Py_ssize_t> got
        if n < 0 or n > <Py_ssize_t> size:
            raise ValueError(f"write() reported {n} bytes for a {size}-byte buffer.")

        if n == 0:
            raise ValueError(f"write() accepted 0 of {size} bytes without returning None.")

        return <size_t> n

    except Exception as e:
        status[0] = SDL_IO_STATUS_ERROR
        set_error(e)
        return 0


cdef cbool py_flush(void *userdata, SDL_IOStatus *status) noexcept with gil:
    cdef FileLikeData *d = <FileLikeData *>userdata
    cdef object f = <object>d.filelike

    try:
        flush = getattr(f, "flush", None)
        if flush is not None:
            flush()

        return True

    except Exception as e:
        status[0] = SDL_IO_STATUS_ERROR
        set_error(e)
        return False


cdef cbool py_close(void *userdata) noexcept with gil:
    cdef FileLikeData *d = <FileLikeData *>userdata
    cdef object f = <object>d.filelike

    try:
        if d.close_filelike:
            f.close()
    except BaseException:
        PyErr_WriteUnraisable(f)

    Py_DECREF(f)
    SDL_free(d)
    return True


cdef SDL_IOStreamInterface py_interface
py_interface.version = <Uint32> sizeof(SDL_IOStreamInterface)
py_interface.size = py_size
py_interface.seek = py_seek
py_interface.read = py_read
py_interface.write = py_write
py_interface.flush = py_flush
py_interface.close = py_close


cdef class IOFileLike(IOStream):
    """
    An IOStream wrapping an arbitrary Python file-like object. Every operation
    reacquires the GIL, prefer IOPath, IOSubFile, or IOBuffer when the data is
    available another way.

    If the wrapped object implements readinto(), reads are zero-copy.

    `filelike`
        A Python file-like object.

    `close`
        If true, closing this object also closes the wrapped object.

    `name`
        If given, a string with a file name this stream represents.
    """

    def __init__(IOFileLike self not None, object filelike, /, bint close=False, str name=None):
        try:
            readable = bool(filelike.readable())
        except AttributeError:
            readable = hasattr(filelike, "read")

        try:
            writable = bool(filelike.writable())
        except AttributeError:
            writable = hasattr(filelike, "write")

        try:
            seekable = bool(filelike.seekable())
        except AttributeError:
            seekable = hasattr(filelike, "seek")

        if not (readable or writable):
            raise TypeError(f"{filelike!r} is not a file-like object.")

        if name is None:
            filelike_name = getattr(filelike, "name", None)
            if isinstance(filelike_name, bytes):
                filelike_name = os.fsdecode(filelike_name)
            elif filelike_name is not None:
                filelike_name = str(filelike_name)
            name = filelike_name

        has_readinto = hasattr(filelike, "readinto")

        cdef FileLikeData *userdata = <FileLikeData *>SDL_malloc(sizeof(FileLikeData))
        if userdata == NULL:
            raise MemoryError("Could not allocate FileLikeData.")

        Py_INCREF(filelike)
        userdata.filelike = <PyObject *> filelike
        userdata.close_filelike = close
        userdata.has_readinto = has_readinto
        userdata.readable = readable
        userdata.writable = writable
        userdata.seekable = seekable

        cdef SDL_IOStream *s = SDL_OpenIO(&py_interface, userdata)
        if s == NULL:
            Py_DECREF(filelike)
            SDL_free(userdata)
            raise MemoryError(f"Could not create SDL_IOStream: {get_error()}")

        self._stream = s
        self._readable = readable
        self._writable = writable
        self._seekable = seekable
        self._close_filelike = close
        self.filelike = filelike
        if readable and writable:
            self.mode = "rb+"
        elif readable:
            self.mode = "rb"
        else:
            self.mode = "wb"
        self.name = name

    def __repr__(IOFileLike self not None, /):
        class_name = f"{type(self).__module__}.{type(self).__qualname__}"
        name = "" if self.name is None else f", name={self.name!r}"
        return f"{class_name}({self.filelike!r}, close={self._close_filelike}{name})"

    def readable(IOFileLike self not None, /):
        self._checkClosed()
        return self._readable

    def writable(IOFileLike self not None, /):
        self._checkClosed()
        return self._writable

    def seekable(IOFileLike self not None, /):
        self._checkClosed()
        return self._seekable

    # Reimplement some function to not drop and reacquire GIL for no reason.
    def seek(IOFileLike self not None, Sint64 offset, int whence=io.SEEK_SET, /):
        self._checkClosed()
        self._checkSeekable()

        return self.filelike.seek(offset, whence)

    def flush(IOFileLike self not None, /):
        self._checkClosed()

        if not self.writable():
            return

        flush = getattr(self.filelike, "flush", None)
        if flush is not None:
            flush()

    def read(IOFileLike self not None, Py_ssize_t size=-1, /):
        self._checkClosed()
        self._checkReadable()

        if size < 0:
            return self.readall()

        return self.filelike.read(size)

    def readinto(IOFileLike self not None, object b, /):
        self._checkClosed()
        self._checkReadable()

        return self.filelike.readinto(b)

    def write(IOFileLike self not None, object b, /):
        self._checkClosed()
        self._checkWritable()

        return self.filelike.write(b)


cpdef IOStream open_io(object obj, str mode="rb", str name=None):
    """
    Coerces `obj` into an IOStream open in `mode`. This accepts, in order:

    * An object with a `raw` field, which is unwrapped.

    * An io.FileIO which is closed and its filename is used to open IOPath.

    * An IOStream object, which is returned unchanged.

    * A str or path-like filename, which is opened.

    * An object that supports the buffer protocol.

    * A file-like object.
    """

    if mode not in ("rb", "wb"):
        raise ValueError(f"invalid mode: {mode!r}")

    # Unwrap all buffered wrappers.
    while hasattr(obj, "raw"):
        obj = obj.raw

    if isinstance(obj, io.FileIO):
        obj.close()
        obj = obj.name

    cdef IOStream stream
    if isinstance(obj, IOStream):
        stream = <IOStream> obj
    elif isinstance(obj, (str, os.PathLike)):
        stream = IOPath(obj, mode, name=name)
    elif PyObject_CheckBuffer(obj):
        stream = IOBuffer(obj, mode == "wb", name=name)
    else:
        # Let IOFileLike handle general file-like.
        stream = IOFileLike(obj, name=name)

    # After it successfully opened, check the mode.
    if mode == "wb":
        stream._checkWritable()
    else:
        stream._checkReadable()

    return stream
