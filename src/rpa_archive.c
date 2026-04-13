#include "rpa_archive.h"
#include <zlib.h>
#include <string.h>
#include <stdlib.h>
#include <stdio.h>

#define RPA_HEADER_V3 "RPA-3.0 "
#define RPA_HEADER_V2 "RPA-2.0 "
#define RPA_HEADER_V1 "\x78\x9c"

#define ZLIB_CHUNK 16384

static const char* error_strings[] = {
    "Success",
    "File not found",
    "Invalid archive header",
    "Index data corrupted",
    "Entry not found in archive",
    "Read error while accessing archive",
    "Zlib decompression error",
    "Out of memory"
};

const char* rpa_archive_error_string(int error) {
    if (error >= RPA_OK && error <= RPA_ERROR_OUT_OF_MEMORY) {
        return error_strings[-error];
    }
    return "Unknown error";
}

static uint64_t parse_hex_uint64(const char* str, int len) {
    uint64_t result = 0;
    for (int i = 0; i < len; i++) {
        result <<= 4;
        char c = str[i];
        if (c >= '0' && c <= '9') {
            result |= (c - '0');
        } else if (c >= 'a' && c <= 'f') {
            result |= (c - 'a' + 10);
        } else if (c >= 'A' && c <= 'F') {
            result |= (c - 'A' + 10);
        }
    }
    return result;
}

static int read_file_header(SDL_RWops* file, char* header, int max_len) {
    if (SDL_RWread(file, header, 1, max_len) != (size_t)max_len) {
        return 0;
    }
    return 1;
}

static uint8_t* decompress_zlib_data(const uint8_t* compressed, size_t compressed_len, size_t* out_decompressed_len) {
    if (compressed_len == 0) {
        *out_decompressed_len = 0;
        return NULL;
    }

    z_stream strm;
    strm.zalloc = Z_NULL;
    strm.zfree = Z_NULL;
    strm.opaque = Z_NULL;
    strm.avail_in = compressed_len;
    strm.next_in = (Bytef*)compressed;

    if (inflateInit(&strm) != Z_OK) {
        return NULL;
    }

    uint8_t* decompressed = (uint8_t*)malloc(ZLIB_CHUNK);
    if (!decompressed) {
        inflateEnd(&strm);
        return NULL;
    }

    size_t total_decompressed = 0;
    int ret;

    do {
        strm.avail_out = ZLIB_CHUNK;
        strm.next_out = decompressed + total_decompressed;

        ret = inflate(&strm, Z_FINISH);

        if (ret != Z_STREAM_END && ret != Z_OK) {
            free(decompressed);
            inflateEnd(&strm);
            return NULL;
        }

        size_t just_decompressed = ZLIB_CHUNK - strm.avail_out;
        total_decompressed += just_decompressed;

        if (ret == Z_STREAM_END) {
            break;
        }

        if (strm.avail_out == 0) {
            uint8_t* new_buffer = (uint8_t*)realloc(decompressed, total_decompressed + ZLIB_CHUNK);
            if (!new_buffer) {
                free(decompressed);
                inflateEnd(&strm);
                return NULL;
            }
            decompressed = new_buffer;
        }

    } while (ret != Z_STREAM_END);

    inflateEnd(&strm);
    *out_decompressed_len = total_decompressed;

    uint8_t* final_buffer = (uint8_t*)realloc(decompressed, total_decompressed);
    if (!final_buffer && total_decompressed > 0) {
        free(decompressed);
        return NULL;
    }

    return final_buffer ? final_buffer : decompressed;
}

