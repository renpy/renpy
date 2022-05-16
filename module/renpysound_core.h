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

#ifndef RPS_H
#define RPS_H

#include <Python.h>
#include <SDL.h>

void RPS_play(int channel, SDL_RWops *rw, const char *ext, const char *name, int fadeout, int tight, int paused, double start, double end, float relative_volume);
void RPS_queue(int channel, SDL_RWops *rw, const char *ext, const char *name, int fadeout, int tight, double start, double end, float relative_volume);
void RPS_stop(int channel);
void RPS_dequeue(int channel, int even_tight);
int RPS_queue_depth(int channel);
PyObject *RPS_playing_name(int channel);
void RPS_fadeout(int channel, int ms);
void RPS_pause(int channel, int pause);
void RPS_unpause_all_at_start(void);
void RPS_set_endevent(int channel, int event);
int RPS_get_pos(int channel);
double RPS_get_duration(int channel);
void RPS_set_volume(int channel, float volume);
float RPS_get_volume(int channel);
void RPS_set_pan(int channel, float pan, float delay);
void RPS_set_secondary_volume(int channel, float vol2, float delay);


int RPS_video_ready(int channel);
PyObject *RPS_read_video(int channel);
void RPS_sample_surfaces(PyObject *rgb, PyObject *rgba);
void RPS_set_video(int channel, int video);

void RPS_init(int freq, int stereo, int samples, int status, int equal_mono);
void RPS_quit(void);

void RPS_advance_time(void);
void RPS_periodic(void);

char *RPS_get_error(void);

#endif
