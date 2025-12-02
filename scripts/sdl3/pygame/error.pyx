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

from pygame.sdl cimport *

class error(RuntimeError):

    def __init__(self, message=None):
        if message is None:
            message = bytes(SDL_GetError())
            message = message.decode("utf-8")

        RuntimeError.__init__(self, message)

def get_error():
    cdef const char *message = SDL_GetError()

    if message:
        return message.decode("utf-8")
    else:
        return ''

def set_error(message):
    if isinstance(message, unicode):
        message = message.encode("utf-8")

    SDL_SetError("%s", <char *> message)
