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
    # reload is built-in in Python 2, in importlib in Python 3
    reload # type: ignore
except NameError:
    from importlib import reload

ROOT = os.path.dirname(os.path.abspath(__file__))

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

    args = ap.parse_args()

    link_directory("rapt")
    link_directory("renios")

    if args.link_directories:
        return

    if args.sign:
        os.environ["RENPY_MAC_IDENTITY"] = "Developer ID Application: Tom Rothamel (XHTE5H7Z79)"

    if PY2 and not sys.flags.optimize:
        raise Exception("Not running with python optimization.")

    if not os.path.abspath(sys.executable).startswith(ROOT + "/lib"):
        raise Exception("Distribute must be run with the python in lib/.")

    # Revision updating is done early, so we can do it even if the rest
    # of the program fails.

    # Determine the version. We grab the current revision, and if any
    # file has changed, bump it by 1.
    import renpy

    if args.version is None:
        args.version = ".".join(str(i) for i in renpy.version_tuple[:-1]) # @UndefinedVariable

    try:
        s = subprocess.check_output([ "git", "describe", "--tags", "--dirty", ]).decode("utf-8").strip()
        parts = s.strip().split("-")
        dirty = "dirty" in parts

        commits_per_day = collections.defaultdict(int)

        for i in subprocess.check_output([ "git", "log", "-99", "--pretty=%cd", "--date=format:%Y%m%d", "--follow", "HEAD", "--", "." ]).decode("utf-8").split():
            commits_per_day[i[2:]] += 1

        if dirty:
            key = time.strftime("%Y%m%d")[2:]
            vc_version = "{}{:02d}".format(key, commits_per_day[key] + 1)
        else:
            key = max(commits_per_day.keys())
            vc_version = "{}{:02d}".format(key, commits_per_day[key])
    except:
        vc_version = 0

    with open("renpy/vc_version.py", "w") as f:
        import socket
        official = socket.gethostname() == "eileen"
        nightly = args.version and "nightly" in args.version

        f.write("vc_version = {}\n".format(vc_version))
        f.write("official = {}\n".format(official))
        f.write("nightly = {}\n".format(nightly))

    if args.vc_version_only:
        return

    try:
        reload(sys.modules['renpy.vc_version']) # @UndefinedVariable
    except Exception:
        import renpy.vc_version # @UnusedImport

    reload(sys.modules['renpy'])

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

    # Perhaps autobuild.
    if "RENPY_BUILD_ALL" in os.environ:
        print("Autobuild...")
        subprocess.check_call(["scripts/autobuild.sh"])

    # Compile all the python files.
    compileall.compile_dir("renpy/", ddir="renpy/", force=True, quiet=1)

    # Compile the various games.
    if not args.fast:
        for i in [ 'tutorial', 'launcher', 'the_question' ]:
            print("Compiling", i)
            subprocess.check_call([renpy_sh, i, "quit" ])

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
            "-for-renpy-" + args.version,
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
