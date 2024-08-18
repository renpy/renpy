/*
Copyright 2004-2011 Tom Rothamel <pytom@bishoujo.us>

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

#include "renpysound_core.h"
#include <Python.h>
#include <SDL.h>
#include <SDL_thread.h>
#include <stdio.h>
#include <string.h>
#include <pygame_sdl2/pygame_sdl2.h>

apply_audio_filter_type RPS_apply_audio_filter = NULL;

SDL_mutex *name_mutex;

#ifdef __EMSCRIPTEN__

#define LOCK_AUDIO() { }
#define UNLOCK_AUDIO() { }

#define LOCK_NAME() { }
#define UNLOCK_NAME() { }

#else

/* These prevent the audio callback from running when held. Use this to
   prevent the audio callback from running while the state of the audio
   system is being changed. */
#define LOCK_AUDIO() { SDL_LockAudio(); }
#define UNLOCK_AUDIO() { SDL_UnlockAudio(); }

/* This is held while the current track is being changed by the audio callback,
   and can also be held to the current track doesn't change while things are
   being processed. */
#define LOCK_NAME() { SDL_LockMutex(name_mutex); }
#define UNLOCK_NAME() { SDL_UnlockMutex(name_mutex); }

#endif

/* Declarations of ffdecode functions. */
struct MediaState;
typedef struct MediaState MediaState;

void media_init(int rate, int status, int equal_mono);

void media_advance_time(void);
void media_sample_surfaces(SDL_Surface *rgb, SDL_Surface *rgba);
MediaState *media_open(SDL_RWops *, const char *);
void media_want_video(MediaState *, int);
void media_start_end(MediaState *, double, double);
void media_start(MediaState *);
void media_pause(MediaState *, int);
void media_close(MediaState *);

int media_read_audio(struct MediaState *is, Uint8 *stream, int len);

int media_video_ready(struct MediaState *ms);
SDL_Surface *media_read_video(struct MediaState *ms);

double media_duration(struct MediaState *ms);
int media_is_ready(struct MediaState *ms);

/* Min and Max */
#define min(a, b) (((a) < (b)) ? (a) : (b))
#define max(a, b) (((a) > (b)) ? (a) : (b))

/* Various error codes. */
#define SUCCESS 0
#define SDL_ERROR -1
#define SOUND_ERROR -2
#define RPS_ERROR -3

/* This is called with the appropriate error code at the end of a
 * function. */
#define error(err) RPS_error = err
int RPS_error = SUCCESS;
static const char *error_msg = NULL;

/* Have we been initialized? */
static int initialized = 0;

/** Should fades be linear rather than logarithmic? */
static int linear_fades = 0;

struct Interpolate {
    /* The number of samples that are finished so far. */
    unsigned int done;

    /* The duration of the interpolation, in samples. */
    unsigned int duration;

    /* The starting value. */
    float start;

    /* The ending value. */
    float end;
};


void init_interpolate(struct Interpolate *i, float value) {
    i->done = 0;
    i->duration = 0;
    i->start = value;
    i->end = value;
}

static inline float lerp(float start, float end, float done) {
    return start + (end - start) * done;
}

static inline void tick_interpolate(struct Interpolate *i) {
    if (i->done < i->duration) {
        i->done += 1;
    }
}

static inline float get_interpolate(struct Interpolate *i) {
    if (i->done >= i->duration) {
        return i->end;
    } else {
        return lerp(i->start, i->end, (float) i->done / (float) i->duration);
    }
}


// The power corresponding to a magnitude of 0.0.
#define MIN_POWER 0.0

// The power corresponding to a magnitude of 1.0. This controls the
// range in dB that fades happen over. The formula for this is
// fade_range_in_db = 20 * math.log10(2 ** MAX_POWER).
//
// The 6 corresponds to a 36.12 dB range.
#define MAX_POWER 6

/**
 * This interpolates a logarithmic power level to a magnitude.
 *
 * The units of the log power level are odd, to make things faster - it's
 * log2f(power) + MAX_POWER, to make calculations faster.
 */
