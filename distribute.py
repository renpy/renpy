import os.path
import os
import sys

def match_times(source, dest):

    stat = os.stat(source)
    os.utime(dest, (stat.st_atime, stat.st_mtime))
    
def dosify(s):
    return s.replace("\n", "\r\n")

def copy_file(source, dest, license="", dos=True):

    if dest.endswith(".bak"):
        return

    if dest.endswith("~"):
        return
    
    print source, "->", dest

    sf = file(source, "rb")
    df = file(dest, "wb")

    if dest.endswith(".py") or dest.endswith(".rpy"):
        if not dest.endswith("subprocess.py"):
            df.write(license)

    data = sf.read()
    if dest.endswith(".txt") or dest.endswith(".py") or dest.endswith(".pyw") or \
           dest.endswith(".rpy") or dest.endswith(".bat"):
        if dos:
            data = dosify(data)
            if data.startswith("#!"):
                data = data.replace("\r\n", "\n\r\n", 1)

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

        if "/.svn" in dirpath:
            continue

        reldir = dirpath[len(source):]
        dstrel = dest + "/" + reldir

        for i in dirnames:
            if i == "CVS":
                continue

            if i == ".svn":
                continue

            os.mkdir(dstrel + "/" + i)

        for i in filenames:
            if not should_copy(i):
                continue

            if i.startswith("."):
                continue

            copy_file(dirpath + "/" + i, dstrel + "/" + i, license=license)
            

            

def main():

    target = sys.argv[1]
    gamedir = sys.argv[2]

    # Read license.
    lf = file("LICENSE.txt")
    license = "#!/usr/bin/env python\n\r\n"
    
    for l in lf:

        if l.startswith("---"):
            break
        
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
        'example.html',
        'reference.html',
        'style.css',
        'RELEASING.txt',
        'EXTENDING.txt',
        ]

    # Copy doc
    copy_tree("doc", target + "/doc",
              should_copy = lambda fn : fn in doc_files)

    # Copy the game 
    copy_tree(gamedir, target + "/game",
              should_copy = lambda fn : not fn.endswith(".mpg"))

    copy_tree("common", target + "/common")

    # copy_tree("dse", target + "/dse")

    copy_tree("extras", target + "/extras",
              should_copy = lambda fn : not (fn.endswith(".rpyc") or fn.endswith(".rpyb")) )
    
    copy_tree("scripts", target + "/scripts")

    copy_tree("tools", target + "/tools", license=license)

    def cp(x, license="", dos=True):
        copy_file(x, target + "/" + x, dos=dos)

    cp("CHANGELOG.txt")
    cp("LICENSE.txt")
    cp("README_RENPY.txt")
    # cp("archive_images.bat")
    # cp("lint.bat")
    cp("run_game.py", license=license)
    # copy_file("run_game.py", target + "/run_game.pyw", license=license)
    # copy_file("run_game.py", target + "/run_dse.py", license=license)
    # copy_file("run_game.py", target + "/run_dse.pyw", license=license)
    # copy_file("run_game.rpyl", target + "/run_game.rpyl")
    # copy_file("run_dse.rpyl", target + "/run_dse.rpyl")
    # cp("archiver.py", license=license)
    # cp("build_exe.py", license=license)
    # cp("add_from.py", license=license)
    # cp("dump_text.py", license=license)
    # cp("renpy-mode.el")
    
    os.mkdir(target + "/module")

    module_files = [
        "README.txt",
        "_renpy.pyx",
        "_renpy.c",
        "core.c",
        "linmixer.py",
        "native_midi.h",
        "native_midi_common.c",
        "native_midi_common.h",
        "native_midi_mac.c",
        "native_midi_win32.c",
        "nativemidi.c",
        "nativemidi.pyx",
        "pss.c",
        "pss.h",
        "pysdlsound.c",
        "pysdlsound.pyx",
        "rwobject.c",
        "renpy.h",
        "setup.py",
        "setup_mac.py",
        "setup_win32.py",
        "winmixer.c",
        "winmixer.pyx",
        ]

    for i in module_files:
        cp("module/" + i)
    

if __name__ == "__main__":
    main()

    
