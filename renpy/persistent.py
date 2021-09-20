# Copyright 2004-2021 Tom Rothamel <pytom@bishoujo.us>
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

from __future__ import division, absolute_import, with_statement, print_function, unicode_literals
from renpy.compat import *

import os
import copy
import time
import zlib
import weakref
import marshal

import renpy

from renpy.loadsave import dump, dumps, loads

# The class that's used to hold the persistent data.


class Persistent(object):

    def __init__(self):
        self._update()

    def __setstate__(self, data):
        self.__dict__.update(data)

    def __getstate__(self):
        return self.__dict__

    # Undefined attributes return None.
    def __getattr__(self, attr):
        if attr.startswith("__") and attr.endswith("__"):
            raise AttributeError("Persistent object has no attribute %r", attr)

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

    def _update(self, seen_data=None):
        """
        Updates the persistent data to be the latest version of
        the persistent data.
        """

        if seen_data is None:
            seen_data = { }

        if self._preferences is None:
            self._preferences = renpy.preferences.Preferences()

        def dictset_merge(field, default):
            self_f = getattr(self, field)
            seen_f = seen_data.get(field, default)

            if not self_f:
                return seen_f

            self_f.update(seen_f)
            return self_f

        # The set of statements seen ever.
        self._seen_ever = dictset_merge("_seen_ever", { })

        # The set of images seen ever.
        self._seen_images = dictset_merge("_seen_images", { })

        # The set of chosen menu choices.
        self._chosen = dictset_merge("_chosen", { })

        # The set of audio files seen ever.
        self._seen_audio = dictset_merge("_seen_audio", { })

        # The set of seen translate identifiers.
        self._seen_translates = dictset_merge("_seen_translates", set())

        # A map from the name of a field to the time that field was last
        # changed at.
        if self._changed is None:
            self._changed = {
                "_preferences" : 0,
                "_seen_ever" : 0,
                "_chosen" : 0,
                "_seen_audio" : 0,
                "_seen_translates" : 0,
            }


renpy.game.Persistent = Persistent
renpy.game.persistent = Persistent()


def safe_deepcopy(o):
    """
    A "safe" version of deepcopy. If an object doesn't implement __eq__
    correctly, we replace it with its original.

    This tries to ensure we don't constantly find changes in the same
    field.
    """

    rv = copy.deepcopy(o)

    if not (o == rv):

        if renpy.config.developer:
            raise Exception("To be persisted, %r must support equality comparison." % o)
        else:
            rv = o

    return rv


# A map from field names to a backup of the field names in the persistent
# object.
backup = { }


def find_changes():
    """
    This finds changes in the persistent object. When it finds a change, it
    backs up that changed, and puts the current time for that field into
    persistent._changed.

    This returns True if there was at least one change, and False
    otherwise.
    """

    rv = False

    now = time.time()

    persistent = renpy.game.persistent
    pvars = vars(persistent)

    fields = set(backup.keys()) | set(pvars.keys())

    for f in fields:

        if f == "_changed":
            continue

        old = backup.get(f, None)
        new = pvars.get(f, None)

        if not (new == old):

            persistent._changed[f] = now
            backup[f] = safe_deepcopy(new)

            rv = True

    return rv


def load(filename, seen_filename):
    """
    Loads persistence data from `filename` and `seen_filename`.
    Returns None if the data could not be loaded, or a Persistent
    object if it could be loaded.
    """

    if not os.path.exists(filename):
        return None

    # Unserialize the persistent data.
    try:
        with open(filename, "rb") as f:
            s = zlib.decompress(f.read())
        persistent = loads(s)

        seen_data = None
        if os.path.exists(seen_filename):
            with open(seen_filename, "rb") as f:
                s = zlib.decompress(f.read())
            seen_data = marshal.loads(s)

    except:
        import renpy.display

        try:
            renpy.display.log.write("Loading persistent.")
            renpy.display.log.exception()
        except:
            pass

        return None

    persistent._update(seen_data)

    return persistent