static inline float get_interpolate_power(struct Interpolate *i) {

    float log_power = get_interpolate(i);

    if (linear_fades) {
        return log_power / MAX_POWER;
    }

    if (log_power == MIN_POWER) {
        return 0;
    } else if (log_power == MAX_POWER) {
        return 1.0;
    } else {
        return powf(2, log_power - MAX_POWER);
    }
}

/**
 * This converts a magnitude to a logarithmic power level.
 */
static inline float log_power(float power) {

    if (linear_fades) {
        return power * MAX_POWER;
    }

    if (power <= 0.0) {
        return MIN_POWER;
    } else if (power >= 1.0) {
        return MAX_POWER;
    } else {
        return log2f(power) + MAX_POWER;
    }
}


/*
 * This structure represents a channel the system knows about
 * and can play from.
 */
struct Channel {

    /* The currently playing stream, NULL if this sample isn't playing
       anything. */
    struct MediaState *playing;

    /* The name of the playing stream. */
    char *playing_name;

    /* The number of ms to take to fade in the playing stream. */
    int playing_fadein;

    /* Is the playing stream tight? */
    int playing_tight;

    /* The start time of the playing stream, in ms. */
    int playing_start_ms;

    /* The relative volume of the playing stream. */
    float playing_relative_volume;

    /* Is the playing sample waiting for a synchro start? */
    int playing_synchro_start;

    /* The number of samples of silence to pad the playing stream with.*/
    int playing_pad;

    /**
     * The AudioFilter that is currently in use on this channel. NULL
     * if no filter is in use.
     */
    PyObject *playing_audio_filter;

    /* The queued up stream. */
    struct MediaState *queued;

    /* The name of the queued up stream. */
    char *queued_name;

    /* The number of ms to take to fade in the queued stream. */
    int queued_fadein;

    /* Is the queued stream tight? */
    int queued_tight;

    /* The start time of the queued stream, in ms. */
    int queued_start_ms;

    /* The relative volume of the queued stream. */
    float queued_relative_volume;

    /* Is the queued sample waiting for a synchro start? */
    int queued_synchro_start;

    /* The AudioFilter that is queued on this channel. */
    PyObject *queued_audio_filter;

    /* Is this channel paused? */
    int paused;

    /* The user set mixer volume. */
    float mixer_volume;

    /* The channel specific volume. */
    struct Interpolate secondary_volume;

    /* The position (in samples) that this channel has queued to. */
    int pos;

    /* Information about the current fading. */
    struct Interpolate fade;

    /* The number of samples in which we'll stop. */
    int stop_samples;

    /* The event posted to the queue when we finish the playing stream. */
    int event;

    /* The pan of the channel. */
    struct Interpolate pan;

    /* This is set to 1 if this is a movie channel with dropping, 2 if it's a
     * video channel without dropping. */
    int video;

    /**
     * Was this playing the last time we checked?
     */
    int last_playing;

    /**
     * The last volume.
     */
    float last_volume;

};

struct Dying {
    struct MediaState *stream;
    PyObject *audio_filter;
    struct Dying *next;
};

static struct Dying *dying = NULL;

/*
 * The number of channels the system knows about.
 */
int num_channels = 0;

/*
 * All of the channels that the system knows about.
 */
struct Channel *channels = NULL;

/*
 * The spec of the audio that is playing.
 */
SDL_AudioSpec audio_spec;

static int ms_to_samples(int ms) {
    return ((long long) ms) * audio_spec.freq / 1000;
}

static int samples_to_ms(int samples) {
    return ((long long) samples) * 1000 / audio_spec.freq;
}

static void start_stream(struct Channel* c, int reset_fade) {

    if (!c) return;

    c->pos = 0;
    if (!c->queued) {
        c->playing_pad = audio_spec.freq * 2;
    }

    if (reset_fade) {

        c->fade.start = MIN_POWER;
        c->fade.end = MAX_POWER;
        c->fade.done = 0;
        c->fade.duration = ms_to_samples(c->playing_fadein);

        c->stop_samples = -1;
    }
}

static void free_stream(struct MediaState *ss) {
    media_close(ss);
}


#define MAX_SHORT (32767)
#define MIN_SHORT (-32768)



static void post_event(struct Channel *c) {
    if (! c->event) {
        return;
    }

    SDL_Event e;
    memset(&e, 0, sizeof(e));
    e.type = c->event;
    SDL_PushEvent(&e);
}

