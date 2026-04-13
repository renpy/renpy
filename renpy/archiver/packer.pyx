# Copyright 2004-2026 Tom Rothamel <pytom@bishoujo.us>
#
# Permission is hereby granted, free of charge, to any person
# obtaining a copy of this software and associated documentation files
# (the "Software"), to deal in the Software without restriction,
# including without limitation the rights to use, copy, modify, merge,
# publish, distribute, sublicense, and/or sell copies of the Software,
# and to permit persons to whom the Software is furnished to do so,
# subject to the following conditions:
#
# The above copyright notice and this permission notice shall be
# included in all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND,
# EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF
# MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND
# NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE
# LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION
# OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION
# WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.

from __future__ import print_function

cdef extern from "rpa_packer.h":
    ctypedef struct RPAPacker:
        pass

    ctypedef struct RPAOptions:
        int version
        uint64_t key
        bint compress_index
        int compression_level

    ctypedef enum RPAPackerError:
        RPA_PACKER_OK = 0
        RPA_PACKER_ERROR_FILE_NOT_FOUND = -1
        RPA_PACKER_ERROR_FILE_WRITE = -2
        RPA_PACKER_ERROR_OUT_OF_MEMORY = -3
        RPA_PACKER_ERROR_ZLIB_ERROR = -4
        RPA_PACKER_ERROR_INVALID_PATH = -5
        RPA_PACKER_ERROR_ENTRY_EXISTS = -6

    int rpa_packer_create(const char* output_path, RPAOptions* options, RPAPacker** out_packer)
    int rpa_packer_add_file(RPAPacker* packer, const char* name, const char* path)
    int rpa_packer_add_data(RPAPacker* packer, const char* name, const uint8_t* data, size_t len)
    int rpa_packer_close(RPAPacker* packer)
    const char* rpa_packer_error_string(int error)

cdef extern from "rpa_encryption.h":
    cdef int RPA_ENCRYPTION_KEY_SIZE
    int rpa_encryption_init()
    int rpa_encryption_encrypt(const uint8_t* data, size_t len, const uint8_t* key, uint8_t** out_encrypted, size_t* out_len)
    int rpa_encryption_decrypt(const uint8_t* encrypted, size_t len, const uint8_t* key, uint8_t** out_decrypted, size_t* out_len)
    int rpa_encryption_derive_key(const char* password, uint8_t* out_key)

cdef class RPAPacker:
    cdef RPAPacker* packer
    cdef bytes _output_path

    def __init__(self, output_path, key=0x42424242, encryption_key=None):
        cdef RPAOptions options
        cdef int result

        self._output_path = output_path.encode('utf-8') if isinstance(output_path, str) else output_path

        options.version = 3
        options.key = key
        options.compress_index = True
        options.compression_level = 9
        options.encrypt_index = (encryption_key is not None)
        
        if encryption_key:
            if len(encryption_key) != RPA_ENCRYPTION_KEY_SIZE:
                raise ValueError("Encryption key must be %d bytes" % RPA_ENCRYPTION_KEY_SIZE)
            memcpy(options.encryption_key, <const uint8_t*>encryption_key, RPA_ENCRYPTION_KEY_SIZE)
        else:
            memset(options.encryption_key, 0, RPA_ENCRYPTION_KEY_SIZE)

        result = rpa_packer_create(<const char*>self._output_path, &options, &self.packer)
        if result != RPA_PACKER_OK:
            raise Exception("Failed to create RPA packer: %s" % rpa_packer_error_string(result).decode('utf-8'))

    def add_file(self, name, path):
        cdef int result
        cdef bytes py_name
        cdef bytes py_path

        if not self.packer:
            raise Exception("Packer not initialized")

        py_name = name.encode('utf-8') if isinstance(name, str) else name
        py_path = path.encode('utf-8') if isinstance(path, str) else path

        result = rpa_packer_add_file(self.packer, <const char*>py_name, <const char*>py_path)
        if result != RPA_PACKER_OK:
            raise Exception("Failed to add file: %s" % rpa_packer_error_string(result).decode('utf-8'))

    def add_data(self, name, data):
        cdef int result
        cdef bytes py_name

        if not self.packer:
            raise Exception("Packer not initialized")

        py_name = name.encode('utf-8') if isinstance(name, str) else name

        result = rpa_packer_add_data(self.packer, <const char*>py_name, <const uint8_t*>data, len(data))
        if result != RPA_PACKER_OK:
            raise Exception("Failed to add data: %s" % rpa_packer_error_string(result).decode('utf-8'))

    def close(self):
        cdef int result

        if self.packer:
            result = rpa_packer_close(self.packer)
            self.packer = NULL
            if result != RPA_PACKER_OK:
                raise Exception("Failed to close packer: %s" % rpa_packer_error_string(result).decode('utf-8'))

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.close()

def create_rpa_packer(output_path, key=0x42424242, encryption_key=None):
    return RPAPacker(output_path, key, encryption_key)

def secretbox_encrypt(bytes message, bytes key):
    """
    Encrypts the given message using the RPA encryption system.
    """
    cdef int result
    cdef uint8_t* encrypted
    cdef size_t encrypted_len
    
    if len(key) != RPA_ENCRYPTION_KEY_SIZE:
        raise ValueError("Key must be %d bytes" % RPA_ENCRYPTION_KEY_SIZE)
    
    result = rpa_encryption_encrypt(<const uint8_t*>message, len(message), <const uint8_t*>key, &encrypted, &encrypted_len)
    if result != 0:
        raise ValueError("Encryption failed")
    
    try:
        return bytes(encrypted[:encrypted_len])
    finally:
        free(encrypted)

def secretbox_decrypt(bytes cyphertext, bytes key):
    """
    Decrypts the given cyphertext using the RPA encryption system.
    """
    cdef int result
    cdef uint8_t* decrypted
    cdef size_t decrypted_len
    
    if len(key) != RPA_ENCRYPTION_KEY_SIZE:
        raise ValueError("Key must be %d bytes" % RPA_ENCRYPTION_KEY_SIZE)
    
    result = rpa_encryption_decrypt(<const uint8_t*>cyphertext, len(cyphertext), <const uint8_t*>key, &decrypted, &decrypted_len)
    if result != 0:
        raise ValueError("Decryption failed")
    
    try:
        return bytes(decrypted[:decrypted_len])
    finally:
        free(decrypted)

def derive_key(str password):
    """
    Derives a encryption key from a password.
    """
    cdef int result
    cdef uint8_t key[RPA_ENCRYPTION_KEY_SIZE]
    
    result = rpa_encryption_derive_key(password.encode('utf-8'), key)
    if result != 0:
        raise ValueError("Key derivation failed")
    
    return bytes(key)

RPA_ENCRYPTION_KEY_SIZE = RPA_ENCRYPTION_KEY_SIZE

