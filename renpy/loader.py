import renpy
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

        try:
            fn = transfn(prefix + ".rpi")
            index = loads(file(fn, "rb").read().decode("zlib")) 
            archives.append((prefix, index))
        except:
            if renpy.config.debug:
                raise

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

def transfn(name):
    """
    Tries to translate the name to a file that exists in one of the
    searched directories.
    """

    for d in renpy.config.searchpath:
        if os.path.exists(d + "/" + name):
            return d + "/" + name

    raise Exception("Couldn't find file '%s'." % name)
