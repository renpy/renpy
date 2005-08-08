cdef extern from "pss.h":

    cdef struct SDL_RWops:
        int (* close)(SDL_RWops *)

    SDL_RWops* RWopsFromPython(object obj)

    cdef int SDL_GetTicks()

cdef extern from "native_midi.h":

    cdef struct _NativeMidiSong:
        pass

    ctypedef _NativeMidiSong NativeMidiSong

    int native_midi_detect()
    NativeMidiSong *native_midi_loadsong(char *midifile)
    NativeMidiSong *native_midi_loadsong_RW(SDL_RWops *rw)
    void native_midi_freesong(NativeMidiSong *song)
    void native_midi_start(NativeMidiSong *song)
    void native_midi_stop()
    int native_midi_active()
    void native_midi_setvolume(int volume)
    char *native_midi_error()

cdef NativeMidiSong *current
cdef int start

current = NULL

def init():
    if not native_midi_detect():
        raise Exception("Could not initialize native midi support.")

def play(file):
    cdef SDL_RWops *rw

    if current:
        stop()

    rw = RWopsFromPython(file)

    if rw == NULL:
        raise Exception, "Could not create RWops."

    global current
    current = native_midi_loadsong_RW(rw)

    rw.close(rw)

    if current == NULL:
        raise Exception, "Could not load midi file."
    
    global start
    start = SDL_GetTicks()
    native_midi_start(current)

    
def stop():

    global current

    if not current:
        return

    native_midi_stop()
    native_midi_freesong(current)
    current = NULL

def busy():
    return native_midi_active()

def get_pos():

    if not busy():
        return -1

    return SDL_GetTicks() - start

def set_volume(volume):
    native_midi_setvolume(int(volume * 128))
        
