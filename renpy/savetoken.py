# Copyright 2004-2023 Tom Rothamel <pytom@bishoujo.us>
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

from __future__ import division, absolute_import, with_statement, print_function, unicode_literals
from renpy.compat import PY2, basestring, bchr, bord, chr, open, pystr, range, round, str, tobytes, unicode # *

import base64
import ecdsa
import os
import zipfile

import renpy


# The directory containing the save token information.
token_dir = None # type: str|None

# A list of the keys used to sign saves, stored as DER-encoded strings.
signing_keys = [ ] # type: list[str]

# A list of the keys used to verify saves, stored as DER-encoded strings.
verifying_keys = [ ] # type: list[str]

# True if the save files and persistent data should be upgraded.
should_upgrade = False # type: bool

def encode_line(key, a, b=None): #type (str, bytes, bytes|None) -> str
    """
    This encodes a line that contains a key and up to 2 base64-encoded fields.
    It returns the line with the newline appended, as a string.
    """

    if b is None:
        return key + " " + base64.b64encode(a).decode("ascii") + "\n"
    else:
        return key + " " + base64.b64encode(a).decode("ascii") + " " + base64.b64encode(b).decode("ascii") + "\n"

def decode_line(line): #type (str) -> (str, bytes, bytes|None)
    """
    This decodes a line that contains a key and up to 2 base64-encoded fields.
    It returns a tuple of the key, the first field, and the second field.
    If the second field is not present, it is None.
    """

    line = line.strip()

    if not line or line[0] == "#":
        return '', b'', None

    parts = line.split(None, 2)

    try:
        if len(parts) == 2:
            return parts[0], base64.b64decode(parts[1]), None
        else:
            return parts[0], base64.b64decode(parts[1]), base64.b64decode(parts[2])
    except Exception:
        return '', b'', None


def sign_data(data):
    """
    Signs `data` with the signing keys and returns the
    signature. If there are no signing keys, returns None.
    """

    rv = ""

    for i in signing_keys:
        sk = ecdsa.SigningKey.from_der(i)

        if sk is not None and sk.verifying_key is not None:
            sig = sk.sign(data)
            rv += encode_line("signature", sk.verifying_key.to_der(), sig)

    return rv

def verify_data(data, signatures, check_verifying=True):
    """
    Verifies that `data` has been signed by the keys in `signatures`.
    """

    for i in signatures.splitlines():
        kind, key, sig = decode_line(i)

        if kind == "signature":

            if key is None:
                continue

            if check_verifying and key not in verifying_keys:
                continue

            try:
                vk = ecdsa.VerifyingKey.from_der(key)
                if vk.verify(sig, data):
                    return True
            except Exception:
                continue

    return False

def get_keys_from_signatures(signatures):
    """
    Given a string containing signatures, get the verification keys
    for those signatures.
    """

    rv = [ ]

    for l in signatures.splitlines():
        kind, key, _ = decode_line(l)

        if kind == "signature":
            rv.append(key)

    return rv

def check_load(log, signatures):
    """
    This checks the token that was loaded from a save file to see if it's
    valid. If not, it will prompt the user to confirm the load.
    """

    if token_dir is None:
        return True

    if not signing_keys:
        return True

    # The web sandbox should be enough.
    if renpy.emscripten:
        return True

    if verify_data(log, signatures):
        return True

    def ask(prompt):
        """
        Asks the user a yes/no question. Returns True if the user says yes,
        and false otherwise.
        """

        return renpy.exports.invoke_in_new_context(renpy.store.layout.yesno_prompt, None, prompt)

    if not ask(renpy.store.gui.UNKNOWN_TOKEN):
        return False

    new_keys = [ i for i in get_keys_from_signatures(signatures) if i not in verifying_keys ]

    if new_keys and ask(renpy.store.gui.TRUST_TOKEN):

        keys_text = os.path.join(token_dir, "security_keys.txt")

        with open(keys_text, "a") as f:
            for k in new_keys:
                f.write(encode_line("verifying-key", k))
                verifying_keys.append(k)

    if not signatures:
        return True

    # This check catches the case where the signature is not correct.
    return verify_data(log, signatures, False)


