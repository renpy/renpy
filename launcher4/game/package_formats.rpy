init python in distribute:
    
    import time
    
    import zipfile
    import tarfile
    
    
    class MyZipFile(zipfile.ZipFile):
        """
         Modified ZipFile class that can insert a file into the archive,
         using a supplied ZipInfo object. Code comes from the writestr
         and write methods of ZipFile.
         """

        def write_file_with_zipinfo(self, filename, path, zinfo, compress_type=None):
            """Put the bytes from filename into the archive under the name
            arcname."""
            st = os.stat(path)

            if compress_type is None:
                zinfo.compress_type = self.compression
            else:
                zinfo.compress_type = compress_type

            zinfo.file_size = st.st_size
            zinfo.flag_bits = 0x00
            zinfo.header_offset = self.fp.tell()    # Start of header bytes

            self._writecheck(zinfo)
            self._didModify = True

            fp = open(path, "rb")

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


    class ZipPackage(object):
        """
        A class that creates a zip file.
        """
        
        def __init__(self, filename):
            self.zipfile = MyZipFile(filename, "w", zipfile.ZIP_DEFLATED)
            
        def add_file(self, name, path, xbit):
            
            if path is None:
                raise Exception("path for " + name + " must not be None.")

            zi = zipfile.ZipInfo(name)

            s = os.stat(path)
            zi.date_time = time.gmtime(s.st_mtime)[:6]                            
            zi.compress_type = zipfile.ZIP_DEFLATED
            zi.create_system = 3

            if xbit:
                zi.external_attr = long(0100777) << 16
            else:
                zi.external_attr = long(0100666) << 16 

            self.zipfile.write_file_with_zipinfo(name, path, zi)

        def add_directory(self, name, path):
            return
            
        def close(self):
            self.zipfile.close()


    class TarPackage(object):
        
        def __init__(self, filename, mode, notime=False):
            """
            notime
                If true, times will be forced to the epoch.
            """
            
            self.tarfile = tarfile.open(filename, mode)
            self.tarfile.deference = True            
            self.notime = notime

        def add_file(self, name, path, xbit):

            if path is not None:
                info = self.tarfile.gettarinfo(path, name)
            else:
                info = tarfile.TarInfo(name)
                info.size = 0
                info.mtime = time.time()
                info.type = tarfile.DIRTYPE

            if xbit:
                info.mode = 0777
            else:
                info.mode = 0666

            info.uid = 1000
            info.gid = 1000
            info.uname = "renpy"
            info.gname = "renpy"

            if self.notime:
                self.mtime = 0

            if info.isreg():
                self.tarfile.addfile(info, open(path, "rb"))
            else:
                self.tarfile.addfile(info)

        def add_directory(self, name, path):
            self.add_file(name, path, True)

        def close(self):
            self.tarfile.close()
