#include "rpa_packer.h"
#include "rpa_encryption.h"
#include <zlib.h>
#include <string.h>
#include <stdlib.h>
#include <stdio.h>

#define RPA_HEADER_V3 "RPA-3.0 "
#define RPA_PADDING "Made with Ren'Py."
#define INITIAL_CAPACITY 1024
#define ZLIB_CHUNK 16384

static const char* error_strings[] = {
    "Success",
    "File not found",
    "File write error",
    "Out of memory",
    "Zlib compression error",
    "Invalid path",
    "Entry already exists"
};

const char* rpa_packer_error_string(int error) {
    if (error >= RPA_PACKER_OK && error <= RPA_PACKER_ERROR_ENTRY_EXISTS) {
        return error_strings[-error];
    }
    return "Unknown error";
}

static int rpa_packer_entry_exists(RPAPacker* packer, const char* name) {
    for (int i = 0; i < packer->entry_count; i++) {
        if (packer->entry_names[i] && strcmp(packer->entry_names[i], name) == 0) {
            return 1;
        }
    }
    return 0;
}

static int rpa_packer_grow_entries(RPAPacker* packer) {
    int new_capacity = packer->entry_capacity * 2;
    if (new_capacity < INITIAL_CAPACITY) {
        new_capacity = INITIAL_CAPACITY;
    }

    RPAPackerEntry* new_entries = (RPAPackerEntry*)realloc(packer->entries, sizeof(RPAPackerEntry) * new_capacity);
    if (!new_entries) {
        return RPA_PACKER_ERROR_OUT_OF_MEMORY;
    }

    char** new_entry_names = (char**)realloc(packer->entry_names, sizeof(char*) * new_capacity);
    if (!new_entry_names) {
        free(new_entries);
        return RPA_PACKER_ERROR_OUT_OF_MEMORY;
    }

    packer->entries = new_entries;
    packer->entry_names = new_entry_names;
    packer->entry_capacity = new_capacity;

    return RPA_PACKER_OK;
}

static int rpa_packer_add_entry(RPAPacker* packer, const char* name, uint64_t offset, uint64_t length, const char* start_data, size_t start_data_length) {
    if (rpa_packer_entry_exists(packer, name)) {
        return RPA_PACKER_ERROR_ENTRY_EXISTS;
    }

    if (packer->entry_count >= packer->entry_capacity) {
        int result = rpa_packer_grow_entries(packer);
        if (result != RPA_PACKER_OK) {
            return result;
        }
    }

    packer->entry_names[packer->entry_count] = strdup(name);
    if (!packer->entry_names[packer->entry_count]) {
        return RPA_PACKER_ERROR_OUT_OF_MEMORY;
    }

    packer->entries[packer->entry_count].offset = offset;
    packer->entries[packer->entry_count].length = length;

    if (start_data && start_data_length > 0) {
        packer->entries[packer->entry_count].start_data = (char*)malloc(start_data_length);
        if (!packer->entries[packer->entry_count].start_data) {
            free(packer->entry_names[packer->entry_count]);
            return RPA_PACKER_ERROR_OUT_OF_MEMORY;
        }
        memcpy(packer->entries[packer->entry_count].start_data, start_data, start_data_length);
        packer->entries[packer->entry_count].start_data_length = start_data_length;
    } else {
        packer->entries[packer->entry_count].start_data = NULL;
        packer->entries[packer->entry_count].start_data_length = 0;
    }

    packer->entry_count++;
    return RPA_PACKER_OK;
}

static size_t rpa_packer_compress_data(const uint8_t* data, size_t data_len, uint8_t** out_compressed) {
    z_stream strm;
    strm.zalloc = Z_NULL;
    strm.zfree = Z_NULL;
    strm.opaque = Z_NULL;
    strm.avail_in = data_len;
    strm.next_in = (Bytef*)data;

    if (deflateInit(&strm, Z_BEST_COMPRESSION) != Z_OK) {
        return 0;
    }

    uint8_t* compressed = (uint8_t*)malloc(ZLIB_CHUNK);
    if (!compressed) {
        deflateEnd(&strm);
        return 0;
    }

    size_t total_compressed = 0;
    int ret;

    do {
        strm.avail_out = ZLIB_CHUNK;
        strm.next_out = compressed + total_compressed;

        ret = deflate(&strm, Z_FINISH);

        if (ret != Z_STREAM_END && ret != Z_OK) {
            free(compressed);
            deflateEnd(&strm);
            return 0;
        }

        size_t just_compressed = ZLIB_CHUNK - strm.avail_out;
        total_compressed += just_compressed;

        if (ret == Z_STREAM_END) {
            break;
        }

        if (strm.avail_out == 0) {
            uint8_t* new_buffer = (uint8_t*)realloc(compressed, total_compressed + ZLIB_CHUNK);
            if (!new_buffer) {
                free(compressed);
                deflateEnd(&strm);
                return 0;
            }
            compressed = new_buffer;
        }

    } while (ret != Z_STREAM_END);

    deflateEnd(&strm);

    uint8_t* final_buffer = (uint8_t*)realloc(compressed, total_compressed);
    if (!final_buffer && total_compressed > 0) {
        free(compressed);
        return 0;
    }

    *out_compressed = final_buffer ? final_buffer : compressed;
    return total_compressed;
}

