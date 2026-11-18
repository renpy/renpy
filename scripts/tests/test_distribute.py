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

"""Tests for the parts of distribute.py that run without building a distribution."""

import importlib.util
import json
import pathlib
import struct
import sys
import zipfile

import pytest

import distribute

VERSION = "8.6.0"
FULL_VERSION = "8.6.0.26110101"


def make_version_dict(branch="master", commit=26110101, dirty=False):
    """Returns the fields of a version dict that distribute.check_tree reads."""

    return {"branch": branch, "semver": (8, 6, 0, commit), "dirty": dirty}


def make_pyc(flags=distribute.CHECKED_HASH_FLAGS):
    """Returns the start of a .pyc file with the given flags."""

    return b"\0\0\0\0" + struct.pack("<I", flags) + b"\0" * 8


def write_sdk_zip(path, version=FULL_VERSION, flags=distribute.CHECKED_HASH_FLAGS, omit=None, pyc=True):
    """Writes a zip that passes distribute.verify_sdk_zip unless the arguments change that."""

    root = "renpy-" + VERSION + "-sdk/"

    with zipfile.ZipFile(path, "w") as zf:
        for name in distribute.REQUIRED_SDK_FILES:
            if name == omit:
                continue

            if name == "renpy/vc_version.py":
                zf.writestr(root + name, "branch = 'master'\nversion = {!r}\nversion_name = 'Name'\n".format(version))
            else:
                zf.writestr(root + name, "data")

        if pyc:
            zf.writestr(root + "renpy/__pycache__/ast.{}.pyc".format(sys.implementation.cache_tag), make_pyc(flags))


def write_full_build(directory, renpy_version=FULL_VERSION):
    """Writes the files of a full, unsigned build."""

    base = "renpy-" + VERSION + "-"

    for fn in [
        "rapt.zip",
        "renios.zip",
        "sdk.7z.exe",
        "sdk.tar.bz2",
        "sdkarm.tar.bz2",
        "source.tar.bz2",
        "steam.zip",
        "web.zip",
        "windev.zip",
    ]:
        (directory / (base + fn)).write_bytes(b"data")

    for fn in ["android-native-symbols.zip", "updates.ecdsa", "updates.json.sig"]:
        (directory / fn).write_bytes(b"data")

    (directory / "updates.json").write_text(json.dumps({"sdk": {"renpy_version": renpy_version}}))

    write_sdk_zip(directory / (base + "sdk.zip"), version=FULL_VERSION)


@pytest.mark.parametrize("kwargs", [{"branch": "unknown"}, {"commit": 0}])
@pytest.mark.parametrize("options", [{}, {"fast": True}, {"nightly": True}, {"allow_dirty": True}])
def test_check_tree_refuses_failed_git_lookup(kwargs, options):
    """
    check_tree refuses to release when git could not report the branch or commit, in every build mode.

    A branch of 'unknown' or a commit of 0 means the version lookup failed, so none of the options that relax
    other checks (fast, nightly, allow_dirty) may let the build continue.
    """

    with pytest.raises(Exception, match="git"):
        distribute.check_tree(make_version_dict(**kwargs), **options)


def test_check_tree_refuses_dirty_full_build():
    """A full build is refused when the git tree has uncommitted changes."""

    with pytest.raises(Exception, match="dirty"):
        distribute.check_tree(make_version_dict(dirty=True))


@pytest.mark.parametrize("options", [{"fast": True}, {"nightly": True}, {"allow_dirty": True}])
def test_check_tree_allows_dirty_when_requested(options):
    """The fast, nightly, and allow_dirty options each permit building from a dirty tree."""

    distribute.check_tree(make_version_dict(dirty=True), **options)


def test_check_tree_allows_clean_tree():
    """A clean tree on a real branch with a real commit passes check_tree."""

    distribute.check_tree(make_version_dict())


def test_compile_python_writes_checked_hash_pyc(tmp_path):
    """
    compile_python writes .pyc files that Python validates by source hash, not by timestamp.

    Checked-hash pycs keep the shipped SDK's bytecode tied to its source, whatever the timestamps after extraction.
    """

    (tmp_path / "good.py").write_text("x = 1\n")

    distribute.compile_python(str(tmp_path))

    data = pathlib.Path(importlib.util.cache_from_source(str(tmp_path / "good.py"), optimization="")).read_bytes()
    assert struct.unpack("<I", data[4:8])[0] == distribute.CHECKED_HASH_FLAGS


def test_compile_python_removes_orphan_pycs(tmp_path):
    """
    compile_python deletes __pycache__ pycs with no source, but keeps sourceless .pyc files beside the code.

    A top-level sourceless .pyc is how a shipped module is distributed, so only the stale cache entry is removed.
    """

    (tmp_path / "__pycache__").mkdir()
    orphan = tmp_path / "__pycache__" / "gone.cpython-312.pyc"
    orphan.write_bytes(b"data")
    sourceless = tmp_path / "sourceless.pyc"
    sourceless.write_bytes(b"data")
    (tmp_path / "good.py").write_text("x = 1\n")

    distribute.compile_python(str(tmp_path))

    assert not orphan.exists()
    assert sourceless.exists()
    assert pathlib.Path(importlib.util.cache_from_source(str(tmp_path / "good.py"), optimization="")).exists()


