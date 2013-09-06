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
