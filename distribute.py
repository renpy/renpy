#!/home/tom/bin/renpython -O
# Builds a distributions of Ren'Py.

import sys
import os
import zipfile
import tarfile
import zlib
import compileall
import shutil
import subprocess
import makeupdate
import glob
import time
import argparse

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
    ap.add_argument("--fast", action="store_true")
    ap.add_argument("prefix")
    
    args = ap.parse_args()

    # Revision updating is done early, so we can do it even if the rest
    # of the program fails.
    
    # Determine the version. We grab the current revision, and if any
    # file has changed, bump it by 1.
    p = subprocess.Popen(["bzr", "revno"], stdout=subprocess.PIPE)
    revno = p.stdout.read().strip()
    revno = int(revno)
    p.wait()

    p = subprocess.Popen(["bzr", "status", "-V"], stdout=subprocess.PIPE)
    status = p.stdout.read().strip()
    p.wait()
    
    if status:
        revno += 1
        
    # Write the revno to the necessary files.
    f = file("lib/update-version.txt", "w")
    f.write("{revno}-{now} base\n".format(revno=revno, now=time.time()))
    f.close()

    f = file("renpy/vc_version.py", "w")
    f.write("""\
# The version of Ren'Py reported by the version control software.
vc_version = {revno}
""".format(revno=revno))
    f.close()
    
    prefix = args.prefix

    # Copy over the screens, to keep them up to date.
    shutil.copy("tutorial/game/screens.rpy", "template/game/screens.rpy")

    # Compile all the python files.
    compileall.compile_dir("renpy/", ddir="renpy/", force=1)

    # os.environ['RENPY_PATH_ELIDE'] = '/home/tom/ab/renpy:' + prefix

    # Chmod the mac app.
    os.chmod("./renpy.app/Contents/MacOS/Ren'Py Launcher", 0755)

    # Chmod down renpy.py, for now.
    os.chmod("renpy.py", 0644)
    
    # Compile the various games
    for i in [ 'tutorial/game', 'launcher', 'template/game', 'the_question/game' ]:
        os.system("./renpy.sh --compile --game " + i)
    
    files = [ ]
    more_files = [ ]

    # files.append("CHANGELOG.txt")
    files.append("LICENSE.txt")
    files.extend(tree("common"))
    files.extend(tree("launcher"))
    files.extend(tree("tutorial"))
    files.extend(tree("the_question"))

    more_files.extend(tree("jedit"))
    more_files.extend(tree("lib"))
    more_files.extend(tree("lib/linux-x86"))
    
    module_files = [
        "README.txt",
        "*.c",
        "gen/*.c",
        "*.h",
        "*.py*",
        "include/*.pxd",
        "pysdlsound/*.py",
        "pysdlsound/*.pyx",
        ]

    for i in module_files:
        files.extend(glob.glob('module/' + i))

    files.extend(tree('renpy'))
    files.append('renpy.py')

    more_files.append('python26.dll')
    more_files.append('msvcr90.dll')
    more_files.append('Microsoft.VC90.CRT.manifest')
    more_files.extend(tree('renpy.app'))
    more_files.append('renpy.exe')   
    more_files.append("console.exe")
    more_files.append('renpy.sh')

    files.extend(tree('template'))
    files.extend(tree('doc'))

    files.sort()
    more_files.sort()

    for fn in files + more_files:
        if "~" in fn or "#" in fn:
            raise Exception("Bad filename {0}.".format(fn))

    zipup("dists/" + prefix + "-sdk.zip", prefix, files + more_files)

    if not args.fast:
        print "----"
        tarup("dists/" + prefix + "-sdk.tar.bz2", prefix, files + more_files)
        print "----"
        tarup("dists/" + prefix + "-source.tar.bz2", prefix, files)
        print "----"

        # Make the 7zip.
        os.chdir("dists")
        os.system("unzip " + prefix + "-sdk.zip")
    
        try:
            os.unlink(prefix + "-sdk.7z")
        except:
            pass
    
        os.system("7z a " + prefix + "-sdk.7z " + prefix)
        os.system("cat ../7z.sfx " + prefix + "-sdk.7z > " + prefix + "-sdk.7z.exe""")
        os.unlink(prefix + "-sdk.7z")
    
        os.chdir("..")
    
        if os.path.exists("updates/prerelease"):
            shutil.rmtree("updates/prerelease")
    
        os.rename("dists/" + prefix, "updates/prerelease")
        os.unlink("updates/prerelease/lib/update-version.txt")
    
        makeupdate.make_update("updates/prerelease", str(revno))
    
    os.chmod("renpy.py", 0755)

    print
    print "Did you remember to rebuild the exe after the last change?"
    print "Did you run me with renpython -OO?"
    print "Did you update renpy.py and launcher/script_version.rpy?"
    print "Did you run with a RENPY_SCALE_FACTOR?"
    
if __name__ == "__main__":
    main()
