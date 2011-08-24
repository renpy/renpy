import os.path
import zipfile
import tarfile
import time
import sys
import struct
import zlib
zlib.Z_DEFAULT_COMPRESSION = 9

import binascii
import change_icon

import argparse

# The directory containing the project that we'll be distributing.
project_path = None

# The path to the Ren'Py base directory.
renpy_base = None

# A function that is called to give information about what is going
# on now.
def info(title, body):
    return

# A function that is called to give a progress report.
def progress(title, total, amount):
    amount += 1

    if amount % 25 == 0:
        print title, amount, "of", total

# A translation function.
def _(s):
    return s

# These are files that are ignored wherever they are found in a
# distribution.
ignored_files = (
    "thumbs.db",
    "traceback.txt",
    "errors.txt",
    "files.txt",
    "saves"
    )

# These are files (and directories) that are ignored when found in
# the root directory of the distribution.
root_ignored_files = (
    "common",
    "renpy",
    "renpy.code",
    "python23.dll",
    "python24.dll",
    "python25.dll",
    "msvcr71.dll",                     
    "lib",
    "iliad-icon.png",
    "manifest.xml",
    "icon.ico",
    "icon.icns",
    "launcherinfo.py",
    "archived",
    )

# Extensions that should be made executable.
executable_extensions = (
    "MacOS",
    "so",
    "dylib",
    ".sh",
    "python",
    "python.real",
    )
    
class MyZipFile(zipfile.ZipFile):
    """
     Modified ZipFile class that can insert a file into the archive,
     using a supplied ZipInfo object. Code comes from the writestr
     and write methods of ZipFile.
     """

    def write_file_with_zipinfo(self, filename, zinfo, compress_type=None):
        """Put the bytes from filename into the archive under the name
        arcname."""
        st = os.stat(filename)

        if compress_type is None:
            zinfo.compress_type = self.compression
        else:
            zinfo.compress_type = compress_type

        zinfo.file_size = st.st_size
        zinfo.flag_bits = 0x00
        zinfo.header_offset = self.fp.tell()    # Start of header bytes

        self._writecheck(zinfo)
        self._didModify = True

        fp = open(filename, "rb")

        # Must overwrite CRC and sizes with correct data later
        zinfo.CRC = CRC = 0
        zinfo.compress_size = compress_size = 0
        zinfo.file_size = file_size = 0

        self.fp.write(zinfo.FileHeader())

        if zinfo.compress_type == zipfile.ZIP_DEFLATED:
            cmpr = zlib.compressobj(zlib.Z_DEFAULT_COMPRESSION,
                 zlib.DEFLATED, -15)
        else:
            cmpr = None
        while 1:
            buf = fp.read(1024 * 64)
            if not buf:
                break
            file_size = file_size + len(buf)
            CRC = binascii.crc32(buf, CRC)
            if cmpr:
                buf = cmpr.compress(buf)
                compress_size = compress_size + len(buf)
            self.fp.write(buf)
        fp.close()
        if cmpr:
            buf = cmpr.flush()
            compress_size = compress_size + len(buf)
            self.fp.write(buf)
            zinfo.compress_size = compress_size
        else:
            zinfo.compress_size = file_size

        zinfo.CRC = CRC
        zinfo.file_size = file_size

        # Seek backwards and write CRC and file sizes
        position = self.fp.tell()       # Preserve current position in file
        self.fp.seek(zinfo.header_offset + 14, 0)
        self.fp.write(struct.pack("<lLL", zinfo.CRC, zinfo.compress_size,
              zinfo.file_size))

        self.fp.seek(position, 0)
        self.filelist.append(zinfo)
        self.NameToInfo[zinfo.filename] = zinfo

def tree(
    src,
    dest,
    exclude_suffix=[ ".pyc", "~", ".bak", ".old", ".new" ],
    exclude_prefix=[ "#", "." ],
    exclude_files = set(ignored_files),
    root_exclude_prefix = [ ],
    root_exclude_suffix = [ ".py", ".sh", ".app" ],
    root_exclude_files = set(root_ignored_files),
    root=False):

    """
     Returns a list of source-filename, destination-filename pairs.
     """

    if dest[0] != "/":
        raise Exception("Destination must begin with /: %r" % dest)

    src = src.rstrip('/')
    dest = dest.rstrip('/')

    def include(fn, is_root):
        """
         Returns True if the file should be included in the list of
         files we are copying.
         """

        for i in exclude_suffix:
            if fn.endswith(i):
                return False

        for i in exclude_prefix:
            if fn.startswith(i):
                return False

        if fn in exclude_files:
            return False

        if not root or not is_root:
            return True

        for i in root_exclude_suffix:
            if fn.endswith(i):
                return False

        for i in root_exclude_prefix:
            if fn.startswith(i):
                return False

        if fn in root_exclude_files:
            return False

        return True

    rv = [ ]

    # Walk the tree, including what is necessary.
    for srcdir, dirs, files in os.walk(src):

        is_root = (srcdir == src)

        srcdir += "/"
        destdir = dest + srcdir[len(src):]
        destdir.replace("\\", "/")

        rv.append((srcdir, destdir))

        for fn in files:

            if not include(fn, is_root):
                continue

            sfn = srcdir + fn
            dfn = destdir + fn

            rv.append((sfn, dfn))

        dirs[:] = [ i for i in dirs if include(i, is_root) ]

    rv = [ (a.replace("\\", "/"), b.replace("\\", "/")) for a, b in rv ]

    return rv