static size_t rpa_packer_build_index(RPAPacker* packer, uint8_t** out_index_data) {
    size_t index_size = 0;
    index_size += 4; // entry count

    for (int i = 0; i < packer->entry_count; i++) {
        index_size += 4; // name length
        index_size += strlen(packer->entry_names[i]);
        index_size += 8; // offset
        index_size += 8; // length
        index_size += 4; // start data length
        index_size += packer->entries[i].start_data_length;
    }

    uint8_t* index_data = (uint8_t*)malloc(index_size);
    if (!index_data) {
        return 0;
    }

    size_t pos = 0;
    uint32_t entry_count = packer->entry_count ^ (uint32_t)packer->key;
    memcpy(index_data + pos, &entry_count, 4);
    pos += 4;

    for (int i = 0; i < packer->entry_count; i++) {
        const char* name = packer->entry_names[i];
        uint32_t name_len = strlen(name) ^ (uint32_t)packer->key;
        memcpy(index_data + pos, &name_len, 4);
        pos += 4;

        memcpy(index_data + pos, name, strlen(name));
        pos += strlen(name);

        uint64_t offset = packer->entries[i].offset ^ packer->key;
        memcpy(index_data + pos, &offset, 8);
        pos += 8;

        uint64_t length = packer->entries[i].length ^ packer->key;
        memcpy(index_data + pos, &length, 8);
        pos += 8;

        uint32_t start_data_len = packer->entries[i].start_data_length ^ (uint32_t)packer->key;
        memcpy(index_data + pos, &start_data_len, 4);
        pos += 4;

        if (packer->entries[i].start_data && packer->entries[i].start_data_length > 0) {
            memcpy(index_data + pos, packer->entries[i].start_data, packer->entries[i].start_data_length);
            pos += packer->entries[i].start_data_length;
        }
    }

    *out_index_data = index_data;
    return index_size;
}

int rpa_packer_create(const char* output_path, RPAOptions* options, RPAPacker** out_packer) {
    if (!output_path || !out_packer) {
        return RPA_PACKER_ERROR_INVALID_PATH;
    }

    // Initialize encryption system
    if (rpa_encryption_init() != RPA_ENCRYPTION_OK) {
        return RPA_PACKER_ERROR_ZLIB_ERROR;
    }

    FILE* file = fopen(output_path, "wb");
    if (!file) {
        return RPA_PACKER_ERROR_FILE_NOT_FOUND;
    }

    RPAPacker* packer = (RPAPacker*)calloc(1, sizeof(RPAPacker));
    if (!packer) {
        fclose(file);
        return RPA_PACKER_ERROR_OUT_OF_MEMORY;
    }

    packer->output_path = strdup(output_path);
    if (!packer->output_path) {
        fclose(file);
        free(packer);
        return RPA_PACKER_ERROR_OUT_OF_MEMORY;
    }

    packer->file = file;
    packer->entry_capacity = INITIAL_CAPACITY;
    packer->entries = (RPAPackerEntry*)malloc(sizeof(RPAPackerEntry) * packer->entry_capacity);
    packer->entry_names = (char**)malloc(sizeof(char*) * packer->entry_capacity);

    if (!packer->entries || !packer->entry_names) {
        rpa_packer_close(packer);
        return RPA_PACKER_ERROR_OUT_OF_MEMORY;
    }

    if (options && options->key != 0) {
        packer->key = options->key;
    } else {
        packer->key = 0x42424242;
    }

    packer->is_open = true;

    char padding[40];
    snprintf(padding, sizeof(padding), "RPA-3.0 %016llx %08llx\n", 0ULL, (unsigned long long)packer->key);
    if (fwrite(padding, 1, 39, file) != 39) {
        rpa_packer_close(packer);
        return RPA_PACKER_ERROR_FILE_WRITE;
    }

    *out_packer = packer;
    return RPA_PACKER_OK;
}

