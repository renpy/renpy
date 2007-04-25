#!/home/tom/bin/renpython -O
# Builds a distributions of Ren'Py.

import sys
import os
import zipfile
import tarfile
import time
import zlib
import compileall

zlib.Z_DEFAULT_COMPRESSION = 9

# Gets the data for the given file.
def data(fn):

    rv = file(fn, "rb").read()

    if fn.startswith("renpy.app"):
        return rv

    if fn.endswith(".rpy") or fn.endswith(".py"):
        rv = rv.replace("\n", "\r\n")
        rv = rv.replace("\r\r\n", "\r\n")

    return rv
    

def tarup(filename, prefix, files):

    tf = tarfile.open(filename, "w:bz2")
    tf.dereference = True

    print

    for fn in files:
        print fn
        
        tf.add(fn, prefix + "/" + fn, False)

    tf.close()
    

# Creates a zip file.
def zipup(filename, prefix, files):

    zf = zipfile.ZipFile(filename, "w")

    print

    for fn in files:

        print fn

        zi = zipfile.ZipInfo(prefix + "/" + fn)

        st = os.stat(fn)

        zi.date_time = time.gmtime(st.st_mtime)[:6]
        zi.compress_type = zipfile.ZIP_DEFLATED
        zi.create_system = 3
        zi.external_attr = long(st.st_mode) << 16

        zf.writestr(zi, data(fn))
        
    zf.close()
    
    

def tree(root):

    rv = [ ]

    for dirname, dirs, filenames in os.walk(root):

        if "saves" in dirs:
            dirs.remove("saves")

        if ".svn" in dirs:
            dirs.remove(".svn")
        else:
            if not root == "lib":
                print "Note:", dirname, "not in subversion."
            

        for f in filenames:
            if f[-1] == '~' or f[0] == '.':
                continue

            if f.endswith(".bak") or f.endswith(".pyc") or f.endswith(".pyo"):
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
    for i in [ 'demo/game', 'data', 'dse/game', 'template/game', 'the_question' ]:
        os.system("./renpy.sh --compile --game " + i)
    

    files = [ ]
    more_files = [ ]

    files.append("CHANGELOG.txt")
    files.append("LICENSE.txt")
    files.extend(tree("common"))
    files.append("console.exe")
    files.extend(tree("data"))
    files.extend(tree("demo"))
    files.extend(tree("dse"))
    files.extend(tree("the_question"))

    editor = tree("editor")
    editor.remove("editor/scite.exe")
    files.append("editor/scite.exe")
    more_files.extend(editor)

    # files.extend(tree("extras"))
    more_files.extend(tree("lib"))

    module_files = [
        "lib/pysdlsound/linmixer.py",
        "lib/pysdlsound/__init__.py",
        "README.txt",
        "_renpy.pyx",
        "_renpy.c",
        "core.c",
        "mmx.h",
        "native_midi.h",
        "native_midi_common.c",
        "native_midi_common.h",
        "native_midi_mac.c",
        "native_midi_win32.c",
        "nativemidi.c",
        "nativemidi.pyx",
        "pss.c",
        "pss.h",
        "sound.c",
        "sound.pyx",
        "rwobject.c",
        "renpy.h",
        "setup.py",
        "winmixer.c",
        "winmixer.pyx",
        "IMG_savepng.c",
        "IMG_savepng.h",
        ]

    for i in module_files:
        more_files.append('module/' + i)

    files.append('python23.dll')
    files.extend(tree('renpy'))
    more_files.extend(tree('renpy.app'))
    files.append('renpy.code')
    files.append('renpy.exe')
    files.append('renpy.py')

    more_files.append('renpy.sh')

    files.extend(tree('template'))
    files.extend(tree('tools'))

    files.append('doc/index.html')
    files.append('doc/screen.css')
    files.extend(tree('doc/reference'))
    files.extend(tree('doc/tutorials'))
    
    files.sort()
    more_files.sort()

    zipup("dists/" + prefix + "-win32.zip", prefix, files)
    print "----"
    zipup("dists/" + prefix + "-full.zip", prefix, files + more_files)
    print "----"
    tarup("dists/" + prefix + "-full.tar.bz2", prefix, files + more_files)

    
    
    print
    print "Did you remember to rebuild the exe after the last change?"
    print "Did you run me with renpython -O?"
    
if __name__ == "__main__":
    main()
