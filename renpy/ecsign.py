# Copyright 2004-2026 Tom Rothamel <pytom@bishoujo.us>
# Copyright 2010 Brian Warner <warner-pyecdsa@lothar.com>
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

from __future__ import annotations

from typing import Any, Callable
import base64
import hashlib
import os
import secrets


################################################################################
# Exceptions
################################################################################

class BadSignatureError(Exception):
    pass


class BadDigestError(Exception):
    pass


################################################################################
# Curve Definitions (NIST256p / P-256 / SECP256r1 / prime256v1)
################################################################################

_P = 0xFFFFFFFF00000001000000000000000000000000FFFFFFFFFFFFFFFFFFFFFFFF
_A = _P - 3
_B = 0x5AC635D8AA3A93E7B3EBBD55769886BC651D06B0CC53B0F63BCE3C3E27D2604B
_N = 0xFFFFFFFF00000000FFFFFFFFFFFFFFFFBCE6FAADA7179E84F3B9CAC2FC632551
_GX = 0x6B17D1F2E12C4247F8BCE6E563A440F277037D812DEB33A0F4A13945D898C296
_GY = 0x4FE342E2FE1A7F9B8EE7EB4A7C0F9E162BCE33576B315ECECBB6406837BF51F5

_INFINITY = (0, 1, 0)

# Pre-computed DER prefixes for NIST256p
_SPKI_PREFIX = bytes.fromhex("3059301306072a8648ce3d020106082a8648ce3d03010703420004")
_SEC1_PREFIX = bytes.fromhex("30770201010420")
_SEC1_MID = bytes.fromhex("a00a06082a8648ce3d030107a14403420004")
_OID_EC_PUBLIC_KEY = bytes.fromhex("2a8648ce3d0201")
_OID_P256 = bytes.fromhex("2a8648ce3d030107")


class Curve(object):
    name = "NIST256p"
    baselen = 32
    verifying_key_length = 64
    signature_length = 64
    p = _P
    a = _A
    b = _B
    order = _N
    generator = (_GX, _GY)


NIST256p = Curve()


def _digest_to_int(curve: Curve, digest: bytes) -> int:
    if len(digest) > curve.baselen:
        raise BadDigestError(
            f"Digest length ({len(digest)} bytes) exceeds {curve.name}'s base length ({curve.baselen} bytes)"
        )
    return int.from_bytes(digest, "big")


################################################################################
# Point Arithmetic in Jacobian Coordinates
################################################################################

def _double_jacobian(X1, Y1, Z1):
    if Y1 == 0 or Z1 == 0:
        return _INFINITY
    Z1_sq = (Z1 * Z1) % _P
    M = (3 * (X1 - Z1_sq) * (X1 + Z1_sq)) % _P
    Y1_sq = (Y1 * Y1) % _P
    S = (4 * X1 * Y1_sq) % _P
    X3 = (M * M - 2 * S) % _P
    Y3 = (M * (S - X3) - 8 * Y1_sq * Y1_sq) % _P
    Z3 = (2 * Y1 * Z1) % _P
    return (X3, Y3, Z3)


def _add_jacobian(X1, Y1, Z1, X2, Y2, Z2):
    if Z1 == 0:
        return (X2, Y2, Z2)
    if Z2 == 0:
        return (X1, Y1, Z1)
    Z1_sq = (Z1 * Z1) % _P
    Z2_sq = (Z2 * Z2) % _P
    U1 = (X1 * Z2_sq) % _P
    U2 = (X2 * Z1_sq) % _P
    S1 = (Y1 * Z2 * Z2_sq) % _P
    S2 = (Y2 * Z1 * Z1_sq) % _P
    if U1 == U2:
        if S1 != S2:
            return _INFINITY
        return _double_jacobian(X1, Y1, Z1)
    H = (U2 - U1) % _P
    R = (S2 - S1) % _P
    H_sq = (H * H) % _P
    H_cu = (H * H_sq) % _P
    X3 = (R * R - H_cu - 2 * U1 * H_sq) % _P
    Y3 = (R * (U1 * H_sq - X3) - S1 * H_cu) % _P
    Z3 = (H * Z1 * Z2) % _P
    return (X3, Y3, Z3)


def _mul_jacobian(k, X, Y, Z):
    R = _INFINITY
    P = (X, Y, Z)
    while k > 0:
        if k & 1:
            R = _add_jacobian(R[0], R[1], R[2], P[0], P[1], P[2])
        P = _double_jacobian(P[0], P[1], P[2])
        k >>= 1
    return R


