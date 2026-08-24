/*
 Copyright 2026 B.Kats and Tom Rothamel <pytom@bishoujo.us>

 Permission is hereby granted, free of charge, to any person
 obtaining a copy of this software and associated documentation files
 (the "Software"), to deal in the Software without restriction,
 including without limitation the rights to use, copy, modify, merge,
 publish, distribute, sublicense, and/or sell copies of the Software,
 and to permit persons to whom the Software is furnished to do so,
 subject to the following conditions:

 The above copyright notice and this permission notice shall be
 included in all copies or substantial portions of the Software.

 THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND,
 EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF
 MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND
 NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE
 LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION
 OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION
 WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
*/

#ifdef __EMSCRIPTEN__

#include <stdlib.h>
#include <string.h>
#include <emscripten.h>
#include <emscripten/console.h>

#include "ec_sign_core.h"

/*
*******************************
       Key conversion
*******************************
*/

/*
 * crypto.subtle only imports EC private keys as PKCS#8 PrivateKeyInfo, but
 * Ren'Py releases before this one stored what OpenSSL produces by default,
 * which is a bare SEC1 ECPrivateKey. Wrapping the latter keeps tokens created
 * by an older desktop build usable in the web build.
 */

// SEQUENCE { OID id-ecPublicKey, OID prime256v1 }
static const unsigned char EC_P256_ALGID[] = {
    0x30, 0x13,
    0x06, 0x07, 0x2a, 0x86, 0x48, 0xce, 0x3d, 0x02, 0x01,
    0x06, 0x08, 0x2a, 0x86, 0x48, 0xce, 0x3d, 0x03, 0x01, 0x07,
};

static size_t PutDerLength(unsigned char *out, size_t len)
{
    if (len < 0x80)
    {
        out[0] = (unsigned char)len;
        return 1;
    }

    if (len < 0x100)
    {
        out[0] = 0x81;
        out[1] = (unsigned char)len;
        return 2;
    }

    out[0] = 0x82;
    out[1] = (unsigned char)(len >> 8);
    out[2] = (unsigned char)len;
    return 3;
}

/*
 * Reads the DER element at *offset, advancing *offset past it. Returns the
 * tag and the range of the contents, or 0 if the element is malformed.
 */
static int ReadDerHeader(const unsigned char *der, size_t der_len, size_t *offset, size_t *content, size_t *content_len)
{
    size_t i = *offset;

    if (i + 2 > der_len)
    {
        return 0;
    }

    int tag = der[i++];
    size_t len = der[i++];

    if (len & 0x80)
    {
        size_t n = len & 0x7f;

        if (n == 0 || n > 4 || i + n > der_len)
        {
            return 0;
        }

        len = 0;

        while (n--)
        {
            len = (len << 8) | der[i++];
        }
    }

    if (len > der_len - i)
    {
        return 0;
    }

    *content = i;
    *content_len = len;
    *offset = i + len;

    return tag;
}

/*
 * Returns a malloc'd PKCS#8 PrivateKeyInfo holding `der`, or NULL if `der`
 * isn't a private key we recognize. A key that already is a PrivateKeyInfo is
 * copied unchanged, so the caller always owns the result.
 */
