# Copyright 2004-2015 Tom Rothamel <pytom@bishoujo.us>
#
# Permission is hereby granted, free of charge, to any person
# obtaining a copy of this software and associated documentation files
# (the "Software"), to deal in the Software without restriction,
# including without limitation the rights to use, copy, modify, merge,
# publish, distribute, sublicense, and/or sell copies of the Software,
# and to permit persons to whom the Software is furnished to do so,
# subject to the following conditions:
#
# The above copyright notice and this permission notice shall be
# included in all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND,
# EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF
# MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND
# NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE
# LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION
# OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION
# WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.

init python in distribute:

    import time
    import zipfile
    import tarfile
    import zlib
    import struct
    import stat
    import shutil

    from zipfile import crc32

    zlib.Z_DEFAULT_COMPRESSION = 9

    class ZipFile(zipfile.ZipFile):

        def write_with_info(self, zinfo, filename):
            """Put the bytes from filename into the archive under the name
            arcname."""
            if not self.fp:
                raise RuntimeError(
                      "Attempt to write to ZIP archive that was already closed")

            st = os.stat(filename)
            isdir = stat.S_ISDIR(st.st_mode)

            zinfo.file_size = st.st_size
            zinfo.flag_bits = 0x00
            zinfo.header_offset = self.fp.tell()    # Start of header bytes

            self._writecheck(zinfo)
            self._didModify = True

            if isdir:
                zinfo.file_size = 0
                zinfo.compress_size = 0
                zinfo.CRC = 0
                self.filelist.append(zinfo)
                self.NameToInfo[zinfo.filename] = zinfo
                self.fp.write(zinfo.FileHeader())
                return

            with open(filename, "rb") as fp:
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
                    buf = fp.read(1024 * 1024)
                    if not buf:
                        break
                    file_size = file_size + len(buf)
                    CRC = crc32(buf, CRC) & 0xffffffff
                    if cmpr:
                        buf = cmpr.compress(buf)
                        compress_size = compress_size + len(buf)
                    self.fp.write(buf)
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
            self.fp.write(struct.pack("<LLL", zinfo.CRC, zinfo.compress_size,
                  zinfo.file_size))
            self.fp.seek(position, 0)
            self.filelist.append(zinfo)
            self.NameToInfo[zinfo.filename] = zinfo


    class ZipPackage(object):
        """
        A class that creates a zip file.
        """

        def __init__(self, filename):
            self.zipfile = ZipFile(filename, "w", zipfile.ZIP_DEFLATED, True)

        def get_date_time(self, path):
            """
            Gets the datetime for a file. If the time doesn't exist or is
            weird, use the current time instead.
            """

            try:
                s = os.stat(path)
                rv = time.gmtime(s.st_mtime)[:6]

                # Check that the time is sensible.
                if rv[0] < 2000:
                    rv = None
            except:
                rv = None

            if rv is None:
                rv = time.gmtime()[:6]

            return rv

        def add_file(self, name, path, xbit):

            if path is None:
                raise Exception("path for " + name + " must not be None.")

            zi = zipfile.ZipInfo(name)
            zi.date_time = self.get_date_time(path)
            zi.compress_type = zipfile.ZIP_DEFLATED
            zi.create_system = 3

            if xbit:
                zi.external_attr = long(0100755) << 16
            else:
                zi.external_attr = long(0100644) << 16

            self.zipfile.write_with_info(zi, path)

        def add_directory(self, name, path):
            if path is None:
                return

            zi = zipfile.ZipInfo(name + "/")
            zi.date_time = self.get_date_time(path)
            zi.compress_type = zipfile.ZIP_STORED
            zi.create_system = 3
            zi.external_attr = (long(0040755) << 16) | 0x10

            self.zipfile.write_with_info(zi, path)

        def close(self):
            self.zipfile.close()


    class TarPackage(object):

        def __init__(self, filename, mode, notime=False):
            """
            notime
                If true, times will be forced to the epoch.
            """

            self.tarfile = tarfile.open(filename, mode)
            self.tarfile.dereference = True
            self.notime = notime

        def add_file(self, name, path, xbit):

            if path is not None:
                info = self.tarfile.gettarinfo(path, name)
            else:
                info = tarfile.TarInfo(name)
                info.size = 0
                info.mtime = int(time.time())
                info.type = tarfile.DIRTYPE

            if xbit:
                info.mode = 0755
            else:
                info.mode = 0644

            info.uid = 1000
            info.gid = 1000
            info.uname = "renpy"
            info.gname = "renpy"

            if self.notime:
                info.mtime = 0

            if info.isreg():
                with open(path, "rb") as f:
                    self.tarfile.addfile(info, f)
            else:
                self.tarfile.addfile(info)

        def add_directory(self, name, path):
            self.add_file(name, path, True)

        def close(self):
            self.tarfile.close()

    class DirectoryPackage(object):

        def mkdir(self, path):
            if not os.path.isdir(path):
                os.mkdir(path, 0755)

        def __init__(self, path):
            self.path = path
            self.mkdir(path)

        def add_file(self, name, path, xbit):
            fn = os.path.join(self.path, name)
            shutil.copy2(path, fn)

            if xbit:
                os.chmod(fn, 0755)
            else:
                os.chmod(fn, 0644)

        def add_directory(self, name, path):
            fn = os.path.join(self.path, name)
            self.mkdir(fn)

        def close(self):
            return


