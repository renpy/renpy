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
# Curve Definitions
################################################################################

_OID_EC_PUBLIC_KEY = bytes.fromhex("2a8648ce3d0201")


class Curve:
    """
    A short Weierstrass curve y^2 = x^3 + ax + b over GF(p) with a prime-order base point, used for ECDSA.

    `oid` is the DER contents of the curve's named-curve OBJECT IDENTIFIER, used to encode and recognize keys.
    Only 256-bit curves with cofactor 1 are supported, so validating that a point is on the curve is enough
    to show it is in the prime-order group.
    """

    baselen = 32
    verifying_key_length = 64
    signature_length = 64

    def __init__(self, name: str, p: int, a: int, b: int, order: int, generator: tuple[int, int], oid: bytes):
        self.name = name
        self.p = p
        self.a = a
        self.b = b
        self.order = order
        self.generator = generator
        self.oid = oid

    def __repr__(self) -> str:
        return f"<Curve {self.name}>"


# NIST P-256 / SECP256r1 / prime256v1.
NIST256p = Curve(
    "NIST256p",
    p=0xFFFFFFFF00000001000000000000000000000000FFFFFFFFFFFFFFFFFFFFFFFF,
    a=0xFFFFFFFF00000001000000000000000000000000FFFFFFFFFFFFFFFFFFFFFFFC,
    b=0x5AC635D8AA3A93E7B3EBBD55769886BC651D06B0CC53B0F63BCE3C3E27D2604B,
    order=0xFFFFFFFF00000000FFFFFFFFFFFFFFFFBCE6FAADA7179E84F3B9CAC2FC632551,
    generator=(
        0x6B17D1F2E12C4247F8BCE6E563A440F277037D812DEB33A0F4A13945D898C296,
        0x4FE342E2FE1A7F9B8EE7EB4A7C0F9E162BCE33576B315ECECBB6406837BF51F5,
    ),
    oid=bytes.fromhex("2a8648ce3d030107"),
)

# SECG secp256k1, used by the key that signs launcher extension manifests (renpy_ecdsa_public.pem).
SECP256k1 = Curve(
    "SECP256k1",
    p=0xFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFEFFFFFC2F,
    a=0,
    b=7,
    order=0xFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFEBAAEDCE6AF48A03BBFD25E8CD0364141,
    generator=(
        0x79BE667EF9DCBBAC55A06295CE870B07029BFCDB2DCE28D959F2815B16F81798,
        0x483ADA7726A3C4655DA4FBFC0E1108A8FD17B448A68554199C47D08FFB10D4B8,
    ),
    oid=bytes.fromhex("2b8104000a"),
)

# Maps the DER contents of a named-curve OID to the supported curve.
_CURVES_BY_OID: dict[bytes, Curve] = {c.oid: c for c in (NIST256p, SECP256k1)}

# P-256 constants, kept as module names for compatibility.
_P = NIST256p.p
_A = NIST256p.a
_B = NIST256p.b
_N = NIST256p.order
_GX, _GY = NIST256p.generator

_INFINITY = (0, 1, 0)


def _digest_to_int(curve: Curve, digest: bytes) -> int:
    if len(digest) > curve.baselen:
        raise BadDigestError(
            f"Digest length ({len(digest)} bytes) exceeds {curve.name}'s base length ({curve.baselen} bytes)"
        )
    return int.from_bytes(digest, "big")


################################################################################
# Point Arithmetic in Jacobian Coordinates
################################################################################

def _double_jacobian(curve: Curve, X1, Y1, Z1):
    if Y1 == 0 or Z1 == 0:
        return _INFINITY
    p = curve.p
    Z1_sq = (Z1 * Z1) % p
    M = (3 * X1 * X1 + curve.a * Z1_sq * Z1_sq) % p
    Y1_sq = (Y1 * Y1) % p
    S = (4 * X1 * Y1_sq) % p
    X3 = (M * M - 2 * S) % p
    Y3 = (M * (S - X3) - 8 * Y1_sq * Y1_sq) % p
    Z3 = (2 * Y1 * Z1) % p
    return (X3, Y3, Z3)