#define PI 3.14159265358979323846
#define ZERO_PAN 0.7071067811865476 // cos(PI / 4) and sin(PI / 4)


static inline void mix_sample(struct Channel *c, float left, float right, float *left_out, float *right_out) {

    tick_interpolate(&c->fade);
    tick_interpolate(&c->secondary_volume);
    tick_interpolate(&c->pan);

    float pan = get_interpolate(&c->pan);

    if (pan == 0.0) {
        left *= ZERO_PAN;
        right *= ZERO_PAN;
    } else {
        float theta = PI * (pan + 1) / 4;
        left *= cosf(theta);
        right *= sinf(theta);
    }

    float target_volume = get_interpolate_power(&c->fade) * get_interpolate_power(&c->secondary_volume) * c->playing_relative_volume * c->mixer_volume;
    float volume = c->last_volume + .01 * (target_volume - c->last_volume);

    if (!c->last_playing) {
        volume = target_volume;
    }

    *left_out += left * volume;
    *right_out += right * volume;

    c->last_volume = volume;
}


/** If not NULL, this can be replaced with a function that will be called
    to generate audio. The functtio is called with a consistion of 2*length
    shorts, and should fill the buffer with audio data. */
void (*RPS_generate_audio_c_function)(float *stream, int length) = NULL;


static void callback(void *userdata, Uint8 *stream, int length) {

    // Convert the length to samples.
    length /= (2 * sizeof(float));

    float mix_buffer[length * 2];
    short stream_buffer[length * 2];
    float float_buffer[length * 2];

    memset(mix_buffer, 0, length * 2 * sizeof(float));

    if (RPS_generate_audio_c_function) {
        RPS_generate_audio_c_function(mix_buffer, length);
    }

    for (int channel = 0; channel < num_channels; channel++) {

        // The number of samples that have been mixed.
        int mixed = 0;

        struct Channel *c = &channels[channel];

        if (! c->playing || c->paused) {
            c->last_playing = 0;
            continue;
        }

        while (mixed < length && c->playing && !c->playing_synchro_start) {

            // How much do we have left to mix on this channel?
            int mixleft = length - mixed;

            // The number of samples that we read.
            int read_length;

            // Decode some amount of data.
            read_length = media_read_audio(c->playing, (Uint8 *) stream_buffer, mixleft * 2 * sizeof(short));
            read_length /= (2 * sizeof(short));

            // If we're done with this stream, skip to the next.
            if (c->stop_samples == 0 || read_length == 0) {

                if (!c->playing_audio_filter || c->playing_audio_filter == Py_None || c->queued) {
                    c->playing_pad = 0;
                }

                if (c->playing_pad > 0) {

                    if (c->playing_pad > mixleft) {
                        read_length = mixleft;
                    } else {
                        read_length = c->playing_pad;
                    }

                    c->playing_pad -= read_length;
                    memset(stream_buffer, 0, read_length * 2 * sizeof(short));

                } else {

                    int old_tight = c->playing_tight;
                    struct Dying *d;

                    post_event(c);

                    LOCK_NAME()

                    d = malloc(sizeof(struct Dying));
                    d->next = dying;
                    d->stream = c->playing;

                    // If there's a new audio filter, queue the old one for deallocation.
                    if (c->playing_audio_filter) {
                        d->audio_filter = c->playing_audio_filter;
                    } else {
                        d->audio_filter = NULL;
                    }

                    dying = d;

                    free(c->playing_name);

                    c->playing = c->queued;
                    c->playing_name = c->queued_name;
                    c->playing_fadein = c->queued_fadein;
                    c->playing_tight = c->queued_tight;
                    c->playing_start_ms = c->queued_start_ms;
                    c->playing_relative_volume = c->queued_relative_volume;
                    c->playing_synchro_start = c->queued_synchro_start;

                    c->playing_audio_filter = c->queued_audio_filter;

                    c->queued = NULL;
                    c->queued_name = NULL;
                    c->queued_fadein = 0;
                    c->queued_tight = 0;
                    c->queued_start_ms = 0;
                    c->queued_relative_volume = 1.0;
                    c->queued_audio_filter = NULL;
                    c->queued_synchro_start = 0;

                    if (c->playing_fadein) {
                        old_tight = 0;
                    }

                    UNLOCK_NAME()

                    start_stream(c, !old_tight);

                    continue;
                }
            }

            for (int i = 0; i < read_length; i++) {
                float_buffer[i * 2] = stream_buffer[i * 2] / 1.0 / -MIN_SHORT;
                float_buffer[i * 2 + 1] = stream_buffer[i * 2 + 1] / 1.0 / -MIN_SHORT;
            }

            if (c->playing_audio_filter && c->playing_audio_filter != Py_None) {
                RPS_apply_audio_filter(c->playing_audio_filter, float_buffer, 2, read_length, audio_spec.freq);
            }

            // We have some data in the buffer, so mix it.
            for (int i = 0; (i < read_length) && c->stop_samples; i++) {

                mix_sample(c, float_buffer[i * 2], float_buffer[i * 2 + 1], &mix_buffer[mixed * 2], &mix_buffer[mixed * 2 + 1]);

                if (c->stop_samples > 0) {
                    c->stop_samples--;
                }

                c->pos++;
                mixed += 1;
            }

        }

        c->last_playing = 1;
    }

    // Actually output the sound.
    for (int i = 0; i < length; i++) {
        float left = mix_buffer[i * 2];
        float right = mix_buffer[i * 2 + 1];


        if (left > 1.0) {
            left = 1.0;
        }

        if (left < -1.0) {
            left = -1.0;
        }

        if (right > 1.0) {
            right = 1.0;
        }

        if (right < -1.0) {
            right = -1.0;
        }

        ((float *) stream)[i * 2] = left;
        ((float *) stream)[i * 2 + 1] = right;
    }
}


