#!/usr/bin/env python

# The path to a copy of Atom that's been installed globally, if one exists.
# This is overidden by RENPY_ATOM, if set. If either is given, that is used
# and no special handing of the .atom directory is performed.
ATOM = None

import sys
import os
import subprocess
import platform
import shutil

import renpy


class Editor(renpy.editor.Editor):

    has_projects = True

    def get_atom(self):
        """
        Returns the path to the atom executable, if None. Also takes care
        of setting up the .atom directory if it's not available.
        """

        atom = os.environ.get("RENPY_ATOM", ATOM)

        if atom is not None:
            return atom

        DIR = os.path.abspath(os.path.dirname(os.path.dirname(__file__)))
        DIR = os.path.join(renpy.exports.fsdecode(DIR), "atom")

        if renpy.windows:
            atom = os.path.join(DIR, "atom-windows", "atom.exe")
        elif renpy.macintosh:
            atom = os.path.join(DIR, "Atom.app", "Contents", "Resources", "app", "atom.sh")
        else:
            atom = os.path.join(DIR, "atom-linux-" + platform.machine(), "atom")

        default_dot_atom = os.path.join(DIR, "default-dot-atom")
        dot_atom = os.path.join(DIR, ".atom")

        if not os.path.exists(dot_atom) and os.path.exists(default_dot_atom):
            shutil.copytree(default_dot_atom, dot_atom)

        return atom

    def begin(self, new_window=False, **kwargs):
        self.args = [ ]

    def open(self, filename, line=None, **kwargs):

        if line:
            filename = "{}:{}".format(filename, line)

        self.args.append(filename)

    def open_project(self, project):
        self.args.append(project)

    def end(self, **kwargs):

        atom = self.get_atom()

        self.args.reverse()

        args = [ atom ] + self.args
        args = [ renpy.exports.fsencode(i) for i in args ]

        subprocess.Popen(args)


def main():
    e = Editor()
    e.begin()

    for i in sys.argv[1:]:
        e.open(i)

    e.end()


if __name__ == "__main__":
    main()
