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


class Version:
    def __init__(self, branch: str, semver: tuple[int, int, int], name: str):
        """
        `branch`
            The name of the branch, as a string.

        `semver`
            The Ren'Py version number, a tuple of (major, minor, patch).

        `name`
            The Ren'Py version name.
        """

        self.branch = branch
        self.semver = semver
        self.name = name

        branch_to_version[branch] = self


branch_to_version: dict[str, Version] = {}

Version("main", (8, 6, 0), "Real Artists Ship")

Version("fix", (8, 5, 2), "In Good Health")


class VersionDict(TypedDict):
    """
    Dictionary that stores all the data about current running version.
    """

    semver: tuple[int, int, int, int]
    "The Ren'Py version number, a tuple of (major, minor, patch, commit)."
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


def _make_version_string(
    semver: tuple[int, int, int, int],
    branch: str,
    official: bool,
    nightly: bool,
    dirty: bool,
) -> str:
    major, minor, patch, commit = semver

    suffixes: list[str] = []
    if not official:
        suffixes.append("unofficial")
    elif nightly:
        suffixes.append("nightly")

    if dirty:
        suffixes.append("dirty")

    if branch != "main" or dirty:
        suffixes.append(branch)

    return f"{major}.{minor}.{patch}.{commit:08d}+{'.'.join(suffixes)}"


def get_vc_version() -> VersionDict | None:
    """
    Return version dict from vc_version.py if it exists or None otherwise.
    """

    # vc_version.py contains:
    # branch - Name of the branch from which this the file was generated.
    # dirty - True if the working tree is dirty.
    # official - True if it were an official build.
    # nightly - True if it were a nightly build.
    # version - Semver as a string.
    # version_name - Name of the version.
    try:
        import renpy.vc_version as vc_version  # type: ignore
    except ImportError:
        return None

    major, minor, patch, commit = vc_version.version.split(".")
    semver = (int(major), int(minor), int(patch), int(commit))
    official = vc_version.official and getattr(site, "renpy_build_official", False)
    dirty = getattr(vc_version, "dirty", False)

    return VersionDict(
        semver=semver,
        version=_make_version_string(
            semver,
            vc_version.branch,
            official,
            vc_version.nightly,
            dirty,
        ),
        name=vc_version.version_name,
        branch=vc_version.branch,
        nightly=vc_version.nightly,
        official=official,
        dirty=dirty,
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
        commit = int(f"{key}{commits_per_day[key]:02d}")

    except Exception:
        import traceback

        traceback.print_exc()
        branch = "unknown"
        dirty = False
        commit = 0

    if branch in branch_to_version:
        version_obj = branch_to_version[branch]
    else:
        version_obj = branch_to_version["main"]

    semver = (*version_obj.semver, commit)
    official = socket.gethostname() == "eileen"

    return VersionDict(
        semver=semver,
        version=_make_version_string(
            semver,
            branch,
            official,
            nightly,
            dirty,
        ),
        name=version_obj.name,
        branch=branch,
        official=official,
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
        print(f"version = {version_dict['version'].split('+')[0]!r}", file=f)
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
