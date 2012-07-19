# Copyright 2004-2012 Tom Rothamel <pytom@bishoujo.us>
# See LICENSE.txt for license details.

init python in distribute:
    
    import time
    import zipfile
    import tarfile
    import zlib

    zlib.Z_DEFAULT_COMPRESSION = 9
    
    class ZipPackage(object):
        """
        A class that creates a zip file.
        """
        
        def __init__(self, filename):
            self.zipfile = zipfile.ZipFile(filename, "w", zipfile.ZIP_DEFLATED)
            
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

            with open(path, "rb") as f:
                data = f.read()
                
            self.zipfile.writestr(zi, data)

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
            self.tarfile.dereference = True            
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
