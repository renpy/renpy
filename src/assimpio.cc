#include "assimpio.h"
#include <assimp/IOStream.hpp>
#include <stdio.h>

// RenpyIOStream

class RenpyIOStream : public Assimp::IOStream {
public:
    SDL_IOStream *rw;

    RenpyIOStream(SDL_IOStream *rw) : rw(rw) {}
    ~RenpyIOStream();

    size_t Read(void *pvBuffer, size_t pSize, size_t pCount);
    size_t Write(const void *pvBuffer, size_t pSize, size_t pCount);
    aiReturn Seek(size_t pOffset, aiOrigin pOrigin);
    size_t Tell() const;
    size_t FileSize() const;
    void Flush();
};

RenpyIOStream::~RenpyIOStream() {
    SDL_CloseIO(rw);
}

size_t RenpyIOStream::Read(void *pvBuffer, size_t pSize, size_t pCount) {
    return SDL_ReadIO(rw, pvBuffer, pSize * pCount);
}

size_t RenpyIOStream::Write(const void *pvBuffer, size_t pSize, size_t pCount) {
    return -1;
}

aiReturn RenpyIOStream::Seek(size_t pOffset, aiOrigin pOrigin) {
    return SDL_SeekIO(rw, pOffset, (SDL_IOWhence)pOrigin) == -1 ? aiReturn_FAILURE : aiReturn_SUCCESS;
}

size_t RenpyIOStream::Tell() const {
    return SDL_TellIO(rw);
}

size_t RenpyIOStream::FileSize() const {
    return (size_t)SDL_GetIOSize(rw);
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
    SDL_IOStream *rw = assimp_load(pFile);

    if (!rw) {
        return nullptr;
    }

    return new RenpyIOStream(rw);
}

void RenpyIOSystem::Close(Assimp::IOStream *pFile) {
    delete pFile;
}