static unsigned char *ToPkcs8(const unsigned char *der, size_t der_len, size_t *out_len)
{
    *out_len = 0;

    size_t i = 0;
    size_t seq, seq_len;

    if (ReadDerHeader(der, der_len, &i, &seq, &seq_len) != 0x30)
    {
        return NULL;
    }

    // The version INTEGER tells the two apart: PrivateKeyInfo is version 0,
    // SEC1 ECPrivateKey is version 1.
    size_t ver, ver_len;
    i = seq;

    if (ReadDerHeader(der, der_len, &i, &ver, &ver_len) != 0x02 || ver_len != 1)
    {
        return NULL;
    }

    if (der[ver] == 0x00)
    {
        // Already what we want - hand back a copy, so the caller can free the
        // result either way.
        unsigned char *rv = (unsigned char *)malloc(der_len);

        if (rv != NULL)
        {
            memcpy(rv, der, der_len);
            *out_len = der_len;
        }

        return rv;
    }

    if (der[ver] != 0x01)
    {
        return NULL;
    }

    // Copy the ECPrivateKey, dropping its optional [0] parameters field. The
    // curve is named by the PrivateKeyInfo's AlgorithmIdentifier instead, and
    // RFC 5915 says the inner copy should go.
    unsigned char *inner = (unsigned char *)malloc(seq_len);

    if (inner == NULL)
    {
        return NULL;
    }

    size_t inner_len = 0;
    size_t end = seq + seq_len;

    i = seq;

    while (i < end)
    {
        size_t start = i;
        size_t content, content_len;

        if (!ReadDerHeader(der, end, &i, &content, &content_len))
        {
            free(inner);
            return NULL;
        }

        if (der[start] != 0xa0)
        {
            memcpy(inner + inner_len, der + start, i - start);
            inner_len += i - start;
        }
    }

    unsigned char inner_len_der[4];
    size_t inner_len_der_size = PutDerLength(inner_len_der, inner_len);

    // The ECPrivateKey SEQUENCE goes inside the privateKey OCTET STRING.
    size_t key_len = 1 + inner_len_der_size + inner_len;

    unsigned char key_len_der[4];
    size_t key_len_der_size = PutDerLength(key_len_der, key_len);

    size_t body_len = 3 + sizeof(EC_P256_ALGID) + 1 + key_len_der_size + key_len;

    unsigned char body_len_der[4];
    size_t body_len_der_size = PutDerLength(body_len_der, body_len);

    unsigned char *rv = (unsigned char *)malloc(1 + body_len_der_size + body_len);

    if (rv == NULL)
    {
        free(inner);
        return NULL;
    }

    size_t o = 0;

    rv[o++] = 0x30;
    memcpy(rv + o, body_len_der, body_len_der_size);
    o += body_len_der_size;

    // version
    rv[o++] = 0x02;
    rv[o++] = 0x01;
    rv[o++] = 0x00;

    memcpy(rv + o, EC_P256_ALGID, sizeof(EC_P256_ALGID));
    o += sizeof(EC_P256_ALGID);

    // privateKey
    rv[o++] = 0x04;
    memcpy(rv + o, key_len_der, key_len_der_size);
    o += key_len_der_size;

    rv[o++] = 0x30;
    memcpy(rv + o, inner_len_der, inner_len_der_size);
    o += inner_len_der_size;
    memcpy(rv + o, inner, inner_len);
    o += inner_len;

    free(inner);

    *out_len = o;
    return rv;
}

/*
*******************************
      Asynchronous JS
*******************************
*/

EM_ASYNC_JS(int, ecsign_GenerateKey, (char **key, int *len), {
    try
    {
        const keyPair = await crypto.subtle.generateKey(
            {
                name : "ECDSA",
                namedCurve : "P-256",
            },
            true,
            [ "sign", "verify" ]);

        const exported = await crypto.subtle.exportKey(
            "pkcs8",
            keyPair.privateKey);

        const privkey = new Uint8Array(exported);

        const buf = _malloc(privkey.length);
        HEAPU8.set(privkey, buf);

        setValue(len, privkey.length, 'i32');
        setValue(key, buf, 'i8*');
    }
    catch(e)
    {
        console.log(e);
        return 0;
    }
    return 1;
});

EM_ASYNC_JS(int, ecsign_CheckPrivateKey, (const char *key, int len), {
    try
    {
        const binaryDer = new Uint8Array(HEAPU8.buffer, key, len);
        const pkey = await crypto.subtle.importKey(
            "pkcs8",
            binaryDer,
            {
                name : "ECDSA",
                namedCurve : "P-256",
            },
            true,
            ["sign"]);
    }
    catch(e)
    {
        console.log(e);
        return 0;
    }
    return 1;
});

EM_ASYNC_JS(int, ecsign_CheckPublicKey, (const char *key, int len), {
    try
    {
        const binaryDer = new Uint8Array(HEAPU8.buffer, key, len);
        const pkey = await crypto.subtle.importKey(
            "spki",
            binaryDer,
            {
                name : "ECDSA",
                namedCurve : "P-256",
            },
            true,
            ["verify"]);
    }
    catch(e)
    {
        console.log(e);
        return 0;
    }
    return 1;
});

EM_ASYNC_JS(int, ecsign_Sign, (const char *key, int len, const char *data, int data_len, char *sign), {
    try
    {
        const binaryDer = new Uint8Array(HEAPU8.buffer, key, len);
        const pkey = await crypto.subtle.importKey(
            "pkcs8",
            binaryDer,
            {
                name : "ECDSA",
                namedCurve : "P-256",
            },
            true,
            ["sign"]);

        const msg = new Uint8Array(HEAPU8.buffer, data, data_len);
        let signature = await crypto.subtle.sign(
            {
                name : "ECDSA",
                hash : {name : "SHA-1"},
            },
            pkey,
            msg);
        HEAPU8.set(new Uint8Array(signature), sign);
    }
    catch(e)
    {
        console.log(e);
        return 0;
    }
    return 1;
});

