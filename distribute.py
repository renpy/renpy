#!/home/tom/bin/renpython -OO
# Builds a distributions of Ren'Py.

import sys
import os
import zipfile
import tarfile
import zlib
import compileall
import shutil
import subprocess
import time
import argparse

CWD = os.getcwdu()

zlib.Z_DEFAULT_COMPRESSION = 9

# Gets the data for the given file.
def data(fn):

    rv = file(fn, "rb").read()

    if fn.startswith("renpy.app"):
        return rv

    if fn.endswith(".rpy") or fn.endswith(".rpym") or fn.endswith(".py") or fn.endswith(".txt"):
        rv = rv.replace("\n", "\r\n")
        rv = rv.replace("\r\r\n", "\r\n")

    return rv


def tarup(filename, prefix, files):

    tf = tarfile.open(filename, "w:bz2")
    tf.dereference = True

    sys.stdout.write(filename)
    sys.stdout.flush()

    for fn in files:
        sys.stdout.write(".")
        sys.stdout.flush()

        tf.add(fn, prefix + "/" + fn, False)

    sys.stdout.write("\n")

    tf.close()


# Creates a zip file.
def zipup(filename, prefix, files):

    zf = zipfile.ZipFile(filename, "w")

    sys.stdout.write(filename)
    sys.stdout.flush()

    for fn in files:
        sys.stdout.write(".")
        sys.stdout.flush()

        zi = zipfile.ZipInfo(prefix + "/" + fn)

        st = os.stat(fn)

        zi.date_time = time.gmtime(st.st_mtime)[:6]
        zi.compress_type = zipfile.ZIP_DEFLATED
        zi.create_system = 3
        zi.external_attr = long(st.st_mode) << 16

        zf.writestr(zi, data(fn))

    zf.close()

    sys.stdout.write("\n")
    sys.stdout.flush()


def copy_tutorial_file(src, dest):
    """
    Copies a file from src to dst. Lines between  "# tutorial-only" and
    "# end-tutorial-only" comments are omitted from the copy.
    """

    sf = open(src, "rb")
    df = open(dest, "wb")

    # True if we want to copy the line.
    copy = True

    for l in sf:
        if "# tutorial-only" in l:
            copy = False
        elif "# end-tutorial-only" in l:
            copy = True
        else:
            if copy:
                df.write(l)

    sf.close()
    df.close()


def tree(root):

    rv = [ ]

    for dirname, dirs, filenames in os.walk(root):

        if "saves" in dirs:
            dirs.remove("saves")

        if ".svn" in dirs:
            dirs.remove(".svn")

        if ".doctrees" in dirs:
            dirs.remove(".doctrees")

        for f in filenames:
            if f[-1] == '~' or f[0] == '.':
                continue

            if f.endswith(".bak") or f.endswith(".pyc"):
                continue

            if f == "semantic.cache":
                continue

            if "libSDL_mixer" in f or "mixer_music" in f:
                continue

            rv.append(dirname + "/" + f)

    return rv

def main():

    ap = argparse.ArgumentParser()
    ap.add_argument("version")
    ap.add_argument("--fast", action="store_true")

    args = ap.parse_args()

    # Revision updating is done early, so we can do it even if the rest
    # of the program fails.

    # Determine the version. We grab the current revision, and if any
    # file has changed, bump it by 1.
    import renpy

    match_version = ".".join(str(i) for i in renpy.version_tuple[:2]) #@UndefinedVariable
    zip_version = ".".join(str(i) for i in renpy.version_tuple[:3]) #@UndefinedVariable

    s = subprocess.check_output([ "git", "describe", "--tags", "--dirty", "--match", match_version ])
    parts = s.strip().split("-")
    vc_version = int(parts[1])

    if parts[-1] == "dirty":
        vc_version += 1

    with open("renpy/vc_version.py", "w") as f:
        f.write("vc_version = {}".format(vc_version))

    reload(sys.modules['renpy.vc_version']) #@UndefinedVariable
    reload(sys.modules['renpy'])

    # Check that the versions match.
    full_version = ".".join(str(i) for i in renpy.version_tuple) #@UndefinedVariable
    if args.version != "experimental" and not full_version.startswith(args.version):
        raise Exception("The command-line and Ren'Py versions do not match.")

    print "Version {} ({})".format(args.version, full_version)

    # Copy over the screens, to keep them up to date.
    copy_tutorial_file("tutorial/game/screens.rpy", "template/game/screens.rpy")

    # Compile all the python files.
    compileall.compile_dir("renpy/", ddir="renpy/", force=1, quiet=1)

    # Compile the various games

    if not args.fast:
        for i in [ 'tutorial', 'launcher', 'template', 'the_question' ]:
            print "Compiling", i
            subprocess.check_call(["./renpy.sh", i, "compile" ])

    # The destination directory.
    destination = os.path.join("dl", args.version)

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

    print
    subprocess.check_call(cmd)

    # Sign the update.
    if not args.fast:
        subprocess.check_call([
            "scripts/sign_update.py",
            "/home/tom/ab/keys/renpy_private.pem",
            os.path.join(destination, "updates.json"),
            ])


    # Write 7z.exe.
    sdk = "renpy-{}-sdk".format(zip_version)

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

    print
    print "Did you run me with renpython -OO?"
    print "Did you update renpy.py and launcher/script_version.rpy?"

if __name__ == "__main__":
    main()