/*
 * Checks that the given channel is in range. Returns 0 if it is,
 * sets an error and returns -1 if it is not. Allocates channels
 * that don't already exist.
 */
static int check_channel(int c) {
    int i;

    if (c < 0) {
        error(RPS_ERROR);
        error_msg = "Channel number out of range.";
        return -1;
    }

    if (c >= num_channels) {
        struct Channel *extended_channels = realloc(channels, sizeof(struct Channel) * (c + 1));
        if (extended_channels == NULL) {
            error(RPS_ERROR);
            error_msg = "Unable to allocate additional channels.";
            return -1;
        }
        channels = extended_channels;

        for (i = num_channels; i <= c; i++) {

        	memset(&channels[i], 0, sizeof(struct Channel));

            channels[i].mixer_volume = 1.0;
            channels[i].paused = 0;
            channels[i].event = 0;

            init_interpolate(&channels[i].fade, MAX_POWER);
            init_interpolate(&channels[i].secondary_volume, MAX_POWER);
            init_interpolate(&channels[i].pan, 0.0);
        }

        num_channels = c + 1;
    }

    return 0;
}


/*
 * Loads the provided stream. Returns the stream on success, NULL on
 * failure.
 */
struct MediaState *load_stream(SDL_RWops *rw, const char *ext, double start, double end, int video) {
    struct MediaState *rv;
    rv = media_open(rw, ext);
    if (rv == NULL)
    {
        return NULL;
    }
    media_start_end(rv, start, end);

    if (video) {
        media_want_video(rv, video);
    }

    media_start(rv);
    return rv;
}