def check_persistent(data, signatures):
    """
    This checks a persistent file to see if the token is valid.
    """

    if should_upgrade:
        return True

    if verify_data(data, signatures):
        return True

    return False

def create_token(filename):
    """
    Creates a token and writes it to `filename`, if possible.
    """

    try:
        os.makedirs(os.path.dirname(filename))
    except Exception:
        pass

    sk = ecdsa.SigningKey.generate(curve=ecdsa.NIST256p)
    vk = sk.verifying_key
    if vk is not None:
        line = encode_line("signing-key", sk.to_der(), vk.to_der())

        with open(filename, "w") as f:
            f.write(line)

def upgrade_savefile(fn):
    """
    Given a savegame, fn, upgrades it to include the token.
    """

    if signing_keys is None:
        return

    with zipfile.ZipFile(fn, "a") as zf:

        if "signatures" in zf.namelist():
            return

        log = zf.read("log")
        zf.writestr("signatures", sign_data(log))

def upgrade_all_savefiles():

    if token_dir is None:
        return

    if not should_upgrade:
        return

    upgraded_txt = os.path.join(token_dir, "upgraded.txt")

    for fn in renpy.loadsave.location.list_files():
        try:
            upgrade_savefile(fn)
        except:
            renpy.display.log.write("Error upgrading save file:")
            renpy.display.log.exception()

    upgraded = True

    with open(upgraded_txt, "a") as f:
        f.write(renpy.config.save_directory + "\n")


def init_tokens():
    global token_dir
    global signing_keys
    global verifying_keys
    global should_upgrade

    if renpy.config.save_directory is None:
        should_upgrade = True
        return

    # Determine the current save token, and the list of accepted save tokens.
    token_dir = renpy.__main__.path_to_saves(renpy.config.gamedir, "tokens")

    if token_dir is None:
        return

    keys_fn = os.path.join(token_dir, "security_keys.txt")

    if not os.path.exists(keys_fn):
        create_token(keys_fn)

    # Load the signing and verifying keys.
    with open(keys_fn, "r") as f:
        for l in f:
            kind, key, _ = decode_line(l)

            if kind == "signing-key":
                sk = ecdsa.SigningKey.from_der(key)
                if sk is not None and sk.verifying_key is not None:
                    signing_keys.append(sk.to_der()) # type: ignore
                    verifying_keys.append(sk.verifying_key.to_der())
            elif kind == "verifying-key":
                verifying_keys.append(key) # type: ignore

    # Process config.save_token_keys

    for tk in renpy.config.save_token_keys:

        k = base64.b64decode(tk)
        try:
            vk = ecdsa.VerifyingKey.from_der(k)
            verifying_keys.append(k) # type: ignore
        except Exception:
            try:
                sk = ecdsa.SigningKey.from_der(k)
            except Exception:
                raise Exception("In config.save_token_keys, the key {!r} is not a valid key.".format(tk))

            if sk.verifying_key is not None:
                vk = base64.b64encode(sk.verifying_key.to_der()).decode("utf-8")
            else:
                vk = ""

            raise Exception("In config.save_token_keys, the signing key {!r} was provided, but the verifying key {!r} is required.".format(tk, vk)) # type: ignore

    # Determine if we need to upgrade the current game.

    upgraded_txt = os.path.join(token_dir, "upgraded.txt")

    if os.path.exists(upgraded_txt):
        with open(upgraded_txt, "r") as f:
            upgraded_games = f.read().splitlines()
    else:
        upgraded_games = [ ]

    if renpy.config.save_directory in upgraded_games:
        return

    should_upgrade = True


def init():
    try:
        init_tokens()
    except Exception:
        renpy.display.log.write("Initializing save token:")
        renpy.display.log.exception()

        import traceback
        traceback.print_exc()

def get_save_token_keys():
    """
    :undocumented:

    Returns the list of save token keys.
    """

    rv = [ ]

    for i in signing_keys:
        sk = ecdsa.SigningKey.from_der(i)

        if sk.verifying_key is not None:
            rv.append(base64.b64encode(sk.verifying_key.to_der()).decode("utf-8"))

    return rv
