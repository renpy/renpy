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


from collections import defaultdict
from pathlib import Path
import renpy
import os

# A map from filename to position, target label pairs.
missing = defaultdict[str, list[tuple[int, str]]](list)


def report_missing(target: str, filename: str, number: int):
    """
    Reports that the call statement ending at `position` in `filename`
    is missing a from clause.
    """

    missing[filename].append((number, target))


# Labels that we've created while running add_from.
new_labels = set()


def generate_label(target):
    """
    Generate a reasonable and unique new label for a call to `target`.
    """

    target = target.replace(".", "_")

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


def process_file(fn: str, full_fn: str):
    """
    Adds missing from clauses to `fn`.
    """

    path = Path(full_fn)
    if not path.exists():
        return

    if (lines := renpy.scriptedit.ensure_loaded(full_fn)) is None:
        return

    edits = missing[fn]
    edits.sort()
    edits = iter(edits)
    next_edit, target = next(edits)

    new_lines = []
    for lineno, line in lines.items():
        if lineno == next_edit:
            code = f" from {generate_label(target)}"
            full_text = line.with_added_code(code)
        else:
            full_text = line.full_text

        new_lines.append(full_text)

    new_path = path.with_suffix(f"{path.suffix}.new")
    with new_path.open("w", encoding="utf-8") as f:
        f.write("\ufeff")
        f.writelines(new_lines)

    bak_path = path.with_suffix(f"{path.suffix}.bak")
    bak_path.unlink(missing_ok=True)

    path.rename(bak_path)
    new_path.rename(path)


def add_from():

    renpy.arguments.takes_no_arguments("Adds from clauses to call statements that are missing them.")

    for fn in missing:
        full_fn = renpy.parser.unelide_filename(fn)
        if full_fn.startswith(renpy.config.gamedir):
            process_file(fn, full_fn)

    return False


renpy.arguments.register_command("add_from", add_from)