def _add_jacobian(curve: Curve, X1, Y1, Z1, X2, Y2, Z2):
    if Z1 == 0:
        return (X2, Y2, Z2)
    if Z2 == 0:
        return (X1, Y1, Z1)
    p = curve.p
    Z1_sq = (Z1 * Z1) % p
    Z2_sq = (Z2 * Z2) % p
    U1 = (X1 * Z2_sq) % p
    U2 = (X2 * Z1_sq) % p
    S1 = (Y1 * Z2 * Z2_sq) % p
    S2 = (Y2 * Z1 * Z1_sq) % p
    if U1 == U2:
        if S1 != S2:
            return _INFINITY
        return _double_jacobian(curve, X1, Y1, Z1)
    H = (U2 - U1) % p
    R = (S2 - S1) % p
    H_sq = (H * H) % p
    H_cu = (H * H_sq) % p
    X3 = (R * R - H_cu - 2 * U1 * H_sq) % p
    Y3 = (R * (U1 * H_sq - X3) - S1 * H_cu) % p
    Z3 = (H * Z1 * Z2) % p
    return (X3, Y3, Z3)


def _mul_jacobian(curve: Curve, k, X, Y, Z):
    R = _INFINITY
    P = (X, Y, Z)
    while k > 0:
        if k & 1:
            R = _add_jacobian(curve, R[0], R[1], R[2], P[0], P[1], P[2])
        P = _double_jacobian(curve, P[0], P[1], P[2])
        k >>= 1
    return R


def _to_affine(curve: Curve, X: int, Y: int, Z: int) -> tuple[int, int] | None:
    if Z == 0:
        return None
    p = curve.p
    inv_Z = pow(Z, -1, p)
    inv_Z2 = (inv_Z * inv_Z) % p
    inv_Z3 = (inv_Z * inv_Z2) % p
    return ((X * inv_Z2) % p, (Y * inv_Z3) % p)


def _point_mul_g(curve: Curve, k: int) -> tuple[int, int]:
    gx, gy = curve.generator
    P_jac = _mul_jacobian(curve, k, gx, gy, 1)
    aff = _to_affine(curve, P_jac[0], P_jac[1], P_jac[2])
    if aff is None:
        raise ValueError("Point multiplied to infinity")
    return aff


def _point_mul(curve: Curve, k: int, x: int, y: int) -> tuple[int, int] | None:
    P_jac = _mul_jacobian(curve, k, x, y, 1)
    return _to_affine(curve, P_jac[0], P_jac[1], P_jac[2])


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


