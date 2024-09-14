#!/home/tom/ab/renpy/lib/py3-linux-x86_64/python

# Builds a distribution of Ren'Py.
from __future__ import division, absolute_import, with_statement, print_function, unicode_literals

import future.standard_library
import future.utils
PY2 = future.utils.PY2

import sys
import os
import compileall
import shutil
import subprocess
import argparse
import time
import collections

try:
    from importlib import reload
except ImportError:
    pass


ROOT = os.path.dirname(os.path.abspath(__file__))


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

def link_directory(dirname):
    dn = os.path.join(ROOT, dirname)

    if os.path.exists(dn):
        os.unlink(dn)

    if PY2:
        source = dn + "2"
    else:
        source = dn + "3"

    if os.path.exists(source):
        os.symlink(source, dn)

def main():

    start = time.time()

    ap = argparse.ArgumentParser()
    ap.add_argument("version", nargs="?")
    ap.add_argument("--fast", action="store_true")
    ap.add_argument("--pygame", action="store", default=None)
    ap.add_argument("--no-rapt", action="store_true")
    ap.add_argument("--variant", action="store")
    ap.add_argument("--sign", action="store_true", default=True)
    ap.add_argument("--nosign", action="store_false", dest="sign")
    ap.add_argument("--notarized", action="store_true", dest="notarized")
    ap.add_argument("--vc-version-only", action="store_true")
    ap.add_argument("--link-directories", action="store_true")
    ap.add_argument("--append-version", action="store_true")
    ap.add_argument("--nightly", action="store_true")
    ap.add_argument("--print-version", action="store_true")

    args = ap.parse_args()

    link_directory("rapt")
    link_directory("renios")
    link_directory("web")

    import renpy.versions
    renpy.versions.generate_vc_version(nightly=args.nightly)

    if args.link_directories or args.vc_version_only:
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
        for fn in [ vc_version_base + ".pyc", vc_version_base + ".pyo" ]:
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

    if args.version is None:
        if args.nightly:
            args.version = renpy.version_only
        else:
            args.version = ".".join(str(i) for i in renpy.version_tuple[:-1])

    if args.append_version:
        args.version += "-"  + renpy.version_only

    # Check that the versions match.
    full_version = renpy.version_only # @UndefinedVariable

    if "-" not in args.version \
            and not full_version.startswith(args.version):
        raise Exception("The command-line and Ren'Py versions do not match.")

    os.environ['RENPY_BUILD_VERSION'] = args.version

    # The destination directory.
    destination = os.path.join("dl", args.version)

    if args.variant:
        destination += "-" + args.variant

    if os.path.exists(os.path.join(destination, "checksums.txt")):
        raise Exception("The checksums.txt file exists.")

    print("Version {} ({})".format(args.version, full_version))

    if sys.version_info[0] >= 3:
        renpy_sh = "./renpy3.sh"
    else:
        renpy_sh = "./renpy2.sh"

    # Compile all the python files.
    compileall.compile_dir("renpy/", ddir="renpy/", force=True, quiet=1)

    # Compile the various games.
    if not args.fast:
        for i in [ 'tutorial', 'launcher', 'the_question' ]:
            print("Compiling", i)
            subprocess.check_call([renpy_sh, i, "compile" ])

    # Kick off the rapt build.
    if not args.fast:

        print("Cleaning RAPT.")

        sys.path.insert(0, os.path.join(ROOT, "rapt", "buildlib"))

        import rapt.interface # type: ignore
        import rapt.build # type: ignore

        interface = rapt.interface.Interface()
        rapt.build.distclean(interface)

        print("Compiling RAPT and renios.")

        compileall.compile_dir("rapt/buildlib/", ddir="rapt/buildlib/", quiet=1)
        compileall.compile_dir("renios/buildlib/", ddir="renios/buildlib/", quiet=1)

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
            "scripts/sign_update.py",
            "/home/tom/ab/keys/renpy_private.pem",
            os.path.join(destination, "updates.json"),
            ])

    # Package pygame_sdl2.
    if not args.fast:
        subprocess.check_call([
            "pygame_sdl2/setup.py",
            "-q",
            "egg_info",
            "--tag-build",
            "+renpy" + args.version.replace("+", "-"),
            "sdist",
            "-d",
            os.path.abspath(destination)
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

        subprocess.check_call([ "unzip", "-q", sdk + ".zip" ])

        if os.path.exists(sdk + ".7z"):
            os.unlink(sdk + ".7z")

        sys.stdout.write("Creating -sdk.7z")

        p = subprocess.Popen([ "7z", "a", sdk + ".7z", sdk], stdout=subprocess.PIPE)
        for i, _l in enumerate(p.stdout): # type: ignore
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

    print()

    print("Distribute took {:.0f} seconds.".format(time.time() - start))


if __name__ == "__main__":
    main()
