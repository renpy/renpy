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

#include <openssl/evp.h>
#include <openssl/decoder.h>
#include <openssl/err.h>
#include <string.h>

/*******************************
 *     Forward declarations
 ********************************/

static int AddNumberToDER(char *der, int offset, const char *number);
static int Sign(OSSL_LIB_CTX *libctx, EVP_PKEY *priv_key, const void *data, size_t data_len, void **sign, size_t *sign_len);
static int Verify(OSSL_LIB_CTX *libctx, EVP_PKEY *pub_key, const void *data, size_t data_len, const void *sign, size_t sign_len);

/*******************************
 *     Global functions
 ********************************/

int SignDer(const unsigned char *priv_key_der, size_t key_len, const char *data, size_t data_len, char *signature, size_t signature_len)
{
    OSSL_LIB_CTX *libctx = NULL;
    OSSL_DECODER_CTX *dctx = NULL;
    EVP_PKEY *pkey = NULL;
    int ret = 0;

    if (signature == NULL || signature_len != 64)
    {
        fprintf(stderr, "Parameter 'signature' should point to 64 bytes of memory to receive raw signature\n");
        goto cleanup;
    }

    libctx = OSSL_LIB_CTX_new();
    if (libctx == NULL)
    {
        goto cleanup;
    }

    dctx = OSSL_DECODER_CTX_new_for_pkey(&pkey, "DER", NULL, "EC",
                                         EVP_PKEY_KEYPAIR, libctx, NULL);
    (void)OSSL_DECODER_from_data(dctx, &priv_key_der, &key_len);
    OSSL_DECODER_CTX_free(dctx);

    char *sign;
    size_t sign_len;
    ret = Sign(libctx, pkey, data, data_len, &sign, &sign_len);

    if (ret)
    {
        fprintf(stdout, "Calculated signature as DER:\n");
        BIO_dump_indent_fp(stdout, sign, sign_len, 2);

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
    OSSL_LIB_CTX_free(libctx);
    return ret;
}

int VerifyDer(const unsigned char *public_key_der, size_t key_len, const char *data, size_t data_len, char *signature, size_t signature_len)
{
    OSSL_LIB_CTX *libctx = NULL;
    OSSL_DECODER_CTX *dctx = NULL;
    EVP_PKEY *pkey = NULL;
    int ret = 0;

    if (signature_len != 64)
    {
        fprintf(stderr, "sign size is %d bytes, but expect 64 bytes\n", signature_len);
        goto cleanup;
    }

    // fprintf(stderr, "Verify got: key size: %d data size: %d and sign size: %d\n", key_len, data_len, signature_len);

    libctx = OSSL_LIB_CTX_new();
    if (libctx == NULL)
    {
        goto cleanup;
    }

    dctx = OSSL_DECODER_CTX_new_for_pkey(&pkey, "DER", NULL, "EC",
                                         EVP_PKEY_PUBLIC_KEY, libctx, NULL);
    if (OSSL_DECODER_from_data(dctx, &public_key_der, &key_len) <= 0)
    {
        fprintf(stderr, "Failed to decode public key.\nDER data was: (len: %d)", key_len);
        BIO_dump_indent_fp(stdout, public_key_der, key_len, 2);
    }
    OSSL_DECODER_CTX_free(dctx);

    // Convert signature to DER
    unsigned char der_sign[72];
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

    ret = Verify(libctx, pkey, data, data_len, der_sign, offset);

cleanup:
    EVP_PKEY_free(pkey);
    OSSL_LIB_CTX_free(libctx);
    return ret;
}

/*******************************
 *     Local functions
 ********************************/

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

static int Sign(OSSL_LIB_CTX *libctx, EVP_PKEY *priv_key, const void *data, size_t data_len, void **sign, size_t *sign_len)
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
                               libctx, NULL, priv_key, NULL))
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

static int Verify(OSSL_LIB_CTX *libctx, EVP_PKEY *pub_key, const void *data, size_t data_len, const void *sign, size_t sign_len)
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
                                 libctx, NULL, pub_key, NULL))
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
        fprintf(stderr, "EVP_DigestVerifyUpdate(hamlet_1) failed.\n");
        goto cleanup;
    }
    if (EVP_DigestVerifyFinal(verify_context, sign, sign_len) <= 0)
    {
        fprintf(stderr, "EVP_DigestVerifyFinal failed: ");
        ERR_print_errors_fp(stderr);
        fprintf(stderr, "\n");
        goto cleanup;
    }

    ret = 1;

cleanup:
    /* OpenSSL free functions will ignore NULL arguments */
    EVP_MD_CTX_free(verify_context);
    return ret;
}
