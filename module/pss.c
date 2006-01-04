/*
Copyright 2005 PyTom <pytom@bishoujo.us>

Permission is hereby granted, free of charge, to any person
obtaining a copy of this software and associated documentation files
(the "Software"), to deal in the Software without restriction,
including without limitation the rights to use, copy, modify, merge,
publish, distribute, sublicense, and/or sell copies of the Software,
and to permit persons to whom the Software is furnished to do so,
subject to the following conditions:

The above copyright notice and this permission notice shall be
included in all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND,
EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF
MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND
NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE
LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION
OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION
WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
*/

#include "pss.h"
#include <Python.h>
#include <SDL/SDL.h>
#include <SDL/SDL_sound.h>
#include <stdio.h>

/* The current Python. */
PyInterpreterState* interp;
PyThreadState* thread = NULL;

static void incref(PyObject *ref) {
    PyThreadState *oldstate;

    PyEval_AcquireLock();
    oldstate = PyThreadState_Swap(thread);
    Py_INCREF(ref);    
    PyThreadState_Swap(oldstate);
    PyEval_ReleaseLock();
}

static void decref(PyObject *ref) {
    PyThreadState *oldstate;

    PyEval_AcquireLock();
    oldstate = PyThreadState_Swap(thread);
    Py_DECREF(ref);    
    PyThreadState_Swap(oldstate);
    PyEval_ReleaseLock();
}

/* Locking on entry from python... */
#define BEGIN() PyThreadState *_save;
#define ENTER() { _save = PyEval_SaveThread(); SDL_LockAudio(); }
#define EXIT() { SDL_UnlockAudio(); PyEval_RestoreThread(_save); }

/* Min and Max */
#define min(a, b) (((a) < (b)) ? (a) : (b))
#define max(a, b) (((a) > (b)) ? (a) : (b))

/* The number of channels we support. */
#define NUM_CHANNELS 8

/* Various error codes. */
#define SUCCESS 0
#define SDL_ERROR -1
#define SOUND_ERROR -2
#define PSS_ERROR -3

/* This is called with the appropriate error code at the end of a
 * function. */
#define error(err) PSS_error = err
int PSS_error = SUCCESS;
static const char *error_msg = NULL;

/* Have we been initialized? */
static int initialized = 0;

/*
 * This structure represents a channel the system knows about
 * and can play from.
 */
struct Channel {

    /* The currently playing sample, NULL if this sample isn't playing
       anything. */
    Sound_Sample *playing;

    /* The name of the playing music. */
    PyObject *playing_name;

    /* The number of ms to take to fade in the playing sample. */
    int playing_fadein;
    
    /* The queued up sample. */
    Sound_Sample *queued;    

    /* The name of the queued up sample. */
    PyObject *queued_name;

    /* The number of ms to take to fade in the queued sample. */
    int queued_fadein;
    
    /* Is this channel paused? */
    int paused;
    
    /* The volume of the channel. */
    int volume;

    /* The number of decoded bytes in the buffer. */
    int decoded;

    /* The offset into the buffer that we last stopped at. */
    int last;

    /* The position (in bytes) that this channel has queued to. */
    int pos;

    /* 
     * The number of bytes for each step of fade.
     * 0 when no fade is in progress.
     */
    int fade_step_len;

    /* How many bytes we are into the current fade step. */
    int fade_off;

    /* The current fade volume. */
    int fade_vol;

    /* The change in fade_vol for each step. */
    int fade_delta;

    /* The number of bytes in which we'll stop. */
    int stop_bytes;

    /* The event posted to the queue when we finish a track. */
    int event;

};

/*
 * All of the channels that the system knows about.
 */
struct Channel channels[NUM_CHANNELS];

/*
 * The spec of the audio that is playing.
 */
SDL_AudioSpec audio_spec;


static int ms_to_bytes(int ms) {
    return ms * audio_spec.freq * audio_spec.channels * 2 / 1000;
}

