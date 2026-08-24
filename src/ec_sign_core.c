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
#ifndef __EMSCRIPTEN__

#include "ec_sign_core.h"

#include <openssl/evp.h>
#include <openssl/decoder.h>
#include <openssl/encoder.h>
#include <openssl/err.h>
#include <openssl/core_names.h>

#include <string.h>

/*
*******************************
     Forward declarations
*******************************
*/

static EVP_PKEY *GetKeyFromDer(int public, const unsigned char *key_der, size_t key_len);
static int AddNumberToDER(char *der, int offset, const char *number);
static int GetNumberFromDER(const unsigned char *der, size_t der_len, size_t *offset, char *number);
static int Sign(EVP_PKEY *priv_key, const void *data, size_t data_len, void **sign, size_t *sign_len);
static int Verify(EVP_PKEY *pub_key, const void *data, size_t data_len, const void *sign, size_t sign_len);

/*
*******************************
      Global functions
*******************************
*/

int ECSign(const unsigned char *priv_key_der, size_t key_len, const char *data, size_t data_len, char *signature, size_t signature_len)
{
    char *sign = NULL;
    EVP_PKEY *pkey = NULL;
    int ret = 0;

    if (signature == NULL || signature_len != 64)
    {
        fprintf(stderr, "Parameter 'signature' should point to 64 bytes of memory to receive raw signature\n");
        goto cleanup;
    }

    // Get private key from DER
    pkey = GetKeyFromDer(0, priv_key_der, key_len);

    size_t sign_len;
    ret = Sign(pkey, data, data_len, (void **)&sign, &sign_len);

    if (ret)
    {
        // fprintf(stdout, "Calculated signature as DER:\n");
        // BIO_dump_indent_fp(stdout, sign, sign_len, 2);

        // The signature is a DER SEQUENCE of two INTEGERs, R and S. DER uses
        // the shortest possible encoding, so each of them is anywhere from 1
        // to 33 bytes long - it gains a leading 0 when the top bit is set, and
        // loses leading bytes when the value is small. Copy them out into the
        // fixed-width raw signature.

        size_t offset = 2;

        if (sign_len < 2 || ((unsigned char *)sign)[0] != 0x30)
        {
            fprintf(stderr, "Signature is not a DER SEQUENCE.\n");
            ret = 0;
        }
        else if (!GetNumberFromDER((unsigned char *)sign, sign_len, &offset, signature)      // R
                 || !GetNumberFromDER((unsigned char *)sign, sign_len, &offset, signature + 32)) // S
        {
            fprintf(stderr, "Could not parse the DER signature.\n");
            ret = 0;
        }
    }

cleanup:
    if (sign) {
        free(sign);
    }
    EVP_PKEY_free(pkey);
    return ret;
}

int ECVerify(const unsigned char *public_key_der, size_t key_len, const char *data, size_t data_len, char *signature, size_t signature_len)
{
    EVP_PKEY *pkey = NULL;
    int ret = 0;

    if (signature_len != 64)
    {
        fprintf(stderr, "sign size is %d bytes, but expect 64 bytes\n", (int)signature_len);
        goto cleanup;
    }

    // Get public key from DER
    pkey = GetKeyFromDer(1, public_key_der, key_len);

    // Convert signature to DER
    char der_sign[72];
    int offset = 2;
    // Set header (skip length)
    der_sign[0] = 0x30;
    // der_sign[1] = 0xXX; // length

    // Add R to DER
    offset = AddNumberToDER(der_sign, offset, signature + 0);
    // Add S to DER
    offset = AddNumberToDER(der_sign, offset, signature + 32);

    // Set total length
    der_sign[1] = offset - 2;

    // fprintf(stdout, "Provided signature as DER:\n");
    // BIO_dump_indent_fp(stdout, der_sign, 72, 2);

    ret = Verify(pkey, data, data_len, der_sign, offset);

cleanup:
    EVP_PKEY_free(pkey);
    return ret;
}

