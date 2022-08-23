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


import collections
import renpy
import os

# A map from filename to linenumber, position label pairs.
missing = collections.defaultdict(list)


def report_missing(filename, position, linenumber):
    """
    Reports that the say statement in `filename` at `linenumber`
    is missing an id clause, and that it's ending at `position`.
    """

    missing[filename].append((linenumber, position))


def process_file(short_fn, identifiers):
    """
    Adds missing id clauses to `short_fn`.
    """

    edits = sorted(missing[short_fn]) # list of (linenumber, position) tuples.

    fn = os.path.join(renpy.config.basedir, short_fn)

    if not os.path.exists(fn):
        return

    with open(fn, "rb") as f:
        data = f.read().decode("utf-8")

    # How much of the input has been consumed.
    consumed = 0

    # The output.
    output = u""

    for linenumber, position in edits:
        identifier = identifiers[short_fn, linenumber]
        output += data[consumed:position]
        consumed = position

        output += " id {}".format(identifier)

    output += data[consumed:]

    with open(fn + ".new", "wb") as f:
        f.write(output.encode("utf-8"))

    try:
        os.unlink(fn + ".bak")
    except Exception:
        pass

    os.rename(fn, fn + ".bak")
    os.rename(fn + ".new", fn)

    return True


def add_id():

    renpy.arguments.takes_no_arguments("Adds id clauses to say statements that are missing them.")

    all_stmts = sorted(renpy.game.script.all_stmts, key=(lambda n : n.filename))

    identifiers = {}

    for node in all_stmts:
        if node.filename in missing:
            if isinstance(node, renpy.ast.Translate) and (node.language is None):
                identifiers[node.filename, node.linenumber] = node.identifier

    for fn in missing:
        process_file(fn, identifiers)

    return False


renpy.arguments.register_command("add_id", add_id)