static int bytes_to_ms(int bytes) {
    return ((long long) bytes) * 1000 / (audio_spec.freq * audio_spec.channels * 2);
}

static void start_sample(struct Channel* c) {
    int fade_steps;


    if (!c) return;

    c->decoded = 0;
    c->last = 0;
    c->pos = 0;
    c->stop_bytes = -1;

    if (c->playing_fadein == 0) {
        c->fade_step_len = 0;
    } else {
        fade_steps = c->volume;
        c->fade_delta = 1;
        c->fade_off = 0;
        c->fade_vol = 0;
        
        c->fade_step_len = ms_to_bytes(c->playing_fadein) / fade_steps;
        c->fade_step_len &= ~0x7; // Even sample.
    }
}


static void update_pause(void) {
    int i;
    int pause = 1;
    
    for (i = 0; i < NUM_CHANNELS; i++) {
        if (channels[i].playing) {
            pause = 0;
            break;
        }
    }

    SDL_PauseAudio(pause);
}

static void free_sample(Sound_Sample *ss) {
    Sound_FreeSample(ss);
}

// Actually mixes the audio.
static void mixaudio(Uint8 *dst, Uint8 *src, int length, int volume) {
 
    // SDL_MixAudio may not work when length % 16 != 0.
    if ((length & 0x0f) == 0) {
        SDL_MixAudio(dst, src, length, volume);
    } else {
        int i;
        Uint8 copy[16];

        // This copy is made to ensure we only mix the overlap once.
        for (i = 0; i < 16; i++) {
            copy[i] = dst[length - 16 + i];
        }

        // Mix the audio once.
        SDL_MixAudio(dst, src, length, volume);
        
        // Copy back the overlap.
        for (i = 0; i < 16; i++) {
            dst[length - 16 + i] = copy[i];
        }

        // Mix the last 16 bytes again.
        SDL_MixAudio(&dst[length - 16], &src[length - 16], 16, volume);

    }    
}

// Mixes the audio, while performing fading.
static void fade_mixaudio(struct Channel *c,
                          Uint8 *dst, Uint8 *src, int length) {

    while (length) {

        // No fade case.
        if (c->fade_step_len == 0) {
            mixaudio(dst, src, length, c->volume);
            return;
        }

        // Fading, but we have some space left in the current step.
        if (c->fade_off < c->fade_step_len) {
            int l = min(c->fade_step_len - c->fade_off, length);
            mixaudio(dst, src, l, c->fade_vol);

            length -= l;
            dst += l;
            src += l;
            c->fade_off += l;
        }
        
        // Otherwise, we have no space left in the current fade step.
        // Go to the next step.
        c->fade_off = 0;
        c->fade_vol += c->fade_delta;

        // Don't stop on a fadeout.
        if (c->fade_vol <= 0) {
            c->fade_vol = 0;
        }

        // Stop on a fadein.
        if (c->fade_vol >= c->volume) {
            c->fade_vol = c->volume;
            c->fade_step_len = 0;
        }
    }

    return;
}

static void post_event(struct Channel *c) {
    if (! c->event) {
        return;
    }

    SDL_Event e;
    memset(&e, 0, sizeof(e));
    e.type = c->event;
    SDL_PushEvent(&e);
}

