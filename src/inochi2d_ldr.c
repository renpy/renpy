#include "inochi2d.h"
#include <SDL2/SDL.h>
#include <stdio.h>
#include <string.h>

// NOTE:    Inochi2D does not support web yet until it becomes fully nogc.
//          This will change in later releases and this file will be updated
//          accordingly.

void *load_inochi2d_object(const char *sofile) {
    void *handle = SDL_LoadObject(sofile);
    return handle;
}

void *load_inochi2d_function(void *obj, const char *name) {
    void *func = SDL_LoadFunction(obj, name);
    return func;
}