static int read_v3_index(RPAArchive* archive) {
    char header[40];
    if (SDL_RWread(archive->file, header, 1, 40) != 40) {
        return RPA_ERROR_INVALID_HEADER;
    }

    archive->index_offset = parse_hex_uint64(header + 8, 16);
    archive->key = parse_hex_uint64(header + 25, 8);

    if (SDL_RWseek(archive->file, (Sint64)archive->index_offset, RW_SEEK_SET) < 0) {
        return RPA_ERROR_READ_ERROR;
    }

    Sint64 remaining = SDL_RWsize(archive->file) - SDL_RWtell(archive->file);
    if (remaining <= 0) {
        return RPA_ERROR_INVALID_HEADER;
    }

    size_t compressed_len = (size_t)remaining;
    uint8_t* compressed = (uint8_t*)malloc(compressed_len);
    if (!compressed) {
        return RPA_ERROR_OUT_OF_MEMORY;
    }

    size_t read_len = SDL_RWread(archive->file, compressed, 1, compressed_len);
    if (read_len != compressed_len) {
        free(compressed);
        return RPA_ERROR_READ_ERROR;
    }

    size_t decompressed_len;
    uint8_t* decompressed = decompress_zlib_data(compressed, compressed_len, &decompressed_len);
    free(compressed);

    if (!decompressed) {
        return RPA_ERROR_ZLIB_ERROR;
    }

    size_t pos = 0;
    int entry_count = 0;

    while (pos + 4 <= decompressed_len) {
        uint32_t num_entries = *(uint32_t*)(decompressed + pos);
        entry_count = num_entries ^ (uint32_t)archive->key;
        pos += 4;

        if (entry_count < 0 || entry_count > 100000) {
            free(decompressed);
            return RPA_ERROR_INDEX_CORRUPT;
        }
        break;
    }

    archive->entries = (RPAEntry*)malloc(sizeof(RPAEntry) * entry_count);
    archive->entry_names = (char**)malloc(sizeof(char*) * entry_count);

    if (!archive->entries || !archive->entry_names) {
        free(decompressed);
        return RPA_ERROR_OUT_OF_MEMORY;
    }

    for (int i = 0; i < entry_count; i++) {
        if (pos + 12 > decompressed_len) {
            free(decompressed);
            return RPA_ERROR_INDEX_CORRUPT;
        }

        uint32_t name_len;
        memcpy(&name_len, decompressed + pos, 4);
        name_len ^= (uint32_t)archive->key;
        pos += 4;

        if (name_len >= RPA_MAX_PATH || pos + name_len > decompressed_len) {
            free(decompressed);
            return RPA_ERROR_INDEX_CORRUPT;
        }

        archive->entry_names[i] = (char*)malloc(name_len + 1);
        if (!archive->entry_names[i]) {
            free(decompressed);
            return RPA_ERROR_OUT_OF_MEMORY;
        }

        memcpy(archive->entry_names[i], decompressed + pos, name_len);
        archive->entry_names[i][name_len] = '\0';
        pos += name_len;

        if (pos + 8 > decompressed_len) {
            free(decompressed);
            return RPA_ERROR_INDEX_CORRUPT;
        }

        uint64_t offset, length;
        memcpy(&offset, decompressed + pos, 8);
        offset ^= archive->key;
        pos += 8;

        memcpy(&length, decompressed + pos, 8);
        length ^= archive->key;
        pos += 8;

        archive->entries[i].offset = offset;
        archive->entries[i].length = length;
        archive->entries[i].start = NULL;

        if (pos + 4 <= decompressed_len) {
            uint32_t start_len = *(uint32_t*)(decompressed + pos);
            start_len ^= (uint32_t)archive->key;
            pos += 4;

            if (start_len > 0 && start_len < 4096 && pos + start_len <= decompressed_len) {
                archive->entries[i].start = (char*)malloc(start_len);
                if (archive->entries[i].start) {
                    memcpy(archive->entries[i].start, decompressed + pos, start_len);
                }
            }
        }
    }

    free(decompressed);
    archive->entry_count = entry_count;
    return RPA_OK;
}