void RPS_play(int channel, SDL_RWops *rw, const char *ext, const char *name, int synchro_start, int fadein, int tight, double start, double end, float relative_volume, PyObject *audio_filter) {

    struct Channel *c;

    if (check_channel(channel)) {
        return;
    }

    c = &channels[channel];

    LOCK_AUDIO();

    /* Free playing and queued samples. */
    if (c->playing) {
        free_stream(c->playing);
        c->playing = NULL;
        free(c->playing_name);
        c->playing_name = NULL;
        c->playing_tight = 0;
        c->playing_start_ms = 0;
        c->playing_relative_volume = 1.0;

        if (c->playing_audio_filter) {
            Py_DECREF(c->playing_audio_filter);
            c->queued_audio_filter = NULL;
        }
    }

    if (c->queued) {
        free_stream(c->queued);
        c->queued = NULL;
        free(c->queued_name);
        c->queued_name = NULL;
        c->queued_tight = 0;
        c->queued_start_ms = 0;
        c->queued_relative_volume = 1.0;

        if (c->queued_audio_filter) {
            Py_DECREF(c->queued_audio_filter);
            c->queued_audio_filter = NULL;
        }
    }

    /* Allocate playing sample. */

    c->playing = load_stream(rw, ext, start, end, c->video);

    if (! c->playing) {
        UNLOCK_AUDIO();
        error(SOUND_ERROR);
        return;
    }

    c->playing_name = strdup(name);
    c->playing_fadein = fadein;
    c->playing_tight = tight;
    c->playing_start_ms = (int) (start * 1000);
    c->playing_relative_volume = relative_volume;

    if (audio_filter) {
        c->playing_audio_filter = audio_filter;
        Py_INCREF(c->playing_audio_filter);
    } else {
        c->playing_audio_filter = NULL;
    }

    c->playing_synchro_start = synchro_start;

    start_stream(c, 1);

    UNLOCK_AUDIO();

    error(SUCCESS);
}

void RPS_queue(int channel, SDL_RWops *rw, const char *ext, const char *name, int synchro_start, int fadein, int tight, double start, double end, float relative_volume, PyObject *audio_filter) {

    struct Channel *c;

    if (check_channel(channel)) {
        return;
    }

    c = &channels[channel];

    /* If we're not playing, then we should play instead of queue. */
    if (!c->playing) {
        RPS_play(channel, rw, ext, name, synchro_start, fadein, tight, start, end, relative_volume, audio_filter);
        return;
    }

    MediaState *ms = load_stream(rw, ext, start, end, c->video);

    LOCK_AUDIO();

    /* Free queued sample. */

    if (c->queued) {
        free_stream(c->queued);
        c->queued = NULL;
        free(c->queued_name);
        c->queued_name = NULL;
        c->queued_tight = 0;
    }

    if (c->queued_audio_filter) {
        Py_DECREF(c->queued_audio_filter);
        c->queued_audio_filter = NULL;
    }

    /* Allocate queued sample. */
    c->queued = ms;

    if (! c->queued) {
        UNLOCK_AUDIO();

        error(SOUND_ERROR);
        return;
    }

    c->queued_name = strdup(name);
    c->queued_fadein = fadein;
    c->queued_tight = tight;
    c->queued_synchro_start = synchro_start;

    c->queued_start_ms = (int) (start * 1000);
    c->queued_relative_volume = relative_volume;


    if (audio_filter) {
        c->queued_audio_filter = audio_filter;
        Py_INCREF(c->queued_audio_filter);
    } else {
        c->queued_audio_filter = NULL;
    }

    UNLOCK_AUDIO();

    error(SUCCESS);
}


/*
 * Stops all music from playing, freeing the data used by the
 * music.
 */
void RPS_stop(int channel) {

    struct Channel *c;

    if (check_channel(channel)) {
        return;
    }

    c = &channels[channel];

    LOCK_AUDIO();

    if (c->playing) {
        post_event(c);
    }

    /* Free playing and queued samples. */
    if (c->playing) {
        free_stream(c->playing);
        c->playing = NULL;
        free(c->playing_name);
        c->playing_name = NULL;
        c->playing_start_ms = 0;
        c->playing_relative_volume = 1.0;
        c->playing_synchro_start = 0;
    }

    if (c->playing_audio_filter) {
        Py_DECREF(c->playing_audio_filter);
        c->playing_audio_filter = NULL;
    }

    if (c->queued) {
        free_stream(c->queued);
        c->queued = NULL;
        free(c->queued_name);
        c->queued_name = NULL;
        c->queued_start_ms = 0;
        c->queued_relative_volume = 1.0;
        c->queued_synchro_start = 0;

    }

    if (c->queued_audio_filter) {
        Py_DECREF(c->queued_audio_filter);
        c->queued_audio_filter = NULL;
    }

    UNLOCK_AUDIO();

    error(SUCCESS);
}

/*
 * This dequeues the queued sound from the supplied channel, if
 * such a sound is queued. This does nothing to the playing
 * sound.
 *
 * This does nothing if the playing sound is tight, ever_tight is
 * false.
 */
