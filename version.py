#!/usr/bin/env python3

py_branch_to_version = { }

class Version(object):


    def __init__(self, branch, python, version, name="TBD"):
        """
        `branch`
            The name of the branch, as a string. This is used to determine
        `python`
            The version of python.
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

Version("main", 3, "8.2.0")
Version("main", 2, "7.7.0")

Version("fix", 3, "8.1.1", "Where No One Has Gone Before")
Version("fix", 2, "7.6.1", "To Boldy Go")


import subprocess
import collections
import socket
import time
import sys
import os

ROOT = os.path.dirname(os.path.abspath(__file__))
os.chdir(ROOT)
def generate_vc_version(nightly=False):

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
        vc_version = 0

    py = sys.version_info.major

    version = py_branch_to_version.get((py, branch)) or py_branch_to_version[(py, "main")]

    contents = {
        "version" : version.version + "." + str(vc_version),
        "name" : version.name,
        "official" : socket.gethostname() == "eileen",
        "nightly" : nightly,
    }

    with open("renpy/vc_version.py", "w") as f:
        for k, v in sorted(contents.items()):
            f.write("{} = {!r}\n".format(k, v))


def main():
    import argparse

    ap = argparse.ArgumentParser()
    ap.add_argument("--nightly", action="store_true", help="Set the nightly flag.")

    args = ap.parse_args()

    generate_vc_version(nightly=args.nightly)


if __name__ == "__main__":
    main()
