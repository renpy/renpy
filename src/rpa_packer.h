#ifndef RENPY_RPA_PACKER_H
#define RENPY_RPA_PACKER_H

#include <Python.h>
#include <stdint.h>
#include <stdbool.h>

#ifdef __cplusplus
extern "C" {
#endif

#define RPA_PACKER_VERSION_3 3
#define RPA_PACKER_MAX_PATH 4096

typedef struct {
    uint64_t offset;
    uint64_t length;
    char* start_data;
    size_t start_data_length;
} RPAPackerEntry;

typedef struct {
    char* output_path;
    FILE* file;
    RPAPackerEntry* entries;
    char** entry_names;
    int entry_count;
    int entry_capacity;
    uint64_t key;
    uint64_t index_offset;
    bool is_open;
} RPAPacker;

#include "rpa_encryption.h"

typedef struct {
    int version;
    uint64_t key;
    bool compress_index;
    int compression_level;
    bool encrypt_index;
    uint8_t encryption_key[RPA_ENCRYPTION_KEY_SIZE];
} RPAOptions;

typedef enum {
    RPA_PACKER_OK = 0,
    RPA_PACKER_ERROR_FILE_NOT_FOUND = -1,
    RPA_PACKER_ERROR_FILE_WRITE = -2,
    RPA_PACKER_ERROR_OUT_OF_MEMORY = -3,
    RPA_PACKER_ERROR_ZLIB_ERROR = -4,
    RPA_PACKER_ERROR_INVALID_PATH = -5,
    RPA_PACKER_ERROR_ENTRY_EXISTS = -6
} RPAPackerError;

int rpa_packer_create(const char* output_path, RPAOptions* options, RPAPacker** out_packer);
int rpa_packer_add_file(RPAPacker* packer, const char* name, const char* path);
int rpa_packer_add_data(RPAPacker* packer, const char* name, const uint8_t* data, size_t len);
int rpa_packer_close(RPAPacker* packer);

const char* rpa_packer_error_string(int error);

#ifdef __cplusplus
}
#endif

#endif
