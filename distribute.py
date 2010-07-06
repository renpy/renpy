#!/home/tom/bin/renpython -O
# Builds a distributions of Ren'Py.

import sys
import os
import zipfile
import tarfile
import time
import zlib
import compileall
import shutil

zlib.Z_DEFAULT_COMPRESSION = 9

# Gets the data for the given file.
def data(fn):

    rv = file(fn, "rb").read()

    if fn.startswith("renpy.app"):
        return rv

    if fn.endswith(".rpy") or fn.endswith(".py") or fn.endswith(".txt"):
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

    if len(sys.argv) != 2:
        print "Usage: %s <prefix>" % sys.argv[0]
        return

    prefix = sys.argv[1]

    compileall.compile_dir("renpy/", ddir=prefix + "/renpy/", force=1)

    os.environ['RENPY_PATH_ELIDE'] = '/home/tom/ab/renpy:' + prefix

    # Chmod the mac app.
    os.chmod("./renpy.app/Contents/MacOS/Ren'Py Launcher", 0755)
    
    # Compile the various games
    for i in [ 'tutorial/game', 'launcher', 'template/game', 'the_question/game' ]:
        os.system("./renpy.sh --compile --game " + i)
    

    files = [ ]
    more_files = [ ]

    files.append("CHANGELOG.txt")
    files.append("LICENSE.txt")
    files.extend(tree("common"))
    more_files.append("console.exe")
    files.extend(tree("launcher"))
    files.extend(tree("tutorial"))
    # files.extend(tree("dse"))
    files.extend(tree("the_question"))

#     editor = tree("editor")
#     editor.remove("editor/scite.exe")
#     files.append("editor/scite.exe")
#     more_files.extend(editor)

    more_files.extend(tree("jedit"))
    
    # files.extend(tree("extras"))
    more_files.extend(tree("lib"))
    more_files.extend(tree("lib/linux-x86"))

    module_files = [
        "lib/pysdlsound/linmixer.py",
        "lib/pysdlsound/__init__.py",
        "core.c",
        "ffdecode.c",
        "IMG_savepng.c",
        "IMG_savepng.h",
        "mmx.h",
        "pss.c",
        "pss.h",
        "README.txt",
        "_renpy.c",
        "renpy_font.c",
        "renpy.h",
        "_renpy.pyx",
        "renpy_ttf.c",
        "renpy_ttf.h",
        "rwobject.c",
        "setup.py",
        "sound.c",
        "sound.pyx",
        "subpixel.c",
        "winmixer.c",
        "winmixer.pyx",
        "_renpybidi.c",
        "renpybidicore.c",
        "_renpybidi.pyx",
        "_renpy_pysdlgl.c",
        "_renpy_pysdlgl.pyx",
        "_renpy_tegl.c",
        "maketegl.py",
        "maketegl.txt",
        ]

    for i in module_files:
        files.append('module/' + i)

    more_files.append('python26.dll')
    more_files.append('msvcr90.dll')
    more_files.append('Microsoft.VC90.CRT.manifest')
    files.extend(tree('renpy'))
    more_files.extend(tree('renpy.app'))
    more_files.append('renpy.code')
    more_files.append('renpy.exe')
    files.append('renpy.py')

    more_files.append('renpy.sh')

    files.extend(tree('template'))
    # files.extend(tree('tools'))

    files.extend(tree('doc'))
    
    # files.append('doc/index.html')
    # files.append('doc/common.css')
    # files.append('doc/docs.css')
    # files.append('doc/monobook.css')
    # files.append('doc/monobook2.css')
    # files.append('doc/shared.css')
    # files.extend(tree('doc/reference'))
    # files.extend(tree('doc/tutorials'))
    # files.extend(tree('doc/images'))
    
    files.sort()
    more_files.sort()

    # zipup("dists/" + prefix + "-win32.zip", prefix, files)
    # print "----"
    zipup("dists/" + prefix + "-sdk.zip", prefix, files + more_files)
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
    shutil.rmtree(prefix)
    os.unlink(prefix + "-sdk.7z")
    
    print
    print "Did you remember to rebuild the exe after the last change?"
    print "Did you run me with renpython -OO?"
    print "Was ming using the right crt?"
    print "Did you update renpy.py and launcher/script_version.rpy?"
    print "Did you run with a RENPY_SCALE_FACTOR?"
    
if __name__ == "__main__":
    main()
