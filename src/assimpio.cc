#include "assimpio.h"
#include <assimp/IOStream.hpp>
#include <stdio.h>

// RenpyIOStream

class RenpyIOStream : public Assimp::IOStream {
public:
    SDL_RWops *rw;

    RenpyIOStream(SDL_RWops *rw) : rw(rw) {}
    ~RenpyIOStream();

    size_t Read(void *pvBuffer, size_t pSize, size_t pCount);
    size_t Write(const void *pvBuffer, size_t pSize, size_t pCount);
    aiReturn Seek(size_t pOffset, aiOrigin pOrigin);
    size_t Tell() const;
    size_t FileSize() const;
    void Flush();
};

RenpyIOStream::~RenpyIOStream() {
    SDL_RWclose(rw);
}

size_t RenpyIOStream::Read(void *pvBuffer, size_t pSize, size_t pCount) {
    return SDL_RWread(rw, pvBuffer, pSize, pCount);
}

size_t RenpyIOStream::Write(const void *pvBuffer, size_t pSize, size_t pCount) {
    return -1;
}

aiReturn RenpyIOStream::Seek(size_t pOffset, aiOrigin pOrigin) {
    return SDL_RWseek(rw, pOffset, pOrigin) == -1 ? aiReturn_FAILURE : aiReturn_SUCCESS;
}

size_t RenpyIOStream::Tell() const {
    return SDL_RWtell(rw);
}

size_t RenpyIOStream::FileSize() const {
    return SDL_RWsize(rw);
}

void RenpyIOStream::Flush() {
    return;
}

// RenpyIOSystem

bool RenpyIOSystem::Exists(const char *pFile) const {
    return assimp_loadable(pFile);
}

char RenpyIOSystem::getOsSeparator() const {
    return '/';
}

Assimp::IOStream *RenpyIOSystem::Open(const char *pFile, const char *pMode) {
    SDL_RWops *rw = assimp_load(pFile);

    if (!rw) {
        return nullptr;
    }

    return new RenpyIOStream(rw);
}

void RenpyIOSystem::Close(Assimp::IOStream *pFile) {
    delete pFile;
}
