// Released under MIT License and sample code from OpenSSL see below.

/************************************************************************************

Code is partially based on Demos from OpenSSL. They are released with following info:

 * Copyright 2021-2023 The OpenSSL Project Authors. All Rights Reserved.
 *
 * Licensed under the Apache License 2.0 (the "License").  You may not use
 * this file except in compliance with the License.  You can obtain a copy
 * in the file LICENSE in the source distribution or at
 * https://www.openssl.org/source/license.html

 ***********************************************************************************/

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
static int Sign(EVP_PKEY *priv_key, const void *data, size_t data_len, void **sign, size_t *sign_len);
static int Verify(EVP_PKEY *pub_key, const void *data, size_t data_len, const void *sign, size_t sign_len);

/*
*******************************
      Global functions
*******************************
*/

int ECSign(const unsigned char *priv_key_der, size_t key_len, const char *data, size_t data_len, char *signature, size_t signature_len)
{
    EVP_PKEY *pkey = NULL;
    int ret = 0;

    if (signature == NULL || signature_len != 64)
    {
        fprintf(stderr, "Parameter 'signature' should point to 64 bytes of memory to receive raw signature\n");
        goto cleanup;
    }

    // Get private key from DER
    pkey = GetKeyFromDer(0, priv_key_der, key_len);

    char *sign;
    size_t sign_len;
    ret = Sign(pkey, data, data_len, (void **)&sign, &sign_len);

    if (ret)
    {
        // fprintf(stdout, "Calculated signature as DER:\n");
        // BIO_dump_indent_fp(stdout, sign, sign_len, 2);

        // Copy R and S from DER sign to raw signature output
        // Check if it has a extra leading 0 to skip (added to keep value positive in DER format)
        int offset = sign[3] == 0x21 ? 5 : 4;
        memcpy(signature, sign + offset, 32); // Copy R

        // Get last 32 bytes which is S
        offset = sign_len - 32;
        memcpy(signature + 32, sign + offset, 32); // Copy S
    }

cleanup:
    free(sign);
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

    // Convert private key to DER
    ectx = OSSL_ENCODER_CTX_new_for_pkey(privkey, EVP_PKEY_KEYPAIR, "DER", NULL, NULL);
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

    // Create public key in DER
    ectx = OSSL_ENCODER_CTX_new_for_pkey(privkey, EVP_PKEY_PUBLIC_KEY, "DER", NULL, NULL);
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
    der[offset++] = 0x02;
    if (((unsigned char *)number)[0] < 128)
    {
        der[offset++] = 0x20; // length R
    }
    else
    {
        der[offset++] = 0x21; // length R
        der[offset++] = 0x00;
    }
    // Copy R value
    memcpy(der + offset, number, 32);
    return offset + 32;
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
