# Copyright 2026 B.Kats and Tom Rothamel <pytom@bishoujo.us>
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


########################################
## WARNING for when editing this file ##
########################################

# This file contain functions that need to support async handling for the web build
# Renaming or reordering any functions will break the async handling
# The cython generated names for the following functions need to be listed
# in the ASYNCIFY_ONLY list: (tasks/renpython.py; 2 names for each function)
# - generate_private_key
# - sign_data
# - verify_data
# - get_public_key_from_private
# - validate_private_key
# - validate_public_key

from libc.stdlib cimport free
import base64

cdef extern from "ec_sign_core.h":
    int ECSign(const unsigned char *priv_key_der, size_t key_len, const char *data, size_t data_len, char *signature, size_t signature_len);
    int ECVerify(const unsigned char *public_key_der, size_t key_len, const char *data, size_t data_len, char *signature, size_t signature_len);

    void ECGeneratePrivateKey(unsigned char **priv_key_der, size_t *priv_len);
    void ECGetPublicKeyFromPrivate(const unsigned char *priv_key_der, size_t priv_len, unsigned char **public_key_der, size_t *pub_len);

    int ECValidateKey(int public, const unsigned char *key_der, size_t key_len);

def generate_private_key() -> bytes | None:
    cdef unsigned char* privkey = NULL
    cdef size_t privlen = 0

    ECGeneratePrivateKey(&privkey, &privlen)

    rv = None
    if privlen > 0 and privkey != NULL:
        rv = bytes(privkey[:privlen])

    free(privkey);

    return rv

def sign_data(data : bytes, private_key : bytes) -> bytes:
    sign = bytes(64)

    if not ECSign(private_key, len(private_key), data, len(data), sign, len(sign)):
        raise Exception("Failed to sign data");

    # print(" ".join("{:02x}".format(x) for x in sign))
    return sign

def verify_data(data : bytes, public_key : bytes, sign : bytes) -> bool:
    # print(" ".join("{:02x}".format(x) for x in sign))
    return ECVerify(public_key, len(public_key), data, len(data), sign, len(sign))

def get_public_key_from_private(private_key : bytes) -> bytes | None:
    cdef unsigned char* pubkey = NULL
    cdef size_t publen = 0

    ECGetPublicKeyFromPrivate(private_key, len(private_key), &pubkey, &publen)

    rv = None
    if publen > 0 and pubkey != NULL:
        rv = bytes(pubkey[:publen])

    free(pubkey)

    return rv

def validate_private_key(private_key : bytes) -> bool:
    return ECValidateKey(0, private_key, len(private_key))

def validate_public_key(public_key : bytes) -> bool:
    return ECValidateKey(1, public_key, len(public_key))

def _pem_lines(contents: bytes) -> typing.Iterator[bytes]:
    in_pem_part = False
    seen_pem_start = False

    for line in contents.splitlines():
        line = line.strip()

        # Skip empty lines
        if not line:
            continue

        # Handle start marker
        if line.startswith(b'-----BEGIN'):
            if in_pem_part:
                raise ValueError('Seen start marker twice')

            in_pem_part = True
            seen_pem_start = True
            continue

        # Skip stuff before first marker
        if not in_pem_part:
            continue

        # Handle end marker
        if in_pem_part and line.startswith(b'-----END'):
            in_pem_part = False
            break

        # Load fields
        if b":" in line:
            continue

        yield line

    # Do some sanity checks
    if not seen_pem_start:
        raise ValueError('No PEM start marker found')

    if in_pem_part:
        raise ValueError('No PEM end marker found')

def pem_to_der(pem : bytes | str) -> bytes:
    if isinstance(pem, str):  # pragma: no branch
        pem = pem.encode()

    d = b"".join(_pem_lines(pem))
    return base64.b64decode(d)


def der_to_pem(der : bytes, name : str) -> bytes:
    b64 = base64.b64encode(der)
    lines = [("-----BEGIN %s KEY-----\n" % name).encode()]
    lines.extend(
        [b64[start : start + 76] + b"\n" for start in range(0, len(b64), 76)]
    )
    lines.append(("-----END %s KEY-----\n" % name).encode())
    return b"".join(lines)