static void callback(void *userdata, Uint8 *stream, int length) {
    int channel = 0;
    
    for (channel = 0; channel < NUM_CHANNELS; channel++) {

        int mixed = 0;
        struct Channel *c = &channels[channel];

        if (! c->playing) {
            continue;
        }

        if (c->paused) {
            continue;
        }
        
        while (mixed < length && c->playing) {

            int mixleft = length - mixed;
            int bufleft = c->decoded - c->last;

            // We have some data in the buffer.
            if (c->stop_bytes && bufleft) {
                int bytes = min(bufleft, mixleft);

                if (c->stop_bytes != -1)
                    bytes = min(c->stop_bytes, bytes);
                
                fade_mixaudio(c, &stream[mixed],
                              &( ((Uint8*) c->playing->buffer) [c->last]),
                              bytes);

                mixed += bytes;
                c->last += bytes;
                
                if (c->stop_bytes != -1)
                    c->stop_bytes -= bytes;

                c->pos += bytes;
                
                continue;
            }

            // Otherwise, no data is left in the buffer. Check why,
            // and act accordingly.

            // EOF or ERROR -- Skip to the next sample.
            if (c->stop_bytes == 0 || c->playing->flags & (SOUND_SAMPLEFLAG_ERROR | SOUND_SAMPLEFLAG_EOF)) {

                post_event(c);

                free_sample(c->playing);
                decref(c->playing_name);

                c->playing = c->queued;
                c->playing_name = c->queued_name;
                c->playing_fadein = c->queued_fadein;
                
                c->queued = NULL;
                c->queued_name = NULL;
                c->queued_fadein = 0;
                
                start_sample(c);
                update_pause();
                
                continue;                
            }

            // If we're here, we're simply out of data in the
            // buffer. Decode some.

            c->decoded = Sound_Decode(c->playing);
            c->last = 0;
        }
    }
}

/*
 * Checks that the given channel is in range. Returns 0 if it is,
 * sets an error and returns -1 if it is not.
 */
static int check_channel(int c) {
    if (c < 0 || c >= NUM_CHANNELS) {
        error(PSS_ERROR);
        error_msg = "Channel number out of range.";
        return -1;
    }

    return 0;
}


/*
 * Loads the provided sample. Returns the sample on success, NULL on
 * failure.
 */
static Sound_Sample *load_sample(SDL_RWops *rw, const char *ext) {
    Sound_AudioInfo ai;
    Sound_Sample *rv;
    
    ai.format = audio_spec.format;
    ai.channels = audio_spec.channels;
    ai.rate = audio_spec.freq;

    rv = Sound_NewSample(rw, ext, &ai, audio_spec.samples * audio_spec.channels * 2);
    return rv;
}

    
void PSS_play(int channel, SDL_RWops *rw, const char *ext, PyObject *name, int fadein, int paused) {

    BEGIN();
    
    struct Channel *c;

    if (check_channel(channel)) {
        return;
    }

    c = &channels[channel];
    ENTER();
    
    /* Free playing and queued samples. */
    if (c->playing) {
        free_sample(c->playing);
        c->playing = NULL;
        decref(c->playing_name);
        c->playing_name = NULL;
    }
        
    if (c->queued) {
        free_sample(c->queued);
        c->queued = NULL;
        decref(c->queued_name);
        c->queued_name = NULL;
    }
        
    /* Allocate playing sample. */
    
    c->playing = load_sample(rw, ext);

    if (! c->playing) {
        EXIT();
        error(SOUND_ERROR);
        return;
    }

    incref(name);
    c->playing_name = name;

    c->playing_fadein = fadein;
    
    c->paused = paused;
    start_sample(c);    
    update_pause();
        
    EXIT();
    error(SUCCESS);
}

void PSS_queue(int channel, SDL_RWops *rw, const char *ext, PyObject *name, int fadein) {

    BEGIN();
    
    struct Channel *c;

    if (check_channel(channel)) {
        return;
    }

    c = &channels[channel];
    
    ENTER();

    /* If we're not playing, then we should play instead of queue. */
    if (!c->playing) {
        EXIT();
        PSS_play(channel, rw, ext, name, fadein, 0);
        return;            
    }
    
    /* Free queued sample. */
        
    if (c->queued) {
        free_sample(c->queued);
        c->queued = NULL;
        decref(c->queued_name);
        c->queued_name = NULL;
    }
        
    /* Allocate queued sample. */
    c->queued = load_sample(rw, ext);

    if (! c->queued) {
        EXIT();
        error(SOUND_ERROR);
        return;
    }

    incref(name);
    c->queued_name = name;
    c->queued_fadein = fadein;

    EXIT();
    error(SUCCESS);
}
              

