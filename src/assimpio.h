#pragma once

#include <SDL2/SDL.h>
#include <assimp/IOSystem.hpp>

int assimp_loadable(const char *filename);
SDL_RWops *assimp_load(const char *filename);

class RenpyIOSystem : public Assimp::IOSystem {
public:
    bool Exists(const char *pFile) const;
    char getOsSeparator() const;
    Assimp::IOStream *Open(const char *pFile, const char *pMode = "rb");
    void Close(Assimp::IOStream *pFile);
};