def _der_tlv(tag: int, value: bytes) -> bytes:
    """
    Encodes a single DER tag-length-value element with a canonical length.
    """

    length = len(value)
    if length < 0x80:
        encoded_length = bytes([length])
    else:
        length_bytes = length.to_bytes((length.bit_length() + 7) // 8, "big")
        encoded_length = bytes([0x80 | len(length_bytes)]) + length_bytes
    return bytes([tag]) + encoded_length + value


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


def _decode_algorithm(algorithm_der: bytes) -> Curve:
    """
    Returns the curve named by the contents of an id-ecPublicKey AlgorithmIdentifier SEQUENCE, or raises
    ValueError if the algorithm or curve is not supported.
    """

    algorithm = _der_parse_sequence(algorithm_der)
    if len(algorithm) != 2 or algorithm[0] != (0x06, _OID_EC_PUBLIC_KEY) or algorithm[1][0] != 0x06:
        raise ValueError("Unsupported public key algorithm or curve")
    curve = _CURVES_BY_OID.get(algorithm[1][1])
    if curve is None:
        raise ValueError("Unsupported public key algorithm or curve")
    return curve


def _encode_algorithm(curve: Curve) -> bytes:
    return _der_tlv(0x30, _der_tlv(0x06, _OID_EC_PUBLIC_KEY) + _der_tlv(0x06, curve.oid))


def _decode_public_point(curve: Curve, point_bytes: bytes) -> tuple[int, int]:
    if len(point_bytes) == 65 and point_bytes[0] == 4:
        point_bytes = point_bytes[1:]
    if len(point_bytes) != 64:
        raise ValueError(f"Invalid {curve.name} public point length")
    point = (int.from_bytes(point_bytes[:32], "big"), int.from_bytes(point_bytes[32:], "big"))
    _validate_public_point(curve, point)
    return point


def _validate_public_point(curve: Curve, point: tuple[int, int]) -> None:
    x, y = point
    p = curve.p
    if not (0 <= x < p and 0 <= y < p):
        raise ValueError(f"{curve.name} public point coordinate out of range")
    if (y * y - (x * x * x + curve.a * x + curve.b)) % p:
        raise ValueError(f"{curve.name} public point is not on the curve")


def _decode_public_key_der(der_data: bytes, curve: Curve = NIST256p) -> tuple[Curve, tuple[int, int]]:
    """
    Decodes a SubjectPublicKeyInfo, taking the curve from its OID, or a raw 64- or 65-byte point on `curve`.
    """

    if len(der_data) == 64:
        return curve, _decode_public_point(curve, der_data)
    if len(der_data) == 65:
        return curve, _decode_public_point(curve, der_data)

    items = _der_decode_sequence(der_data)
    if len(items) != 2 or items[0][0] != 0x30 or items[1][0] != 0x03:
        raise ValueError("Invalid SubjectPublicKeyInfo")
    curve = _decode_algorithm(items[0][1])
    bit_string = items[1][1]
    if not bit_string or bit_string[0] != 0:
        raise ValueError("Invalid public key BIT STRING")
    return curve, _decode_public_point(curve, bit_string[1:])


def _decode_private_key_der(der_data: bytes, curve: Curve = NIST256p) -> tuple[Curve, int]:
    """
    Decodes a PKCS#8 or SEC1 private key, taking the curve from its OID, or a raw 32-byte scalar on `curve`.
    """

    if len(der_data) == 32:
        return curve, int.from_bytes(der_data, "big")
    items = _der_decode_sequence(der_data)

    # PKCS#8 PrivateKeyInfo: version, AlgorithmIdentifier, SEC1 private key.
    if 3 <= len(items) <= 4 and items[0][0] == 0x02 and items[1][0] == 0x30 and items[2][0] == 0x04:
        if _der_decode_integer(items[0][1]) != 0:
            raise ValueError("Unsupported PKCS#8 private key version")
        try:
            pkcs8_curve = _decode_algorithm(items[1][1])
        except ValueError as e:
            raise ValueError("Unsupported private key algorithm or curve") from e
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
        return _decode_private_key_sec1(items[2][1], pkcs8_curve, required=True)

    return _decode_private_key_sec1(der_data, curve, required=False)


def _decode_private_key_sec1(der_data: bytes, curve: Curve, required: bool) -> tuple[Curve, int]:
    """
    Decodes a SEC1 ECPrivateKey. Its optional curve OID selects the curve; if `required` is true, `curve` came
    from an enclosing PKCS#8 structure, and the OID, when present, must name the same curve.
    """

    items = _der_decode_sequence(der_data)
    if len(items) < 2 or items[0][0] != 0x02 or items[1][0] != 0x04:
        raise ValueError("Invalid SEC1 private key")
    if _der_decode_integer(items[0][1]) != 1 or len(items[1][1]) != 32:
        raise ValueError("Invalid SEC1 private key version or length")

    secexp = int.from_bytes(items[1][1], "big")
    offset = 2
    if offset < len(items) and items[offset][0] == 0xA0:
        parameters = _der_parse_sequence(items[offset][1])
        if len(parameters) != 1 or parameters[0][0] != 0x06:
            raise ValueError("Unsupported SEC1 private key curve")
        sec1_curve = _CURVES_BY_OID.get(parameters[0][1])
        if sec1_curve is None or (required and sec1_curve is not curve):
            raise ValueError("Unsupported SEC1 private key curve")
        curve = sec1_curve
        offset += 1
    if offset < len(items) and items[offset][0] == 0xA1:
        public_key = _der_parse_sequence(items[offset][1])
        if len(public_key) != 1 or public_key[0][0] != 0x03 or not public_key[0][1] or public_key[0][1][0] != 0:
            raise ValueError("Invalid SEC1 private key public key")
        point = _decode_public_point(curve, public_key[0][1][1:])
        if not (1 <= secexp < curve.order) or point != _point_mul_g(curve, secexp):
            raise ValueError("SEC1 private key public key does not match private key")
        offset += 1
    if offset != len(items):
        raise ValueError("Invalid SEC1 private key field")
    return curve, secexp


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
        Returns the SPKI DER encoded bytes (91 bytes for NIST256p, 88 for SECP256k1).
        """
        return _der_tlv(0x30, _encode_algorithm(self.curve) + _der_tlv(0x03, b"\x00\x04" + self.to_string()))

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

        curve = self.curve
        n = curve.order

        if len(signature) != 64:
            raise BadSignatureError("Signature verification failed: invalid signature length")

        r = int.from_bytes(signature[:32], "big")
        s = int.from_bytes(signature[32:], "big")

        if not (1 <= r < n and 1 <= s < n):
            raise BadSignatureError("Signature verification failed: r or s out of range")

        if hashfunc is None:
            hashfunc = self.default_hashfunc

        h = hashfunc(data).digest()
        z = _digest_to_int(curve, h)

        w = pow(s, -1, n)
        u1 = (z * w) % n
        u2 = (r * w) % n

        gx, gy = curve.generator
        pub_x, pub_y = self.pubkey
        P1 = _mul_jacobian(curve, u1, gx, gy, 1)
        P2 = _mul_jacobian(curve, u2, pub_x, pub_y, 1)
        P = _add_jacobian(curve, P1[0], P1[1], P1[2], P2[0], P2[1], P2[2])
        aff = _to_affine(curve, P[0], P[1], P[2])

        if aff is None:
            raise BadSignatureError("Signature verification failed: point at infinity")

        if (aff[0] % n) != r:
            raise BadSignatureError("Signature verification failed")

        return True

    @classmethod
    def from_string(cls, string: str | bytes, curve: Curve = NIST256p, hashfunc: Any = hashlib.sha1) -> "VerifyingKey":
        if isinstance(string, str):
            string = string.encode("latin1")
        if len(string) == 64:
            return cls(curve=curve, point=_decode_public_point(curve, string), hashfunc=hashfunc)
        elif len(string) == 65 and string[0] == 4:
            return cls(curve=curve, point=_decode_public_point(curve, string), hashfunc=hashfunc)
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
        """
        Loads a SubjectPublicKeyInfo key on any supported curve, or a raw NIST256p point.
        """
        if isinstance(string, str):
            string = string.encode("latin1")
        curve, point = _decode_public_key_der(string)
        return cls(curve=curve, point=point, hashfunc=hashfunc)

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
        if not (1 <= privkey < curve.order):
            raise ValueError("Secret exponent out of range")
        self.curve = curve
        self.privkey: int = privkey
        self.default_hashfunc = hashfunc
        pub_point = _point_mul_g(curve, privkey)
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
        Returns the SEC1 EC PRIVATE KEY DER encoded bytes (121 bytes for NIST256p, 118 for SECP256k1).
        """
        return _der_tlv(
            0x30,
            _der_tlv(0x02, b"\x01")
            + _der_tlv(0x04, self.to_string())
            + _der_tlv(0xA0, _der_tlv(0x06, self.curve.oid))
            + _der_tlv(0xA1, _der_tlv(0x03, b"\x00\x04" + self.verifying_key.to_string())),
        )

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
        Signs `data` with ECDSA on this key's curve. Returns a 64-byte binary signature (r || s).
        """
        if isinstance(data, str):
            data = data.encode("utf-8")

        if hashfunc is None:
            hashfunc = self.default_hashfunc

        curve = self.curve
        n = curve.order
        gx, gy = curve.generator

        h = hashfunc(data).digest()
        z = _digest_to_int(curve, h)

        while True:
            if k is not None:
                nonce = k
            elif entropy is not None:
                nonce = int.from_bytes(entropy(32), "big") % (n - 1) + 1
            else:
                nonce = secrets.randbelow(n - 1) + 1

            if not (1 <= nonce < n):
                if k is not None:
                    raise ValueError("Specified nonce k is out of range")
                continue

            P_jac = _mul_jacobian(curve, nonce, gx, gy, 1)
            aff = _to_affine(curve, P_jac[0], P_jac[1], P_jac[2])
            if aff is None:
                continue

            r = aff[0] % n
            if r == 0:
                if k is not None:
                    raise ValueError("Signing produced r = 0 with fixed k")
                continue

            k_inv = pow(nonce, -1, n)
            s = (k_inv * (z + r * self.privkey)) % n
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

            if 1 <= secexp < curve.order:
                return cls(curve=curve, privkey=secexp, hashfunc=hashfunc)

    @classmethod
    def from_secret_exponent(
        cls,
        secexp: int,
        curve: Curve = NIST256p,
        hashfunc: Any = hashlib.sha1
    ) -> "SigningKey":
        if not (1 <= secexp < curve.order):
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
        """
        Loads a SEC1 or PKCS#8 private key on any supported curve, or a raw NIST256p scalar.
        """
        if isinstance(string, str):
            string = string.encode("latin1")
        curve, secexp = _decode_private_key_der(string)
        return cls.from_secret_exponent(secexp, curve=curve, hashfunc=hashfunc)

    @classmethod
    def from_pem(
        cls,
        string: str | bytes,
        hashfunc: Any = hashlib.sha1,
        valid_curve_encodings: Any = None
    ) -> "SigningKey":
        der_bytes = _unwrap_pem(string, ("EC PRIVATE KEY", "PRIVATE KEY"))
        return cls.from_der(der_bytes, hashfunc=hashfunc)
