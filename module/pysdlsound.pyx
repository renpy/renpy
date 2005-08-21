cdef extern from "pss.h":

    cdef struct SDL_RWops:
        pass

    SDL_RWops* RWopsFromPythonThreaded(object obj)
    void PSS_play(int channel, SDL_RWops *rw, char *ext, object name, int paused)
    void PSS_queue(int channel, SDL_RWops *rw, char *ext, object name)
    void PSS_stop(int channel)
    void PSS_dequeue(int channel)
    int PSS_queue_depth(int channel)
    object PSS_playing_name(int channel)
    void PSS_fadeout(int channel, int ms)
    void PSS_pause(int channel, int pause)
    void PSS_unpause_all()
    int PSS_get_pos(int channel)
    void PSS_set_endevent(int channel, int event)
    void PSS_set_volume(int channel, float volume)
    float PSS_get_volume(int channel)
    void PSS_init(int freq, int stereo, int samples)
    void PSS_quit()
    char *PSS_get_error()

def _extension(s):
    i = s.rfind('.')
    if i == -1:
        return s
    return s[i+1:]
    
def check_error():
    e = PSS_get_error();
    if e:
        raise Exception, e

def play(channel, file, name, paused=False):
    cdef SDL_RWops *rw

    rw = RWopsFromPythonThreaded(file)

    if rw == NULL:
        raise Exception, "Could not create RWops."

    if paused:
        pause = 1
    else:
        pause = 0

    ext = _extension(name)

    PSS_play(channel, rw, ext, name, pause)
    check_error()

def queue(channel, file, name):
    cdef SDL_RWops *rw

    rw = RWopsFromPythonThreaded(file)

    ext = _extension(name)

    PSS_queue(channel, rw, ext, name)
    check_error()

def stop(channel):
    PSS_stop(channel)
    check_error()

def dequeue(channel):
    PSS_dequeue(channel)

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
    PSS_set_volume(channel, 10 ** volume / 10 )
    check_error()

def set_end_event(channel, event):
    PSS_set_endevent(channel, event)
    check_error()

def get_volume(channel):
    return PSS_get_volume(channel)

def init(freq, stereo, samples):
    PSS_init(freq, stereo, samples)
    check_error()

def quit():
    PSS_quit()

    
