#!/usr/bin/env python3
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

"""
Sets up this checkout of Ren'Py for development, without compiling anything.

This downloads (or reuses) the nightly build that matches the branch this
checkout is on, puts its compiled libraries where the checkout expects them,
and generates the files the checkout needs but doesn't keep in git. When it's
done, renpy.sh (or renpy.exe on Windows) runs the Python code in this
checkout on top of the nightly's compiled modules, which is enough for any
change that doesn't touch Cython or C.

Only the standard library is used, so this runs with whatever python3 is on
the machine, before uv or a virtual environment exists. To work on the
compiled modules, see "Compiling the Modules" in README.rst.

Usage:

    python3 dev_setup.py              # download the matching nightly and link it
    python3 dev_setup.py --list       # show the nightlies that match this checkout
    python3 dev_setup.py --sdk DIR    # use an SDK that's already unpacked
"""

import argparse
import os
import re
import shutil
import subprocess
import sys
import tarfile
import urllib.request
import zipfile
from typing import NoReturn

NIGHTLY_URL = "https://nightly.renpy.org/"

ROOT = os.path.dirname(os.path.abspath(__file__))


def log(message):
    print(message, flush=True)


def fail(message) -> NoReturn:
    print("dev_setup: " + message, file=sys.stderr)
    sys.exit(1)


################################################################################
# Working out which nightly this checkout wants.


def git_branch():
    """
    Returns the name of the current git branch, or None if it can't be found.
    """

    try:
        return subprocess.check_output(
            ["git", "branch", "--show-current"], cwd=ROOT, encoding="utf-8", stderr=subprocess.DEVNULL
        ).strip()
    except Exception:
        return None


def branch_versions():
    """
    Reads the branch-to-version table out of renpy/versions.py, returning a
    map from branch name to a (major, minor) tuple.
    """

    rv = {}

    with open(os.path.join(ROOT, "renpy", "versions.py"), encoding="utf-8") as f:
        for m in re.finditer(r'Version\("([^"]+)",\s*\((\d+),\s*(\d+),\s*(\d+)\)', f.read()):
            rv[m.group(1)] = (int(m.group(2)), int(m.group(3)))

    return rv


def target_version(override):
    """
    Returns the (major, minor) version of nightly this checkout should use,
    and a description of how that was decided.
    """

    if override:
        m = re.match(r"^(\d+)\.(\d+)", override)
        if not m:
            fail("--version should look like 8.5 or 8.6, not {!r}.".format(override))
        return (int(m.group(1)), int(m.group(2))), "given on the command line"

    versions = branch_versions()
    branch = git_branch()

    # The main development branch is called master on GitHub, and main in
    # versions.py.
    if branch == "master":
        lookup = "main"
    else:
        lookup = branch

    if lookup in versions:
        return versions[lookup], "from the {} branch".format(branch)

    fallback = versions.get("main")

    if fallback is None:
        fail("Couldn't read the version table from renpy/versions.py.")

    if branch:
        why = "the {} branch isn't in renpy/versions.py, so using the main branch's version".format(branch)
    else:
        why = "not in a git checkout, so using the main branch's version"

    return fallback, why


################################################################################
# Finding, downloading, and unpacking nightlies.

NIGHTLY_RE = re.compile(r'href="((\d+)\.(\d+)\.(\d+)\.(\d+)\+nightly[^"/]*)/?"')


class Nightly:
    def __init__(self, name, semver):
        self.name = name
        self.semver = semver

        # Builds from a dirty tree or a side branch have a suffix after
        # +nightly. Prefer the plain ones.
        self.plain = name.endswith("+nightly")

    def sort_key(self):
        return (self.semver, self.plain)

    def archive_name(self):
        if sys.platform == "win32":
            return "renpy-{}-sdk.zip".format(self.name)
        else:
            return "renpy-{}-sdk.tar.bz2".format(self.name)

    def url(self):
        return "{}{}/{}".format(NIGHTLY_URL, self.name, self.archive_name())

    def sdk_dir_name(self):
        return "renpy-{}-sdk".format(self.name)


def list_nightlies():
    """
    Returns a list of Nightly objects, newest first.
    """

    try:
        with urllib.request.urlopen(NIGHTLY_URL, timeout=60) as f:
            index = f.read().decode("utf-8", "replace")
    except Exception as e:
        fail("Couldn't fetch the list of nightly builds from {}: {}".format(NIGHTLY_URL, e))

    rv = []

    for m in NIGHTLY_RE.finditer(index):
        semver = tuple(int(i) for i in m.groups()[1:])
        rv.append(Nightly(m.group(1), semver))

    rv.sort(key=Nightly.sort_key, reverse=True)
    return rv


