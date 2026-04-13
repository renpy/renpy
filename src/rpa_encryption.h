#ifndef RENPY_RPA_ENCRYPTION_H
#define RENPY_RPA_ENCRYPTION_H

#include <Python.h>
#include <stdint.h>
#include <stdbool.h>

#ifdef __cplusplus
extern "C" {
#endif

#define RPA_ENCRYPTION_KEY_SIZE 32
#define RPA_ENCRYPTION_HEADER_SIZE 16
#define RPA_ENCRYPTION_CONTEXT "shirocat"

typedef enum {
    RPA_ENCRYPTION_OK = 0,
    RPA_ENCRYPTION_ERROR_INVALID_KEY = -1,
    RPA_ENCRYPTION_ERROR_ENCRYPTION_FAILED = -2,
    RPA_ENCRYPTION_ERROR_DECRYPTION_FAILED = -3,
    RPA_ENCRYPTION_ERROR_OUT_OF_MEMORY = -4,
    RPA_ENCRYPTION_ERROR_INVALID_DATA = -5
} RPAEncryptionError;

int rpa_encryption_init(void);
int rpa_encryption_encrypt(const uint8_t* data, size_t len, const uint8_t* key, uint8_t** out_encrypted, size_t* out_len);
int rpa_encryption_decrypt(const uint8_t* encrypted, size_t len, const uint8_t* key, uint8_t** out_decrypted, size_t* out_len);
int rpa_encryption_derive_key(const char* password, uint8_t* out_key);
bool rpa_encryption_is_encrypted(const uint8_t* data, size_t len);

const char* rpa_encryption_error_string(int error);

#ifdef __cplusplus
}
#endif

#endif