def make_zip(t, filename, files, file_data):
    """
     This creates `filename`.zip, containing `files`, placed in the
     `filename` directory. `file_data` is a map from source file to
     replacement data.
     """

    files.sort(key=lambda a : a[1])
    progress_len = len(files)

    fn = os.path.join(os.path.dirname(project_path), filename)

    zf = MyZipFile(fn + ".zip", "w", zipfile.ZIP_DEFLATED)

    for i, (fn, an) in enumerate(files):

        progress(t, progress_len, i)

        if os.path.isdir(fn):
            continue

        zi = zipfile.ZipInfo(filename + an)

        s = os.stat(fn)
        zi.date_time = time.gmtime(s.st_mtime)[:6]                            
        zi.compress_type = zipfile.ZIP_DEFLATED
        zi.create_system = 3

        for i in executable_extensions:
            if os.path.dirname(fn).endswith(i) or fn.endswith(i):
                zi.external_attr = long(0100777) << 16
                break
        else:
            zi.external_attr = long(0100666) << 16 

        if fn in file_data:
            data = file_data[fn]
            zf.writestr(zi, data)
        else:
            zf.write_file_with_zipinfo(fn, zi)

    zf.close()

def make_tar(t, filename, files):
    """
     Makes a tarfile, as above.
     """

    files.sort(key=lambda a : a[1])
    progress_len = len(files)

    fn = os.path.join(os.path.dirname(project_path), filename)

    tf = tarfile.open(fn + ".tar.bz2", "w:bz2")
    tf.dereference = True

    for j, (fn, an) in enumerate(files):

        progress(t, progress_len, j)

        info = tf.gettarinfo(fn, filename + an)

        perms = 0666

        if info.isdir():
            perms = 0777

        for i in executable_extensions:
            if fn.endswith(i):
                perms = 0777

        info.mode = perms
        info.uid = 1000
        info.gid = 1000
        info.uname = "renpy"
        info.gname = "renpy"

        if info.isreg():
            tf.addfile(info, file(fn, "rb"))
        else:
            tf.addfile(info)

    tf.close()


