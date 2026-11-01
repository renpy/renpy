#!/home/tom/ab/renpy/lib/py3-linux-x86_64/python

# Builds a distribution of Ren'Py.
from __future__ import division, absolute_import, with_statement, print_function, unicode_literals

import future.standard_library
import future.utils

PY2 = future.utils.PY2

import sys
import os
import compileall
import json
import py_compile
import shutil
import struct
import subprocess
import argparse
import time
import collections
import zipfile

try:
    from importlib import reload
except ImportError:
    pass


ROOT = os.path.dirname(os.path.abspath(__file__))

# The files that must be in every SDK zip, relative to the directory in the zip.
REQUIRED_SDK_FILES = [
    "LICENSE.txt",
    "doc/index.html",
    "lib/py3-linux-x86_64/renpy",
    "lib/py3-mac-universal/renpy",
    "lib/py3-windows-x86_64/renpy.exe",
    "renpy.app/Contents/MacOS/renpy",
    "renpy.exe",
    "renpy.py",
    "renpy.sh",
    "renpy/vc_version.py",
]

# The flags field of a .pyc file that was compiled using CHECKED_HASH.
CHECKED_HASH_FLAGS = 0b11


def check_tree(version_dict, fast=False, nightly=False, allow_dirty=False):
    """
    Raises an exception if the git tree described by `version_dict` (as returned by
    renpy.versions.get_git_version) shouldn't be used to build a distribution.

    A tree that couldn't be read by git is always refused. A dirty tree is only allowed
    for fast and nightly builds, or if `allow_dirty` is true.
    """

    if version_dict["branch"] == "unknown" or version_dict["semver"][3] == 0:
        raise Exception("Could not determine the version from git.")

    if version_dict["dirty"] and not (fast or nightly or allow_dirty):
        raise Exception("The git tree is dirty. Commit the changes, or give --allow-dirty.")


def remove_orphan_pycs(directory):
    """
    Removes the .pyc files in __pycache__ directories under `directory` that don't have a
    corresponding .py file. These are left behind when a module is removed, can't be
    imported, and would otherwise be packaged.
    """

    for dn, _dirs, files in os.walk(directory):
        if os.path.basename(dn) != "__pycache__":
            continue

        for fn in files:
            if not fn.endswith(".pyc"):
                continue

            source = os.path.join(os.path.dirname(dn), fn.partition(".")[0] + ".py")

            if not os.path.exists(source):
                os.unlink(os.path.join(dn, fn))


def compile_python(directory):
    """
    Removes orphaned .pyc files from `directory`, then compiles the python files in it,
    raising an exception if that fails.

    The .pyc files are validated by the hash of the source, as packaging and unpacking
    can change the timestamp of a .py file. They're compiled without optimization as
    the engine runs that way, even if distribute.py was run with -O.
    """

    remove_orphan_pycs(directory)

    success = compileall.compile_dir(
        directory,
        ddir=directory,
        force=True,
        quiet=1,
        optimize=0,
        invalidation_mode=py_compile.PycInvalidationMode.CHECKED_HASH,
    )

    if not success:
        raise Exception("Could not compile the python files in {}.".format(directory))


def read_release_version(directory):
    """
    Returns the version of Ren'Py recorded in the updates.json file in `directory`, which
    is the output directory of a build. Raises an exception if it can't be determined.
    """

    with open(os.path.join(directory, "updates.json")) as f:
        return json.load(f)["sdk"]["renpy_version"]


def verify_sdk_zip(path, root, semver):
    """
    Raises an exception if the SDK zip at `path` isn't correct. `root` is the name of the
    directory in the zip, and `semver` is the version it should contain, without suffixes.
    """

    prefix = root + "/"

    with zipfile.ZipFile(path) as zf:
        names = set(zf.namelist())

        for name in REQUIRED_SDK_FILES:
            if prefix + name not in names:
                raise Exception("{} does not contain {}.".format(path, name))

        vc_version = zf.read(prefix + "renpy/vc_version.py").decode("utf-8")

        if "version = {!r}".format(semver) not in vc_version:
            raise Exception("{} is not version {}.".format(path, semver))

        suffix = ".{}.pyc".format(sys.implementation.cache_tag)
        pycs = [i for i in names if i.startswith(prefix + "renpy/") and i.endswith(suffix)]

        if not pycs:
            raise Exception("{} does not contain compiled python files.".format(path))

        for name in pycs:
            flags = struct.unpack("<I", zf.read(name)[4:8])[0]

            if flags != CHECKED_HASH_FLAGS:
                raise Exception("{} in {} is not validated by hash.".format(name, path))