/*
 * Stops all music from playing, freeing the data used by the
 * music.
 */
void PSS_stop(int channel) {
    BEGIN();

    struct Channel *c;

    if (check_channel(channel)) {
        return;
    }

    c = &channels[channel];

    ENTER();

    if (c->playing) {
        post_event(c);
    }
    
    /* Free playing and queued samples. */
    if (c->playing) {
        free_sample(c->playing);
        c->playing = NULL;
        decref(c->playing_name);
        c->playing_name = NULL;
    }
        
    if (c->queued) {
        free_sample(c->queued);
        c->queued = NULL;
        decref(c->queued_name);
        c->queued_name = NULL;
    }
    
    update_pause();
    
    EXIT();    

    error(SUCCESS);
}

/*
 * This dequeues the queued sound from the supplied channel, if
 * such a sound is queued. This does nothing to the playing
 * sound.
 */
void PSS_dequeue(int channel) {
    BEGIN();

    struct Channel *c;

    if (check_channel(channel)) {
        return;
    }

    c = &channels[channel];

    ENTER();

    if (c->queued) {
        free_sample(c->queued);
        c->queued = NULL;
        decref(c->queued_name);
        c->queued_name = NULL;
    }
    
    EXIT();    
    error(SUCCESS);
}

/*
 * Returns the queue depth of the current channel. This is 0 if we're
 * stopped, 1 if there's something playing but nothing queued, and 2
 * if there's both something playing and something queued.
 */
int PSS_queue_depth(int channel) {
    int rv = 0;
    BEGIN();

    struct Channel *c;

    if (check_channel(channel)) {
        return 0;
    }

    c = &channels[channel];

    ENTER();

    if (c->playing) rv++;
    if (c->queued) rv++;
    
    EXIT();    
    error(SUCCESS);

    return rv;
}

PyObject *PSS_playing_name(int channel) {
    BEGIN();
    PyObject *rv;
    
    struct Channel *c;

    if (check_channel(channel)) {
        Py_INCREF(Py_None);
        return Py_None;
    }

    ENTER();

    c = &channels[channel];

    if (c->playing_name) {
        rv = c->playing_name;
    } else {
        rv = Py_None;
    }

    incref(rv);

    EXIT();
    error(SUCCESS);
        
    return rv;
}

/*
 * Causes the given channel to fadeout playing after a specified
 * number of milliseconds. The playing sound stops once the
 * fadeout finishes (a queued sound may then start at full volume).
 */
void PSS_fadeout(int channel, int ms) {
    BEGIN();
    int fade_steps;
    struct Channel *c;

    if (check_channel(channel)) {
        return;
    }

    c = &channels[channel];

    ENTER();

    if (ms == 0) {
        c->stop_bytes = 0;
        EXIT();

        error(SUCCESS);
        return;
    }

    fade_steps = c->volume;
    c->fade_delta = -1;
    c->fade_off = 0;
    c->fade_vol = c->volume;

    c->fade_step_len = ms_to_bytes(ms) / fade_steps;
    c->fade_step_len &= ~0x7; // Even sample.

    c->stop_bytes = ms_to_bytes(ms);

    EXIT();    

    error(SUCCESS);
}

/*
 * Sets the pause flag on the given channel 0 = unpaused, 1 = paused.
 */
void PSS_pause(int channel, int pause) {
    BEGIN();
    
    struct Channel *c;

    if (check_channel(channel)) {
        return;
    }

    c = &channels[channel];

    ENTER();

    c->paused = pause;

    EXIT();

    error(SUCCESS);
    
}

void PSS_unpause_all(void) {

    int i;
    
    BEGIN();

    ENTER();

    for (i = 0; i < NUM_CHANNELS; i++) {
        channels[i].paused = 0;
    }

    EXIT();

    error(SUCCESS);
    
}

