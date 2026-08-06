# Copyright 2014-2026 Tom Rothamel <pytom@bishoujo.us>
# Copyright 2014 Patrick Dawson <pat@dw.is>
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

from .error import error

from libc.string cimport memcpy

try:
    import emscripten
except ImportError:
    emscripten = None

################################################################################
# MIME-type clipboard data
################################################################################

cdef struct ClipboardData:
    # Array of null-terminated MIME type strings, one per entry.
    char **mime_types

    # Array of data buffers, one per entry.
    char **data_ptrs

    # Array of data buffer sizes, one per entry.
    size_t *data_sizes

    # Number of entries in the arrays.
    size_t count


cdef const void *_clipboard_data_callback(void *userdata, const char *mime_type, size_t *size) noexcept nogil:
    cdef ClipboardData *cd = <ClipboardData *> userdata
    cdef size_t i

    for i in range(cd.count):
        if SDL_strcmp(cd.mime_types[i], mime_type) == 0:
            size[0] = cd.data_sizes[i]
            return <const void *> cd.data_ptrs[i]

    size[0] = 0
    return NULL


cdef void _clipboard_cleanup(void *userdata) noexcept nogil:
    cdef ClipboardData *cd = <ClipboardData *> userdata
    cdef size_t i

    if cd == NULL:
        return

    if cd.mime_types != NULL:
        for i in range(cd.count):
            if cd.mime_types[i] != NULL:
                SDL_free(cd.mime_types[i])

        SDL_free(cd.mime_types)

    if cd.data_ptrs != NULL:
        for i in range(cd.count):
            if cd.data_ptrs[i] != NULL:
                SDL_free(cd.data_ptrs[i])

        SDL_free(cd.data_ptrs)

    if cd.data_sizes != NULL:
        SDL_free(cd.data_sizes)

    SDL_free(cd)


def init():
    pass


def quit():
    SDL_ClearClipboardData()


SCRAP_TEXT = "text/plain"

def get(type):
    cdef char *text = NULL
    if type == SCRAP_TEXT:
        text = SDL_GetClipboardText()
        if text == NULL:
            raise error()
        rv = bytes(text)
        SDL_free(text)
        return rv
    else:
        raise error("Not implemented.")


def get_data(mime_type):
    """
    Returns the clipboard data for the given MIME type as bytes.
    """
    cdef size_t size = 0
    cdef void *data = SDL_GetClipboardData(mime_type.encode("utf-8"), &size)

    if data == NULL:
        raise error()

    rv = bytes((<char *>data)[:size])
    SDL_free(data)

    return rv


def get_types():
    return [SCRAP_TEXT]


def get_mime_types():
    """
    Returns the list of MIME types currently available in the clipboard.
    """
    cdef size_t num_mime_types = 0
    cdef char **mime_types = SDL_GetClipboardMimeTypes(&num_mime_types)

    if mime_types == NULL:
        return []

    rv = []

    cdef size_t i
    for i in range(num_mime_types):
        if mime_types[i] != NULL:
            rv.append(bytes(mime_types[i]).decode("utf-8"))

    SDL_free(mime_types)

    return rv


def put(type, data):
    if type != SCRAP_TEXT:
        raise error("Not implemented.")

    if emscripten is not None:
        # SDL_SetClipboardText() is not implemented for Web
        import re
        text = data.decode('utf-8')
        script = 'navigator.clipboard.writeText(`%s`)' % (re.sub(r'([\\`$])', r'\\\1', text),)
        emscripten.run_script(script)
        return

    data = bytes(data)

    if not SDL_SetClipboardText(data):
        raise error()

    SDL_SetPrimarySelectionText(data)


def put_data(data_dict):
    """
    :doc: clipboard
    :name: renpy.pygame.scrap.put_data
    :args: (data_dict)

    Sets up clipboard data for multiple MIME types.

    `data_dict`
        A dictionary mapping MIME type strings or bytes to data strings
        or bytes. String values are encoded as UTF-8.
    """
    cdef size_t count = len(data_dict)
    cdef ClipboardData *cd
    cdef char **mime_types_array
    cdef size_t i
    cdef bytes mime_bytes
    cdef bytes data_bytes
    cdef char *mime_str
    cdef char *data_ptr
    cdef size_t data_len
    cdef size_t mime_len
    cdef bytes plain_text = None

    if count == 0:
        SDL_ClearClipboardData()
        return

    cd = <ClipboardData *> SDL_malloc(sizeof(ClipboardData))
    if cd == NULL:
        raise error("Out of memory.")

    cd.mime_types = <char **> SDL_malloc(count * sizeof(char *))
    cd.data_ptrs = <char **> SDL_malloc(count * sizeof(char *))
    cd.data_sizes = <size_t *> SDL_malloc(count * sizeof(size_t))
    cd.count = count

    if cd.mime_types == NULL or cd.data_ptrs == NULL or cd.data_sizes == NULL:
        _clipboard_cleanup(<void *> cd)
        raise error("Out of memory.")

    mime_types_array = <char **> SDL_malloc(count * sizeof(char *))
    if mime_types_array == NULL:
        _clipboard_cleanup(<void *> cd)
        raise error("Out of memory.")

    i = 0
    for mime, data in data_dict.items():
        mime_bytes = mime.encode("utf-8") if isinstance(mime, str) else bytes(mime)
        data_bytes = data.encode("utf-8") if isinstance(data, str) else bytes(data)

        mime_len = len(mime_bytes)
        data_len = len(data_bytes)

        cd.mime_types[i] = <char *> SDL_malloc(mime_len + 1)
        cd.data_ptrs[i] = <char *> SDL_malloc(data_len)
        cd.data_sizes[i] = data_len

        if cd.mime_types[i] == NULL or cd.data_ptrs[i] == NULL:
            _clipboard_cleanup(<void *> cd)
            SDL_free(mime_types_array)
            raise error("Out of memory.")

        mime_str = cd.mime_types[i]
        memcpy(mime_str, <const char *> mime_bytes, mime_len)
        mime_str[mime_len] = 0

        data_ptr = cd.data_ptrs[i]
        memcpy(data_ptr, <const char *> data_bytes, data_len)

        mime_types_array[i] = mime_str

        if mime_bytes == b"text/plain":
            plain_text = data_bytes

        i += 1

    if not SDL_SetClipboardData(_clipboard_data_callback, _clipboard_cleanup, <void *> cd, <const char **> mime_types_array, count):
        SDL_free(mime_types_array)
        _clipboard_cleanup(<void *> cd)
        raise error()

    SDL_free(mime_types_array)

    if plain_text is not None:
        SDL_SetPrimarySelectionText(plain_text)


def contains(type):
    if type != SCRAP_TEXT:
        return False

    return SDL_HasClipboardText()


def lost():
    return False


def set_mode(mode):
    pass
