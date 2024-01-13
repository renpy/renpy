# Copyright 2004-2024 Tom Rothamel <pytom@bishoujo.us>
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
    import sys
    import threading

    from zipfile import crc32

    # Since the long type doesn't exist on py3, define it here
    if not PY2:
        long = int

    zlib.Z_DEFAULT_COMPRESSION = 5

    if PY2:

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
                    file_size = 0

                    zip64 = self._allowZip64 and \
                            zinfo.file_size * 1.05 > zipfile.ZIP64_LIMIT

                    self.fp.write(zinfo.FileHeader(zip64))

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

                if not zip64 and self._allowZip64:
                    if file_size > zipfile.ZIP64_LIMIT:
                        raise RuntimeError('File size has increased during compressing')
                    if compress_size > zipfile.ZIP64_LIMIT:
                        raise RuntimeError('Compressed size larger than uncompressed size')

                # Seek backwards and write CRC and file sizes
                position = self.fp.tell()       # Preserve current position in file
                self.fp.seek(zinfo.header_offset, 0)

                self.fp.write(zinfo.FileHeader(zip64))

                self.fp.seek(position, 0)
                self.filelist.append(zinfo)
                self.NameToInfo[zinfo.filename] = zinfo

    else:

        class ZipFile(zipfile.ZipFile):

            def write_with_info(self, zinfo, filename):

                if zinfo.filename.endswith("/"):
                    data = b''
                else:
                    with open(filename, "rb") as f:
                        data = f.read()

                self.writestr(zinfo, data)


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
            except Exception:
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
                zi.external_attr = long(0o100755) << 16
            else:
                zi.external_attr = long(0o100644) << 16

            self.zipfile.write_with_info(zi, path)

        def add_directory(self, name, path):
            if path is None:
                return

            zi = zipfile.ZipInfo(name + "/")
            zi.date_time = self.get_date_time(path)
            zi.compress_type = zipfile.ZIP_STORED
            zi.create_system = 3
            zi.external_attr = (long(0o040755) << 16) | 0x10

            self.zipfile.write_with_info(zi, path)

        def close(self, progress=None):
            self.zipfile.close()


    class TarPackage(object):

        def __init__(self, filename, mode, notime=False):
            """
            notime
                If true, times will be forced to the epoch.
            """

            self.tarfile = tarfile.open(filename, mode, format=tarfile.PAX_FORMAT)
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
                info.mode = 0o755
            else:
                info.mode = 0o644

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

        def close(self, progress=None):
            self.tarfile.close()


    class UpdatePackage(TarPackage):

        def __init__(self, filename, basename, destination):
            self.path = filename
            self.basename = basename
            self.destination = destination

            TarPackage.__init__(self, filename, "w", notime=True)

        def close(self, progress=None):
            TarPackage.close(self)

            cmd = [
                updater.zsync_path("zsyncmake"),
                "-z",
                # -u url to gzipped data - not a local filename!
                "-u", self.basename + ".update.gz",
                "-o", os.path.join(self.destination, self.basename + ".zsync"),
                os.path.abspath(self.path),
                ]

            subprocess.check_call([ renpy.fsencode(i) for i in cmd ])

            # Build the sums file. This is a file with an adler32 hash of each 64k block
            # of the zsync file. It's used to help us determine how much of the file is
            # downloaded.
            with open(self.path, "rb") as src:
                with open(renpy.fsencode(os.path.join(self.destination, self.basename + ".sums")), "wb") as sums:
                    while True:
                        data = src.read(65536)

                        if not data:
                            break

                        sums.write(struct.pack("<I", zlib.adler32(data) & 0xffffffff))


    class DirectoryPackage(object):

        def mkdir(self, path):
            if not os.path.isdir(path):
                os.makedirs(path, 0o755)

        def __init__(self, path):
            self.path = path

            if os.path.isdir(path):
                shutil.rmtree(path)

            self.mkdir(path)

        def add_file(self, name, path, xbit):
            fn = os.path.join(self.path, name)

            # If this is not a directory, ensure all parent directories
            # have been created
            self.mkdir(os.path.dirname(fn))
            shutil.copy(path, fn)

            if xbit:
                os.chmod(fn, 0o755)
            else:
                os.chmod(fn, 0o644)

        def add_directory(self, name, path):
            fn = os.path.join(self.path, name)
            self.mkdir(fn)

        def close(self, progress=None):
            return


    class ExternalZipPackage(object):

        def __init__(self, path):
            self.path = path
            self.directory = path + ".zd"
            self.dp = DirectoryPackage(self.directory)

        def add_file(self, name, path, xbit):
            self.dp.add_file(name, path, xbit)

        def add_directory(self, name, path):
            self.dp.add_directory(name, path)

        def close(self, progress=None):
            self.dp.close()

            if os.path.exists(self.path):
                os.unlink(self.path)

            p = subprocess.Popen([
                "zip",
                "-9rq",
                os.path.abspath(self.path),
            ] + os.listdir(self.directory),
            cwd=os.path.abspath(self.directory)
            )

            p.wait()

            shutil.rmtree(self.directory)


    class DMGPackage(DirectoryPackage):
        def __init__(self, path, make_dmg):
            self.make_dmg = make_dmg
            DirectoryPackage.__init__(self, path)

        def close(self, progress=None):
            DirectoryPackage.close(self)
            self.make_dmg()


    class RPUPackage(object):

        generator = None

        def __init__(self, directory, variant):
            import renpy.update.common

            self.directory = directory + "/rpu"
            self.variant = variant
            self.file_list = renpy.update.common.FileList()

            if not os.path.exists(self.directory):
                os.mkdir(self.directory)

        def add_file(self, name, path, xbit):
            self.file_list.add_file(name, path, xbit)

        def add_directory(self, name, _path):
            self.file_list.add_directory(name)

        def close(self, progress=None):
            import renpy.update.generate

            if RPUPackage.generator is None:
                RPUPackage.generator = renpy.update.generate.BlockGenerator(self.directory)

            RPUPackage.generator.generate(self.variant, self.file_list, progress)

        @staticmethod
        def reset():
            RPUPackage.generator = None


    class NullPackage(object):
        """
        A package format that doesn't create an output file,
        only updates.
        """

        def add_file(self, name, path, xbit):
            return

        def add_directory(self, name, _path):
            return

        def close(self, progress=None):
            return


    parallel_threads = [ ]

    class ParallelPackage(object):

        def __init__(self, package, done, what):
            self.package = package
            self.done = done
            self.what = what

            self.worklist = [ ]

        def add_file(self, name, path, xbit):
            self.worklist.append((False, name, path, xbit))

        def add_directory(self, name, path):
            self.worklist.append((True, name, path, True))

        def close(self, progress=None):
            t = threading.Thread(target=self.run)
            t.start()

            self.thread = t
            parallel_threads.append(self)

        def run(self):

            for i in self.worklist:
                directory, name, path, xbit = i
                if directory:
                    self.package.add_directory(name, path)
                else:
                    self.package.add_file(name, path, xbit)

            self.package.close()


    def wait_parallel_threads():

        t = 0

        while parallel_threads:

            alive = [ ]

            for i in parallel_threads:
                i.thread.join(0)
                if i.thread.is_alive():
                    alive.append(i)

            if not alive:
                break

            t += 1
            print("\r " + str(t) + " " + " ".join(sorted([ i.what for i in alive ])))

            time.sleep(1)

        for i in parallel_threads:
            if i.done:
                i.done()