EM_ASYNC_JS(int, ecsign_Verify, (const char *key, int len, const char *data, int data_len, const char *sign), {
    try
    {
        const binaryDer = new Uint8Array(HEAPU8.buffer, key, len);
        const pkey = await crypto.subtle.importKey(
            "spki",
            binaryDer,
            {
                name : "ECDSA",
                namedCurve : "P-256",
            },
            true,
            ["verify"]);

        const msg = new Uint8Array(HEAPU8.buffer, data, data_len);
        const signature = new Uint8Array(HEAPU8.buffer, sign, 64);
        const ok = await crypto.subtle.verify(
            {
                name : "ECDSA",
                hash : {name : "SHA-1"},
            },
            pkey,
            signature,
            msg);
        return ok ? 1 : 0;
    }
    catch(e)
    {
        console.log(e);
        return 0;
    }
    return 1;
});

EM_ASYNC_JS(int, ecsign_GetPublicKey, (const char *key, int len, char **pub, int *pub_len), {
    try
    {
        const binaryDer = new Uint8Array(HEAPU8.buffer, key, len);
        const privateKey = await crypto.subtle.importKey(
            "pkcs8",
            binaryDer,
            {
                name : "ECDSA",
                namedCurve : "P-256",
            },
            true,
            ["sign"]);

        const jwkPrivate = await crypto.subtle.exportKey("jwk", privateKey);
        delete jwkPrivate.d;
        jwkPrivate.key_ops = ["verify"];
        const publicKey = await crypto.subtle.importKey("jwk", jwkPrivate, {name : "ECDSA", namedCurve : "P-256"}, true, ["verify"]);

        const exported = await crypto.subtle.exportKey(
            "spki",
            publicKey);

        const pubkey = new Uint8Array(exported);
        const buf = _malloc(pubkey.length);
        HEAPU8.set(pubkey, buf);

        setValue(pub_len, pubkey.length, 'i32');
        setValue(pub, buf, 'i8*');
    }
    catch(e)
    {
        console.log(e);
        return 0;
    }
    return 1;
});

int ECSign(const unsigned char *priv_key_der, size_t key_len, const char *data, size_t data_len, char *signature, size_t signature_len)
{
    if (signature_len != 64)
        return 0;

    size_t pkcs8_len;
    unsigned char *pkcs8 = ToPkcs8(priv_key_der, key_len, &pkcs8_len);

    if (pkcs8 == NULL)
        return 0;

    int rv = ecsign_Sign((char *)pkcs8, (int)pkcs8_len, data, (int)data_len, signature);

    free(pkcs8);
    return rv;
}

int ECVerify(const unsigned char *public_key_der, size_t key_len, const char *data, size_t data_len, char *signature, size_t signature_len)
{
    if (signature_len != 64)
        return 0;
    return ecsign_Verify((char *)public_key_der, (int)key_len, data, (int)data_len, signature);
}

void ECGeneratePrivateKey(unsigned char **priv_key_der, size_t *priv_len)
{
    int len;
    emscripten_console_log("Key generated started");
    if (ecsign_GenerateKey((char **)priv_key_der, &len))
    {
        emscripten_console_log("Key generated successful");
        *priv_len = len;
    }
    else
    {
        emscripten_console_log("Key generated failed");
        *priv_len = 0;
        *priv_key_der = NULL;
    }
}

void ECGetPublicKeyFromPrivate(const unsigned char *priv_key_der, size_t priv_len, unsigned char **public_key_der, size_t *pub_len)
{
    int len;

    size_t pkcs8_len;
    unsigned char *pkcs8 = ToPkcs8(priv_key_der, priv_len, &pkcs8_len);

    if (pkcs8 != NULL && ecsign_GetPublicKey((char *)pkcs8, (int)pkcs8_len, (char **)public_key_der, &len))
    {
        *pub_len = len;
    }
    else
    {
        *pub_len = 0;
        *public_key_der = NULL;
    }

    free(pkcs8);
}

int ECValidateKey(int public, const unsigned char *key_der, size_t key_len)
{
    if (public)
    {
        return ecsign_CheckPublicKey((char *)key_der, (int)key_len);
    }

    size_t pkcs8_len;
    unsigned char *pkcs8 = ToPkcs8(key_der, key_len, &pkcs8_len);

    if (pkcs8 == NULL)
        return 0;

    int rv = ecsign_CheckPrivateKey((char *)pkcs8, (int)pkcs8_len);

    free(pkcs8);
    return rv;
}

#endif // __EMSCRIPTEN__
