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

# This file contains the add_ids command, which adds an id clause to each
# say statement that doesn't have one, using the translation identifier
# Ren'Py generated for it. Once a say statement has an explicit identifier,
# changing its text no longer changes the identifier, so translations, voice
# files, and speech bubbles keep matching it.

import collections
import os

import renpy


def in_game_directory(filename):
    """
    Returns true if the elided `filename` is in the game directory, but not
    in the translation (tl) directory under it.
    """

    gamedir = os.path.abspath(renpy.config.gamedir)
    tldir = os.path.join(gamedir, "tl")

    fn = os.path.abspath(renpy.lexer.unelide_filename(filename))

    if not fn.startswith(gamedir + os.sep):
        return False

    return not fn.startswith(tldir + os.sep)


def find_edits():
    """
    Finds the say statements that need an id clause.

    Returns a tuple of (edits, skipped). `edits` is a map from elided filename
    to a list of (linenumber, identifier) pairs. `skipped` is a list of
    (filename, linenumber, reason) tuples for say statements that were
    found, but that can't be given an id clause.
    """

    translator = renpy.game.script.translator

    # A map from (filename, linenumber) to the identifiers of the say
    # statements on that line. A logical line normally has one say statement,
    # but monologue mode produces several from a single statement.
    by_line = collections.defaultdict(list)

    for identifier, node in translator.default_translates.items():
        if isinstance(node, renpy.ast.TranslateSay):
            says = [node]
        else:
            says = [i for i in node.block if isinstance(i, renpy.ast.Say)]

        if not says:
            continue

        say = says[-1]

        if say.explicit_identifier:
            continue

        if not in_game_directory(say.filename):
            continue

        by_line[(say.filename, say.linenumber)].append(identifier)

    edits = collections.defaultdict(list)
    skipped = []

    for (filename, linenumber), identifiers in by_line.items():
        if len(identifiers) > 1:
            skipped.append((
                filename,
                linenumber,
                "monologue mode say statements can't take an id clause. Split the statement up, or add ids by hand.",
            ))
            continue

        edits[filename].append((linenumber, identifiers[0]))

    return edits, skipped


def process_file(filename, edits, dry_run):
    """
    Adds id clauses to the say statements in `filename`, an elided filename.

    `edits`
        A list of (linenumber, identifier) pairs.

    `dry_run`
        If true, the changes are reported but not made.

    Returns the number of id clauses added, and a list of
    (filename, linenumber, reason) tuples for lines that were skipped.
    """

    renpy.scriptedit.ensure_loaded(filename)

    fullfn = renpy.lexer.unelide_filename(filename)

    # The line positions in renpy.scriptedit are computed on the file as
    # read in text mode, with newlines translated to \n. Read the file the
    # same way, but remember what the line endings were so they can be
    # written back unchanged.
    with open(fullfn, "rb") as f:
        newline = "\r\n" if b"\r\n" in f.read() else "\n"

    with open(fullfn, "r", encoding="utf-8") as f:
        data = f.read()

    # How much of the input has been consumed.
    consumed = 0

    # The output.
    output = ""

    count = 0
    skipped = []

    for linenumber, identifier in sorted(edits):
        line = renpy.scriptedit.lines.get((filename, linenumber), None)

        if line is None:
            skipped.append((filename, linenumber, "couldn't find the line in the file."))
            continue

        end = line.end

        if end < consumed:
            skipped.append((filename, linenumber, "couldn't find the end of the statement."))
            continue

        if dry_run:
            print(f"{filename}:{linenumber}: would add id {identifier}")
        else:
            output += data[consumed:end]
            output += " id " + identifier
            consumed = end

        count += 1

    if dry_run or not count:
        return count, skipped

    output += data[consumed:]

    with open(fullfn + ".new", "w", encoding="utf-8", newline=newline) as f:
        f.write(output)

    try:
        os.unlink(fullfn + ".bak")
    except OSError:
        pass

    os.rename(fullfn, fullfn + ".bak")
    os.rename(fullfn + ".new", fullfn)

    return count, skipped


def add_ids_command():
    ap = renpy.arguments.ArgumentParser(
        description="Adds an id clause to each say statement that doesn't have one, so that the translation identifier stays the same when the dialogue is changed."
    )

    ap.add_argument(
        "--dry-run",
        action="store_true",
        help="Reports the id clauses that would be added, without changing any files.",
    )

    args = ap.parse_args()

    edits, skipped = find_edits()

    total = 0

    for filename in sorted(edits):
        count, file_skipped = process_file(filename, edits[filename], args.dry_run)
        skipped.extend(file_skipped)
        total += count

        if not args.dry_run and count:
            print(f"{filename}: added {count} id clause{'' if count == 1 else 's'}.")

    for filename, linenumber, reason in sorted(skipped):
        print(f"{filename}:{linenumber}: skipped, {reason}")

    if args.dry_run:
        print(f"{total} id clause{'' if total == 1 else 's'} would be added.")
    elif not total:
        print("Every say statement already has an id clause.")

    return False


renpy.arguments.register_command("add_ids", add_ids_command)