def _to_affine(X: int, Y: int, Z: int) -> tuple[int, int] | None:
    if Z == 0:
        return None
    inv_Z = pow(Z, -1, _P)
    inv_Z2 = (inv_Z * inv_Z) % _P
    inv_Z3 = (inv_Z * inv_Z2) % _P
    return ((X * inv_Z2) % _P, (Y * inv_Z3) % _P)


def _point_mul_g(k: int) -> tuple[int, int]:
    P_jac = _mul_jacobian(k, _GX, _GY, 1)
    aff = _to_affine(P_jac[0], P_jac[1], P_jac[2])
    if aff is None:
        raise ValueError("Point multiplied to infinity")
    return aff


def _point_mul(k: int, x: int, y: int) -> tuple[int, int] | None:
    P_jac = _mul_jacobian(k, x, y, 1)
    return _to_affine(P_jac[0], P_jac[1], P_jac[2])


################################################################################
# ASN.1 DER / PEM Parsing and Encoding
################################################################################

def _der_read_tlv(data: bytes, offset: int = 0) -> tuple[int, bytes, int]:
    if offset >= len(data):
        raise ValueError("Unexpected end of DER data")
    tag = data[offset]
    offset += 1
    if offset >= len(data):
        raise ValueError("Unexpected end of DER length")
    length = data[offset]
    offset += 1
    if length & 0x80:
        num_octets = length & 0x7F
        if num_octets == 0 or offset + num_octets > len(data):
            raise ValueError("Invalid DER length octets")
        if data[offset] == 0:
            raise ValueError("Non-canonical DER length")
        length = int.from_bytes(data[offset:offset + num_octets], "big")
        offset += num_octets
        if length < 128:
            raise ValueError("Non-canonical DER length")
    if offset + length > len(data):
        raise ValueError("DER length exceeds available data")
    value = data[offset:offset + length]
    return tag, value, offset + length


def _der_parse_sequence(data: bytes) -> list[tuple[int, bytes]]:
    items = []
    offset = 0
    while offset < len(data):
        tag, val, offset = _der_read_tlv(data, offset)
        items.append((tag, val))
    return items


def _der_decode_sequence(data: bytes) -> list[tuple[int, bytes]]:
    tag, value, end = _der_read_tlv(data)
    if tag != 0x30 or end != len(data):
        raise ValueError("Invalid DER SEQUENCE")
    return _der_parse_sequence(value)


def _der_decode_integer(value: bytes) -> int:
    if not value or value[0] & 0x80:
        raise ValueError("Invalid DER INTEGER")
    if len(value) > 1 and value[0] == 0 and not (value[1] & 0x80):
        raise ValueError("Non-canonical DER INTEGER")
    return int.from_bytes(value, "big")


def _decode_public_point(point_bytes: bytes) -> tuple[int, int]:
    if len(point_bytes) == 65 and point_bytes[0] == 4:
        point_bytes = point_bytes[1:]
    if len(point_bytes) != 64:
        raise ValueError("Invalid P-256 public point length")
    point = (int.from_bytes(point_bytes[:32], "big"), int.from_bytes(point_bytes[32:], "big"))
    _validate_public_point(point)
    return point


def _validate_public_point(point: tuple[int, int]) -> None:
    x, y = point
    if not (0 <= x < _P and 0 <= y < _P):
        raise ValueError("P-256 public point coordinate out of range")
    if (y * y - (x * x * x + _A * x + _B)) % _P:
        raise ValueError("P-256 public point is not on the curve")


def _decode_public_key_der(der_data: bytes) -> tuple[int, int]:
    if len(der_data) == 64:
        return _decode_public_point(der_data)
    if len(der_data) == 65:
        return _decode_public_point(der_data)

    items = _der_decode_sequence(der_data)
    if len(items) != 2 or items[0][0] != 0x30 or items[1][0] != 0x03:
        raise ValueError("Invalid P-256 SubjectPublicKeyInfo")
    algorithm = _der_parse_sequence(items[0][1])
    if algorithm != [(0x06, _OID_EC_PUBLIC_KEY), (0x06, _OID_P256)]:
        raise ValueError("Unsupported public key algorithm or curve")
    bit_string = items[1][1]
    if not bit_string or bit_string[0] != 0:
        raise ValueError("Invalid P-256 public key BIT STRING")
    return _decode_public_point(bit_string[1:])


