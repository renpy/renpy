import renpy
import os.path
from cPickle import loads
from cStringIO import StringIO

archives = [ ]

def index_archives():
    """
    Loads in the indexes for the archive files.
    """

    global archives
    archives = [ ]

    for prefix in renpy.config.archives:
        fn = transfn(prefix + ".rpi")
        index = loads(file(fn, "rb").read().decode("zlib")) 

        print index.keys()

        archives.append((prefix, index))

def load(name):
    """
    Returns an open python file object of the given type.
    """

    # Look for the file directly.
    try:
        fn = transfn(name)
        return file(fn, "rb")
    except:
        pass

    # Look for it in archive files.
    for prefix, index in archives:
        if not name in index:
            continue

        offset, dlen = index[name]

        f = file(transfn(prefix + ".rpa"), "rb")
        f.seek(offset)
        rv = StringIO(f.read(dlen))
        f.close()

        return rv

    raise Exception("Couldn't find file '%s'." % name)

def transfn(name):
    """
    Tries to translate the name to a file that exists in one of the
    searched directories.
    """

    for d in renpy.game.searchpath:
        if os.path.exists(d + "/" + name):
            return d + "/" + name

    raise Exception("Couldn't find file '%s'." % name)
