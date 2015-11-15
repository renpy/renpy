# Copyright 2004-2015 Tom Rothamel <pytom@bishoujo.us>
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

import collections
import renpy
import os
import codecs

# A map from filename to position, target label pairs.
missing = collections.defaultdict(list)

def report_missing(target, filename, position):
    """
    Reports that the call statement ending at `position` in `filename`
    is missing a from clause.

    `target`
        The string
    """

    missing[filename].append((position, target))


# Labels that we've created while running add_from.
new_labels = set()

def generate_label(target):
    """
    Generate a reasonable and unique new label for a call to `target`.
    """

    n = 0

    while True:
        if n:
            label = "_call_{}_{}".format(target, n)
        else:
            label = "_call_{}".format(target)

        if not renpy.exports.has_label(label) and not (label in new_labels):
            break

        n += 1

    new_labels.add(label)
    return label


def process_file(fn):
    """
    Adds missing from clauses to `fn`.
    """

    if not os.path.exists(fn):
        return

    edits = missing[fn]
    edits.sort()

    with codecs.open(fn, "r", "utf-8") as f:
        data = f.read()

    # How much of the input has been consumed.
    consumed = 0

    # The output.
    output = u""

    for position, target in edits:
        output += data[consumed:position]
        consumed = position

        output += " from {}".format(generate_label(target))

    output += data[consumed:]

    with codecs.open(fn + ".new", "w", "utf-8") as f:
        f.write(output)

    try:
        os.unlink(fn + ".bak")
    except:
        pass

    os.rename(fn, fn + ".bak")
    os.rename(fn + ".new", fn)

def add_from():

    renpy.arguments.takes_no_arguments("Adds from clauses to call statements that are missing them.")

    for fn in missing:
        if fn.startswith(renpy.config.gamedir):
            process_file(fn)

    return False

renpy.arguments.register_command("add_from", add_from)

