# Copyright 2004-2024 Tom Rothamel <pytom@bishoujo.us>
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

py_branch_to_version = { }

import sys
import os

class Version(object):

    def __init__(self, branch, python, version, name):
        """
        `branch`
            The name of the branch, as a string.
        `python`
            The version of python, 2 or 3.
        `version`
            The Ren'Py version number, a string.
        `name`
            The Ren'Py version name.
        """

        self.branch = branch
        self.python = python
        self.version = version
        self.name = name

        py_branch_to_version[(python, branch)] = self

Version("main", 3, "8.3.0", "TBD")
Version("main", 2, "7.8.0", "TBD")

Version("fix", 3, "8.2.1", "64bit Sensation")
Version("fix", 2, "7.7.1", "32bit Sensation")


def make_dict(branch, suffix="00000000", official=False, nightly=False):
    """
    Returns a dictionary that contains the information usually stored
    in vc_version.py.

    `branch`
        The branch.

    `suffix`
        The suffix, normally the YYMMDDCC code.

    `official`
        True if this is an official release.

    `nightly`
        True if this is a nightly release.
    """

    py = sys.version_info.major
    version = py_branch_to_version.get((py, branch)) or py_branch_to_version[(py, "main")]

    return {
        "version" : version.version + "." + str(suffix),
        "version_name" : version.name,
        "official" : official,
        "nightly" : nightly,
        "branch" : branch,
    }

def get_version():
    """
    Tries to return a version dict without using the information in
    vc_version.
    """

    import re

    git_head = os.path.join(os.path.dirname(__file__), "..", ".git", "HEAD")

    branch = "main"

    try:

        for l in open(git_head, "r"):
            l = l.rstrip()
            m = re.match(r"ref: refs/heads/(.*)", l)
            if m:
                branch = m.group(1)
                break

    except:
        import traceback
        traceback.print_exc()

    return make_dict(branch)



def generate_vc_version(nightly=False):
    """
    Generates the vc_version.py file.

    `nightly`
        If true, the nightly flag is set.
    """

    import subprocess
    import collections
    import socket
    import time

    try:

        branch = subprocess.check_output([ "git", "branch", "--show-current" ]).decode("utf-8").strip()

        s = subprocess.check_output([ "git", "describe", "--tags", "--dirty", ]).decode("utf-8").strip()
        parts = s.strip().split("-")
        dirty = "dirty" in parts

        commits_per_day = collections.defaultdict(int)

        for i in subprocess.check_output([ "git", "log", "-99", "--pretty=%cd", "--date=format:%Y%m%d" ]).decode("utf-8").split():
            commits_per_day[i[2:]] += 1

        if dirty:
            key = time.strftime("%Y%m%d")[2:]
            vc_version = "{}{:02d}".format(key, commits_per_day[key] + 1)
        else:
            key = max(commits_per_day.keys())
            vc_version = "{}{:02d}".format(key, commits_per_day[key])

    except Exception:
        branch = "main"
        vc_version = "00000000"
        official = False

    version_dict = make_dict(
        branch,
        suffix=vc_version,
        official=socket.gethostname() == "eileen",
        nightly=nightly)

    vc_version_fn = os.path.join(os.path.dirname(__file__), "vc_version.py")

    with open(vc_version_fn, "w") as f:
        for k, v in sorted(version_dict.items()):
            f.write("{} = {!r}\n".format(k, v))

    return version_dict


def main():
    import argparse

    ap = argparse.ArgumentParser()
    ap.add_argument("--nightly", action="store_true", help="Set the nightly flag.")
    args = ap.parse_args()

    generate_vc_version(nightly=args.nightly)


if __name__ == "__main__":
    main()