def _decode_private_key_der(der_data: bytes) -> int:
    if len(der_data) == 32:
        return int.from_bytes(der_data, "big")
    items = _der_decode_sequence(der_data)

    # PKCS#8 PrivateKeyInfo: version, AlgorithmIdentifier, SEC1 private key.
    if 3 <= len(items) <= 4 and items[0][0] == 0x02 and items[1][0] == 0x30 and items[2][0] == 0x04:
        if _der_decode_integer(items[0][1]) != 0:
            raise ValueError("Unsupported PKCS#8 private key version")
        algorithm = _der_parse_sequence(items[1][1])
        if algorithm != [(0x06, _OID_EC_PUBLIC_KEY), (0x06, _OID_P256)]:
            raise ValueError("Unsupported private key algorithm or curve")
        if len(items) == 4:
            if items[3][0] != 0xA0:
                raise ValueError("Invalid PKCS#8 private key attributes")
            for tag, value in _der_parse_sequence(items[3][1]):
                if tag != 0x30:
                    raise ValueError("Invalid PKCS#8 private key attribute")
                attribute = _der_parse_sequence(value)
                if len(attribute) != 2 or attribute[0][0] != 0x06 or attribute[1][0] != 0x31:
                    raise ValueError("Invalid PKCS#8 private key attribute")
                if not _der_parse_sequence(attribute[1][1]):
                    raise ValueError("Invalid PKCS#8 private key attribute values")
        return _decode_private_key_sec1(items[2][1])

    return _decode_private_key_sec1(der_data)


def _decode_private_key_sec1(der_data: bytes) -> int:
    items = _der_decode_sequence(der_data)
    if len(items) < 2 or items[0][0] != 0x02 or items[1][0] != 0x04:
        raise ValueError("Invalid SEC1 private key")
    if _der_decode_integer(items[0][1]) != 1 or len(items[1][1]) != 32:
        raise ValueError("Invalid SEC1 private key version or length")

    secexp = int.from_bytes(items[1][1], "big")
    offset = 2
    if offset < len(items) and items[offset][0] == 0xA0:
        if _der_parse_sequence(items[offset][1]) != [(0x06, _OID_P256)]:
            raise ValueError("Unsupported SEC1 private key curve")
        offset += 1
    if offset < len(items) and items[offset][0] == 0xA1:
        public_key = _der_parse_sequence(items[offset][1])
        if len(public_key) != 1 or public_key[0][0] != 0x03 or not public_key[0][1] or public_key[0][1][0] != 0:
            raise ValueError("Invalid SEC1 private key public key")
        point = _decode_public_point(public_key[0][1][1:])
        if not (1 <= secexp < _N) or point != _point_mul_g(secexp):
            raise ValueError("SEC1 private key public key does not match private key")
        offset += 1
    if offset != len(items):
        raise ValueError("Invalid SEC1 private key field")
    return secexp


def _wrap_pem(header: str, der_bytes: bytes) -> bytes:
    b64 = base64.b64encode(der_bytes).decode("ascii")
    lines = [b64[i:i+64] for i in range(0, len(b64), 64)]
    res = "-----BEGIN " + header + "-----\n" + "\n".join(lines) + "\n-----END " + header + "-----\n"
    return res.encode("ascii")


def _unwrap_pem(pem_bytes: str | bytes, headers: tuple[str, ...]) -> bytes:
    if isinstance(pem_bytes, bytes):
        try:
            pem_str = pem_bytes.decode("ascii")
        except UnicodeDecodeError as e:
            raise ValueError("PEM must be ASCII") from e
    else:
        pem_str = pem_bytes
    lines = pem_str.splitlines()
    if len(lines) < 3:
        raise ValueError("Invalid PEM")
    header = next((h for h in headers if lines[0] == f"-----BEGIN {h}-----"), None)
    if header is None or lines[-1] != f"-----END {header}-----":
        raise ValueError("Invalid PEM boundaries")
    if any(not line or line.startswith("-----") for line in lines[1:-1]):
        raise ValueError("Invalid PEM body")
    try:
        return base64.b64decode("".join(lines[1:-1]), validate=True)
    except ValueError as e:
        raise ValueError("Invalid PEM Base64") from e


