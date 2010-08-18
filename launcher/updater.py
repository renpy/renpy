import urllib2
import bz2
import os
import hashlib
import public

class UpdateException(Exception):
    """
    The exception that we return if the update fails.
    """

    pass

class Updater(object):
    """
    A class that attempts to update a tree of files, with a reasonable
    degree of safety, security, speed, and progress reporting.
    """

    def __init__(self, local, remote, tags):
        """
        Create a new updater.

        `local`
            The name of the local directory where the files are stored.
        `remote`
            The remote url base.
        `tags`
            A list of tags to update.            
            """

        self.local = local
        self.remote = remote

        # The remote version we're upgrading to.
        self.version = None

        # A list of directory names.
        self.directories = [ ]
        
        # A list of file, bz2-size, adler32 tuples.
        self.files = [ ]

        # Xbit files.
        self.xbit = [ ]

        # The tags we use.
        self.tags = set(tags)
        
    def snarf(self, url):
        """
        Gets the url as a string.
        """

        try:
            url = urllib2.urlopen(self.remote + "/" + url, None, 5)
            return url.read()
        except Exception, e:
            raise UpdateException("Could not download %r: %r" % (url, e))

    def retrieve(self, relative):
        """
        Downloads the bz2-compressed file, and then decompresses it into
        relative.new.
        """

        bz = os.path.join(self.local, relative + ".new.bz2")
        new = os.path.join(self.local, relative + ".new")
        
        try:
            url = urllib2.urlopen(self.remote + "/" + relative + ".bz2", None, 5)

            f = file(bz, "wb")
            f.write(url.read())
            f.close()

            url.close()
            
            bzf = bz2.BZ2File(bz, "rb")
            f = file(new, "wb")

            while True:
                buf = bzf.read(1024 * 1024)

                if not buf:
                    break
                
                f.write(buf)

            f.close()
            bzf.close()

            os.unlink(bz)
            
        except Exception, e:
            raise UpdateException("Could not download %r: %r" % (url, e))


    def check_version(self, version):
        """
        Checks to see if version is still up to date. Returns a new-version,
        verbose-version string. new-version is an internal representation
        of the version being downloaded, while verbose-version is a
        string that can be presented to the user.

        The `version` argument should be given the new-version returned
        from the last successful update. new-version is None if we are
        up to date.
        """

        remote_version = self.snarf("version")
        
        self.version, verbose_version = remote_version.split("\n", 1)
        self.version += " " + " ".join(sorted(self.tags))
        
        if self.version == version:
            return None, verbose_version
        else:
            return self.version, verbose_version

    def verify_hash(self, relative, digest):
        """
        Verifies that the file `relative` has the hash value `digest`.
        """

        fn = os.path.join(self.local, relative)
        
        if not os.path.exists(fn):
            return False

        hash = hashlib.sha256()
        
        try:
            f = file(fn, "rb")

            while True:
                data = f.read(1024 * 1024)
                if not data:
                    break
                hash.update(data)

            f.close()
            
        except:
            return False

        return hash.hexdigest() == digest
        
        
    def get_catalog(self):
        """
        Downloads the catalog file from the server, checking the signature
        as necessary.
        """
        
        self.retrieve("catalog1")
        catalog_fn = os.path.join(self.local, "catalog1.new")

        verified = False
        
        try:
            hash = hashlib.sha256()

            f = file(catalog_fn, "rb")

            # Read control information.
            for l in f:
                if l[0] == "-":
                    break

                hash.update(l)
                
                l = l[:-1]

                a = l.split("\t")

                if a[0] == "file":
                    cmd, digest, size, tag, name = a

                    if tag in self.tags:
                        self.files.append((name, digest, int(size)))

                elif a[0] == "dir":
                    cmd, tag, name = a

                    if tag in self.tags:
                        self.directories.append(name)

                elif a[0] == "xbit":
                    cmd, name = a
                    self.xbit.append(name)

                else:
                    raise UpdateException("Unknown upgrade command: %r" % l)

            # Compute the unsigned message.
            unsigned = int("01" + hash.hexdigest(), 16)

            for l in f:
                a = l[:-1].split("\t")

                if a[0] != "signature":
                    continue

                signature = int(a[1], 16)
                if pow(signature, public.exponent, public.modulus) == unsigned:
                    verified = True

            f.close()
            os.unlink(catalog_fn)
                
        except UpdateException:
            raise
        except Exception, e:
            raise UpdateException("Could not download catalog: %r" % (e,))

        if not verified:
            raise UpdateException("Could not verify catalog signature.")

        
    def step(self):
        """
        This is a generator that performs the steps in the update
        process. It yields a (message, complete, total) tuple for
        each step, and terminates upon success.
        """

        yield (u"Retrieving catalog", 0, 1)
        self.get_catalog()

        updated_files = [ ]
        download_size = 0
        
        for i, (name, hash, size) in enumerate(self.files):
            yield (u"Checking files", i, len(self.files))

            if not self.verify_hash(name, hash):
                updated_files.append((name, hash, size))
                download_size += size

        complete_size = 0

        # Todo: Make directories.
        
        for i, dir in enumerate(self.directories):

            yield (u"Making directories.", i, len(self.directories))

            dir = os.path.join(self.local, dir)

            if not os.path.exists(dir):            
                try:
                    os.mkdir(dir)
                except:
                    raise UpdateException("Couldn't make directory %r." % dir)
        
        for name, hash, size in updated_files:

            yield (u"Downloading updated files", complete_size, download_size)
            
            if self.verify_hash(name + ".new", hash):
                complete_size += size
                continue

            self.retrieve(name)

            if not self.verify_hash(name + ".new", hash):
                raise UpdateException("Could not verify download of %r." % name)
            
            complete_size += size

        umask = os.umask(0)
        os.umask(umask)            

        for i, (name, hash, size) in enumerate(updated_files):

            yield (u"Renaming files", i, len(updated_files))
 
            fn = os.path.join(self.local, name)
           
            if os.path.exists(fn):
                os.rename(fn, fn + ".old")

            os.rename(fn + ".new", fn)

        for i, name in enumerate(self.xbit):
            yield (u"Fixing permissions.", i, len(self.xbit))

            fn = os.path.join(self.local, name)
                        
            if os.path.exists(fn):
                os.chmod(fn, 0777 & (~umask))
                          
        
if __name__ == "__main__":
    
    up = Updater("/tmp/renpy-1", "file:///tmp/renpy-6.11.0", [ "base" ])
    version, verbose_version = up.check_version(1)

    for message, done, total in up.step():        
        print message, "(%d/%d)" % (done, total)

    print version
    print verbose_version
    
        
