/* Copyright 2026 Tom Rothamel <pytom@bishoujo.us>
 *
 * Permission is hereby granted, free of charge, to any person obtaining a copy
 * of this software and associated documentation files (the "Software"), to
 * deal in the Software without restriction, including without limitation the
 * rights to use, copy, modify, merge, publish, distribute, sublicense, and/or
 * sell copies of the Software, and to permit persons to whom the Software is
 * furnished to do so, subject to the following conditions:
 *
 * The above copyright notice and this permission notice shall be included in
 * all copies or substantial portions of the Software.
 *
 * THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
 * IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
 * FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
 * AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
 * LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING
 * FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS
 * IN THE SOFTWARE.
 */

#ifndef RENPY_SURFACE_DEALLOCATION_H
#define RENPY_SURFACE_DEALLOCATION_H

#include <SDL3/SDL.h>

#ifdef __EMSCRIPTEN__
#define RENPY_SURFACE_DEALLOCATION_THREADED 0
#else
#define RENPY_SURFACE_DEALLOCATION_THREADED 1
#endif

typedef struct RenpySurfaceDeallocation RenpySurfaceDeallocation;

/* Lifecycle calls and producers are serialized by the Python GIL. Only the
 * native consumer runs concurrently, and it never calls Python. */
bool renpy_surface_deallocation_init(void);
void renpy_surface_deallocation_quit(void);
RenpySurfaceDeallocation *renpy_surface_deallocation_new(void);
void renpy_surface_deallocation_discard(RenpySurfaceDeallocation *entry);
void renpy_surface_deallocation_enqueue(RenpySurfaceDeallocation *entry, SDL_Surface *surface);

#endif