################################################################################
# VerifyingKey and SigningKey
################################################################################

class VerifyingKey(object):
    def __init__(self, curve: Curve = NIST256p, point: tuple[int, int] = (0, 0), hashfunc: Any = hashlib.sha1):
        self.curve = curve
        self.pubkey: tuple[int, int] = point
        self.default_hashfunc = hashfunc

    def to_string(self) -> bytes:
        """
        Returns the uncompressed 64-byte binary representation (X || Y).
        """
        x, y = self.pubkey
        return x.to_bytes(32, "big") + y.to_bytes(32, "big")

    def to_der(self, *args: Any, **kwargs: Any) -> bytes:
        """
        Returns the SPKI DER encoded bytes (91 bytes).
        """
        return _SPKI_PREFIX + self.to_string()

    def to_pem(self, *args: Any, **kwargs: Any) -> bytes:
        """
        Returns the PEM-encoded public key bytes.
        """
        return _wrap_pem("PUBLIC KEY", self.to_der())

    def verify(
        self,
        signature: str | bytes,
        data: str | bytes,
        hashfunc: Any = None
    ) -> bool:
        """
        Verifies that `signature` is valid for `data`.
        Returns True if valid, or raises BadSignatureError if invalid.
        """
        if isinstance(signature, str):
            signature = signature.encode("latin1")
        if isinstance(data, str):
            data = data.encode("utf-8")

        if len(signature) != 64:
            raise BadSignatureError("Signature verification failed: invalid signature length")

        r = int.from_bytes(signature[:32], "big")
        s = int.from_bytes(signature[32:], "big")

        if not (1 <= r < _N and 1 <= s < _N):
            raise BadSignatureError("Signature verification failed: r or s out of range")

        if hashfunc is None:
            hashfunc = self.default_hashfunc

        h = hashfunc(data).digest()
        z = _digest_to_int(self.curve, h)

        w = pow(s, -1, _N)
        u1 = (z * w) % _N
        u2 = (r * w) % _N

        pub_x, pub_y = self.pubkey
        P1 = _mul_jacobian(u1, _GX, _GY, 1)
        P2 = _mul_jacobian(u2, pub_x, pub_y, 1)
        P = _add_jacobian(P1[0], P1[1], P1[2], P2[0], P2[1], P2[2])
        aff = _to_affine(P[0], P[1], P[2])

        if aff is None:
            raise BadSignatureError("Signature verification failed: point at infinity")

        if (aff[0] % _N) != r:
            raise BadSignatureError("Signature verification failed")

        return True

    @classmethod
    def from_string(cls, string: str | bytes, curve: Curve = NIST256p, hashfunc: Any = hashlib.sha1) -> "VerifyingKey":
        if isinstance(string, str):
            string = string.encode("latin1")
        if len(string) == 64:
            return cls(curve=curve, point=_decode_public_point(string), hashfunc=hashfunc)
        elif len(string) == 65 and string[0] == 4:
            return cls(curve=curve, point=_decode_public_point(string), hashfunc=hashfunc)
        else:
            raise ValueError("Invalid public key string length")

    @classmethod
    def from_der(
        cls,
        string: str | bytes,
        hashfunc: Any = hashlib.sha1,
        valid_encodings: Any = None,
        valid_curve_encodings: Any = None
    ) -> "VerifyingKey":
        if isinstance(string, str):
            string = string.encode("latin1")
        point = _decode_public_key_der(string)
        return cls(curve=NIST256p, point=point, hashfunc=hashfunc)

    @classmethod
    def from_pem(
        cls,
        string: str | bytes,
        hashfunc: Any = hashlib.sha1,
        valid_encodings: Any = None,
        valid_curve_encodings: Any = None
    ) -> "VerifyingKey":
        der_bytes = _unwrap_pem(string, ("PUBLIC KEY",))
        return cls.from_der(der_bytes, hashfunc=hashfunc)


