#ifndef WRITE_PNG_H
#define WRITE_PNG_H

#include <SDL.h>

int Pygame_SDL2_SavePNG(const char *file, SDL_Surface *surf,int compression);
int Pygame_SDL2_SavePNG_RW(SDL_RWops *src, SDL_Surface *surf,int compression);

#endif
