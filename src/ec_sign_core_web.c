/*
 Copyright 2025 B.Kats and Tom Rothamel <pytom@bishoujo.us>

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

#include <stdlib.h>
#include <emscripten.h>

#include "ec_sign_core.h"

EM_ASYNC_JS(int, generateKey, (char **key, int *len), {
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

EM_ASYNC_JS(int, CheckPrivateKey, (const char *key, int len), {
    try
    {
        const binaryDer = new Uint8Array(HEAPU8.buffer, key, len);
        pkey = await crypto.subtle.importKey(
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

EM_ASYNC_JS(int, CheckPublicKey, (const char *key, int len), {
    try
    {
        const binaryDer = new Uint8Array(HEAPU8.buffer, key, len);
        pkey = await crypto.subtle.importKey(
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

EM_ASYNC_JS(int, Sign, (const char *key, int len, const char *data, int data_len, char *sign), {
    try
    {
        const binaryDer = new Uint8Array(HEAPU8.buffer, key, len);
        pkey = await crypto.subtle.importKey(
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

EM_ASYNC_JS(int, Verify, (const char *key, int len, const char *data, int data_len, const char *sign), {
    try
    {
        const binaryDer = new Uint8Array(HEAPU8.buffer, key, len);
        pkey = await crypto.subtle.importKey(
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
        return await crypto.subtle.verify(
            {
                name : "ECDSA",
                hash : {name : "SHA-1"},
            },
            pkey,
            signature,
            msg);
    }
    catch(e)
    {
        console.log(e);
        return 0;
    }
    return 1;
});

EM_ASYNC_JS(int, GetPublicKey, (const char *key, int len, char **pub, int *pub_len), {
    try
    {
        const binaryDer = new Uint8Array(HEAPU8.buffer, key, len);
        privateKey = await crypto.subtle.importKey(
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

int SignDer(const unsigned char *priv_key_der, size_t key_len, const char *data, size_t data_len, char *signature, size_t signature_len)
{
    if (signature_len != 64)
        return 0;
    return Sign((char *)priv_key_der, (int)key_len, data, (int)data_len, signature);
}

int VerifyDer(const unsigned char *public_key_der, size_t key_len, const char *data, size_t data_len, char *signature, size_t signature_len)
{
    if (signature_len != 64)
        return 0;
    return Verify((char *)public_key_der, (int)key_len, data, (int)data_len, signature);
}

void GeneratePrivateKey(unsigned char **priv_key_der, size_t *priv_len)
{
    int len;
    if (generateKey((char **)priv_key_der, &len))
    {
        *priv_len = len;
    }
    else
    {
        *priv_len = 0;
        *priv_key_der = NULL;
    }
}

void GetPublicKeyFromPrivate(const unsigned char *priv_key_der, size_t priv_len, unsigned char **public_key_der, size_t *pub_len)
{
    int len;
    if (GetPublicKey((char *)priv_key_der, (int)priv_len, (char **)public_key_der, &len))
    {
        *pub_len = len;
    }
    else
    {
        *pub_len = 0;
        *public_key_der = NULL;
    }
}

int VerifyKeyDer(int public, const unsigned char *key_der, size_t key_len)
{
    if (public)
    {
        return CheckPublicKey((char *)key_der, (int)key_len);
    }
    else
    {
        return CheckPrivateKey((char *)key_der, (int)key_len);
    }
}