class SigningKey(object):
    def __init__(self, curve: Curve = NIST256p, privkey: int = 0, hashfunc: Any = hashlib.sha1):
        if not (1 <= privkey < _N):
            raise ValueError("Secret exponent out of range")
        self.curve = curve
        self.privkey: int = privkey
        self.default_hashfunc = hashfunc
        pub_point = _point_mul_g(privkey)
        self._verifying_key = VerifyingKey(curve=curve, point=pub_point, hashfunc=hashfunc)

    @property
    def verifying_key(self) -> VerifyingKey:
        return self._verifying_key

    def to_string(self) -> bytes:
        """
        Returns the raw 32-byte private key scalar.
        """
        return self.privkey.to_bytes(32, "big")

    def to_der(self, *args: Any, **kwargs: Any) -> bytes:
        """
        Returns the SEC1 EC PRIVATE KEY DER encoded bytes (121 bytes).
        """
        return _SEC1_PREFIX + self.to_string() + _SEC1_MID + self.verifying_key.to_string()

    def to_pem(self, *args: Any, **kwargs: Any) -> bytes:
        """
        Returns the PEM-encoded EC private key bytes.
        """
        return _wrap_pem("EC PRIVATE KEY", self.to_der())

    def sign(
        self,
        data: str | bytes,
        hashfunc: Any = None,
        entropy: Callable[[int], bytes] | None = None,
        k: int | None = None
    ) -> bytes:
        """
        Signs `data` with ECDSA (NIST256p). Returns a 64-byte binary signature (r || s).
        """
        if isinstance(data, str):
            data = data.encode("utf-8")

        if hashfunc is None:
            hashfunc = self.default_hashfunc

        h = hashfunc(data).digest()
        z = _digest_to_int(self.curve, h)

        while True:
            if k is not None:
                nonce = k
            elif entropy is not None:
                nonce = int.from_bytes(entropy(32), "big") % (_N - 1) + 1
            else:
                nonce = secrets.randbelow(_N - 1) + 1

            if not (1 <= nonce < _N):
                if k is not None:
                    raise ValueError("Specified nonce k is out of range")
                continue

            P_jac = _mul_jacobian(nonce, _GX, _GY, 1)
            aff = _to_affine(P_jac[0], P_jac[1], P_jac[2])
            if aff is None:
                continue

            r = aff[0] % _N
            if r == 0:
                if k is not None:
                    raise ValueError("Signing produced r = 0 with fixed k")
                continue

            k_inv = pow(nonce, -1, _N)
            s = (k_inv * (z + r * self.privkey)) % _N
            if s == 0:
                if k is not None:
                    raise ValueError("Signing produced s = 0 with fixed k")
                continue

            return r.to_bytes(32, "big") + s.to_bytes(32, "big")

    @classmethod
    def generate(
        cls,
        curve: Curve = NIST256p,
        hashfunc: Any = hashlib.sha1,
        entropy: Callable[[int], bytes] | None = None
    ) -> "SigningKey":
        while True:
            if entropy is not None:
                secexp = int.from_bytes(entropy(32), "big")
            else:
                secexp = int.from_bytes(os.urandom(32), "big")

            if 1 <= secexp < _N:
                return cls(curve=curve, privkey=secexp, hashfunc=hashfunc)

    @classmethod
    def from_secret_exponent(
        cls,
        secexp: int,
        curve: Curve = NIST256p,
        hashfunc: Any = hashlib.sha1
    ) -> "SigningKey":
        if not (1 <= secexp < _N):
            raise ValueError("Secret exponent out of range")
        return cls(curve=curve, privkey=secexp, hashfunc=hashfunc)

    @classmethod
    def from_string(
        cls,
        string: str | bytes,
        curve: Curve = NIST256p,
        hashfunc: Any = hashlib.sha1
    ) -> "SigningKey":
        if isinstance(string, str):
            string = string.encode("latin1")
        if len(string) != 32:
            raise ValueError("Private key string must be 32 bytes")
        secexp = int.from_bytes(string, "big")
        return cls.from_secret_exponent(secexp, curve=curve, hashfunc=hashfunc)

    @classmethod
    def from_der(
        cls,
        string: str | bytes,
        hashfunc: Any = hashlib.sha1,
        valid_curve_encodings: Any = None
    ) -> "SigningKey":
        if isinstance(string, str):
            string = string.encode("latin1")
        secexp = _decode_private_key_der(string)
        return cls.from_secret_exponent(secexp, curve=NIST256p, hashfunc=hashfunc)

    @classmethod
    def from_pem(
        cls,
        string: str | bytes,
        hashfunc: Any = hashlib.sha1,
        valid_curve_encodings: Any = None
    ) -> "SigningKey":
        der_bytes = _unwrap_pem(string, ("EC PRIVATE KEY", "PRIVATE KEY"))
        return cls.from_der(der_bytes, hashfunc=hashfunc)
