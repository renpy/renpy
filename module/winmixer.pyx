# Copyright 2005 PyTom <pytom@bishoujo.us>

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

cdef extern from "windows.h":
    pass

cdef extern from "mmsystem.h":

    unsigned int waveOutGetNumDevs()
    unsigned int waveOutGetVolume(int dev, unsigned int *volume)
    unsigned int waveOutSetVolume(int dev, unsigned int volume)

    unsigned int midiOutGetNumDevs()
    unsigned int midiOutGetVolume(int dev, unsigned int *volume)
    unsigned int midiOutSetVolume(int dev, unsigned int volume)
    # Setting volume done through hMidiStream.

cdef unsigned int vol_to_uint(vol):
    cdef unsigned int v
    v = int(0xffff * vol)
    return v + (v << 16)

cdef uint_to_vol(unsigned int u):
    cdef unsigned int v1
    cdef unsigned int v2

    v1 = u & 0xffff
    v2 = u >> 16
    
    return (v1 + v2) / 2.0 / 0xffff

midi_dev = None
wave_dev = None

def init():

    global midi_dev
    global wave_dev

    cdef unsigned int volume

    for i in range(0, waveOutGetNumDevs()):
        if not waveOutGetVolume(i, &volume):
            wave_dev = i
            break

    for i in range(0, midiOutGetNumDevs()):
        if not midiOutGetVolume(i, &volume):
            midi_dev = i
            break
        
    return

init()
    
def get_wave():
    global wave_dev
    cdef unsigned int volume

    if wave_dev is None:
        return None

    waveOutGetVolume(wave_dev, &volume)
    return uint_to_vol(volume)

def set_wave(vol):
    global wave_dev

    if wave_dev is None:
        return

    waveOutSetVolume(wave_dev, vol_to_uint(vol))

def get_midi():
    global midi_dev
    cdef unsigned int volume

    if midi_dev is None:
        return None

    midiOutGetVolume(midi_dev, &volume)
    return uint_to_vol(volume)

def set_midi(vol):
    global midi_dev

    if midi_dev is None:
        return

    midiOutSetVolume(midi_dev, vol_to_uint(vol))