int rpa_packer_add_file(RPAPacker* packer, const char* name, const char* path) {
    if (!packer || !name || !path) {
        return RPA_PACKER_ERROR_INVALID_PATH;
    }

    if (!packer->is_open) {
        return RPA_PACKER_ERROR_FILE_WRITE;
    }

    FILE* input_file = fopen(path, "rb");
    if (!input_file) {
        return RPA_PACKER_ERROR_FILE_NOT_FOUND;
    }

    fseek(input_file, 0, SEEK_END);
    size_t file_size = ftell(input_file);
    fseek(input_file, 0, SEEK_SET);

    uint8_t* data = (uint8_t*)malloc(file_size);
    if (!data) {
        fclose(input_file);
        return RPA_PACKER_ERROR_OUT_OF_MEMORY;
    }

    if (fread(data, 1, file_size, input_file) != file_size) {
        free(data);
        fclose(input_file);
        return RPA_PACKER_ERROR_FILE_NOT_FOUND;
    }

    int result = rpa_packer_add_data(packer, name, data, file_size);
    
    free(data);
    fclose(input_file);
    
    return result;
}

int rpa_packer_add_data(RPAPacker* packer, const char* name, const uint8_t* data, size_t len) {
    if (!packer || !name || !data) {
        return RPA_PACKER_ERROR_INVALID_PATH;
    }

    if (!packer->is_open) {
        return RPA_PACKER_ERROR_FILE_WRITE;
    }

    if (fwrite(RPA_PADDING, 1, strlen(RPA_PADDING), packer->file) != strlen(RPA_PADDING)) {
        return RPA_PACKER_ERROR_FILE_WRITE;
    }

    uint64_t offset = ftell(packer->file);
    if (offset < 0) {
        return RPA_PACKER_ERROR_FILE_WRITE;
    }

    if (fwrite(data, 1, len, packer->file) != len) {
        return RPA_PACKER_ERROR_FILE_WRITE;
    }

    return rpa_packer_add_entry(packer, name, offset, len, NULL, 0);
}

int rpa_packer_close(RPAPacker* packer) {
    if (!packer) {
        return RPA_PACKER_OK;
    }

    if (packer->is_open) {
        packer->index_offset = ftell(packer->file);
        if (packer->index_offset < 0) {
            packer->is_open = false;
            return RPA_PACKER_ERROR_FILE_WRITE;
        }

        uint8_t* index_data;
        size_t index_size = rpa_packer_build_index(packer, &index_data);
        if (index_size == 0) {
            packer->is_open = false;
            return RPA_PACKER_ERROR_OUT_OF_MEMORY;
        }

        uint8_t* compressed_index;
        size_t compressed_size = rpa_packer_compress_data(index_data, index_size, &compressed_index);
        free(index_data);

        if (compressed_size == 0) {
            packer->is_open = false;
            return RPA_PACKER_ERROR_ZLIB_ERROR;
        }

        if (fwrite(compressed_index, 1, compressed_size, packer->file) != compressed_size) {
            free(compressed_index);
            packer->is_open = false;
            return RPA_PACKER_ERROR_FILE_WRITE;
        }

        free(compressed_index);

        rewind(packer->file);
        char header[40];
        snprintf(header, sizeof(header), "RPA-3.0 %016llx %08llx\n", 
                 (unsigned long long)packer->index_offset, 
                 (unsigned long long)packer->key);
        if (fwrite(header, 1, 39, packer->file) != 39) {
            packer->is_open = false;
            return RPA_PACKER_ERROR_FILE_WRITE;
        }

        fclose(packer->file);
        packer->file = NULL;
        packer->is_open = false;
    }

    if (packer->entries) {
        for (int i = 0; i < packer->entry_count; i++) {
            if (packer->entries[i].start_data) {
                free(packer->entries[i].start_data);
            }
        }
        free(packer->entries);
    }

    if (packer->entry_names) {
        for (int i = 0; i < packer->entry_count; i++) {
            if (packer->entry_names[i]) {
                free(packer->entry_names[i]);
            }
        }
        free(packer->entry_names);
    }

    if (packer->output_path) {
        free(packer->output_path);
    }

    free(packer);
    return RPA_PACKER_OK;
}
