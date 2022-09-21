# Copyright 2004-2022 Tom Rothamel <pytom@bishoujo.us>
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

import renpy.config as config
import renpy.exports as renpy

"""renpy
init python:
"""

class JSONDB(object):

    def __init__(self, fn, key=None):

        if not renpy.is_init_phase():
            raise Exception("JSONDBs can only be created during init.")

        # The filename the database is stored in.
        self.fn = fn

        # The data contained in the database.
        self.data = { }

        # True if an data has been changed after the databse was loaded.
        self.dirty = False

        # Either a key function to use to index the database, or None to
        # use the standard key of 'data'.
        self.key = key

        # Schedule the database to be saved when the game quits.
        config.at_exit_callbacks.append(self.save)

        # Load the database.
        import json

        if not renpy.loadable(self.fn):
            return

        with renpy.open_file(self.fn, "utf-8") as f:
            self.data = json.load(f)

    def save(self):

        if not self.dirty:
            return

        import os, json

        fn = os.path.join(config.gamedir, self.fn)

        with open(fn + ".new", "w") as f:
            json.dump(self.data, f, indent=4, sort_keys=True)

        try:
            os.rename(fn + ".new", fn)
        except Exception:
            os.remove(fn)
            os.rename(fn + ".new", fn)

        self.dirty = False

    def check(self, value):
        if not config.developer:
            raise RuntimeError("A JSONDB can only be modified when config.developer is True.")

        import json

        try:
            json.dumps(value)
        except:
            raise TypeError("The data {!r} is not JSON serializable.".format(value))

    def get_dict(self):
        if self.key is not None:
            key = self.key()
        else:
            key = 'data'

        if key not in self.data:
            self.data[key] = { }

        return self.data[key]

    def __iter__(self):
        return iter(self.get_dict())

    def __len__(self):
        return len(self.get_dict())

    def __getitem__(self, key):
        return self.get_dict()[key]

    def __setitem__(self, key, value):
        self.check(value)
        self.get_dict()[key] = value
        self.dirty = True

    def __delitem__(self, key):
        self.dirty = True
        del self.get_dict()[key]

    def __contains__(self, key):
        return key in self.get_dict()

    def clear(self):
        self.dirty = True
        self.get_dict().clear()

    def copy(self):
        return self.get_dict().copy()

    def has_key(self, key):
        return key in self.get_dict()

    def get(self, key, default=None):
        return self.get_dict().get(key, default)

    def items(self):
        return self.get_dict().items()

    def keys(self):
        return self.get_dict().keys()

    def pop(self, key, default=None):
        self.dirty = True
        return self.get_dict().pop(key, default)

    def popitem(self):
        self.dirty = True
        return self.get_dict().popitem()

    def reversed(self):
        return self.get_dict().reversed()

    def setdefault(self, key, default=None):

        d = self.get_dict()
        if key not in d:
            self.check(default)
            self.dirty = True

        return d.setdefault(key, default)

    def update(self, *args, **kwargs):
        self.dirty = True

        d = dict()
        d.update(*args, **kwargs)
        self.check(d)

        self.get_dict().update(d)

    def values(self):
        return self.get_dict().values()

    def __ior__(self, other):
        self.dirty = True
        self.get_dict().update(other)
        return self

    def __eq__(self, other):
        return self.get_dict() == other

    def __ne__(self, other):
        return self.get_dict() != other

    def __le__(self, other):
        return self.get_dict() <= other

    def __lt__(self, other):
        return self.get_dict() < other

    def __ge__(self, other):
        return self.get_dict() >= other

    def __gt__(self, other):
        return self.get_dict() > other

    def __repr__(self):
        d = self.get_dict()
        return "<JSONDB {!r} {!r}>".format(self.fn, d)

    def __reversed__(self):
        return reversed(self.get_dict())
