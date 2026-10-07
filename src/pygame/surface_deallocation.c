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

#include "surface_deallocation.h"

struct RenpySurfaceDeallocation {
    SDL_Surface *surface;
    RenpySurfaceDeallocation *next;
};

#if RENPY_SURFACE_DEALLOCATION_THREADED
static SDL_Mutex *mutex;
static SDL_Condition *condition;
static SDL_Thread *thread;
static RenpySurfaceDeallocation *head;
static RenpySurfaceDeallocation *tail;
static bool stopping;

static int SDLCALL destroy_surfaces(void *userdata)
{
    (void) userdata;

    SDL_LockMutex(mutex);

    for (;;) {
        while (!head && !stopping) {
            SDL_WaitCondition(condition, mutex);
        }

        if (!head) {
            SDL_UnlockMutex(mutex);
            return 0;
        }

        RenpySurfaceDeallocation *entry = head;
        head = entry->next;
        if (!head) {
            tail = NULL;
        }

        SDL_UnlockMutex(mutex);
        SDL_DestroySurface(entry->surface);
        SDL_free(entry);
        SDL_LockMutex(mutex);
    }
}
#endif

bool renpy_surface_deallocation_init(void)
{
#if RENPY_SURFACE_DEALLOCATION_THREADED
    if (thread) {
        return true;
    }

    mutex = SDL_CreateMutex();
    if (!mutex) {
        return false;
    }

    condition = SDL_CreateCondition();
    if (condition) {
        stopping = false;
        thread = SDL_CreateThread(destroy_surfaces, "surface destruction", NULL);
        if (thread) {
            return true;
        }
    }

    char error[1024];
    SDL_strlcpy(error, SDL_GetError(), sizeof(error));
    SDL_DestroyCondition(condition);
    condition = NULL;
    SDL_DestroyMutex(mutex);
    mutex = NULL;
    SDL_SetError("%s", error);
    return false;
#else
    return true;
#endif
}

void renpy_surface_deallocation_quit(void)
{
#if RENPY_SURFACE_DEALLOCATION_THREADED
    if (!thread) {
        return;
    }

    SDL_LockMutex(mutex);
    stopping = true;
    SDL_SignalCondition(condition);
    SDL_UnlockMutex(mutex);

    /* The caller can retain the GIL while joining: the worker needs only SDL. */
    SDL_WaitThread(thread, NULL);
    thread = NULL;

    SDL_DestroyCondition(condition);
    condition = NULL;
    SDL_DestroyMutex(mutex);
    mutex = NULL;
#endif
}

RenpySurfaceDeallocation *renpy_surface_deallocation_new(void)
{
    RenpySurfaceDeallocation *entry = SDL_malloc(sizeof(*entry));
    if (!entry) {
        SDL_OutOfMemory();
    }
    return entry;
}

void renpy_surface_deallocation_discard(RenpySurfaceDeallocation *entry)
{
    SDL_free(entry);
}

void renpy_surface_deallocation_enqueue(RenpySurfaceDeallocation *entry, SDL_Surface *surface)
{
#if RENPY_SURFACE_DEALLOCATION_THREADED
    if (thread) {
        entry->surface = surface;
        entry->next = NULL;

        SDL_LockMutex(mutex);
        if (tail) {
            tail->next = entry;
        } else {
            head = entry;
        }
        tail = entry;
        SDL_SignalCondition(condition);
        SDL_UnlockMutex(mutex);
        return;
    }
#endif

    SDL_DestroySurface(surface);
    SDL_free(entry);
}
