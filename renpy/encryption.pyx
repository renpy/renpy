# Copyright 2004-2024 Tom Rothamel <pytom@bishoujo.us>
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

from libc.stdint cimport uint8_t, uint64_t
from libc.stddef cimport size_t

cdef extern from "libhydrogen/hydrogen.c":

    enum:
        hydro_secretbox_HEADERBYTES
        hydro_secretbox_KEYBYTES

    int hydro_init()

    int hydro_secretbox_encrypt(uint8_t *c, const void *m_, size_t mlen, uint64_t msg_id,
                                const char    ctx[8],
                                const uint8_t key[32])

    int hydro_secretbox_decrypt(void *m_, const uint8_t *c, size_t clen, uint64_t msg_id,
                                const char    ctx[8],
                                const uint8_t key[32])

    pass

if hydro_init() != 0:
    raise ImportError("Failed to initialize libhydrogen.")

SECRETBOX_KEYBYTES = hydro_secretbox_KEYBYTES

def secretbox_encrypt(bytes message, bytes key):
    """
    Encrypts the given message and returns the ciphertext.

    Keys must be 32 bytes long.
    """

    if len(key) != hydro_secretbox_KEYBYTES:
        raise ValueError("Key must be %d bytes" % hydro_secretbox_KEYBYTES)

    cdef bytearray cyphertext = bytearray(hydro_secretbox_HEADERBYTES + len(message))

    if hydro_secretbox_encrypt(<uint8_t *> <char *> cyphertext, <char *> message, len(message), 0, b"shirocat", <const uint8_t *> <char *> key) != 0:
        raise ValueError("Encryption failed")

    return bytes(cyphertext)

def secretbox_decrypt(bytes cyphertext, bytes key):
    """
    Decrypts the given cyphertext and returns the message.

    Keys must be 32 bytes long.
    """

    if len(key) != hydro_secretbox_KEYBYTES:
        raise ValueError("Key must be %d bytes" % hydro_secretbox_KEYBYTES)

    cdef bytearray message = bytearray(len(cyphertext) - hydro_secretbox_HEADERBYTES)

    if hydro_secretbox_decrypt(<char *> message, <const uint8_t *> <char *> cyphertext, len(cyphertext), 0, b"shirocat", <const uint8_t *> <char *> key) != 0:
        raise ValueError("Decryption failed")

    return bytes(message)