def test_compile_python_raises_on_syntax_error(tmp_path):
    """A source file that does not compile aborts compile_python instead of shipping without bytecode."""

    (tmp_path / "bad.py").write_text("def\n")

    with pytest.raises(Exception, match="Could not compile"):
        distribute.compile_python(str(tmp_path))


def test_read_release_version(tmp_path):
    """read_release_version returns the renpy_version recorded in updates.json."""

    (tmp_path / "updates.json").write_text(json.dumps({"sdk": {"renpy_version": FULL_VERSION}}))

    assert distribute.read_release_version(str(tmp_path)) == FULL_VERSION


def test_verify_sdk_zip_accepts_good_zip(tmp_path):
    """A zip with every required file, a matching version, and checked-hash bytecode passes verify_sdk_zip."""

    path = tmp_path / "sdk.zip"
    write_sdk_zip(path)

    distribute.verify_sdk_zip(str(path), "renpy-" + VERSION + "-sdk", FULL_VERSION)


@pytest.mark.parametrize(
    ("kwargs", "message"),
    [
        ({"omit": "renpy.sh"}, "does not contain renpy.sh"),
        ({"omit": "LICENSE.txt"}, "does not contain LICENSE.txt"),
        ({"version": "8.6.0.25112108"}, "is not version"),
        ({"pyc": False}, "compiled python"),
        ({"flags": 0}, "not validated by hash"),
    ],
)
def test_verify_sdk_zip_rejects_bad_zip(tmp_path, kwargs, message):
    """
    verify_sdk_zip names the problem for a zip with a missing file, wrong version, or bad bytecode.

    Each case changes one thing about an otherwise valid zip: a missing required file, a vc_version.py for another
    release, no compiled python at all, or bytecode that is not validated by hash.
    """

    path = tmp_path / "sdk.zip"
    write_sdk_zip(path, **kwargs)

    with pytest.raises(Exception, match=message):
        distribute.verify_sdk_zip(str(path), "renpy-" + VERSION + "-sdk", FULL_VERSION)


def test_verify_distribution_accepts_full_build(tmp_path):
    """A directory holding every artifact of a full unsigned build passes verify_distribution."""

    write_full_build(tmp_path)

    distribute.verify_distribution(str(tmp_path), VERSION, FULL_VERSION)


def test_verify_distribution_ignores_suffix_in_sdk_version(tmp_path):
    """A '+nightly' style suffix on the version in updates.json is not treated as a version mismatch."""

    write_full_build(tmp_path, renpy_version=FULL_VERSION + "+nightly")

    distribute.verify_distribution(str(tmp_path), VERSION, FULL_VERSION + "+nightly")


def test_verify_distribution_requires_dmg_when_signing(tmp_path):
    """A signed release must include the macOS dmg, which write_full_build does not create."""

    write_full_build(tmp_path)

    with pytest.raises(Exception, match="dmg was not built"):
        distribute.verify_distribution(str(tmp_path), VERSION, FULL_VERSION, sign=True)


@pytest.mark.parametrize("contents", [None, b""], ids=["missing", "empty"])
def test_verify_distribution_rejects_missing_or_empty_package(tmp_path, contents):
    """
    verify_distribution fails when a package that should exist was never built, or was built as an empty file.

    verify_distribution checks that each package exists and is not zero bytes, so both cases give the same error.
    """

    write_full_build(tmp_path)
    package = tmp_path / ("renpy-" + VERSION + "-web.zip")

    if contents is None:
        package.unlink()
    else:
        package.write_bytes(contents)

    with pytest.raises(Exception, match="web.zip was not built"):
        distribute.verify_distribution(str(tmp_path), VERSION, FULL_VERSION)


def test_verify_distribution_rejects_mismatched_updates(tmp_path):
    """updates.json written for a different release than the one being verified is rejected."""

    write_full_build(tmp_path, renpy_version="8.6.0.25112108")

    with pytest.raises(Exception, match="updates.json is for"):
        distribute.verify_distribution(str(tmp_path), VERSION, FULL_VERSION)


def test_verify_distribution_fast_needs_only_sdk(tmp_path):
    """A fast build only has to contain the sdk zip and tarball, not the other packages."""

    base = "renpy-" + VERSION + "-"
    write_sdk_zip(tmp_path / (base + "sdk.zip"))
    (tmp_path / (base + "sdk.tar.bz2")).write_bytes(b"data")

    distribute.verify_distribution(str(tmp_path), VERSION, FULL_VERSION, fast=True)
