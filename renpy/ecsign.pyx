# Copyright 2004-2025 Tom Rothamel <pytom@bishoujo.us>
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

from libc.stdlib cimport free
import base64

cdef extern from "ec_sign_core.h":
    int SignDer(const unsigned char *priv_key_der, size_t key_len, const char *data, size_t data_len, char *signature, size_t signature_len);
    int VerifyDer(const unsigned char *public_key_der, size_t key_len, const char *data, size_t data_len, char *signature, size_t signature_len);

    void GeneratePrivateKey(unsigned char **priv_key_der, size_t *priv_len);
    void GetPublicKeyFromPrivate(const unsigned char *priv_key_der, size_t priv_len, unsigned char **public_key_der, size_t *pub_len);

    int VerifyKeyDer(int public, const unsigned char *key_der, size_t key_len);

def GeneratePrivateKeyAsDER() -> bytes | None:
    cdef unsigned char* privkey = NULL
    cdef size_t privlen = 0

    GeneratePrivateKey(&privkey, &privlen)

    rv = None
    if privlen > 0 and privkey != NULL:
        rv = bytes(privkey[:privlen])

    free(privkey);

    return rv

def SignDataWithDER(data : bytes, private_key : bytes) -> bytes:
    sign = bytes(64)

    if not SignDer(private_key, len(private_key), data, len(data), sign, len(sign)):
        raise Exception("Failed to sign data");

    # print(" ".join("{:02x}".format(x) for x in sign))
    return sign

def VerifyDataWithDER(data : bytes, public_key : bytes, sign : bytes) -> bool:
    # print(" ".join("{:02x}".format(x) for x in sign))
    return VerifyDer(public_key, len(public_key), data, len(data), sign, len(sign))

def GetPublicKeyFromPrivateDER(private_key : bytes) -> bytes | None:
    cdef unsigned char* pubkey = NULL
    cdef size_t publen = 0

    GetPublicKeyFromPrivate(private_key, len(private_key), &pubkey, &publen)

    rv = None
    if publen > 0 and pubkey != NULL:
        rv = bytes(pubkey[:publen])

    free(pubkey);

    return rv

def VerifyPrivateKeyDER(private_key : bytes) -> bool:
    return VerifyKeyDer(0, private_key, len(private_key))

def VerifyPublicKeyDER(public_key : bytes) -> bool:
    return VerifyKeyDer(1, public_key, len(public_key))

def PEMtoDER(pem : bytes | str) -> bytes:
    if isinstance(pem, str):  # pragma: no branch
        pem = pem.encode()
    d = b"".join(
        [
            l.strip()
            for l in pem.split(b"\n")
            if l and not l.startswith(b"-----")
        ]
    )
    return base64.b64decode(d)


def DERtoPEM(der : bytes, name : str) -> bytes:
    b64 = base64.b64encode(der)
    lines = [("-----BEGIN %s KEY-----\n" % name).encode()]
    lines.extend(
        [b64[start : start + 76] + b"\n" for start in range(0, len(b64), 76)]
    )
    lines.append(("-----END %s KEY-----\n" % name).encode())
    return b"".join(lines)
