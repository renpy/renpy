# Copyright 2017 Tom Rothamel <tom@rothamel.us>
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

powerstate_to_name = {
    SDL_POWERSTATE_UNKNOWN : "POWERSTATE_UNKNOWN",
    SDL_POWERSTATE_ON_BATTERY : "POWERSTATE_ON_BATTERY",
    SDL_POWERSTATE_NO_BATTERY : "POWERSTATE_NO_BATTERY",
    SDL_POWERSTATE_CHARGING : "POWERSTATE_CHARGING",
    SDL_POWERSTATE_CHARGED : "POWERSTATE_CHARGED",
}


class PowerInfo(object):
    def __init__(self):
        self.state = SDL_POWERSTATE_UNKNOWN
        self.seconds = -1
        self.percent = -1

    def __repr__(self):
        return "<PowerInfo state={} seconds={} percent={}>".format(
            powerstate_to_name.get(self.state, "INVALID"),
            self.seconds,
            self.percent)

def get_power_info():

    cdef int seconds
    cdef int percent

    state = SDL_GetPowerInfo(&seconds, &percent)

    rv = PowerInfo()
    rv.state = state
    rv.seconds = seconds
    rv.percent = percent

    return rv
