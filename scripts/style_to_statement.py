from __future__ import print_function
# Scans a file for python style assignments, and turns such lines into
# style statements.
#
# The result of this probably won't be legal Ren'Py, but it should be
# a reasonable starting point for conversions.

import argparse
import sys
import os
import re

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import renpy

renpy.import_all()
renpy.config.basedir = '/'
renpy.config.renpy_base = '/'

def main():

    ap = argparse.ArgumentParser()
    ap.add_argument("script")
    args = ap.parse_args()

    current_name = None
    current_parent = None
    current_entries = None

    def emit():
        if not current_name:
            return

        print()

        if current_parent and current_entries:
            print("style {} is {}:".format(current_name, current_parent))
        elif current_parent:
            print("style {} is {}".format(current_name, current_parent))
        elif current_entries:
            print("style {}:".format(current_name))
        else:
            print("style {}".format(current_name))

        for name, expr in current_entries:
            if expr:
                print("    {} {}".format(name, expr.strip()))
            else:
                print("    {}".format(name))


    for _fn, _lineno, l in renpy.parser.list_logical_lines(args.script):

        m = re.search(r'style\.(\w+)\s*=\s*Style\(\s*(["\'](\w+)["\']|style\.(\w+))', l)

        new_name = None
        new_parent = None
        new_entries = [ ]

        if m:
            name = m.group(1)
            parent = m.group(3) or m.group(4)

            new_name = name
            new_parent = parent

        m = re.search(r'style\.create\(["\'](\w+)["\'],\s*["\'](\w+)["\']', l)
        if m:
            new_name = m.group(1)
            new_parent = m.group(2)

        m = re.search(r'style\.(\w+)\.(\w+)\s*=\s*(.*)', l, re.S)
        if m:
            new_name = m.group(1)
            new_entries.append((m.group(2), m.group(3)))

        m = re.search(r'style\.(\w+)\.clear\(\)', l)
        if m:
            new_name = m.group(1)
            new_entries.append(("clear", None))

        m = re.search(r'style\.(\w+)\.take\((.*)\)', l)
        if m:
            new_name = m.group(1)
            new_entries.append(("take", m.group(2)))

        m = re.search(r'style\.(\w+)\.set_parent\(style\.(.*)\)', l)
        if m:
            new_name = m.group(1)
            new_entries.append(("is", m.group(2)))

        m = re.search(r'style\.(\w+)\.set_parent\([\'"](.*)[\'"]\)', l)
        if m:
            new_name = m.group(1)
            new_entries.append(("is", m.group(2)))

        if new_name is None:
            continue

        if new_name != current_name:
            emit()
            current_name = new_name
            current_parent = new_parent
            current_entries = new_entries
        else:
            if new_parent:
                current_parent = new_parent

            current_entries.extend(new_entries)

    emit()





if __name__ == "__main__":
    main()
