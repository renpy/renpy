#include "rpa_encryption.h"
#include <zlib.h>
#include <string.h>
#include <stdlib.h>

#define HYDROGEN_IMPLEMENTATION
#include "libhydrogen/hydrogen.h"

static const char* error_strings[] = {
    "Success",
    "Invalid key",
    "Encryption failed",
    "Decryption failed",
    "Out of memory",
    "Invalid data"
};

const char* rpa_encryption_error_string(int error) {
    if (error >= RPA_ENCRYPTION_OK && error <= RPA_ENCRYPTION_ERROR_INVALID_DATA) {
        return error_strings[-error];
    }
    return "Unknown error";
}

int rpa_encryption_init(void) {
    if (hydro_init() != 0) {
        return RPA_ENCRYPTION_ERROR_ENCRYPTION_FAILED;
    }
    return RPA_ENCRYPTION_OK;
}

int rpa_encryption_encrypt(const uint8_t* data, size_t len, const uint8_t* key, uint8_t** out_encrypted, size_t* out_len) {
    if (!data || !key || !out_encrypted || !out_len) {
        return RPA_ENCRYPTION_ERROR_INVALID_DATA;
    }

    if (len == 0) {
        *out_encrypted = NULL;
        *out_len = 0;
        return RPA_ENCRYPTION_OK;
    }

    size_t encrypted_len = hydro_secretbox_HEADERBYTES + len;
    uint8_t* encrypted = (uint8_t*)malloc(encrypted_len);
    if (!encrypted) {
        return RPA_ENCRYPTION_ERROR_OUT_OF_MEMORY;
    }

    int result = hydro_secretbox_encrypt(
        encrypted,
        data,
        len,
        0,
        RPA_ENCRYPTION_CONTEXT,
        key
    );

    if (result != 0) {
        free(encrypted);
        return RPA_ENCRYPTION_ERROR_ENCRYPTION_FAILED;
    }

    *out_encrypted = encrypted;
    *out_len = encrypted_len;
    return RPA_ENCRYPTION_OK;
}

int rpa_encryption_decrypt(const uint8_t* encrypted, size_t len, const uint8_t* key, uint8_t** out_decrypted, size_t* out_len) {
    if (!encrypted || !key || !out_decrypted || !out_len) {
        return RPA_ENCRYPTION_ERROR_INVALID_DATA;
    }

    if (len < hydro_secretbox_HEADERBYTES) {
        return RPA_ENCRYPTION_ERROR_INVALID_DATA;
    }

    size_t decrypted_len = len - hydro_secretbox_HEADERBYTES;
    uint8_t* decrypted = (uint8_t*)malloc(decrypted_len);
    if (!decrypted) {
        return RPA_ENCRYPTION_ERROR_OUT_OF_MEMORY;
    }

    int result = hydro_secretbox_decrypt(
        decrypted,
        encrypted,
        len,
        0,
        RPA_ENCRYPTION_CONTEXT,
        key
    );

    if (result != 0) {
        free(decrypted);
        return RPA_ENCRYPTION_ERROR_DECRYPTION_FAILED;
    }

    *out_decrypted = decrypted;
    *out_len = decrypted_len;
    return RPA_ENCRYPTION_OK;
}

int rpa_encryption_derive_key(const char* password, uint8_t* out_key) {
    if (!password || !out_key) {
        return RPA_ENCRYPTION_ERROR_INVALID_KEY;
    }

    hydro_hash_state state;
    hydro_hash_init(&state, RPA_ENCRYPTION_CONTEXT, NULL);
    hydro_hash_update(&state, (const uint8_t*)password, strlen(password));
    hydro_hash_final(&state, out_key, RPA_ENCRYPTION_KEY_SIZE);

    return RPA_ENCRYPTION_OK;
}

bool rpa_encryption_is_encrypted(const uint8_t* data, size_t len) {
    if (!data || len < hydro_secretbox_HEADERBYTES) {
        return false;
    }

    return true;
}
