#include "assimpio.h"

#include <assimp/cfileio.h>
#include <assimp/cimport.h>
#include <stdint.h>
#include <stdlib.h>

static size_t assimpio_read(struct aiFile *file, char *buffer, size_t size, size_t count);
static size_t assimpio_write(struct aiFile *file, const char *buffer, size_t size, size_t count);
static size_t assimpio_tell(struct aiFile *file);
static size_t assimpio_file_size(struct aiFile *file);
static aiReturn assimpio_seek(struct aiFile *file, size_t offset, enum aiOrigin origin);
static void assimpio_flush(struct aiFile *file);

static struct aiFile *assimpio_open(struct aiFileIO *io, const char *filename, const char *mode) {
    SDL_IOStream *stream;
    struct aiFile *file;

    (void)io;
    (void)mode;

    stream = assimp_load(filename);
    if (stream == NULL) {
        return NULL;
    }

    file = malloc(sizeof(*file));
    if (file == NULL) {
        SDL_CloseIO(stream);
        return NULL;
    }

    file->ReadProc = assimpio_read;
    file->WriteProc = assimpio_write;
    file->TellProc = assimpio_tell;
    file->FileSizeProc = assimpio_file_size;
    file->SeekProc = assimpio_seek;
    file->FlushProc = assimpio_flush;
    file->UserData = (char *)stream;

    return file;
}

static size_t assimpio_read(struct aiFile *file, char *buffer, size_t size, size_t count) {
    SDL_IOStream *stream = (SDL_IOStream *)file->UserData;

    if (size == 0 || count > SIZE_MAX / size) {
        return 0;
    }

    return SDL_ReadIO(stream, buffer, size * count) / size;
}

static size_t assimpio_write(struct aiFile *file, const char *buffer, size_t size, size_t count) {
    (void)file;
    (void)buffer;
    (void)size;
    (void)count;
    return 0;
}

static size_t assimpio_tell(struct aiFile *file) {
    return (size_t)SDL_TellIO((SDL_IOStream *)file->UserData);
}

static size_t assimpio_file_size(struct aiFile *file) {
    Sint64 size = SDL_GetIOSize((SDL_IOStream *)file->UserData);
    return size < 0 ? 0 : (size_t)size;
}

static aiReturn assimpio_seek(struct aiFile *file, size_t offset, enum aiOrigin origin) {
    SDL_IOWhence whence;

    switch (origin) {
    case aiOrigin_SET:
        whence = SDL_IO_SEEK_SET;
        break;
    case aiOrigin_CUR:
        whence = SDL_IO_SEEK_CUR;
        break;
    case aiOrigin_END:
        whence = SDL_IO_SEEK_END;
        break;
    default:
        return aiReturn_FAILURE;
    }

    return SDL_SeekIO((SDL_IOStream *)file->UserData, (Sint64)offset, whence) < 0
        ? aiReturn_FAILURE
        : aiReturn_SUCCESS;
}

static void assimpio_flush(struct aiFile *file) {
    SDL_FlushIO((SDL_IOStream *)file->UserData);
}

static void assimpio_close(struct aiFileIO *io, struct aiFile *file) {
    (void)io;
    SDL_CloseIO((SDL_IOStream *)file->UserData);
    free(file);
}

static void assimpio_init(struct aiFileIO *io) {
    io->OpenProc = assimpio_open;
    io->CloseProc = assimpio_close;
    io->UserData = NULL;
}

const struct aiScene *assimpio_import(const char *filename, unsigned int flags) {
    struct aiFileIO io;

    assimpio_init(&io);
    return aiImportFileEx(filename, flags, &io);
}