void ECGeneratePrivateKey(unsigned char **priv_key_der, size_t *priv_len)
{
    OSSL_ENCODER_CTX *ectx = NULL;
    EVP_PKEY *privkey = NULL;
    OSSL_PARAM params[3];
    EVP_PKEY_CTX *genctx = NULL;
    const char *curvename = "P-256"; // stands for prime256v1 which is also known as SECP256R1 & NIST256p
    int use_cofactordh = 1;

    genctx = EVP_PKEY_CTX_new_from_name(NULL, "EC", NULL);
    if (genctx == NULL)
    {
        fprintf(stderr, "EVP_PKEY_CTX_new_from_name() failed\n");
        goto cleanup;
    }

    if (EVP_PKEY_keygen_init(genctx) <= 0)
    {
        fprintf(stderr, "EVP_PKEY_keygen_init() failed\n");
        goto cleanup;
    }

    params[0] = OSSL_PARAM_construct_utf8_string(OSSL_PKEY_PARAM_GROUP_NAME,
                                                 (char *)curvename, 0);
    /*
     * This is an optional parameter.
     * For many curves where the cofactor is 1, setting this has no effect.
     */
    params[1] = OSSL_PARAM_construct_int(OSSL_PKEY_PARAM_USE_COFACTOR_ECDH,
                                         &use_cofactordh);
    params[2] = OSSL_PARAM_construct_end();
    if (!EVP_PKEY_CTX_set_params(genctx, params))
    {
        fprintf(stderr, "EVP_PKEY_CTX_set_params() failed\n");
        goto cleanup;
    }

    if (EVP_PKEY_generate(genctx, &privkey) <= 0)
    {
        fprintf(stderr, "EVP_PKEY_generate() failed\n");
        goto cleanup;
    }

    // char out_curvename[80];
    // if (EVP_PKEY_get_utf8_string_param(privkey, OSSL_PKEY_PARAM_GROUP_NAME,
    //                                    out_curvename, sizeof(out_curvename),
    //                                    NULL))
    // {
    //     fprintf(stdout, "Curve name: %s\n", out_curvename);
    // }

    // Convert private key to DER. The output structure has to be named
    // explicitly - the default for EC is the type-specific SEC1 ECPrivateKey,
    // which crypto.subtle in the web build can't import.
    ectx = OSSL_ENCODER_CTX_new_for_pkey(privkey, EVP_PKEY_KEYPAIR, "DER", "PrivateKeyInfo", NULL);
    if (OSSL_ENCODER_to_data(ectx, priv_key_der, priv_len) <= 0)
    {
        fprintf(stderr, "Failed to get private key as DER\n");
        free(*priv_key_der);
        *priv_key_der = NULL;
        *priv_len = 0;
    }
    OSSL_ENCODER_CTX_free(ectx);

cleanup:
    EVP_PKEY_CTX_free(genctx);
    EVP_PKEY_free(privkey);
}

void ECGetPublicKeyFromPrivate(const unsigned char *priv_key_der, size_t priv_len, unsigned char **public_key_der, size_t *pub_len)
{
    OSSL_ENCODER_CTX *ectx = NULL;
    EVP_PKEY *privkey = NULL;

    // Get private key from DER
    privkey = GetKeyFromDer(0, priv_key_der, priv_len);

    // Create public key in DER. This is the default for EC, but name it
    // anyway, to match ECGeneratePrivateKey.
    ectx = OSSL_ENCODER_CTX_new_for_pkey(privkey, EVP_PKEY_PUBLIC_KEY, "DER", "SubjectPublicKeyInfo", NULL);
    if (OSSL_ENCODER_to_data(ectx, public_key_der, pub_len) <= 0)
    {
        fprintf(stderr, "Failed to get public key\n");
        free(*public_key_der);
        *public_key_der = NULL;
        *pub_len = 0;
    }
    OSSL_ENCODER_CTX_free(ectx);

    EVP_PKEY_free(privkey);
}

int ECValidateKey(int public, const unsigned char *key_der, size_t key_len)
{
    // Get key from DER
    EVP_PKEY *pkey = GetKeyFromDer(public, key_der, key_len);

    // check if it got a key
    int ret = pkey != NULL;

    EVP_PKEY_free(pkey);

    return ret;
}

/*
*******************************
       Local functions
*******************************
*/

static EVP_PKEY *GetKeyFromDer(int public, const unsigned char *key_der, size_t key_len)
{
    OSSL_DECODER_CTX *dctx = NULL;
    EVP_PKEY *pkey = NULL;
    int selection = public ? EVP_PKEY_PUBLIC_KEY : EVP_PKEY_KEYPAIR;

    // Get private key from DER
    dctx = OSSL_DECODER_CTX_new_for_pkey(&pkey, "DER", NULL, "EC",
                                         selection, NULL, NULL);
    if (OSSL_DECODER_from_data(dctx, &key_der, &key_len) <= 0)
    {
        fprintf(stderr, "Invalid key provided\n");
        EVP_PKEY_free(pkey);
        pkey = NULL;
    }

    OSSL_DECODER_CTX_free(dctx);

    return pkey;
}

static int AddNumberToDER(char *der, int offset, const char *number)
{
    const unsigned char *n = (const unsigned char *)number;

    // DER requires the shortest possible encoding, so leading zero bytes have
    // to go. Keep the last byte, so that a zero encodes as a single 0x00 - a
    // zero R or S is not a valid signature, but it's OpenSSL's job to say so.
    int start = 0;
    while (start < 31 && n[start] == 0x00)
    {
        start++;
    }

    int len = 32 - start;

    der[offset++] = 0x02;

    if (n[start] < 128)
    {
        der[offset++] = len;
    }
    else
    {
        // Add a leading 0 to keep the value positive.
        der[offset++] = len + 1;
        der[offset++] = 0x00;
    }

    memcpy(der + offset, number + start, len);
    return offset + len;
}

