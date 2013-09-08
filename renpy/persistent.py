# Copyright 2004-2013 Tom Rothamel <pytom@bishoujo.us>
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

import os
import renpy

from renpy.loadsave import dump, loads
from cPickle import dumps


# The class that's used to hold the persistent data.
class Persistent(object):

    def __setstate__(self, data):
        vars(self).update(data)

    def __getstate__(self):
        return vars(self)

    # Undefined attributes return None.
    def __getattr__(self, attr):
        return None

    def _clear(self, progress=False):
        """
        Resets the persistent data.

        `progress`
            If true, also resets progress data that Ren'Py keeps.
        """


        keys = list(self.__dict__)

        for i in keys:
            if i[0] == "_":
                continue

            del self.__dict__[i]

        if progress:
            self._seen_ever.clear()
            self._seen_images.clear()
            self._chosen.clear()
            self._seen_audio.clear()







def load_persistent():
    """
    Loads the persistent data from disk.
    """

    # Unserialize the persistent data.
    try:
        f = file(renpy.config.savedir + "/persistent", "rb")
        s = f.read().decode("zlib")
        f.close()
        persistent = loads(s)
    except:
        persistent = Persistent()

    update_persistent(persistent)
    return persistent

def update_persistent(persistent):

    # Initialize the set of statements seen ever.
    if not persistent._seen_ever:
        persistent._seen_ever = { }

    renpy.game.seen_ever = persistent._seen_ever

    # Initialize the set of images seen ever.
    if not persistent._seen_images:
        persistent._seen_images = { }

    # Initialize the set of chosen menu choices.
    if not persistent._chosen:
        persistent._chosen = { }

    if not persistent._seen_audio:
        persistent._seen_audio = { }

def save_persistent():
    """
    Saves the persistent data to disk.
    """

    try:
        f = file(renpy.config.savedir + "/persistent", "wb")
        f.write(dumps(renpy.game.persistent).encode("zlib"))
        f.close()
    except:
        if renpy.config.debug:
            raise

renpy.game.persistent = Persistent()

class _MultiPersistent(object):

    def __getstate__(self):
        state = self.__dict__.copy()
        del state['_filename']
        return state

    def __setstate__(self, state):
        self.__dict__.update(state)

    def __getattr__(self, name):

        if name.startswith("__") and name.endswith("__"):
            raise AttributeError()

        return None

    def save(self):

        fn = self._filename
        f = file(fn + ".new", "wb")
        dump(self, f)
        f.close()

        try:
            os.rename(fn + ".new", fn)
        except:
            os.unlink(fn)
            os.rename(fn + ".new", fn)


def MultiPersistent(name):

    if not renpy.game.context().init_phase:
        raise Exception("MultiPersistent objects must be created during the init phase.")

    if renpy.windows:
        files = [ os.path.expanduser("~/RenPy/Persistent") ]

        if 'APPDATA' in os.environ:
            files.append(os.environ['APPDATA'] + "/RenPy/persistent")

    elif renpy.macintosh:
        files = [ os.path.expanduser("~/.renpy/persistent"),
                  os.path.expanduser("~/Library/RenPy/persistent") ]
    else:
        files = [ os.path.expanduser("~/.renpy/persistent") ]

    # Make the new persistent directory, why not?
    try:
        os.makedirs(files[-1])
    except:
        pass

    fn = "" # prevent a warning from happening.

    # Find the first file that actually exists. Otherwise, use the last
    # file.
    for fn in files:
        fn = fn + "/" + name
        if os.path.exists(fn):
            break

    try:
        rv = loads(file(fn).read())
    except:
        rv = _MultiPersistent()

    rv._filename = fn # W0201
    return rv

renpy.loadsave._MultiPersistent = _MultiPersistent
renpy.loadsave.MultiPersistent = MultiPersistent
