import os.path
import os
import sys

def match_times(source, dest):

    stat = os.stat(source)
    os.utime(dest, (stat.st_atime, stat.st_mtime))
    
def dosify(s):
    return s.replace("\n", "\r\n")
    return s

def copy_file(source, dest, license=""):

    print source, "->", dest

    sf = file(source, "rb")
    df = file(dest, "wb")

    df.write(license)

    data = sf.read()
    if dest.endswith(".txt") or dest.endswith(".py") or dest.endswith(".rpy"):
        data = dosify(data)

    df.write(data)

    sf.close()
    df.close()

    match_times(source, dest)


def copy_tree(source, dest, should_copy=lambda fn : True, license=""):

    os.makedirs(dest)

    for dirpath, dirnames, filenames in os.walk(source):

        if "/saves" in dirpath:
            continue

        if "/CVS" in dirpath:
            continue

        reldir = dirpath[len(source):]
        dstrel = dest + "/" + reldir

        for i in dirnames:
            if i == "CVS":
                continue
            
            os.mkdir(dstrel + "/" + i)

        for i in filenames:
            if not should_copy(i):
                continue

            copy_file(dirpath + "/" + i, dstrel + "/" + i, license=license)
            

            

def main():

    target = sys.argv[1]
    gamedir = sys.argv[2]

    # Read license.
    lf = file("LICENSE.txt")
    license = "#!/usr/bin/env python\n\n"
    
    for l in lf:
        license += "# " + l

    lf.close()

    license = dosify(license)

    if os.path.exists(target):
        raise Exception("Target exists!")

    # Start off with the target.
    copy_tree("dist", target,
              should_copy = lambda fn : fn not in [ 'traceback.txt' ] and not fn.endswith(".log"))

    # Copy renpy modules.
    copy_tree("renpy", target + "/renpy",
              should_copy = lambda fn : fn.endswith(".py"),              
              license=license)

    doc_files = [
        'tutorial.html',
        'style.css',
        ]

    # Copy doc
    copy_tree("doc", target + "/doc",
              should_copy = lambda fn : fn in doc_files)

    # Copy the game
    copy_tree(gamedir, target + "/game",
              should_copy = lambda fn : not fn.startswith(".") and not fn.endswith("~"))

    def cp(x, license=""):
        copy_file(x, target + "/" + x)

    cp("CHANGELOG.txt")
    cp("LICENSE.txt")
    cp("README_RENPY.txt")
    cp("run_game.py", license=license)
    cp("archiver.py", license=license)
    cp("build_exe.py", license=license)
    cp("renpy-mode.el")
    
       


if __name__ == "__main__":
    main()

    
