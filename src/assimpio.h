#pragma once

#include <SDL3/SDL.h>
#include <assimp/scene.h>

SDL_IOStream *assimp_load(const char *filename);

const struct aiScene *assimpio_import(const char *filename, unsigned int flags);