void RPS_dequeue(int channel, int even_tight) {

    struct Channel *c;

    if (check_channel(channel)) {
        return;
    }

    c = &channels[channel];

    LOCK_AUDIO();

    if (c->queued && (! c->playing_tight || even_tight)) {
        free_stream(c->queued);
        c->queued = NULL;
        free(c->queued_name);
        c->queued_name = NULL;
    } else {
        c->queued_tight = 0;
    }

    c->queued_start_ms = 0;
    c->queued_synchro_start = 0;

    if (c->queued_audio_filter) {
        Py_DECREF(c->queued_audio_filter);
        c->queued_audio_filter = NULL;
    }

    UNLOCK_AUDIO();

    error(SUCCESS);
}

/*
 * Returns the queue depth of the current channel. This is 0 if we're
 * stopped, 1 if there's something playing but nothing queued, and 2
 * if there's both something playing and something queued.
 */
int RPS_queue_depth(int channel) {
    int rv = 0;

    struct Channel *c;

    if (check_channel(channel)) {
        return 0;
    }

    c = &channels[channel];

    LOCK_NAME();

    if (c->playing) rv++;
    if (c->queued) rv++;

    UNLOCK_NAME();

    error(SUCCESS);

    return rv;
}

PyObject *RPS_playing_name(int channel) {
    PyObject *rv;
    struct Channel *c;

    if (check_channel(channel)) {
        Py_INCREF(Py_None);
        return Py_None;
    }

    c = &channels[channel];

    LOCK_NAME();

    if (c->playing_name) {
        rv = PyBytes_FromString(c->playing_name);
    } else {
        Py_INCREF(Py_None);
        rv = Py_None;
    }

    UNLOCK_NAME();

    error(SUCCESS);

    return rv;
}

/*
 * Causes the given channel to fadeout playing after a specified
 * number of milliseconds. The playing sound stops once the
 * fadeout finishes (a queued sound may then start at full volume).
 */
void RPS_fadeout(int channel, int ms) {

    struct Channel *c;

    if (check_channel(channel)) {
        return;
    }

    c = &channels[channel];

    LOCK_AUDIO();

    if (c->queued) {

        float position = samples_to_ms(c->pos) / 1000.0 + c->playing_start_ms;
        float duration = media_duration(c->playing);

        // If the fadeout will fit into the current file, dequeue the next file, so
        // that the next track will begin playing immediately.
        if ((position + ms / 1000.0 < duration) || (! c->playing_tight) || (ms <= 32)) {
                free_stream(c->queued);
                c->queued = NULL;
                free(c->queued_name);
                c->queued_name = NULL;
                c->queued_start_ms = 0;
                c->queued_relative_volume = 1.0;
        }
    }

    if (ms == 0 || c->playing_synchro_start) {
        c->stop_samples = 0;
        c->playing_tight = 0;
        c->playing_synchro_start = 0;
        UNLOCK_AUDIO();

        error(SUCCESS);
        return;
    }

    if (ms > 16) {
        c->fade.start = get_interpolate(&c->fade);
        c->fade.end = MIN_POWER;
        c->fade.done = 0;
        c->fade.duration = ms_to_samples(ms - 16);
    } else {
        c->fade.start = MIN_POWER;
        c->fade.end = MIN_POWER;
        c->fade.done = 1;
        c->fade.duration = 1;
    }

    c->stop_samples = ms_to_samples(ms);
    c->queued_tight = 0;

    if (!c->queued) {
        c->playing_tight = 0;
    }

    UNLOCK_AUDIO();

    error(SUCCESS);
}

/*
 * Sets the pause flag on the given channel 0 = unpaused, 1 = paused.
 */
void RPS_pause(int channel, int pause) {

    struct Channel *c;

    if (check_channel(channel)) {
        return;
    }

    c = &channels[channel];

    c->paused = pause;

    if (c->playing) {
        media_pause(c->playing, pause);
    }

    error(SUCCESS);

}


/**
 * Starts and stops the SDL audio playback.
 */
void RPS_global_pause(int pause) {
    int i;

    SDL_PauseAudio(pause);

    for (i = 0; i < num_channels; i++) {
        if (channels[i].playing) {
            media_pause(channels[i].playing, pause);
        }
    }
}