def distribute(
    _project_path,
    _renpy_base,
    base_name,
    executable_name,
    ignore_extensions,
    documentation_extensions,
    build_windows,
    build_linux,
    build_mac,
    build_all):

    global project_path
    global renpy_base
    project_path = _project_path
    renpy_base = _renpy_base
    
    base_name = base_name.encode("utf-8")
    executable_name = executable_name.encode("utf-8")
    ignore_extensions = ignore_extensions.encode("utf-8")
    documentation_extensions = documentation_extensions.encode("utf-8")

    # Convert some of these to more useful formats.
    ignore_extensions = [ i.strip() for i in ignore_extensions.split() ]
    documentation_extensions = [ i.strip() for i in documentation_extensions.split() ]

    # Scan for the files we want to include in the various distributions.
    info(_(u"Scanning..."), "")

    # Files included in the various distributions.
    multi_files = [ ]
    win_files = [ ]
    linux_files = [ ]
    mac_files = [ ]

    # A map from source file name to replacement data to be placed in
    # that file.
    file_data = { }


    ######################################################################
    # Multi files.

    rb = renpy_base.replace("\\", "/") + "/"

    # Project files.
    multi_files.extend(tree(project_path, "/", root=True, exclude_suffix=ignore_extensions))
    multi_files.append((rb + "renpy.py",  "/" + executable_name + ".py"))

    # Renpy files.
    multi_files.extend(tree(rb + "common", "/common"))
    multi_files.extend(tree(rb + "renpy", "/renpy"))
    multi_files.append((rb + "LICENSE.txt", "/renpy/LICENSE.txt"))

    def add_script_version(fn, ignore_extensions=ignore_extensions, multi_files=multi_files, rb=rb):
        """
         Add a script_version file if it does not already exist, and if the
         extension is allowed by the game.
         """

        for _a, b in multi_files:
            if b == "/game/" + fn:
                return

        for i in ignore_extensions:
            if fn.endswith(i):
                return

        multi_files.append((rb + "launcher/" + fn, "/game/" + fn))

    add_script_version("script_version.rpy")
    add_script_version("script_version.rpyc")


    ######################################################################
    # Windows files.

    if build_windows or build_all:

        win_files.append((rb + "renpy.exe", "/" + executable_name + ".exe"))
        win_files.append((rb + "python26.dll", "/python26.dll"))
        win_files.append((rb + "msvcr90.dll", "/msvcr90.dll"))
        win_files.append((rb + "Microsoft.VC90.CRT.manifest", "/Microsoft.VC90.CRT.manifest"))

        win_files.append((rb + "lib", "/lib"))
        win_files.append((rb + "lib/dxwebsetup.exe", "/lib/dxwebsetup.exe"))
        win_files.extend(tree(rb + "lib/windows-x86", "/lib/windows-x86"))
        
        if os.path.exists(project_path + "/icon.ico"):
            file_data[rb + "renpy.exe"] = change_icon.change_icons(
                rb + "renpy.exe",
                project_path + "/icon.ico",
                )


    ######################################################################
    # Linux files.

    if build_linux or build_all:

        linux_files.append((rb + "renpy.sh", "/" + executable_name + ".sh"))
        linux_files.append((rb + "lib", "/lib"))
        linux_files.append((rb + "lib/python", "/lib/python"))
        linux_files.extend(tree(rb + "lib/linux-x86", "/lib/linux-x86"))

        # Warning: The tar.bz2 builder doesn't support file_data.


    ######################################################################
    # Mac (non-app) files.

    if build_mac or build_all:
        mac_files = tree(rb + "renpy.app",
                         "/" + executable_name + ".app")

        # Rename executable.
        mac_files = [ (fn, an.replace("Ren'Py Launcher", executable_name)) for (fn, an) in mac_files ]

        # Plist file.
        quoted_name = executable_name.replace("&", "&amp;").replace("<", "&lt;")                                               
        info_plist = file(rb + "renpy.app/Contents/Info.plist", "rb").read().replace("Ren'Py Launcher", quoted_name)
        file_data[rb + "renpy.app/Contents/Info.plist"] = info_plist

        # Launcher script.
        quoted_name = executable_name.replace("\"", "\\\"")
        launcher_py = file(rb + "renpy.app/Contents/Resources/launcher.py", "rb").read().replace("Ren'Py Launcher", quoted_name)
        file_data[rb + "renpy.app/Contents/Resources/launcher.py"] = launcher_py

        # Icon file.
        if os.path.exists(project_path + "/icon.icns"):
            icon_data = file(project_path + "/icon.icns", "rb").read()
            file_data[rb + "renpy.app/Contents/Resources/launcher.icns"] = icon_data


    ######################################################################
    # Now, build the various distributions.

    if build_windows:
        make_zip(
            _(u"Building Windows..."),
            base_name + "-win32",
            multi_files + win_files,
            file_data)

    if build_linux:
        make_tar(
            _(u"Building Linux..."),
            base_name + "-linux-x86",
            multi_files + linux_files)


    if build_mac:

        # Reorganize the files so all the non application files live inside
        # the application. If there's documentation involved, then it
        # lives in both places.
        macapp_files = [ ]

        for fn, an in multi_files + mac_files:
            if not an.startswith("/" + executable_name + ".app"):
                new_an = "/" + executable_name + ".app/Contents/Resources/autorun" + an
                macapp_files.append((fn, new_an))

                if an.rindex('/') == 0:
                    for i in documentation_extensions:
                        if fn.endswith(i):
                            macapp_files.append((fn, an))
                            break
            else:
                macapp_files.append((fn, an))

        make_zip(
            _(u"Building Macintosh..."),
            base_name + "-mac",
            macapp_files,
            file_data)


    if build_all:
        make_zip(
            _(u"Building Combined..."),
            base_name + "-all",
            multi_files + win_files + linux_files + mac_files,
            file_data)

def main():

    ap = argparse.ArgumentParser(description="Prepare a Ren'Py game for distribution.")

    ap.add_argument("project_path", type=str, help="The path to the directory containing the project.")
    ap.add_argument("base_name", type=str, help="The base name of the archive files produced.")
    ap.add_argument("executable_name", type=str, help="The name of the executables produced.")
    ap.add_argument("--renpy-base", type=str, default=None, help="The path to the Ren'Py distribution.")

    ap.add_argument("--ignore-extensions", type=str, default="~ .bak", help="A space-separated list of extensions to ignore.")
    ap.add_argument("--documentation-extensions", type=str, default="txt html", help="A space-separated list of extensions to treat as documentation.")

    ap.add_argument("--build-windows", action="store_true", default=False, help="Build the Windows distribution.")
    ap.add_argument("--build-mac", action="store_true", default=False, help="Build the Mac OS X distribution.")
    ap.add_argument("--build-linux", action="store_true", default=False, help="Build the Windows distribution.")
    ap.add_argument("--build-all", action="store_true", default=False, help="Build the All Platforms distribution.")

    args = ap.parse_args()

    renpy_base = args.renpy_base
    if renpy_base is None:
        renpy_base = os.path.dirname(os.path.dirname(os.path.abspath(sys.argv[0])))
    
    distribute(
        args.project_path, 
        renpy_base,
        base_name=args.base_name,
        executable_name=args.executable_name,
        ignore_extensions=args.ignore_extensions,
        documentation_extensions=args.documentation_extensions,
        build_windows=args.build_windows,
        build_mac=args.build_mac,
        build_linux=args.build_linux,
        build_all=args.build_all)

if __name__ == "__main__":
    main()
