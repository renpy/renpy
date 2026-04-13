#ifndef RENPY_RPA_ARCHIVE_H
#define RENPY_RPA_ARCHIVE_H

#include <Python.h>
#include <SDL2/SDL.h>
#include <stdint.h>
#include <stdbool.h>

#ifdef __cplusplus
extern "C" {
#endif

#define RPA_VERSION_1 1
#define RPA_VERSION_2 2
#define RPA_VERSION_3 3

#define RPA_MAX_PATH 4096

typedef struct {
    uint64_t offset;
    uint64_t length;
    char* start;
} RPAEntry;

typedef struct {
    char* filename;
    int version;
    SDL_RWops* file;
    uint64_t index_offset;
    uint64_t key;
    RPAEntry* entries;
    char** entry_names;
    int entry_count;
    bool is_open;
} RPAArchive;

typedef enum {
    RPA_OK = 0,
    RPA_ERROR_FILE_NOT_FOUND = -1,
    RPA_ERROR_INVALID_HEADER = -2,
    RPA_ERROR_INDEX_CORRUPT = -3,
    RPA_ERROR_ENTRY_NOT_FOUND = -4,
    RPA_ERROR_READ_ERROR = -5,
    RPA_ERROR_ZLIB_ERROR = -6,
    RPA_ERROR_OUT_OF_MEMORY = -7
} RPAError;

int rpa_archive_open(const char* path, RPAArchive** out_archive);
int rpa_archive_open_v3(const char* path, RPAArchive** out_archive);
int rpa_archive_open_v2(const char* path, RPAArchive** out_archive);
int rpa_archive_open_v1(const char* path, RPAArchive** out_archive);

void rpa_archive_close(RPAArchive* archive);

int rpa_archive_read_entry(RPAArchive* archive, const char* name, uint8_t** out_data, size_t* out_len);
int rpa_archive_has_entry(RPAArchive* archive, const char* name);

const char* rpa_archive_error_string(int error);

int rpa_archive_get_entry_count(RPAArchive* archive);
const char* rpa_archive_get_entry_name(RPAArchive* archive, int index);

#ifdef __cplusplus
}
#endif

#endif
