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

from typing import TypedDict

import site
import socket
import pathlib
import subprocess
import collections

py_branch_to_version = {}


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


Version("main", 3, "8.6.0", "Real Artists Ship")

Version("fix", 3, "8.5.1", "In Good Health")


class VersionDict(TypedDict):
    """
    Dictionary that stores all the data about current running version.
    """

    version: str
    "The full version number with suffixes as a string."
    name: str
    "The name of the version."
    branch: str
    "The name of the branch from which this version was made."
    official: bool
    "True if this is an official release."
    nightly: bool
    "True if this is a nightly build."
    dirty: bool
    "True if working tree was dirty when this version was made."


def get_vc_version() -> VersionDict | None:
    """
    Return version dict from vc_version.py if it exists or None otherwise.
    """

    # vc_version.py contains:
    # branch - Name of the branch from which this the file was generated.
    # official - True if it were an official build.
    # nightly - True if it were a nightly build.
    # version - Semver as a string.
    # version_name - Name of the version.
    try:
        import renpy.vc_version as vc_version  # type: ignore
    except ImportError:
        return None

    return VersionDict(
        branch=vc_version.branch,
        official=vc_version.official and getattr(site, "renpy_build_official", False),
        nightly=vc_version.nightly,
        version=vc_version.version,
        name=vc_version.version_name,
        dirty=getattr(vc_version, "dirty", False),
    )


def get_git_version(nightly: bool = False) -> VersionDict:
    """
    Return `Version` read from the git repository if it exists or None otherwise.
    """

    def get_output(args: list[str]) -> str:
        return subprocess.check_output(args, encoding="utf-8").strip()

    try:
        git_root = get_output(["git", "rev-parse", "--show-toplevel"])

        root = pathlib.Path(__file__).parent.parent
        if not root.samefile(git_root):
            raise Exception("Current git repository is not Ren'Py repository.")

        branch = get_output(["git", "branch", "--show-current"])
        dirty = get_output(["git", "status", "--porcelain"]) != ""
        commits = get_output(["git", "log", "-99", "--pretty=%cd", "--date=format:%y%m%d"])

        commits_per_day = collections.Counter[str](commits.split())
        key = max(commits_per_day.keys())
        commit = f"{key}{commits_per_day[key]:02d}"

    except Exception:
        import traceback

        traceback.print_exc()

        branch = "unknown"
        commit = "00000000"

    if (3, branch) in py_branch_to_version:
        version_obj = py_branch_to_version[3, branch]
    else:
        version_obj = py_branch_to_version[3, "main"]

    return VersionDict(
        version=f"{version_obj.version}.{commit}",
        name=version_obj.name,
        branch=branch,
        official=socket.gethostname() == "eileen",
        nightly=nightly,
        dirty=dirty,
    )


def get_version() -> VersionDict:
    """
    Return a version dict either from local vc_version or from git.
    """

    if (vc_version := get_vc_version()) is not None:
        return vc_version

    return get_git_version()


def generate_vc_version(nightly: bool = False) -> VersionDict:
    """
    Generates the vc_version.py file.

    `nightly`
        If true, the nightly flag is set.
    """

    version_dict = get_git_version(nightly)

    vc_version_path = pathlib.Path(__file__).parent / "vc_version.py"

    with vc_version_path.open("w") as f:
        print(f"branch = '{version_dict['branch']}'", file=f)
        if version_dict["dirty"]:
            print("dirty = True", file=f)
        print(f"official = {version_dict['official']}", file=f)
        print(f"nightly = {version_dict['nightly']}", file=f)
        print(f"version = {version_dict['version']!r}", file=f)
        print(f"version_name = {version_dict['name']!r}", file=f)

    return version_dict


def main():
    import argparse

    ap = argparse.ArgumentParser()
    ap.add_argument("--nightly", action="store_true", help="Set the nightly flag.")
    args = ap.parse_args()

    generate_vc_version(nightly=args.nightly)


if __name__ == "__main__":
    main()
