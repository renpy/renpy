/*
Copyright 2004-2026 Tom Rothamel <pytom@bishoujo.us>

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is furnished
to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
*/

#ifndef RENPY_FFMEDIA_H
#define RENPY_FFMEDIA_H

#include <stdint.h>

struct MediaState;

typedef struct MediaVideoYUV {
    int width;
    int height;
    uint8_t *y;
    uint8_t *uv;
    int full_range;
    int bt709;
} MediaVideoYUV;

int media_read_video_yuv(struct MediaState *ms, MediaVideoYUV *rv);
void media_free_video_yuv(MediaVideoYUV *frame);

#endif
