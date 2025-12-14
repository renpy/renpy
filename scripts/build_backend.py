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

# This file contains PEP 517 and PEP 660 hooks.

import sys
import os

from typing import Mapping
from pathlib import Path

type ConfigSettings = Mapping[str, str | list[str]] | None


def _get_metadata():
    from tomllib import load
    from packaging.version import parse
    from pyproject_metadata import StandardMetadata

    # It is unsafe to import renpy as a whole, but renpy.version is safe.
    sys.path.append(".")

    from renpy.versions import get_version

    sys.path.pop()

    with open("pyproject.toml", "rb") as f:
        data = load(f)

    metadata = StandardMetadata.from_pyproject(
        data,
        metadata_version="2.5",
        all_errors=True,
    )

    metadata.version = parse(get_version()["version"])
    return metadata


#################
# editable installs
#################
def get_requires_for_build_editable(config_settings: ConfigSettings = None):
    return ["setuptools", "cython", "pyproject-metadata", "packaging"]


def prepare_metadata_for_build_editable(metadata_directory: os.PathLike[str], config_settings: ConfigSettings = None):
    metadata = _get_metadata()

    dist_info_path = Path(metadata_directory, f"{metadata.name}-{metadata.version}.dist-info")
    dist_info_path.mkdir(parents=True, exist_ok=True)

    (dist_info_path / "METADATA").write_bytes(metadata.as_rfc822().as_bytes())
    return dist_info_path.name


def build_editable(
    wheel_directory: os.PathLike[str],
    config_settings: ConfigSettings = None,
    metadata_directory: os.PathLike[str] | None = None,
):
    from sysconfig import get_platform
    from textwrap import dedent
    from zipfile import ZipFile, ZIP_DEFLATED

    metadata = _get_metadata()

    meta_name = f"{metadata.name}-{metadata.version}"
    py_version = f"cp{sys.version_info.major}{sys.version_info.minor}"
    platform = get_platform().replace("-", "_")
    tag = f"{py_version}-{py_version}-{platform}"

    whl_path = Path(wheel_directory, f"{meta_name}-{tag}.whl")
    with ZipFile(whl_path, "w", compression=ZIP_DEFLATED) as whl:
        whl.writestr(f"{meta_name}.dist-info/METADATA", metadata.as_rfc822().as_bytes())
        wheel_data = dedent(f"""\
            Wheel-Version: 1.0
            Generator: Ren'Py build backend
            Root-Is-Purelib: true
            Tag: {tag}
            """)
        whl.writestr(f"{meta_name}.dist-info/WHEEL", wheel_data)

        whl.writestr("renpy.pth", f"{Path.cwd().resolve()}\n")

        record_lines: list[str] = []
        for info in whl.infolist():
            record_lines.append(f"{info.filename},,\n")

        whl.writestr(f"{meta_name}.dist-info/RECORD", "\n".join(record_lines))

    return whl_path.name


#################
# wheel creation
#################
def build_wheel(wheel_directory, config_settings=None, metadata_directory=None):
    raise Exception("Ren'Py does not support wheel creation.")


#################
# sdist creation
#################
def build_sdist(sdist_directory, config_settings=None):
    raise Exception("Ren'Py does not support sdist creation.")