static int read_v2_index(RPAArchive* archive) {
    char header[24];
    if (SDL_RWread(archive->file, header, 1, 24) != 24) {
        return RPA_ERROR_INVALID_HEADER;
    }

    archive->index_offset = parse_hex_uint64(header + 8, 16);

    if (SDL_RWseek(archive->file, (Sint64)archive->index_offset, RW_SEEK_SET) < 0) {
        return RPA_ERROR_READ_ERROR;
    }

    Sint64 remaining = SDL_RWsize(archive->file) - SDL_RWtell(archive->file);
    if (remaining <= 0) {
        return RPA_ERROR_INVALID_HEADER;
    }

    size_t compressed_len = (size_t)remaining;
    uint8_t* compressed = (uint8_t*)malloc(compressed_len);
    if (!compressed) {
        return RPA_ERROR_OUT_OF_MEMORY;
    }

    size_t read_len = SDL_RWread(archive->file, compressed, 1, compressed_len);
    if (read_len != compressed_len) {
        free(compressed);
        return RPA_ERROR_READ_ERROR;
    }

    size_t decompressed_len;
    uint8_t* decompressed = decompress_zlib_data(compressed, compressed_len, &decompressed_len);
    free(compressed);

    if (!decompressed) {
        return RPA_ERROR_ZLIB_ERROR;
    }

    size_t pos = 0;
    int entry_count = 0;

    while (pos + 4 <= decompressed_len) {
        uint32_t num_entries = *(uint32_t*)(decompressed + pos);
        entry_count = num_entries;
        pos += 4;

        if (entry_count < 0 || entry_count > 100000) {
            free(decompressed);
            return RPA_ERROR_INDEX_CORRUPT;
        }
        break;
    }

    archive->entries = (RPAEntry*)malloc(sizeof(RPAEntry) * entry_count);
    archive->entry_names = (char**)malloc(sizeof(char*) * entry_count);

    if (!archive->entries || !archive->entry_names) {
        free(decompressed);
        return RPA_ERROR_OUT_OF_MEMORY;
    }

    for (int i = 0; i < entry_count; i++) {
        if (pos + 4 > decompressed_len) {
            free(decompressed);
            return RPA_ERROR_INDEX_CORRUPT;
        }

        uint32_t name_len = *(uint32_t*)(decompressed + pos);
        pos += 4;

        if (name_len >= RPA_MAX_PATH || pos + name_len > decompressed_len) {
            free(decompressed);
            return RPA_ERROR_INDEX_CORRUPT;
        }

        archive->entry_names[i] = (char*)malloc(name_len + 1);
        if (!archive->entry_names[i]) {
            free(decompressed);
            return RPA_ERROR_OUT_OF_MEMORY;
        }

        memcpy(archive->entry_names[i], decompressed + pos, name_len);
        archive->entry_names[i][name_len] = '\0';
        pos += name_len;

        if (pos + 16 > decompressed_len) {
            free(decompressed);
            return RPA_ERROR_INDEX_CORRUPT;
        }

        uint64_t offset, length;
        memcpy(&offset, decompressed + pos, 8);
        pos += 8;

        memcpy(&length, decompressed + pos, 8);
        pos += 8;

        archive->entries[i].offset = offset;
        archive->entries[i].length = length;
        archive->entries[i].start = NULL;
    }

    free(decompressed);
    archive->entry_count = entry_count;
    return RPA_OK;
}

static int read_v1_index(RPAArchive* archive) {
    Sint64 remaining = SDL_RWsize(archive->file) - SDL_RWtell(archive->file);
    if (remaining <= 0) {
        return RPA_ERROR_INVALID_HEADER;
    }

    size_t compressed_len = (size_t)remaining;
    uint8_t* compressed = (uint8_t*)malloc(compressed_len);
    if (!compressed) {
        return RPA_ERROR_OUT_OF_MEMORY;
    }

    size_t read_len = SDL_RWread(archive->file, compressed, 1, compressed_len);
    if (read_len != compressed_len) {
        free(compressed);
        return RPA_ERROR_READ_ERROR;
    }

    size_t decompressed_len;
    uint8_t* decompressed = decompress_zlib_data(compressed, compressed_len, &decompressed_len);
    free(compressed);

    if (!decompressed) {
        return RPA_ERROR_ZLIB_ERROR;
    }

    size_t pos = 0;
    int entry_count = 0;

    while (pos + 4 <= decompressed_len) {
        uint32_t num_entries = *(uint32_t*)(decompressed + pos);
        entry_count = num_entries;
        pos += 4;

        if (entry_count < 0 || entry_count > 100000) {
            free(decompressed);
            return RPA_ERROR_INDEX_CORRUPT;
        }
        break;
    }

    archive->entries = (RPAEntry*)malloc(sizeof(RPAEntry) * entry_count);
    archive->entry_names = (char**)malloc(sizeof(char*) * entry_count);

    if (!archive->entries || !archive->entry_names) {
        free(decompressed);
        return RPA_ERROR_OUT_OF_MEMORY;
    }

    for (int i = 0; i < entry_count; i++) {
        if (pos + 4 > decompressed_len) {
            free(decompressed);
            return RPA_ERROR_INDEX_CORRUPT;
        }

        uint32_t name_len = *(uint32_t*)(decompressed + pos);
        pos += 4;

        if (name_len >= RPA_MAX_PATH || pos + name_len > decompressed_len) {
            free(decompressed);
            return RPA_ERROR_INDEX_CORRUPT;
        }

        archive->entry_names[i] = (char*)malloc(name_len + 1);
        if (!archive->entry_names[i]) {
            free(decompressed);
            return RPA_ERROR_OUT_OF_MEMORY;
        }

        memcpy(archive->entry_names[i], decompressed + pos, name_len);
        archive->entry_names[i][name_len] = '\0';
        pos += name_len;

        if (pos + 8 > decompressed_len) {
            free(decompressed);
            return RPA_ERROR_INDEX_CORRUPT;
        }

        uint64_t offset, length;
        memcpy(&offset, decompressed + pos, 8);
        pos += 8;

        memcpy(&length, decompressed + pos, 8);
        pos += 8;

        archive->entries[i].offset = offset;
        archive->entries[i].length = length;
        archive->entries[i].start = NULL;
    }

    free(decompressed);
    archive->entry_count = entry_count;
    return RPA_OK;
}