def choose_nightly(nightlies, target, exact=None):
    """
    Picks the nightly to use. Returns the Nightly, and a note if the choice
    isn't ideal.
    """

    if exact:
        for n in nightlies:
            if n.name == exact:
                return n, None

        fail("There's no nightly build called {!r}.".format(exact))

    matching = [n for n in nightlies if n.semver[:2] == target]

    plain = [n for n in matching if n.plain]

    if plain:
        return plain[0], None

    if matching:
        return matching[0], "the newest matching nightly was built from a modified tree"

    if nightlies:
        return nightlies[0], "no nightly matches version {}.{}, so using the newest one there is".format(*target)

    fail("No nightly builds were found at {}.".format(NIGHTLY_URL))


def download(url, dest):
    """
    Downloads `url` to `dest`, showing progress.
    """

    part = dest + ".part"

    def report(count, block_size, total_size):
        done = count * block_size

        if total_size > 0:
            percent = min(100, done * 100 // total_size)
            sys.stdout.write("\r  {:3d}% of {:.0f} MB".format(percent, total_size / 1e6))
        else:
            sys.stdout.write("\r  {:.0f} MB".format(done / 1e6))

        sys.stdout.flush()

    try:
        urllib.request.urlretrieve(url, part, report)
    except Exception as e:
        try:
            os.unlink(part)
        except OSError:
            pass

        fail("\nCouldn't download {}: {}".format(url, e))

    sys.stdout.write("\n")
    os.replace(part, dest)


def unpack(archive, dest_dir):
    """
    Unpacks `archive` into `dest_dir`.
    """

    log("Unpacking {}...".format(os.path.basename(archive)))

    if archive.endswith(".zip"):
        with zipfile.ZipFile(archive) as z:
            z.extractall(dest_dir)
    else:
        with tarfile.open(archive, "r:bz2") as t:
            if hasattr(tarfile, "data_filter"):
                t.extractall(dest_dir, filter="data")
            else:
                t.extractall(dest_dir)


def fetch_nightly(nightly, download_dir):
    """
    Makes sure `nightly` is downloaded and unpacked in `download_dir`, and
    returns the path to the SDK directory.
    """

    sdk = os.path.join(download_dir, nightly.sdk_dir_name())

    if os.path.isdir(os.path.join(sdk, "lib")):
        log("Using the {} already in {}".format(nightly.name, download_dir))
        return sdk

    os.makedirs(download_dir, exist_ok=True)

    archive = os.path.join(download_dir, nightly.archive_name())

    if not os.path.exists(archive):
        log("Downloading {}".format(nightly.url()))
        download(nightly.url(), archive)

    unpack(archive, download_dir)

    if not os.path.isdir(os.path.join(sdk, "lib")):
        fail("Unpacked {}, but didn't find {}/lib.".format(archive, sdk))

    return sdk


################################################################################
# Linking the SDK into the checkout.


def remove(path):
    """
    Removes a symlink, file, or junction at `path`, if there is one. Refuses
    to remove a real directory, since that's probably the developer's own.
    """

    if os.path.islink(path) or os.path.isfile(path):
        os.unlink(path)
        return

    if not os.path.isdir(path):
        return

    # A directory junction on Windows can be removed with rmdir, but a real
    # directory is refused.
    if sys.platform == "win32":
        try:
            os.rmdir(path)
            return
        except OSError:
            pass

    fail(
        "{} is a real directory, not a link. Move it out of the way if you'd like dev_setup to replace it.".format(path)
    )


def link_directory(src, dst):
    """
    Makes `dst` refer to the directory `src`, as a symlink where possible and
    a junction on Windows otherwise. Returns a word describing what was made.
    """

    try:
        os.symlink(src, dst, target_is_directory=True)
        return "linked"
    except OSError:
        if sys.platform != "win32":
            raise

    try:
        import _winapi

        _winapi.CreateJunction(src, dst)
        return "junctioned"
    except Exception:
        pass

    shutil.copytree(src, dst)
    return "copied"


def link_sdk(sdk):
    """
    Puts the parts of `sdk` that the checkout needs into ROOT.
    """

    sdk = os.path.abspath(sdk)

    lib = os.path.join(ROOT, "lib")
    remove(lib)
    how = link_directory(os.path.join(sdk, "lib"), lib)
    log("lib: {} from {}".format(how, os.path.join(sdk, "lib")))

    # renpy.app is only useful on macOS, but it doesn't hurt elsewhere.
    app = os.path.join(sdk, "renpy.app")

    if os.path.isdir(app):
        dst = os.path.join(ROOT, "renpy.app")
        remove(dst)

        try:
            os.symlink(app, dst, target_is_directory=True)
            log("renpy.app: linked")
        except OSError:
            log("renpy.app: skipped (couldn't make a link)")

    # renpy.sh and renpy.exe must be copies, not links. Both find the
    # directory to run from by looking at where they are, and renpy.sh
    # resolves symlinks first, so a linked renpy.sh runs the SDK's copy of
    # Ren'Py instead of this checkout, silently.
    for fn in ("renpy.sh", "renpy.exe"):
        src = os.path.join(sdk, fn)

        if not os.path.exists(src):
            continue

        dst = os.path.join(ROOT, fn)
        remove(dst)
        shutil.copy2(src, dst)
        log("{}: copied".format(fn))


################################################################################
# Generated files, and checking the result.


def generate():
    """
    Generates the files the checkout needs that aren't in git.
    """

    log("Generating style data...")

    subprocess.check_call([sys.executable, os.path.join(ROOT, "scripts", "generate_styles.py")], cwd=ROOT)


def bundled_python(sdk):
    """
    Returns the path to the Python interpreter the SDK ships for this
    platform, or None if it can't be found.
    """

    lib = os.path.join(sdk, "lib")

    if sys.platform == "win32":
        candidates = ["py3-windows-x86_64/python.exe", "py3-windows-i686/python.exe"]
    elif sys.platform == "darwin":
        candidates = ["py3-mac-universal/python"]
    else:
        candidates = ["py3-linux-x86_64/python", "py3-linux-aarch64/python", "py3-linux-i686/python"]

    for i in candidates:
        path = os.path.join(lib, i)

        if os.path.exists(path):
            return path

    return None


def verify(sdk):
    """
    Checks that Ren'Py, when run through the SDK's Python, imports the renpy
    package from this checkout rather than from the SDK.
    """

    python = bundled_python(sdk)

    if python is None:
        log("Couldn't find the SDK's Python for this platform, so skipping the check.")
        return

    code = "import os, renpy; print(os.path.dirname(os.path.abspath(renpy.__file__)))"

    try:
        out = subprocess.check_output(
            [python, "-X", "utf8", "-c", code], cwd=ROOT, encoding="utf-8", stderr=subprocess.DEVNULL
        ).strip()
    except Exception as e:
        log("Couldn't check where renpy imports from: {}".format(e))
        return

    expected = os.path.join(ROOT, "renpy")

    if os.path.normcase(os.path.abspath(out)) == os.path.normcase(expected):
        log("Checked: renpy imports from this checkout.")
    else:
        fail("renpy imports from {} rather than {}.".format(out, expected))


def how_to_run():
    if sys.platform == "win32":
        return ".\\renpy.exe launcher"
    else:
        return "./renpy.sh launcher"


################################################################################


def main():
    ap = argparse.ArgumentParser(description=__doc__.strip().split("\n\n")[0])

    ap.add_argument("--sdk", metavar="DIR", help="Use this unpacked Ren'Py SDK or nightly, rather than downloading one.")
    ap.add_argument(
        "--version", metavar="X.Y", help="Use the newest nightly for this version (for example 8.5), whatever the branch."
    )
    ap.add_argument("--nightly", metavar="NAME", help="Use this exact nightly (for example 8.6.0.26082403+nightly).")
    ap.add_argument(
        "--download-dir",
        metavar="DIR",
        default=os.path.join(ROOT, "nightly"),
        help="Where nightlies are downloaded and unpacked. Defaults to nightly/ in the checkout.",
    )
    ap.add_argument("--list", action="store_true", help="List the nightlies that match this checkout, then exit.")
    ap.add_argument("--no-generate", action="store_true", help="Don't regenerate the style data.")

    args = ap.parse_args()

    if args.sdk:
        sdk = os.path.abspath(args.sdk)

        if not os.path.isdir(os.path.join(sdk, "lib")):
            fail("{} doesn't look like a Ren'Py SDK (no lib directory).".format(sdk))

    else:
        target, why = target_version(args.version)
        log("Looking for a {}.{} nightly ({}).".format(target[0], target[1], why))

        nightlies = list_nightlies()

        if args.list:
            for n in nightlies:
                if n.semver[:2] == target:
                    log("  " + n.name)
            return

        nightly, note = choose_nightly(nightlies, target, args.nightly)

        if note:
            log("Note: {}.".format(note))

        log("Using {}".format(nightly.name))

        sdk = fetch_nightly(nightly, os.path.abspath(args.download_dir))

    link_sdk(sdk)

    if not args.no_generate:
        generate()

    verify(sdk)

    log("")
    log("Done. Run Ren'Py with:")
    log("")
    log("    " + how_to_run())
    log("")
    log("Changes to the Python code in this checkout take effect on the next run.")
    log("Changes to Cython or C need the modules compiled - see README.rst.")


if __name__ == "__main__":
    main()