def init():
    """
    Loads the persistent data from disk.

    This performs the initial load of persistent data from the local
    disk.
    """

    seen_filename = os.path.join(renpy.config.savedir, "seen")
    for pfn in [ seen_filename + ".new", seen_filename ]:
        if os.path.exists(pfn):
            seen_filename = pfn
            break

    filename = os.path.join(renpy.config.savedir, "persistent.new")
    persistent = load(filename, seen_filename)

    if persistent is None:
        filename = os.path.join(renpy.config.savedir, "persistent")
        persistent = load(filename, seen_filename)

    if persistent is None:
        persistent = Persistent()

    # Create the backup of the persistent data.
    for k, v in vars(persistent).items():
        backup[k] = safe_deepcopy(v)

    return persistent


# A map from field name to merge function.
registry = { }


def register_persistent(field, func):
    """
    :doc: persistent

    Registers a function that is used to merge values of a persistent field
    loaded from disk with values of current persistent object.

    `field`
        The name of a field on the persistent object.

    `function`
        A function that is called with three parameters, `old`, `new`, and
        `current`:

        `old`
            The value of the field in the older object.

        `new`
            The value of the field in the newer object.

        `current`
            The value of the field in the current persistent object. This is
            provided for cases where the identity of the object referred to
            by the field can't change.

        The function is expected to return the new value of the field in the
        persistent object.
    """

    registry[field] = func


def default_merge(old, new, current):
    return new


def dictset_merge(old, new, current):
    current.update(old)
    current.update(new)
    return current


# These fields should only contain types that can be serialised
# by marshal module, and will be saved in a separate 'seen' file.
marshal_fields = [
    "_seen_ever",
    "_seen_images",
    "_seen_audio",
    "_seen_translates",
    "_chosen",
]

register_persistent("_seen_ever", dictset_merge)
register_persistent("_seen_images", dictset_merge)
register_persistent("_seen_audio", dictset_merge)
register_persistent("_seen_translates", dictset_merge)
register_persistent("_chosen", dictset_merge)


def merge(other):
    """
    Merges `other` (which must be a persistent object) into the
    current persistent object.
    """

    now = time.time()

    persistent = renpy.game.persistent

    pvars = vars(persistent)
    ovars = vars(other)

    fields = set(pvars.keys()) | set(ovars.keys())

    for f in fields:
        pval = pvars.get(f, None)
        oval = ovars.get(f, None)

        if pval == oval:
            continue

        ptime = persistent._changed.get(f, 0)

        otime = other._changed.get(f, 0)
        otime = min(now, otime)

        if ptime >= otime:
            new = pval
            old = oval
            t = ptime
        else:
            new = oval
            old = pval
            t = otime

        merge_func = registry.get(f, default_merge)

        val = merge_func(old, new, pval)

        pvars[f] = val
        backup[f] = safe_deepcopy(val)
        persistent._changed[f] = t


# The mtime of the most recently processed savefile.
persistent_mtime = 0


def check_update():
    """
    Checks to see if we need to run update. If we do, runs update and
    restarts the interaction.
    """

    for mtime, _data in renpy.loadsave.location.load_persistent():
        if mtime > persistent_mtime:
            break
    else:
        return

    update()
    renpy.exports.restart_interaction()


def update(force_save=False):
    """
    Loads the persistent data from persistent files that are newer than
    persistent_mtime, and merges it into the persistent object.
    """

    need_save = find_changes()
    need_save = need_save or force_save

    global persistent_mtime

    # A list of (mtime, other) pairs, where other is a persistent file
    # we might want to merge in.
    pairs = renpy.loadsave.location.load_persistent()
    pairs.sort(key=lambda a : a[0])

    # Deals with the case where we don't have any persistent data for
    # some reason.
    mtime = persistent_mtime

    for mtime, other in pairs:

        if mtime <= persistent_mtime:
            continue

        if other is None:
            continue

        merge(other)

    persistent_mtime = mtime

    if need_save:
        save()


should_save_persistent = True


