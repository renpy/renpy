# Copyright 2004-2022 Tom Rothamel <pytom@bishoujo.us>
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
import os
import zipfile

import renpy


# The directory containing the save token information.
token_dir = None # type: str|None

# The save token that is used for this computer. This may also
# be a space separated list of tokens.
token = None # type: str|None

# A set of save tokens that the user considers valid.
save_tokens = set() # type: set[str]

# True if the save files and persistent data should be upgraded.
should_upgrade = False # type: bool

def check_load(token):
    """
    This checks the token that was loaded from a save file to see if it's
    valid. If not, it will prompt the user to confirm the load.
    """

    if token_dir is None:
        return True

    if token is None:
        return True

    # The web sandbox should be enough.
    if renpy.emscripten:
        return True

    for i in token.split():
        if i and (i in save_tokens):
            return True

    def ask(prompt):
        """
        Asks the user a yes/no question. Returns True if the user says yes,
        and false otherwise.
        """

        return renpy.exports.invoke_in_new_context(renpy.store.layout.yesno_prompt, None, prompt)

    if not ask(renpy.store.gui.UNKNOWN_TOKEN):
        return False

    if token and ask(renpy.store.gui.TRUST_TOKEN):

        tokens_txt = os.path.join(token_dir, "security_tokens.txt")

        for i in token.split():
            if i not in save_tokens:
                save_tokens.add(i)

                with open(tokens_txt, "a") as f:
                        f.write(i + "\n")

    return True


def check_persistent(token):
    """
    This checks a persistent file to see if the token is valid.
    """

    for i in token.split():
        if i and (i in save_tokens):
            return True

    if should_upgrade:
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

    token = base64.b64encode(os.urandom(32)).decode("utf-8")

    with open(filename, "w") as f:
        f.write(token + "\n")

def upgrade_savefile(fn):
    """
    Given a savegame, fn, upgrades it to include the token.
    """

    if token is None:
        return

    with zipfile.ZipFile(fn, "a") as zf:

        if "token.txt" in zf.namelist():
            return

        zf.writestr("token.txt", token)

def upgrade_all_savefiles():

    if token is None:
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
    global token
    global save_tokens
    global should_upgrade

    if renpy.config.save_directory is None:
        should_upgrade = True
        return

    # Determine the current save token, and the list of accepted save tokens.
    token_dir = renpy.__main__.path_to_saves(renpy.config.gamedir, "tokens")

    tokens_txt = os.path.join(token_dir, "security_tokens.txt")

    if not os.path.exists(tokens_txt):
        create_token(tokens_txt)

    with open(tokens_txt, "r") as f:
        tokens = f.read().splitlines()

    token = tokens[0]
    save_tokens = set(tokens)

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
