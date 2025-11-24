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

import cython
import math
from sdl2 cimport *
import renpy.pygame
from renpy.pygame.error import error
from renpy.pygame import register_init, register_quit

cdef int timer_id = 0

@register_init
def init():
    renpy.pygame.display.sdl_main_init()

    if SDL_InitSubSystem(SDL_INIT_TIMER):
        raise error()

@register_quit
def quit(): # @ReservedAssignment
    SDL_QuitSubSystem(SDL_INIT_TIMER)

def get_ticks():
    return SDL_GetTicks()

def wait(int milliseconds):
    cdef int start

    start = SDL_GetTicks()
    with nogil:
        SDL_Delay(milliseconds)
    return SDL_GetTicks() - start

def delay(milliseconds):
    # SDL_Delay() should be accurate enough.
    return wait(milliseconds)

cdef Uint32 timer_callback(Uint32 interval, void *param) nogil:
    cdef SDL_Event e
    e.type = <int>param
    e.user.code = 0
    e.user.data1 = NULL
    e.user.data2 = NULL
    SDL_PushEvent(&e)
    return interval

# A map from eventid to SDL_Timer_ID.
cdef dict timer_by_event = { }

def set_timer(eventid, milliseconds):

    cdef int timer_id = timer_by_event.get(eventid, 0)

    if timer_id != 0:
        SDL_RemoveTimer(timer_id)
        timer_id = 0

    if milliseconds > 0:
        timer_id = SDL_AddTimer(milliseconds, <SDL_TimerCallback>timer_callback, <void*><int>eventid)
        if timer_id == 0:
            raise error()

    timer_by_event[eventid] = timer_id

class Clock:
    def __init__(self):
        self.last = SDL_GetTicks()
        self.last_frames = []
        self.frametime = 0
        self.raw_frametime = 0

    def tick(self, framerate=0):
        cdef int now = SDL_GetTicks()
        self.raw_frametime = now - self.last
        while len(self.last_frames) > 9:
            self.last_frames.pop(0)
        if framerate == 0:
            self.last = now
            self.last_frames.append(self.raw_frametime)
            return self.raw_frametime
        cdef int frame_duration = 1.0 / framerate * 1000
        if self.raw_frametime < frame_duration:
            delay(frame_duration - self.raw_frametime)
        now = SDL_GetTicks()
        self.frametime = now - self.last
        self.last = now
        self.last_frames.append(self.frametime)
        return self.frametime

    def tick_busy_loop(self, framerate=0):
        return self.tick(framerate)

    def get_time(self):
        return self.frametime

    def get_rawtime(self):
        return self.raw_frametime

    @cython.cdivision(True)
    def get_fps(self):
        cdef int total_time = sum(self.last_frames)
        cdef float average_time = total_time / 1000.0 / len(self.last_frames)
        cdef float average_fps = 1.0 / average_time
        return 0 if math.isnan(average_fps) else average_fps