def save():
    """
    Saves the persistent data to disk.
    """

    if not should_save_persistent:
        return

    try:
        seen_fields = dict.fromkeys(marshal_fields)
        persistent = renpy.game.persistent
        for field in seen_fields:
            seen_fields[field] = persistent.__dict__.pop(field)

        data = zlib.compress(dumps(persistent), 3)
        seen_data = zlib.compress(marshal.dumps(seen_fields), 3)
        renpy.loadsave.location.save_persistent(data, seen_data)

    except:
        if renpy.config.developer:
            raise

    finally:
        persistent.__dict__.update(seen_fields)



################################################################################
# MultiPersistent
################################################################################


save_MP_instances = weakref.WeakSet()


def save_MP():
    for ins in save_MP_instances:
        ins.save()


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
        with open(fn + b".new", "wb") as f:
            dump(self, f)

        try:
            os.rename(fn + b".new", fn)
        except:
            os.unlink(fn)
            os.rename(fn + b".new", fn)


def MultiPersistent(name, save_on_quit=False):

    name = renpy.exports.fsencode(name)

    if not renpy.game.context().init_phase:
        raise Exception("MultiPersistent objects must be created during the init phase.")

    if renpy.android or renpy.ios:
        # Due to the security policy of mobile devices, we store MultiPersistent
        # in the same place as common persistent.
        # This is better than not working at all.
        files = [ renpy.config.savedir ]

    elif renpy.windows:
        files = [ os.path.expanduser(b"~/RenPy/Persistent") ]

        if 'APPDATA' in os.environ:
            files.append(os.environ[b'APPDATA'] + b"/RenPy/persistent")

    elif renpy.macintosh:
        files = [ os.path.expanduser(b"~/.renpy/persistent"),
                  os.path.expanduser(b"~/Library/RenPy/persistent") ]
    else:
        files = [ os.path.expanduser(b"~/.renpy/persistent") ]

    if "RENPY_MULTIPERSISTENT" in os.environ:
        files = [ os.environ["RENPY_MULTIPERSISTENT"] ]

    # Make the new persistent directory, why not?
    try:
        os.makedirs(files[-1])
    except:
        pass

    fn = b"" # prevent a warning from happening.
    data = None

    # Find the first file that actually exists. Otherwise, use the last
    # file.
    for fn in files:
        fn = os.path.join(fn, name)
        if os.path.isfile(fn):
            try:
                data = open(fn, "rb").read()
                break
            except:
                pass

    if data is not None:
        try:
            rv = loads(data)
        except:
            data = None
            renpy.display.log.write("Loading MultiPersistent at %r:" % fn)
            renpy.display.log.exception()

    if data is None:
        rv = _MultiPersistent()

    rv._filename = fn # W0201

    if save_on_quit:
        save_MP_instances.add(rv)

    return rv


renpy.loadsave._MultiPersistent = _MultiPersistent
renpy.loadsave.MultiPersistent = MultiPersistent




def compare_oldnew_save():
    script = renpy.game.script
    persistent = renpy.game.persistent
    persistent._seen_ever.update({k: True for k, v in script.namemap.items() if isinstance(v, renpy.ast.Say)})
    persistent._seen_ever.update({k: True for k, v in script.namemap.items() if isinstance(v, renpy.ast.With)})
    persistent._seen_ever.update({k: True for k, v in script.namemap.items() if isinstance(v, renpy.ast.UserStatement) and v.line.startswith(("pause", "call"))})
    persistent._seen_translates.update(script.translator.default_translates)

    times = [ ]
    for reps in range(10):
        start = time.clock()
        save()
        times.append(time.clock() - start)

    times.sort()
    print("New save:")
    print(" ".join("{:.4f}".format(t) for t in times))

    times = [ ]
    for reps in range(10):
        start = time.clock()

        try:
            data = zlib.compress(dumps(persistent), 3)
            renpy.loadsave.location.save_persistent(data, b"")
        except:
            if renpy.config.developer:
                raise
        times.append(time.clock() - start)

    times.sort()
    print("Old save:")
    print(" ".join("{:.4f}".format(t) for t in times))

    save()
