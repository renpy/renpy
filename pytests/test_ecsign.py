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

"""
Tests for the pure-Python ECDSA P-256 implementation in ecsign: key generation, signing and verification,
DER and PEM encodings, and rejection of malformed keys, digests, and signatures.
"""

import base64
import hashlib

import pytest

from renpy import ecsign

P256_PKCS8_PRIVATE_KEY = bytes.fromhex(
    "308193020100301306072a8648ce3d020106082a8648ce3d0301070479"
    "30770201010420"
    "0000000000000000000000000000000000000000000000000000000000000001"
    "a00a06082a8648ce3d030107a14403420004"
    "6b17d1f2e12c4247f8bce6e563a440f277037d812deb33a0f4a13945d898c296"
    "4fe342e2fe1a7f9b8ee7eb4a7c0f9e162bce33576b315ececbb6406837bf51f5"
)

# The secret exponent 1 gives a fixed key, so the malformed-input cases below are deterministic.
SEC1_DER = ecsign.SigningKey.from_secret_exponent(1).to_der()
SEC1_PEM = ecsign.SigningKey.from_secret_exponent(1).to_pem()
VERIFYING_KEY_DER = ecsign.SigningKey.from_secret_exponent(1).verifying_key.to_der()

INVALID_PUBLIC_KEYS = (
    pytest.param(ecsign._P.to_bytes(32, "big") + b"\x00" * 32, id="out-of-range-coordinate"),
    pytest.param(b"\x00" * 64, id="off-curve"),
)

INVALID_SPKI = (
    pytest.param(VERIFYING_KEY_DER + b"\x00", id="trailing-byte"),
    pytest.param(b"\x30\x81\x59" + VERIFYING_KEY_DER[2:], id="non-canonical-length"),
    pytest.param(
        VERIFYING_KEY_DER.replace(bytes.fromhex("2a8648ce3d030107"), bytes.fromhex("2a8648ce3d030108")),
        id="wrong-curve-oid",
    ),
    pytest.param(VERIFYING_KEY_DER[:-66] + b"\x01" + VERIFYING_KEY_DER[-65:], id="nonzero-unused-bits"),
)

INVALID_SEC1_DER = (
    pytest.param(SEC1_DER + b"\x00", id="trailing-byte"),
    pytest.param(SEC1_DER[:-1] + bytes([SEC1_DER[-1] ^ 1]), id="mismatched-public-key"),
    pytest.param(SEC1_DER[:39] + SEC1_DER[51:] + SEC1_DER[39:51], id="reversed-optional-fields"),
)

INVALID_PRIVATE_PEMS = (
    pytest.param(b"-----BEGIN PUBLIC KEY-----\nAAAA\n-----END EC PRIVATE KEY-----\n", id="mismatched-label"),
    pytest.param(b"-----BEGIN EC PRIVATE KEY-----\n!!!!\n-----END EC PRIVATE KEY-----\n", id="invalid-base64"),
    pytest.param(b"prefix\n" + SEC1_PEM, id="text-before-pem"),
)


def test_key_generation():
    """A generated P-256 key pair has a 32-byte private scalar and a 64-byte public point."""

    sk = ecsign.SigningKey.generate(curve=ecsign.NIST256p)
    vk = sk.verifying_key
    assert vk is not None
    assert len(sk.to_string()) == 32
    assert len(vk.to_string()) == 64


def test_der_pem_roundtrip():
    """
    Signing and verifying keys serialized as DER or PEM load back to the same key material.
    """

    sk = ecsign.SigningKey.generate(curve=ecsign.NIST256p)
    vk = sk.verifying_key

    sk_der = sk.to_der()
    vk_der = vk.to_der()
    sk_pem = sk.to_pem()
    vk_pem = vk.to_pem()

    sk_from_der = ecsign.SigningKey.from_der(sk_der)
    sk_from_pem = ecsign.SigningKey.from_pem(sk_pem)
    vk_from_der = ecsign.VerifyingKey.from_der(vk_der)
    vk_from_pem = ecsign.VerifyingKey.from_pem(vk_pem)

    assert sk.to_string() == sk_from_der.to_string()
    assert sk.to_string() == sk_from_pem.to_string()
    assert vk.to_string() == vk_from_der.to_string()
    assert vk.to_string() == vk_from_pem.to_string()


def test_sign_and_verify():
    """
    A signature made with the signing key verifies against the same data. Verification fails with
    BadSignatureError when the data was altered, or when the signature is not 64 bytes long.
    """

    sk = ecsign.SigningKey.generate(curve=ecsign.NIST256p)
    vk = sk.verifying_key

    data = b"Hello, Ren'Py ECDSA signing test!"
    signature = sk.sign(data)
    assert len(signature) == 64

    assert vk.verify(signature, data)

    # Tampered data should fail verification
    with pytest.raises(ecsign.BadSignatureError):
        vk.verify(signature, b"Tampered data")

    # Invalid signature length should fail verification
    with pytest.raises(ecsign.BadSignatureError):
        vk.verify(b"\x00" * 32, data)


