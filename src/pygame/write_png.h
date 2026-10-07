#ifndef WRITE_PNG_H
#define WRITE_PNG_H

#include <SDL3/SDL.h>

int Pygame_SDL3_SavePNG_IO(SDL_IOStream *src, SDL_Surface *surf,int compression);

#endif