/*
 * Returns the position of the given channel, in ms.
 */
int RPS_get_pos(int channel) {
    int rv;
    struct Channel *c;

    if (check_channel(channel)) {
        return -1;
    }

    c = &channels[channel];

    LOCK_NAME();

    if (c->playing) {
        rv = samples_to_ms(c->pos) + c->playing_start_ms;
    } else {
        rv = -1;
    }

    UNLOCK_NAME();

    error(SUCCESS);
    return rv;
}

/*
 * Returns the duration of the file playing on the given channel, in
 * seconds.
 */
double RPS_get_duration(int channel) {
    double rv;
    struct Channel *c;

    if (check_channel(channel)) {
        return 0.0;
    }

    c = &channels[channel];

    LOCK_NAME();

    if (c->playing) {
        rv = media_duration(c->playing);
    } else {
        rv = 0.0;
    }

    UNLOCK_NAME();

    error(SUCCESS);
    return rv;
}

/*
 * Sets an event that is queued up when the track on the given channel
 * ends due to natural termination or a forced stop.
 */
void RPS_set_endevent(int channel, int event) {
    struct Channel *c;

    if (check_channel(channel)) {
        return;
    }

    c = &channels[channel];

    c->event = event;

    error(SUCCESS);
}

/*
 * This sets the mixer volume of the channel.
 */
void RPS_set_volume(int channel, float volume) {
    struct Channel *c;

    if (check_channel(channel)) {
        return;
    }

    c = &channels[channel];
    c->mixer_volume = volume;

    error(SUCCESS);
}


float RPS_get_volume(int channel) {

    struct Channel *c;

    if (check_channel(channel)) {
        return 0.0;
    }

    c = &channels[channel];

    error(SUCCESS);
    return c->mixer_volume;
}

/*
 * This sets the pan of the channel... independent volumes for the
 * left and right channels.
 */
void RPS_set_pan(int channel, float pan, float delay) {
    struct Channel *c;

    if (check_channel(channel)) {
        return;
    }

    c = &channels[channel];

    LOCK_AUDIO();

    c->pan.start = get_interpolate(&c->pan);
    c->pan.end = pan;
    c->pan.done = 0;
    c->pan.duration = ms_to_samples(delay * 1000);

    UNLOCK_AUDIO();

    error(SUCCESS);
}

/*
 * This sets the secondary volume of the channel.
 */
void RPS_set_secondary_volume(int channel, float vol2, float delay) {
    struct Channel *c;

    if (check_channel(channel)) {
        return;
    }

    c = &channels[channel];

    LOCK_AUDIO();

    c->secondary_volume.start = get_interpolate(&c->secondary_volume);
    c->secondary_volume.end = log_power(vol2);
    c->secondary_volume.done = 0;
    c->secondary_volume.duration = ms_to_samples(delay * 1000);

    UNLOCK_AUDIO();

    error(SUCCESS);
}


/**
 * Replaces audio filters with the given PyObject.
 */
void RPS_replace_audio_filter(int channel, PyObject *new_filter) {

    struct Channel *c;

    if (check_channel(channel)) {
        return;
    }

    c = &channels[channel];

    LOCK_AUDIO();

    if (c->playing_audio_filter) {
        Py_DECREF(c->playing_audio_filter);
        Py_INCREF(new_filter);
        c->playing_audio_filter = new_filter;
    }

    if (c->queued_audio_filter) {
        Py_DECREF(c->queued_audio_filter);
        Py_INCREF(new_filter);
        c->queued_audio_filter = new_filter;
    }

    UNLOCK_AUDIO();

    error(SUCCESS);


}


PyObject *RPS_read_video(int channel) {
    struct Channel *c;
    SDL_Surface *surf = NULL;

    if (check_channel(channel)) {
        Py_INCREF(Py_None);
        return Py_None;
    }

    c = &channels[channel];

    if (c->playing) {
        Py_BEGIN_ALLOW_THREADS
        surf = media_read_video(c->playing);
        Py_END_ALLOW_THREADS
    }

    error(SUCCESS);

    if (surf) {
        return PySurface_New(surf);
    } else {
        Py_INCREF(Py_None);
        return Py_None;
    }

}

