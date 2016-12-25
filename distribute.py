#!/home/tom/ab/renpy/lib/linux-x86_64/python -O

# Builds a distribution of Ren'Py.
from __future__ import print_function

import sys
import os
import compileall
import shutil
import subprocess
import argparse

if not sys.flags.optimize:
    raise Exception("Optimization disabled.")

ROOT = os.path.dirname(os.path.abspath(__file__))


def copy_tutorial_file(src, dest):
    """
    Copies a file from src to dst. Lines between  "# tutorial-only" and
    "# end-tutorial-only" comments are omitted from the copy.
    """

    # True if we want to copy the line.
    copy = True

    with open(src, "rb") as sf, open(dest, "wb") as df:
        for l in sf:
            if "# tutorial-only" in l:
                copy = False
            elif "# end-tutorial-only" in l:
                copy = True
            else:
                if copy:
                    df.write(l)


def main():

    if not sys.flags.optimize:
        raise Exception("Not running with python optimization.")

    ap = argparse.ArgumentParser()
    ap.add_argument("version")
    ap.add_argument("--fast", action="store_true")
    ap.add_argument("--pygame", action="store", default=None)
    ap.add_argument("--no-rapt", action="store_true")
    ap.add_argument("--variant", action="store")
    ap.add_argument("--sign", action="store_true")

    args = ap.parse_args()

    if args.sign:
        os.environ["RENPY_MAC_IDENTITY"] = "Developer ID Application: Tom Rothamel (XHTE5H7Z79)"

    # Revision updating is done early, so we can do it even if the rest
    # of the program fails.

    # Determine the version. We grab the current revision, and if any
    # file has changed, bump it by 1.
    import renpy

    match_version = ".".join(str(i) for i in renpy.version_tuple[:2])  # @UndefinedVariable

    s = subprocess.check_output([ "git", "describe", "--tags", "--dirty", "--match", "start-" + match_version ])
    parts = s.strip().split("-")

    if len(parts) <= 3:
        vc_version = 0
    else:
        vc_version = int(parts[2])

    if parts[-1] == "dirty":
        vc_version += 1

    with open("renpy/vc_version.py", "w") as f:
        f.write("vc_version = {}".format(vc_version))

    try:
        reload(sys.modules['renpy.vc_version'])  # @UndefinedVariable
    except:
        import renpy.vc_version  # @UnusedImport

    reload(sys.modules['renpy'])

    # Check that the versions match.
    full_version = renpy.version_only  # @UndefinedVariable
    if "-" not in args.version \
            and not full_version.startswith(args.version):
        raise Exception("The command-line and Ren'Py versions do not match.")

    os.environ['RENPY_BUILD_VERSION'] = args.version

    # The destination directory.
    destination = os.path.join("dl", args.version)

    if args.variant:
        destination += "-" + args.variant

    print("Version {} ({})".format(args.version, full_version))

    # Perhaps autobuild.
    if "RENPY_BUILD_ALL" in os.environ:
        print("Autobuild...")
        subprocess.check_call(["scripts/autobuild.sh"])

    # Compile all the python files.
    compileall.compile_dir("renpy/", ddir="renpy/", force=1, quiet=1)

    # Compile the various games.
    if not args.fast:
        for i in [ 'tutorial', 'launcher', 'the_question' ]:
            print("Compiling", i)
            subprocess.check_call(["./renpy.sh", i, "quit" ])

    # Kick off the rapt build.
    if not args.fast:

        print("Cleaning RAPT.")

        sys.path.insert(0, os.path.join(ROOT, "rapt", "buildlib"))

        import rapt.interface  # @UnresolvedImport
        import rapt.build  # @UnresolvedImport

        interface = rapt.interface.Interface()
        rapt.build.distclean(interface)

        print("Compiling RAPT and renios.")

        compileall.compile_dir("rapt/buildlib/", ddir="rapt/buildlib/", quiet=1)
        compileall.compile_dir("renios/buildlib/", ddir="renios/buildlib/", quiet=1)

    if not os.path.exists(destination):
        os.makedirs(destination)

    if args.fast:

        cmd = [
            "./renpy.sh",
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
            "./renpy.sh",
            "launcher",
            "distribute",
            "launcher",
            "--destination",
            destination,
            ]

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

        p = subprocess.Popen([ "7z", "a", sdk +".7z", sdk], stdout=subprocess.PIPE)
        for i, _l in enumerate(p.stdout):
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

    if not (args.fast or args.sign):
        print("For a final-ish release, remember to use --sign so we're signed on the mac.")


if __name__ == "__main__":
    main()
