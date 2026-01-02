# Copyright 2026 B.Kats and Tom Rothamel <pytom@bishoujo.us>
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

def generate_private_key() -> bytes | None:
    """
        Generates a EC private key and return key in DER format
    """

def sign_data(data : bytes, private_key : bytes) -> bytes:
    """
        returns ecdsa signature for data using sha1 hash

        `data`
            The data to sign

        `private_key`
            The private key to use in DER format
    """

def verify_data(data : bytes, public_key : bytes, sign : bytes) -> bool:
    """
        verifies ecdsa signature for data using sha1 hash and returns result

        `data`
            The data to sign

        `public_key`
            The public key to use in DER format

        `sign`
            The signature to verify
    """

def get_public_key_from_private(private_key : bytes) -> bytes | None:
    """
        returns public key in DER format from the private key

        `private_key`
            The private key to use in DER format
    """

def validate_private_key(private_key : bytes) -> bool:
    """
        Validates if given key is a private key
    """

def validate_public_key(public_key : bytes) -> bool:
    """
        Validates if given key is a public key
    """

def pem_to_der(pem : bytes | str) -> bytes:
    """
        unpacks DER from a PEM file
    """

def der_to_pem(der : bytes, name : str) -> bytes:
    """
        packs a DER into a PEM file
    """