int rpa_archive_open(const char* path, RPAArchive** out_archive) {
    if (!path || !out_archive) {
        return RPA_ERROR_FILE_NOT_FOUND;
    }

    SDL_RWops* file = SDL_RWFromFile(path, "rb");
    if (!file) {
        return RPA_ERROR_FILE_NOT_FOUND;
    }

    char header[16];
    if (SDL_RWread(file, header, 1, 8) != 8) {
        SDL_RWclose(file);
        return RPA_ERROR_INVALID_HEADER;
    }

    if (SDL_RWseek(file, 0, RW_SEEK_SET) < 0) {
        SDL_RWclose(file);
        return RPA_ERROR_READ_ERROR;
    }

    if (strncmp(header, RPA_HEADER_V3, 7) == 0) {
        return rpa_archive_open_v3(path, out_archive);
    } else if (strncmp(header, RPA_HEADER_V2, 7) == 0) {
        return rpa_archive_open_v2(path, out_archive);
    } else if (header[0] == '\x78' && header[1] == '\x9c') {
        return rpa_archive_open_v1(path, out_archive);
    }

    SDL_RWclose(file);
    return RPA_ERROR_INVALID_HEADER;
}

int rpa_archive_open_v3(const char* path, RPAArchive** out_archive) {
    SDL_RWops* file = SDL_RWFromFile(path, "rb");
    if (!file) {
        return RPA_ERROR_FILE_NOT_FOUND;
    }

    RPAArchive* archive = (RPAArchive*)calloc(1, sizeof(RPAArchive));
    if (!archive) {
        SDL_RWclose(file);
        return RPA_ERROR_OUT_OF_MEMORY;
    }

    archive->filename = (char*)malloc(strlen(path) + 1);
    if (!archive->filename) {
        SDL_RWclose(file);
        free(archive);
        return RPA_ERROR_OUT_OF_MEMORY;
    }
    strcpy(archive->filename, path);
    archive->file = file;
    archive->version = RPA_VERSION_3;
    archive->is_open = true;

    int result = read_v3_index(archive);
    if (result != RPA_OK) {
        rpa_archive_close(archive);
        return result;
    }

    *out_archive = archive;
    return RPA_OK;
}

int rpa_archive_open_v2(const char* path, RPAArchive** out_archive) {
    SDL_RWops* file = SDL_RWFromFile(path, "rb");
    if (!file) {
        return RPA_ERROR_FILE_NOT_FOUND;
    }

    RPAArchive* archive = (RPAArchive*)calloc(1, sizeof(RPAArchive));
    if (!archive) {
        SDL_RWclose(file);
        return RPA_ERROR_OUT_OF_MEMORY;
    }

    archive->filename = (char*)malloc(strlen(path) + 1);
    if (!archive->filename) {
        SDL_RWclose(file);
        free(archive);
        return RPA_ERROR_OUT_OF_MEMORY;
    }
    strcpy(archive->filename, path);
    archive->file = file;
    archive->version = RPA_VERSION_2;
    archive->is_open = true;

    int result = read_v2_index(archive);
    if (result != RPA_OK) {
        rpa_archive_close(archive);
        return result;
    }

    *out_archive = archive;
    return RPA_OK;
}

