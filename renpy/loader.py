import renpy
import os
import os.path
from pickle import loads
from cStringIO import StringIO

archives = [ ]

def index_archives():
    """
    Loads in the indexes for the archive files.
    """

    global archives
    archives = [ ]

    for prefix in renpy.config.archives:

        fn = transfn(prefix + ".rpa")

        try:
            fn = transfn(prefix + ".rpa")
            f = file(fn, "rb")
            l = f.readline()

            # 2.0 Branch.
            if l.startswith("RPA-2.0 "):
                offset = int(l[8:], 16)
                f.seek(offset)
                index = loads(f.read().decode("zlib"))
                archives.append((prefix, index))
                f.close()
                continue

            # 1.0 Branch.
        
            f.close()
            
            fn = transfn(prefix + ".rpi")
            index = loads(file(fn, "rb").read().decode("zlib")) 
            archives.append((prefix, index))
        except:
            if renpy.config.debug:
                raise
            

def listdirfiles():
    """
    Returns a list of directory, file tuples known to the system. If
    the file is in an archive, the directory is None.
    """

    rv = [ ]

    for i in renpy.config.searchpath:
        for j in os.listdir(i):
            rv.append((i, j))

    for prefix, index in archives:
        for j in index.iterkeys():
            rv.append((None, j))

    return rv
    

def load(name):
    """
    Returns an open python file object of the given type.
    """

    # Look for the file directly.
    if not renpy.config.force_archives:

        try:
            fn = transfn(name)
            return file(fn, "rb")
        except:
            pass

    # Look for it in archive files.
    for prefix, index in archives:
        if not name in index:
            continue

        f = file(transfn(prefix + ".rpa"), "rb")

        data = [ ]

        for offset, dlen in index[name]:           
            f.seek(offset)
            data.append(f.read(dlen))

        rv = StringIO(''.join(data))
        f.close()

        return rv

    raise Exception("Couldn't find file '%s'." % name)

def loadable(name):
    """
    Returns True if the name is loadable with load, False if it is not.
    """

    try:
        transfn(name)
        return True
    except:
        pass

    for prefix, index in archives:
        if name in index:
            return True

    return False
    

def transfn(name):
    """
    Tries to translate the name to a file that exists in one of the
    searched directories.
    """

    for d in renpy.config.searchpath:
        if os.path.exists(d + "/" + name):
            return d + "/" + name

    raise Exception("Couldn't find file '%s'." % name)