static int GetNumberFromDER(const unsigned char *der, size_t der_len, size_t *offset, char *number)
{
    size_t i = *offset;

    if (i + 2 > der_len || der[i] != 0x02)
    {
        return 0;
    }

    // R and S are at most 33 bytes, so the length is always in short form.
    size_t len = der[i + 1];
    if (len > 0x7f || len > der_len - (i + 2))
    {
        return 0;
    }

    i += 2;

    // Drop the leading zeroes DER adds to keep the value positive.
    while (len > 0 && der[i] == 0x00)
    {
        i++;
        len--;
    }

    if (len > 32)
    {
        return 0;
    }

    // Right-align the value in the fixed-width output.
    memset(number, 0, 32);
    memcpy(number + (32 - len), der + i, len);

    *offset = i + len;
    return 1;
}

static int Sign(EVP_PKEY *priv_key, const void *data, size_t data_len, void **sign, size_t *sign_len)
{
    int ret = 0;
    const char *sig_name = "SHA1";
    size_t sig_len = 0;
    EVP_MD_CTX *sign_context = NULL;

    /*
     * Make a message signature context to hold temporary state
     * during signature creation
     */
    sign_context = EVP_MD_CTX_new();
    if (sign_context == NULL)
    {
        fprintf(stderr, "EVP_MD_CTX_new failed.\n");
        goto cleanup;
    }
    /*
     * Initialize the sign context to use the fetched
     * sign provider.
     */
    if (!EVP_DigestSignInit_ex(sign_context, NULL, sig_name,
                               NULL, NULL, priv_key, NULL))
    {
        fprintf(stderr, "EVP_DigestSignInit_ex failed.\n");
        goto cleanup;
    }
    /*
     * EVP_DigestSignUpdate() can be called several times on the same context
     * to include additional data.
     */
    if (!EVP_DigestSignUpdate(sign_context, data, data_len))
    {
        fprintf(stderr, "EVP_DigestSignUpdate(hamlet_1) failed.\n");
        goto cleanup;
    }
    /* Call EVP_DigestSignFinal to get signature length sig_len */
    if (!EVP_DigestSignFinal(sign_context, NULL, &sig_len))
    {
        fprintf(stderr, "EVP_DigestSignFinal failed.\n");
        goto cleanup;
    }
    if (sig_len <= 0)
    {
        fprintf(stderr, "EVP_DigestSignFinal returned invalid signature length.\n");
        goto cleanup;
    }

    *sign = malloc(sig_len);
    if (*sign == NULL)
    {
        fprintf(stderr, "No memory.\n");
        goto cleanup;
    }
    if (!EVP_DigestSignFinal(sign_context, *sign, &sig_len))
    {
        fprintf(stderr, "EVP_DigestSignFinal failed.\n");
        goto cleanup;
    }

    *sign_len = sig_len;
    ret = 1;

cleanup:
    /* OpenSSL free functions will ignore NULL arguments */
    if (ret == 0)
        free(*sign);
    EVP_MD_CTX_free(sign_context);
    return ret;
}

static int Verify(EVP_PKEY *pub_key, const void *data, size_t data_len, const void *sign, size_t sign_len)
{
    int ret = 0;
    const char *sig_name = "SHA1";
    EVP_MD_CTX *verify_context = NULL;

    /*
     * Make a message signature context to hold temporary state
     * during signature creation
     */
    verify_context = EVP_MD_CTX_new();
    if (verify_context == NULL)
    {
        fprintf(stderr, "EVP_MD_CTX_new failed.\n");
        goto cleanup;
    }
    /* Verify */
    if (!EVP_DigestVerifyInit_ex(verify_context, NULL, sig_name,
                                 NULL, NULL, pub_key, NULL))
    {
        fprintf(stderr, "EVP_DigestVerifyInit failed.\n");
        goto cleanup;
    }
    /*
     * EVP_DigestVerifyUpdate() can be called several times on the same context
     * to include additional data.
     */
    if (!EVP_DigestVerifyUpdate(verify_context, data, data_len))
    {
        fprintf(stderr, "EVP_DigestVerifyUpdate failed.\n");
        goto cleanup;
    }
    if (EVP_DigestVerifyFinal(verify_context, sign, sign_len) <= 0)
    {
        fprintf(stderr, "EVP_DigestVerifyFinal failed\n");
        goto cleanup;
    }

    ret = 1;

cleanup:
    /* OpenSSL free functions will ignore NULL arguments */
    EVP_MD_CTX_free(verify_context);
    return ret;
}

#endif // __EMSCRIPTEN__
