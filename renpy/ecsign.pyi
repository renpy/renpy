# Copyright 2004-2025 Tom Rothamel <pytom@bishoujo.us>
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

def GeneratePrivateKeyAsDER() -> bytes | None:
    """
        Generates a EC private key
    """

def SignDataWithDER(data : bytes, private_key : bytes) -> bytes:
    """
        returns ecdsa signature for data using sha1 hash

        `data`
            The data to sign

        `private_key`
            The private key to use (EC)
    """

def VerifyDataWithDER(data : bytes, public_key : bytes, sign : bytes) -> bool:
    """
        verifies ecdsa signature for data using sha1 hash and returns result

        `data`
            The data to sign

        `public_key`
            The private key to use (EC)

        `sign`
            The signature to verify
    """

def GetPublicKeyFromPrivateDER(private_key : bytes) -> bytes | None:
    """
        returns public key from the private key

        `private_key`
            The private key to use (EC)
    """

def VerifyPrivateKeyDER(private_key : bytes) -> bool:
    """
        Verifies if given key is a valid private key
    """

def VerifyPublicKeyDER(public_key : bytes) -> bool:
    """
        Verifies if given key is a valid public key
    """