@pytest.mark.parametrize("hashfunc", (hashlib.sha224, hashlib.sha256), ids=lambda hashfunc: hashfunc.__name__)
def test_supported_hashfuncs(hashfunc):
    """
    Signing and verifying with a per-call hash function succeeds for sha224 and sha256, even though the
    key was generated with sha256 as its default. The same hash function must be passed to both calls.
    """

    sk = ecsign.SigningKey.generate(curve=ecsign.NIST256p, hashfunc=hashlib.sha256)
    vk = sk.verifying_key

    data = f"Custom hashfunc {hashfunc.__name__} test".encode("ascii")
    signature = sk.sign(data, hashfunc=hashfunc)
    assert vk.verify(signature, data, hashfunc=hashfunc)


@pytest.mark.parametrize("hashfunc", (hashlib.sha384, hashlib.sha512), ids=lambda hashfunc: hashfunc.__name__)
def test_rejects_oversized_digests(hashfunc):
    """
    Hash functions whose digests are wider than P-256's 32-byte base length are rejected with
    BadDigestError, both when signing and when verifying. A valid sha256 signature is used for the
    verification side, so the only reason for the failure is the digest size.
    """

    sk = ecsign.SigningKey.generate(curve=ecsign.NIST256p)
    vk = sk.verifying_key
    data = b"Oversized digest test"
    valid_signature = sk.sign(data, hashfunc=hashlib.sha256)

    with pytest.raises(ecsign.BadDigestError):
        sk.sign(data, hashfunc=hashfunc)
    with pytest.raises(ecsign.BadDigestError):
        vk.verify(valid_signature, data, hashfunc=hashfunc)


def test_p256_sec1_and_pkcs8_private_key_compatibility():
    """
    A private key for scalar 1 loads from SEC1 DER, from PKCS#8 DER, from PKCS#8 DER with optional
    attributes, and from PKCS#8 PEM. This checks that every supported private key encoding yields the
    same key.
    """

    expected = (1).to_bytes(32, "big")

    assert ecsign.SigningKey.from_der(SEC1_DER).to_string() == expected
    assert ecsign.SigningKey.from_der(P256_PKCS8_PRIVATE_KEY).to_string() == expected

    attributes = bytes.fromhex("a00c300a06032a03043103020100")
    pkcs8_with_attributes = b"\x30\x81\xa1" + P256_PKCS8_PRIVATE_KEY[3:] + attributes
    assert ecsign.SigningKey.from_der(pkcs8_with_attributes).to_string() == expected

    pem = b"-----BEGIN PRIVATE KEY-----\n" + base64.b64encode(P256_PKCS8_PRIVATE_KEY) + b"\n-----END PRIVATE KEY-----\n"
    assert ecsign.SigningKey.from_pem(pem).to_string() == expected


@pytest.mark.parametrize("public_key", INVALID_PUBLIC_KEYS)
def test_rejects_invalid_public_points(public_key):
    """
    A 64-byte public point is rejected with ValueError when a coordinate is outside the field, or when
    the point is not on the P-256 curve. Both the raw and DER loaders must reject it.
    """

    with pytest.raises(ValueError):
        ecsign.VerifyingKey.from_string(public_key)
    with pytest.raises(ValueError):
        ecsign.VerifyingKey.from_der(public_key)


@pytest.mark.parametrize("der", INVALID_SPKI)
def test_rejects_noncanonical_or_invalid_spki(der):
    """
    A verifying key in SubjectPublicKeyInfo DER is rejected with ValueError when it has trailing bytes, a
    length that is not in canonical DER form, a different curve OID, or nonzero unused bits in the BIT
    STRING. Each case starts from a valid key and changes one aspect of it.
    """

    with pytest.raises(ValueError):
        ecsign.VerifyingKey.from_der(der)


@pytest.mark.parametrize("der", INVALID_SEC1_DER)
def test_rejects_invalid_private_key_der(der):
    """
    A SEC1 private key in DER is rejected with ValueError when it has trailing bytes, when its embedded
    public key does not match the private scalar, or when its optional fields are out of order.
    """

    with pytest.raises(ValueError):
        ecsign.SigningKey.from_der(der)


@pytest.mark.parametrize("pem", INVALID_PRIVATE_PEMS)
def test_rejects_invalid_private_key_pem(pem):
    """
    A private key PEM is rejected with ValueError when its BEGIN and END labels disagree, when its body is
    not valid Base64, or when extra text precedes the PEM block.
    """

    with pytest.raises(ValueError):
        ecsign.SigningKey.from_pem(pem)


@pytest.mark.parametrize("scalar", (0, ecsign._N, ecsign._N + 1), ids=["zero", "order", "order-plus-one"])
def test_rejects_invalid_private_key_constructor_scalar(scalar):
    """
    The SigningKey constructor rejects a private scalar outside 1..N-1, where N is the curve order. Zero,
    N, and N+1 are the boundary values that must fail.
    """

    with pytest.raises(ValueError):
        ecsign.SigningKey(privkey=scalar)
