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
    with pytest.raises(Exception, match="git"):
        distribute.check_tree(make_version_dict(**kwargs), **options)


def test_check_tree_refuses_dirty_full_build():
    with pytest.raises(Exception, match="dirty"):
        distribute.check_tree(make_version_dict(dirty=True))


@pytest.mark.parametrize("options", [{"fast": True}, {"nightly": True}, {"allow_dirty": True}])
def test_check_tree_allows_dirty_when_requested(options):
    distribute.check_tree(make_version_dict(dirty=True), **options)


def test_check_tree_allows_clean_tree():
    distribute.check_tree(make_version_dict())


def test_compile_python_writes_checked_hash_pyc(tmp_path):
    (tmp_path / "good.py").write_text("x = 1\n")

    distribute.compile_python(str(tmp_path))

    data = pathlib.Path(importlib.util.cache_from_source(str(tmp_path / "good.py"), optimization="")).read_bytes()
    assert struct.unpack("<I", data[4:8])[0] == distribute.CHECKED_HASH_FLAGS


def test_compile_python_removes_orphan_pycs(tmp_path):
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
    (tmp_path / "bad.py").write_text("def\n")

    with pytest.raises(Exception, match="Could not compile"):
        distribute.compile_python(str(tmp_path))


def test_read_release_version(tmp_path):
    (tmp_path / "updates.json").write_text(json.dumps({"sdk": {"renpy_version": FULL_VERSION}}))

    assert distribute.read_release_version(str(tmp_path)) == FULL_VERSION


def test_verify_sdk_zip_accepts_good_zip(tmp_path):
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
    path = tmp_path / "sdk.zip"
    write_sdk_zip(path, **kwargs)

    with pytest.raises(Exception, match=message):
        distribute.verify_sdk_zip(str(path), "renpy-" + VERSION + "-sdk", FULL_VERSION)


def test_verify_distribution_accepts_full_build(tmp_path):
    write_full_build(tmp_path)

    distribute.verify_distribution(str(tmp_path), VERSION, FULL_VERSION)


def test_verify_distribution_ignores_suffix_in_sdk_version(tmp_path):
    write_full_build(tmp_path, renpy_version=FULL_VERSION + "+nightly")

    distribute.verify_distribution(str(tmp_path), VERSION, FULL_VERSION + "+nightly")


def test_verify_distribution_requires_dmg_when_signing(tmp_path):
    write_full_build(tmp_path)

    with pytest.raises(Exception, match="dmg was not built"):
        distribute.verify_distribution(str(tmp_path), VERSION, FULL_VERSION, sign=True)


def test_verify_distribution_rejects_missing_package(tmp_path):
    write_full_build(tmp_path)
    (tmp_path / ("renpy-" + VERSION + "-web.zip")).unlink()

    with pytest.raises(Exception, match="web.zip was not built"):
        distribute.verify_distribution(str(tmp_path), VERSION, FULL_VERSION)


def test_verify_distribution_rejects_empty_package(tmp_path):
    write_full_build(tmp_path)
    (tmp_path / ("renpy-" + VERSION + "-web.zip")).write_bytes(b"")

    with pytest.raises(Exception, match="web.zip was not built"):
        distribute.verify_distribution(str(tmp_path), VERSION, FULL_VERSION)


def test_verify_distribution_rejects_mismatched_updates(tmp_path):
    write_full_build(tmp_path, renpy_version="8.6.0.25112108")

    with pytest.raises(Exception, match="updates.json is for"):
        distribute.verify_distribution(str(tmp_path), VERSION, FULL_VERSION)


def test_verify_distribution_fast_needs_only_sdk(tmp_path):
    base = "renpy-" + VERSION + "-"
    write_sdk_zip(tmp_path / (base + "sdk.zip"))
    (tmp_path / (base + "sdk.tar.bz2")).write_bytes(b"data")

    distribute.verify_distribution(str(tmp_path), VERSION, FULL_VERSION, fast=True)