/*
 * Returns the position of the given channel, in ms.
 */
int PSS_get_pos(int channel) {
    int rv;
    struct Channel *c;

    BEGIN();
    
    if (check_channel(channel)) {
        return -1;
    }

    c = &channels[channel];

    ENTER();
    
    if (c->playing) {
        rv = bytes_to_ms(c->pos);
    } else {
        rv = -1;
    }

    EXIT();
    
    error(SUCCESS);
    return rv;
}

/*
 * Sets an event that is queued up when the track on the given channel
 * ends due to natural termination or a forced stop.
 */
void PSS_set_endevent(int channel, int event) {
    struct Channel *c;
    BEGIN();
    
    if (check_channel(channel)) {
        return;
    }

    c = &channels[channel];

    ENTER();
    
    c->event = event;
    
    EXIT();
    
    error(SUCCESS);    
}

/*
 * This sets the natural volume of the channel. (This may not take
 * effect immediately if a fade is going on.)
 */
void PSS_set_volume(int channel, float volume) {
    struct Channel *c;
    BEGIN();
    
    if (check_channel(channel)) {
        return;
    }

    c = &channels[channel];

    ENTER();
    
    c->volume = (int) (volume * SDL_MIX_MAXVOLUME);
    
    EXIT();
    
    error(SUCCESS);    
}


float PSS_get_volume(int channel) {

    float rv;
    
    struct Channel *c;
    BEGIN();
    
    if (check_channel(channel)) {
        return 0.0;
    }

    c = &channels[channel];

    ENTER();
    
    rv = 1.0 * c->volume / SDL_MIX_MAXVOLUME;
    
    EXIT();
    
    error(SUCCESS);    
    return rv;
}


/*
 * Initializes the sound to the given frequencies, channels, and
 * sample buffer size.
 */
void PSS_init(int freq, int stereo, int samples) {
    int i;

    if (initialized) {
        return;
    }

    PyEval_InitThreads();

    if (!thread) {
        thread = PyThreadState_Get();
        interp = thread->interp;
        thread = PyThreadState_New(interp);
    }
        
    if (!thread) {
        error(SDL_ERROR);
        return;
    }
    
    if (SDL_Init(SDL_INIT_AUDIO)) {
        error(SDL_ERROR);
        return;
    }

    audio_spec.freq = freq;
    audio_spec.format = AUDIO_S16SYS;
    audio_spec.channels = stereo;
    audio_spec.samples = samples;
    audio_spec.callback = callback;
    audio_spec.userdata = NULL;

    if (SDL_OpenAudio(&audio_spec, NULL)) {
        error(SDL_ERROR);
        return;
    }

    if (! Sound_Init()) {
        SDL_CloseAudio();
        error(SOUND_ERROR);
        return;
    }

    /*
     * Initialize the channels.
     */

    for (i = 0; i < NUM_CHANNELS; i++) {
        channels[i].playing = NULL;
        channels[i].queued = NULL;
        channels[i].volume = SDL_MIX_MAXVOLUME;        
        channels[i].paused = 1;
        channels[i].event = 0;
    }
    
    initialized = 1;

    error(SUCCESS);
}

void PSS_quit() {
    BEGIN();

    if (! initialized) {
        return;
    }
    
    int i;

    ENTER();
    SDL_PauseAudio(1);
    EXIT();

    for (i = 0; i < NUM_CHANNELS; i++) {
        PSS_stop(i);
    }

    Sound_Quit();
    SDL_CloseAudio();

    initialized = 0;
    error(SUCCESS);
}


/*
 * Returns the error message string if an error has occured, or
 * NULL if no error has happened.
 */
const char *PSS_get_error() {
    switch(PSS_error) {
    case 0:
        return "";
    case SDL_ERROR:
        return SDL_GetError();
    case SOUND_ERROR:
        return Sound_GetError();
    case PSS_ERROR:
        return error_msg;
    default:
        return "Error getting error.";
    }
}


