# Copyright 2004-2023 Tom Rothamel <pytom@bishoujo.us>
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
from renpy.minstore import _dict, _object

"""renpy
init -1200 python:
"""

class _JSONDBDict(_dict):

    def __init__(self, *args, **kwargs):

        # This is true if the database entry has been changed, in this session.
        # or another session. This is used to determine if it needs to be persisted
        # to the json file.
        self.changed = False

        # This is true if the database entry has been changed in this session.
        # This is used to determine if the json file needs to be changed atall.
        self.dirty = False

        super(_JSONDBDict, self).__init__(*args, **kwargs)

    def check(self, value):
        if not config.developer:
            raise RuntimeError("A JSONDB can only be modified when config.developer is True.")

        import json

        try:
            json.dumps(value)
        except Exception:
            raise TypeError("The data {!r} is not JSON serializable.".format(value))

    def __setitem__(self, key, value):
        self.check(value)

        super(_JSONDBDict, self).__setitem__(key, value)

        self.dirty = True
        self.changed = True

    def __delitem__(self, key):

        super(_JSONDBDict, self).__delitem__(key)

        self.dirty = True
        self.changed = True

    def clear(self):
        super(_JSONDBDict, self).clear()

        self.dirty = True
        self.changed = True

    def setdefault(self, key, default=None):

        if key not in self:
            self.check(default)
            self.dirty = True
            self.changed = True

        return super(_JSONDBDict, self).setdefault(key, default)

    def update(self, *args, **kwargs):

        d = dict()
        d.update(*args, **kwargs)
        self.check(d)

        super(_JSONDBDict, self).update(d)

        self.dirty = True
        self.changed = True

    def __ior__(self, other):
        self.dirty = True
        self.changed = True

        return super(_JSONDBDict, self).__ior__(other)


class JSONDB(_object):
    """
    :doc: jsondb

    A JSONDB is a two-level database that uses JSON to store its data
    It's intended to be used by game developers to store data in a
    database that can be version-controlled as part of the game script.
    For example, this can store information associated with each
    say statement, that can change how a say statement is displayed.

    JSONDBs are not intended for data that is changed through or because
    of the player's actions. :doc:`persistent` or normal save files are
    better choices for that data.

    The database should only contain data that Python can serialize to
    JSON. This includes lists, dictionaries (with strings as keys),
    strings, numbers, True, False, and None. See
    `the Python documentation <https://docs.python.org/3/library/json.html#encoders-and-decoders>`__
    about interoperability, how data converts between the two formats,
    and the various associated pitfalls.

    The two levels of the database are dictionaries both keyed by strings.
    The first level is read only - when a key on the first level dictionary
    is accessed, a second level dictionary is created, optionally with
    default contents. The second level dictionary is read-write, and
    when one of the keys in a second level dictionary is changed,
    that change is saved to the database whe the game exits.

    Like other persistent data, JSONDBs do not participate in rollback.

    A JSONDB should be created during init (in an init python block or
    define statement), and will automatically be saved to the disk provided
    at least one key in the dictionary is set. For example::

        define balloonData = JSONDB("balloon.json", default={ "enabled" : False })

    This creates a JSONDB that is stored in the file balloon.json, and has a
    default values. The second leval values can be used as normal dictionaries::

        screen say(who, what):

            default bd = balloonData[renpy.get_translation_identifier()]

            if bd["enabled"]:
                use balloon_say(who, what)
            else:
                use adv_say(who, what)

            if config.developer:
                textbutton "Dialogue Balloon Mode":
                    action ToggleDict(bd, "enabled")

    The JSONDB constructor takes the following arguments:

    `filename`
        The filename the database is stored in. This is relative to the
        game directory. It's recommended that the filename end in ".json".

    `default`
        If this is not None, it should be a dictionary. When a new second
        level dictionary is created, this object is shallow copied and
        used to initialized the new dictionary. The new dictionary will
        only be saved as part of the database if at least one key in
        it is saved.
    """


    def __init__(self, filename, default=None):

        if not renpy.is_init_phase():
            raise Exception("JSONDBs can only be created during init.")

        # The filename the database is stored in.
        self.fn = filename

        # The data contained in the database.
        self.data = { }

        # True of the database as a whole needs to be saved. There are
        # also dirty flags for each entry, the database is saved if
        # any entry or this flag indicates it is dirty.
        self.dirty = False

        # The default contents of each of the entries of the database.
        if default is not None:
            self.default = default.copy()
        else:
            self.default = { }

        # Schedule the database to be saved when the game quits.
        config.at_exit_callbacks.append(self.save)

        # Load the database.
        import json

        if not renpy.loadable(self.fn):
            return

        with renpy.open_file(self.fn, "utf-8") as f:
            data = json.load(f)

        for k, v in data.items():
            d = _JSONDBDict(v)

            d.dirty = False
            d.changed = True

            self.data[k] = d

    def save(self):

        if not(self.dirty or any(i.dirty for i in self.data.values())):
            return

        d = { k : v for k, v in self.data.items() if v.changed }

        import os, json

        fn = os.path.join(config.gamedir, self.fn)

        with open(fn + ".new", "w") as f:
            json.dump(d, f, indent=4, sort_keys=True)

        try:
            os.rename(fn + ".new", fn)
        except Exception:
            os.remove(fn)
            os.rename(fn + ".new", fn)

    def __getitem__(self, key):

        if key not in self.data:
            self.data[key] = _JSONDBDict(self.default.copy())

        return self.data[key]

    def __delitem__(self, key):
        del self.data[key]

        self.dirty = True

    def __setitem__(self, key, value):
        raise Exception("The keys of a jsondb may not be set directly.")

    def __iter__(self):
        return iter(self.data)

    def __reversed__(self):
        return reversed(self.data)

    def values(self):
        return self.data.values()

    def keys(self):
        return self.data.keys()

    def items(self):
        return self.data.items()

    def __len__(self):
        return len(self.data)

    @property
    def dialogue(self):
        return self[renpy.get_translation_identifier()]