int RPS_video_ready(int channel) {
    struct Channel *c;
    int rv;

    if (check_channel(channel)) {
        return 1;
    }

    c = &channels[channel];

    if (c->playing) {
        rv = media_video_ready(c->playing);
    } else {
        rv = 1;
    }

    error(SUCCESS);

    return rv;
}

/**
 * Marks channel as a video channel.
 */
void RPS_set_video(int channel, int video) {
	struct Channel *c;

	if (check_channel(channel)) {
        return;
    }

    c = &channels[channel];

    c->video = video;
}


/*
 * Initializes the sound to the given frequencies, channels, and
 * sample buffer size.
 */
void RPS_init(int freq, int stereo, int samples, int status, int equal_mono, int linear_fades_) {

    if (initialized) {
        return;
    }

    name_mutex = SDL_CreateMutex();

#ifndef __EMSCRIPTEN__
#if PY_VERSION_HEX < 0x03070000
    PyEval_InitThreads();
#endif
#endif

    import_pygame_sdl2();

    if (SDL_Init(SDL_INIT_AUDIO)) {
        error(SDL_ERROR);
        return;
    }

    audio_spec.freq = freq;
    audio_spec.format = AUDIO_F32;
    audio_spec.channels = stereo;
    audio_spec.samples = samples;
    audio_spec.callback = callback;
    audio_spec.userdata = NULL;

    if (SDL_OpenAudio(&audio_spec, NULL)) {
        error(SDL_ERROR);
        return;
    }

    media_init(audio_spec.freq, status, equal_mono);

    SDL_PauseAudio(0);

    linear_fades = linear_fades_;

    initialized = 1;

    error(SUCCESS);
}

void RPS_quit() {

    if (! initialized) {
        return;
    }

    int i;

    LOCK_AUDIO();
    SDL_PauseAudio(1);
    UNLOCK_AUDIO();

    for (i = 0; i < num_channels; i++) {
        RPS_stop(i);
    }

    SDL_CloseAudio();

    num_channels = 0;
    initialized = 0;
    error(SUCCESS);
}

static void handle_synchro_start() {
    int ready = 1;

    for (int i = 0; i < num_channels; i++) {
        struct Channel *c = &channels[i];

        if (c->playing_synchro_start) {
            c->queued_synchro_start = 0;

            if (c->playing) {
                if (!media_is_ready(c->playing)) {
                    ready = 0;
                }
            } else {
                c->playing_synchro_start = 0;
            }
        }

        if (c->queued && c->queued_synchro_start) {
            ready = 0;
        } else {
            c->queued_synchro_start = 0;
        }
    }

    if (ready) {
        for (int i = 0; i < num_channels; i++) {
            struct Channel *c = &channels[i];

            if (c->playing_synchro_start) {
                c->playing_synchro_start = 0;
            }
        }
    }
}

/* This must be called frequently, to take care of deallocating dead
 * streams. */
void RPS_periodic() {

    LOCK_NAME();
    handle_synchro_start();

    struct Dying *d = dying;
    dying = NULL;
    UNLOCK_NAME();

    while (d) {
        media_close(d->stream);
        struct Dying *next_d = d->next;

        if (d->audio_filter) {
            Py_DECREF(d->audio_filter);
        }

        free(d);
        d = next_d;
    }

}

void RPS_advance_time(void) {
	media_advance_time();
}


void RPS_sample_surfaces(PyObject *rgb, PyObject *rgba) {
    import_pygame_sdl2();

    media_sample_surfaces(
			PySurface_AsSurface(rgb),
			PySurface_AsSurface(rgba)
		);

}


int RPS_get_sample_rate() {
    return audio_spec.freq;
}

/*
 * Returns the error message string if an error has occured, or
 * NULL if no error has happened.
 */
char *RPS_get_error() {
    switch(RPS_error) {
    case 0:
        return (char *) "";
    case SDL_ERROR:
        return (char *) SDL_GetError();
    case SOUND_ERROR:
        return (char *) "Some sort of codec error.";
    case RPS_ERROR:
        return (char *) error_msg;
    default:
        return (char *) "Error getting error.";
    }
}
