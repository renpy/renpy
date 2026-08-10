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

from cpython.buffer cimport PyObject_CheckBuffer

from .sdl cimport SDL_IOStream, Sint64


cdef class IOStream:
    cdef SDL_IOStream *_stream
    cdef bint _closed
    cdef readonly str mode
    cdef readonly str name

    cdef SDL_IOStream *borrow(self) except NULL
    cdef SDL_IOStream *take(self) except NULL


cdef class IOPath(IOStream):
    cdef readonly object path


cdef class IOSubFile(IOStream):
    cdef readonly object path
    cdef readonly Sint64 base
    cdef readonly Sint64 length


cdef class IOBuffer(IOStream):
    cdef readonly object buffer


cdef class IOFileLike(IOStream):
    cdef bint _readable
    cdef bint _writable
    cdef bint _seekable
    cdef bint _close_filelike
    cdef readonly object filelike


cdef inline SDL_IOStream *SDL_IOStreamFromPython(object obj, str name=None) except NULL:
    """
    This accepts, in order:

    * An IOStream object, which is closed and the underlying SDL_IOStream
      object is returned.

    * A str or path-like filename, which is opened.

    * An object with a name field. The name is interpreted as a filename.
      and opened. The object will be closed.

    * An object that supports the buffer protocol.

    * A file-like object.

    It returns an SDL_IOStream object, or NULL on error.

    Calling this function transfers exclusive ownership of `obj` to the returned
    stream, including responsibility for closing it.
    """

    import os
    
    while hasattr(obj, "raw"):
        obj = obj.raw

    cdef IOStream stream
    if isinstance(obj, IOStream):
        stream = <IOStream> obj
    elif isinstance(obj, (str, os.PathLike)):
        stream = IOPath(obj, name=name)
    elif isinstance(obj_path := getattr(obj, "name", None), (str, os.PathLike)):
        stream = IOPath(obj_path, name=name)
    elif PyObject_CheckBuffer(obj):
        stream = IOBuffer(obj, name=name)
    elif hasattr(obj, "read") or hasattr(obj, "write"):
        stream = IOFileLike(obj, name=name)
    else:
        raise TypeError(f"{obj!r} is not a filename or file-like object.")

    return stream.take()
