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
    fn = transfn(name)
    if os.path.exists(fn):
        return file(fn, "rb")

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
    return renpy.game.basepath + "/" + name
