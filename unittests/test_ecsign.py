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

import unittest
import hashlib
import base64
import renpy.ecsign as ecsign


P256_PKCS8_PRIVATE_KEY = bytes.fromhex(
    "308193020100301306072a8648ce3d020106082a8648ce3d0301070479"
    "30770201010420"
    "0000000000000000000000000000000000000000000000000000000000000001"
    "a00a06082a8648ce3d030107a14403420004"
    "6b17d1f2e12c4247f8bce6e563a440f277037d812deb33a0f4a13945d898c296"
    "4fe342e2fe1a7f9b8ee7eb4a7c0f9e162bce33576b315ececbb6406837bf51f5"
)


class TestECSign(unittest.TestCase):
    def test_key_generation(self):
        sk = ecsign.SigningKey.generate(curve=ecsign.NIST256p)
        vk = sk.verifying_key
        self.assertIsNotNone(vk)
        self.assertEqual(len(sk.to_string()), 32)
        self.assertEqual(len(vk.to_string()), 64)

    def test_der_pem_roundtrip(self):
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

        self.assertEqual(sk.to_string(), sk_from_der.to_string())
        self.assertEqual(sk.to_string(), sk_from_pem.to_string())
        self.assertEqual(vk.to_string(), vk_from_der.to_string())
        self.assertEqual(vk.to_string(), vk_from_pem.to_string())

    def test_sign_and_verify(self):
        sk = ecsign.SigningKey.generate(curve=ecsign.NIST256p)
        vk = sk.verifying_key

        data = b"Hello, Ren'Py ECDSA signing test!"
        signature = sk.sign(data)
        self.assertEqual(len(signature), 64)

        self.assertTrue(vk.verify(signature, data))

        # Tampered data should fail verification
        with self.assertRaises(ecsign.BadSignatureError):
            vk.verify(signature, b"Tampered data")

        # Invalid signature length should fail verification
        with self.assertRaises(ecsign.BadSignatureError):
            vk.verify(b"\x00" * 32, data)

    def test_supported_hashfuncs(self):
        sk = ecsign.SigningKey.generate(curve=ecsign.NIST256p, hashfunc=hashlib.sha256)
        vk = sk.verifying_key

        for hashfunc in (hashlib.sha224, hashlib.sha256):
            with self.subTest(hashfunc=hashfunc.__name__):
                data = f"Custom hashfunc {hashfunc.__name__} test".encode("ascii")
                signature = sk.sign(data, hashfunc=hashfunc)
                self.assertTrue(vk.verify(signature, data, hashfunc=hashfunc))

    def test_rejects_oversized_digests(self):
        sk = ecsign.SigningKey.generate(curve=ecsign.NIST256p)
        vk = sk.verifying_key
        data = b"Oversized digest test"
        valid_signature = sk.sign(data, hashfunc=hashlib.sha256)

        for hashfunc in (hashlib.sha384, hashlib.sha512):
            with self.subTest(hashfunc=hashfunc.__name__):
                with self.assertRaises(ecsign.BadDigestError):
                    sk.sign(data, hashfunc=hashfunc)
                with self.assertRaises(ecsign.BadDigestError):
                    vk.verify(valid_signature, data, hashfunc=hashfunc)

    def test_p256_sec1_and_pkcs8_private_key_compatibility(self):
        sec1 = ecsign.SigningKey.from_secret_exponent(1).to_der()
        expected = (1).to_bytes(32, "big")

        self.assertEqual(ecsign.SigningKey.from_der(sec1).to_string(), expected)
        self.assertEqual(ecsign.SigningKey.from_der(P256_PKCS8_PRIVATE_KEY).to_string(), expected)

        attributes = bytes.fromhex("a00c300a06032a03043103020100")
        pkcs8_with_attributes = b"\x30\x81\xa1" + P256_PKCS8_PRIVATE_KEY[3:] + attributes
        self.assertEqual(ecsign.SigningKey.from_der(pkcs8_with_attributes).to_string(), expected)

        pem = b"-----BEGIN PRIVATE KEY-----\n" + base64.b64encode(P256_PKCS8_PRIVATE_KEY) + b"\n-----END PRIVATE KEY-----\n"
        self.assertEqual(ecsign.SigningKey.from_pem(pem).to_string(), expected)

    def test_rejects_invalid_public_points(self):
        out_of_range = ecsign._P.to_bytes(32, "big") + b"\x00" * 32
        off_curve = b"\x00" * 64

        for public_key in (out_of_range, off_curve):
            with self.subTest(public_key=public_key):
                with self.assertRaises(ValueError):
                    ecsign.VerifyingKey.from_string(public_key)
                with self.assertRaises(ValueError):
                    ecsign.VerifyingKey.from_der(public_key)

    def test_rejects_noncanonical_or_invalid_spki(self):
        vk_der = ecsign.SigningKey.from_secret_exponent(1).verifying_key.to_der()

        noncanonical_length = b"\x30\x81\x59" + vk_der[2:]
        wrong_oid = vk_der.replace(bytes.fromhex("2a8648ce3d030107"), bytes.fromhex("2a8648ce3d030108"))
        nonzero_unused_bits = vk_der[:-66] + b"\x01" + vk_der[-65:]

        for der in (vk_der + b"\x00", noncanonical_length, wrong_oid, nonzero_unused_bits):
            with self.subTest(der=der):
                with self.assertRaises(ValueError):
                    ecsign.VerifyingKey.from_der(der)

    def test_rejects_invalid_private_key_der_and_pem(self):
        sec1 = ecsign.SigningKey.from_secret_exponent(1).to_der()
        mismatched_public_key = sec1[:-1] + bytes([sec1[-1] ^ 1])
        reversed_optional_fields = sec1[:39] + sec1[51:] + sec1[39:51]

        for der in (sec1 + b"\x00", mismatched_public_key, reversed_optional_fields):
            with self.subTest(der=der):
                with self.assertRaises(ValueError):
                    ecsign.SigningKey.from_der(der)

        invalid_pems = (
            b"-----BEGIN PUBLIC KEY-----\nAAAA\n-----END EC PRIVATE KEY-----\n",
            b"-----BEGIN EC PRIVATE KEY-----\n!!!!\n-----END EC PRIVATE KEY-----\n",
            b"prefix\n" + ecsign.SigningKey.from_secret_exponent(1).to_pem(),
        )
        for pem in invalid_pems:
            with self.subTest(pem=pem):
                with self.assertRaises(ValueError):
                    ecsign.SigningKey.from_pem(pem)

    def test_rejects_invalid_private_key_constructor_scalar(self):
        for scalar in (0, ecsign._N, ecsign._N + 1):
            with self.subTest(scalar=scalar):
                with self.assertRaises(ValueError):
                    ecsign.SigningKey(privkey=scalar)


if __name__ == "__main__":
    unittest.main()