def verify_distribution(destination, version, full_version, fast=False, sign=False):
    """
    Raises an exception if the build in `destination` is missing something, or
    doesn't match the version being built.

    `version`
        The version used in file names.

    `full_version`
        The full version of Ren'Py being built, including suffixes.

    `fast`
        True if this was a fast build, which only makes the SDK and no updates.

    `sign`
        True if the mac app was signed, which is required to make a dmg.
    """

    base = "renpy-" + version + "-"

    expected = [base + "sdk.zip", base + "sdk.tar.bz2"]

    if sign:
        expected.append(base + "sdk.dmg")

    if not fast:
        expected.extend([
            base + "rapt.zip",
            base + "renios.zip",
            base + "sdk.7z.exe",
            base + "sdkarm.tar.bz2",
            base + "source.tar.bz2",
            base + "steam.zip",
            base + "web.zip",
            base + "windev.zip",
            "android-native-symbols.zip",
            "updates.ecdsa",
            "updates.json",
            "updates.json.sig",
        ])

    for fn in expected:
        path = os.path.join(destination, fn)

        if not os.path.exists(path) or not os.path.getsize(path):
            raise Exception("{} was not built.".format(path))

    verify_sdk_zip(os.path.join(destination, base + "sdk.zip"), base + "sdk", full_version.partition("+")[0])

    if not fast:
        release_version = read_release_version(destination)

        if release_version != full_version:
            raise Exception("updates.json is for {}, not {}.".format(release_version, full_version))


def zip_rapt_symbols(destination):
    """
    Zips up the rapt symbols.
    """

    import zipfile

    if PY2:
        zf = zipfile.ZipFile(destination + "/android-native-symbols.zip", "w", zipfile.ZIP_DEFLATED)
    else:
        zf = zipfile.ZipFile(destination + "/android-native-symbols.zip", "w", zipfile.ZIP_DEFLATED, compresslevel=3)

    for dn, dirs, files in os.walk("rapt/symbols"):
        for fn in dirs + files:
            fn = os.path.join(dn, fn)
            arcname = os.path.relpath(fn, "rapt/symbols")
            zf.write(fn, arcname)

    zf.close()


def copy_tutorial_file(src, dest):
    """
    Copies a file from src to dst. Lines between  "# tutorial-only" and
    "# end-tutorial-only" comments are omitted from the copy.
    """

    # True if we want to copy the line.
    copy = True

    with open(src, "r") as sf, open(dest, "w") as df:
        for l in sf:
            if "# tutorial-only" in l:
                copy = False
            elif "# end-tutorial-only" in l:
                copy = True
            else:
                if copy:
                    df.write(l)


def ensure_license():
    """
    Creates the LICENSE.txt link that's packaged with Ren'Py, if it doesn't exist. It's
    not checked in, and would otherwise be silently left out of the distribution.
    """

    if not os.path.exists("LICENSE.txt"):
        os.symlink("sphinx/source/license.rst", "LICENSE.txt")


