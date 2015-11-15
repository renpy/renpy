# -*- python -*-
# Copyright 2004-2015 Tom Rothamel <pytom@bishoujo.us>

# Permission is hereby granted, free of charge, to any person
# obtaining a copy of this software and associated documentation files
# (the "Software"), to deal in the Software without restriction,
# including without limitation the rights to use, copy, modify, merge,
# publish, distribute, sublicense, and/or sell copies of the Software,
# and to permit persons to whom the Software is furnished to do so,
# subject to the following conditions:

# The above copyright notice and this permission notice shall be
# included in all copies or substantial portions of the Software.

# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND,
# EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF
# MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND
# NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE
# LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION
# OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION
# WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.

from pygame_sdl2 cimport *
import_pygame_sdl2()

cdef extern from "pss.h":

    void PSS_play(int channel, SDL_RWops *rw, char *ext, object name, int fadein, int tight, int paused)
    void PSS_queue(int channel, SDL_RWops *rw, char *ext, object name, int fadein, int tight)
    void PSS_stop(int channel)
    void PSS_dequeue(int channel, int even_tight)
    int PSS_queue_depth(int channel)
    object PSS_playing_name(int channel)
    void PSS_fadeout(int channel, int ms)
    void PSS_pause(int channel, int pause)
    void PSS_unpause_all()
    int PSS_get_pos(int channel)
    void PSS_set_endevent(int channel, int event)
    void PSS_set_volume(int channel, float volume)
    float PSS_get_volume(int channel)
    void PSS_set_pan(int channel, float pan, float delay)
    void PSS_set_secondary_volume(int channel, float vol2, float delay)
    void PSS_init(int freq, int stereo, int samples, int status)
    void PSS_quit()

    void PSS_periodic()
    void PSS_alloc_event(object)
    int PSS_refresh_event()

    char *PSS_get_error()

    int ffpy_needs_alloc
    int ffpy_movie_width
    int ffpy_movie_height

def check_error():
    e = PSS_get_error();

    if str(e):
        raise Exception(e)

def play(channel, file, name, paused=False, fadein=0, tight=False):
    cdef SDL_RWops *rw

    rw = RWopsFromPython(file)

    if rw == NULL:
        raise Exception("Could not create RWops.")

    if paused:
        pause = 1
    else:
        pause = 0

    if tight:
        tight = 1
    else:
        tight = 0

    extension = name.encode("utf-8")
    PSS_play(channel, rw, extension, name, fadein, tight, pause)
    check_error()

def queue(channel, file, name, fadein=0, tight=False):
    cdef SDL_RWops *rw

    rw = RWopsFromPython(file)

    if rw == NULL:
        raise Exception("Could not create RWops.")

    if tight:
        tight = 1
    else:
        tight = 0

    extension = name.encode("utf-8")
    PSS_queue(channel, rw, extension, name, fadein, tight)
    check_error()

def stop(channel):
    PSS_stop(channel)
    check_error()

def dequeue(channel, even_tight=False):
    PSS_dequeue(channel, even_tight)

def queue_depth(channel):
    return PSS_queue_depth(channel)

def playing_name(channel):
    return PSS_playing_name(channel)

def pause(channel):
    PSS_pause(channel, 1)
    check_error()

def unpause(channel):
    PSS_pause(channel, 0)
    check_error()

def unpause_all():
    PSS_unpause_all()

def fadeout(channel, ms):
    PSS_fadeout(channel, ms)
    check_error()

def busy(channel):
    return PSS_get_pos(channel) != -1

def get_pos(channel):
    return PSS_get_pos(channel)

def set_volume(channel, volume):
    if volume == 0:
        PSS_set_volume(channel, 0)
    else:
        PSS_set_volume(channel, volume ** 2)

    check_error()

def set_pan(channel, pan, delay):
    PSS_set_pan(channel, pan, delay)
    check_error()

def set_secondary_volume(channel, volume, delay):
    PSS_set_secondary_volume(channel, volume, delay)
    check_error()

def set_end_event(channel, event):
    PSS_set_endevent(channel, event)
    check_error()

def get_volume(channel):
    return PSS_get_volume(channel)

def init(freq, stereo, samples, status=False):
    if status:
        status = 1
    else:
        status = 0

    PSS_init(freq, stereo, samples, status)
    check_error()

def quit(): # @ReservedAssignment
    PSS_quit()

def periodic():
    PSS_periodic()

def alloc_event(surf):
    PSS_alloc_event(surf)

def refresh_event():
    return PSS_refresh_event()

def needs_alloc():
    return ffpy_needs_alloc

def movie_size():
    return ffpy_movie_width, ffpy_movie_height

def check_version(version):
    if version < 2 or version > 4:
        raise Exception("pysdlsound version mismatch.")