int rpa_archive_open_v1(const char* path, RPAArchive** out_archive) {
    SDL_RWops* file = SDL_RWFromFile(path, "rb");
    if (!file) {
        return RPA_ERROR_FILE_NOT_FOUND;
    }

    RPAArchive* archive = (RPAArchive*)calloc(1, sizeof(RPAArchive));
    if (!archive) {
        SDL_RWclose(file);
        return RPA_ERROR_OUT_OF_MEMORY;
    }

    archive->filename = (char*)malloc(strlen(path) + 1);
    if (!archive->filename) {
        SDL_RWclose(file);
        free(archive);
        return RPA_ERROR_OUT_OF_MEMORY;
    }
    strcpy(archive->filename, path);
    archive->file = file;
    archive->version = RPA_VERSION_1;
    archive->is_open = true;

    int result = read_v1_index(archive);
    if (result != RPA_OK) {
        rpa_archive_close(archive);
        return result;
    }

    *out_archive = archive;
    return RPA_OK;
}

void rpa_archive_close(RPAArchive* archive) {
    if (!archive) {
        return;
    }

    if (archive->entries) {
        for (int i = 0; i < archive->entry_count; i++) {
            if (archive->entries[i].start) {
                free(archive->entries[i].start);
            }
        }
        free(archive->entries);
    }

    if (archive->entry_names) {
        for (int i = 0; i < archive->entry_count; i++) {
            if (archive->entry_names[i]) {
                free(archive->entry_names[i]);
            }
        }
        free(archive->entry_names);
    }

    if (archive->file) {
        SDL_RWclose(archive->file);
    }

    if (archive->filename) {
        free(archive->filename);
    }

    archive->is_open = false;
    free(archive);
}

int rpa_archive_has_entry(RPAArchive* archive, const char* name) {
    if (!archive || !name) {
        return 0;
    }

    for (int i = 0; i < archive->entry_count; i++) {
        if (archive->entry_names[i] && strcmp(archive->entry_names[i], name) == 0) {
            return 1;
        }
    }
    return 0;
}

int rpa_archive_read_entry(RPAArchive* archive, const char* name, uint8_t** out_data, size_t* out_len) {
    if (!archive || !name || !out_data || !out_len) {
        return RPA_ERROR_ENTRY_NOT_FOUND;
    }

    int entry_index = -1;
    for (int i = 0; i < archive->entry_count; i++) {
        if (archive->entry_names[i] && strcmp(archive->entry_names[i], name) == 0) {
            entry_index = i;
            break;
        }
    }

    if (entry_index < 0) {
        return RPA_ERROR_ENTRY_NOT_FOUND;
    }

    RPAEntry* entry = &archive->entries[entry_index];

    if (entry->start && entry->length == 0) {
        size_t start_len = strlen(entry->start);
        *out_data = (uint8_t*)malloc(start_len);
        if (!*out_data) {
            return RPA_ERROR_OUT_OF_MEMORY;
        }
        memcpy(*out_data, entry->start, start_len);
        *out_len = start_len;
        return RPA_OK;
    }

    if (SDL_RWseek(archive->file, (Sint64)entry->offset, RW_SEEK_SET) < 0) {
        return RPA_ERROR_READ_ERROR;
    }

    uint8_t* data = (uint8_t*)malloc((size_t)entry->length);
    if (!data) {
        return RPA_ERROR_OUT_OF_MEMORY;
    }

    size_t read_len = SDL_RWread(archive->file, data, 1, (size_t)entry->length);
    if (read_len != (size_t)entry->length) {
        free(data);
        return RPA_ERROR_READ_ERROR;
    }

    *out_data = data;
    *out_len = (size_t)entry->length;
    return RPA_OK;
}

int rpa_archive_get_entry_count(RPAArchive* archive) {
    if (!archive) {
        return 0;
    }
    return archive->entry_count;
}

const char* rpa_archive_get_entry_name(RPAArchive* archive, int index) {
    if (!archive || index < 0 || index >= archive->entry_count) {
        return NULL;
    }
    return archive->entry_names[index];
}