def main():

    start = time.time()

    ap = argparse.ArgumentParser()
    ap.add_argument("version", nargs="?")
    ap.add_argument(
        "--fast", action="store_true", help="Quickly build the SDK into dl/<version>-fast, without updates."
    )
    ap.add_argument("--variant", action="store")
    ap.add_argument(
        "--sign",
        action="store_true",
        default=None,
        help="Sign the mac app and build a dmg. This is the default unless --fast is given.",
    )
    ap.add_argument(
        "--nosign",
        action="store_false",
        dest="sign",
        help="Do not sign the mac app or build a dmg. The updates are still signed.",
    )
    ap.add_argument("--notarized", action="store_true", dest="notarized")
    ap.add_argument("--vc-version-only", action="store_true")
    ap.add_argument("--append-version", action="store_true")
    ap.add_argument("--nightly", action="store_true")
    ap.add_argument("--print-version", action="store_true")
    ap.add_argument("--allow-dirty", action="store_true", help="Allow a full build from a dirty git tree.")
    ap.add_argument("--check-tree", action="store_true", help="Check the git tree can be built from, then exit.")

    args = ap.parse_args()

    if args.sign is None:
        args.sign = not args.fast

    os.chdir(ROOT)

    import renpy.versions

    if args.check_tree:
        check_tree(renpy.versions.get_git_version(args.nightly), args.fast, args.nightly, args.allow_dirty)
        return

    version_dict = renpy.versions.generate_vc_version(nightly=args.nightly)

    if args.vc_version_only:
        return

    if not os.path.abspath(sys.executable).startswith(ROOT + "/lib"):
        raise Exception("Distribute must be run with the python in lib/.")

    if args.sign:
        os.environ["RENPY_MAC_IDENTITY"] = "Developer ID Application: Tom Rothamel (XHTE5H7Z79)"

    if PY2 and not sys.flags.optimize:
        raise Exception("Not running with python optimization.")

    try:
        vc_version_base = os.path.splitext(renpy.vc_version.__file__)[0]

        # Delete the .pyc and .pyo files, as reload can choose one of them instead
        # of the new .py file.
        for fn in [vc_version_base + ".pyc", vc_version_base + ".pyo"]:
            if os.path.exists(fn):
                os.unlink(fn)

        reload(renpy.vc_version)
    except Exception:
        import renpy.vc_version

    # A normal reload is fine, as renpy/__init__.py won't change.
    reload(renpy)

    if args.print_version:
        print(renpy.version_only)
        return

    check_tree(version_dict, args.fast, args.nightly, args.allow_dirty)

    if args.version is None:
        if args.nightly:
            args.version = renpy.version_only
        else:
            args.version = ".".join(str(i) for i in renpy.version_tuple[:-1])

    if args.append_version:
        args.version += "-" + renpy.version_only

    # Check that the versions match.
    full_version = renpy.version_only  # @UndefinedVariable

    if "-" not in args.version and not full_version.startswith(args.version):
        raise Exception("The command-line and Ren'Py versions do not match.")

    os.environ["RENPY_BUILD_VERSION"] = args.version

    # The destination directory.
    destination = os.path.join("dl", args.version)

    if args.variant:
        destination += "-" + args.variant

    # Keep fast builds, which are incomplete, away from the files of a full build.
    if args.fast:
        destination += "-fast"

    if os.path.exists(os.path.join(destination, "checksums.txt")):
        raise Exception("The checksums.txt file exists.")

    print("Version {} ({})".format(args.version, full_version))

    renpy_sh = "./renpy.sh"

    ensure_license()

    # Compile all the python files.
    compile_python("renpy/")

    # Compile the various games.
    if not args.fast:
        for i in ["tutorial", "launcher", "the_question"]:
            print("Compiling", i)
            subprocess.check_call([renpy_sh, i, "compile"])

    # Kick off the rapt build.
    if not args.fast:
        print("Cleaning RAPT.")

        sys.path.insert(0, os.path.join(ROOT, "rapt", "buildlib"))

        import rapt.interface  # type: ignore
        import rapt.build  # type: ignore

        interface = rapt.interface.Interface()
        rapt.build.distclean(interface)

        print("Compiling RAPT and renios.")

        compile_python("rapt/buildlib/")
        compile_python("renios/buildlib/")

    if not os.path.exists(destination):
        os.makedirs(destination)

    zip_rapt_symbols(destination)

    if args.fast:
        cmd = [
            renpy_sh,
            "launcher",
            "distribute",
            "launcher",
            "--package",
            "sdk",
            "--destination",
            destination,
            "--no-update",
        ]

    else:
        cmd = [
            renpy_sh,
            "launcher",
            "distribute",
            "launcher",
            "--destination",
            destination,
        ]

        if args.notarized:
            cmd.extend([
                "--macapp",
                "notarized/out",
            ])

    print()
    subprocess.check_call(cmd)

    # Sign the update.
    if not args.fast:
        subprocess.check_call([
            "uv",
            "run",
            "scripts/sign_update.py",
            "/home/tom/ab/keys/renpy_private.pem",
            os.path.join(destination, "updates.json"),
        ])

    # Write 7z.exe.
    sdk = "renpy-{}-sdk".format(args.version)

    if not args.fast:
        # shutil.copy("renpy-ppc.zip", os.path.join(destination, "renpy-ppc.zip"))

        with open("7z.sfx", "rb") as f:
            sfx = f.read()

        os.chdir(destination)

        if os.path.exists(sdk):
            shutil.rmtree(sdk)

        subprocess.check_call(["unzip", "-q", sdk + ".zip"])

        if os.path.exists(sdk + ".7z"):
            os.unlink(sdk + ".7z")

        sys.stdout.write("Creating -sdk.7z")

        p = subprocess.Popen(["7z", "a", sdk + ".7z", sdk], stdout=subprocess.PIPE)
        for i, _l in enumerate(p.stdout):  # type: ignore
            if i % 10 != 0:
                continue

            sys.stdout.write(".")
            sys.stdout.flush()

        if p.wait() != 0:
            raise Exception("7z failed")

        with open(sdk + ".7z", "rb") as f:
            data = f.read()

        with open(sdk + ".7z.exe", "wb") as f:
            f.write(sfx)
            f.write(data)

        os.unlink(sdk + ".7z")
        shutil.rmtree(sdk)

    else:
        os.chdir(destination)

        if os.path.exists(sdk + ".7z.exe"):
            os.unlink(sdk + ".7z.exe")

    os.chdir(ROOT)

    verify_distribution(destination, args.version, full_version, args.fast, args.sign)

    print()

    print("Distribute took {:.0f} seconds.".format(time.time() - start))


if __name__ == "__main__":
    main()
