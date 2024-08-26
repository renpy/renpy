# Copyright 2004-2024 Tom Rothamel <pytom@bishoujo.us>
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
from renpy.compat import PY2, basestring, bchr, bord, chr, open, pystr, range, round, str, tobytes, unicode # *



import os
import copy
import time
import zlib
import weakref

import renpy

from renpy.compat.pickle import dump, dumps, loads

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
            raise AttributeError("Persistent object has no attribute %r" % attr)

        return None

    def _hasattr(self, field_name):
        return field_name in self.__dict__

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

        renpy.exports.execute_default_statement()

    def _update(self):
        """
        Updates the persistent data to be the latest version of
        the persistent data.
        """

        if self._preferences is None:
            self._preferences = renpy.preferences.Preferences()

        # Initialize the set of statements seen ever.
        if not self._seen_ever:
            self._seen_ever = { }

        # Initialize the set of images seen ever.
        if not self._seen_images:
            self._seen_images = { }

        # Initialize the set of chosen menu choices.
        if not self._chosen:
            self._chosen = { }

        if not self._seen_audio:
            self._seen_audio = { }

        self._seen_audio = { str(i) : True for i in self._seen_audio }

        # The set of seen translate identifiers.
        if not self._seen_translates:
            self._seen_translates = set()

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


renpy.game.Persistent = Persistent # type: ignore
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

            persistent._changed[f] = now # type: ignore
            backup[f] = safe_deepcopy(new)

            rv = True

    return rv


def load(filename):
    """
    Loads persistence data from `filename`. Returns None if the data
    could not be loaded, or a Persistent object if it could be
    loaded.
    """

    if not os.path.exists(filename):
        return None

    # Unserialize the persistent data.
    try:
        with open(filename, "rb") as f:
            do = zlib.decompressobj()
            s = do.decompress(f.read())

            if not renpy.savetoken.check_persistent(s, do.unused_data.decode("utf-8")):
                return None

        persistent = loads(s)

    except Exception:
        try:
            renpy.display.log.write("Loading persistent.")
            renpy.display.log.exception()
        except Exception:
            pass

        return None

    persistent._update()

    return persistent


def init():
    """
    Loads the persistent data from disk.

    This performs the initial load of persistent data from the local
    disk, so that we can configure the savelocation system.
    """

    if renpy.config.early_developer and not PY2:
        init_debug_pickler()

    filename = os.path.join(renpy.config.savedir, "persistent.new") # type: ignore
    persistent = load(filename)

    if persistent is None:
        filename = os.path.join(renpy.config.savedir, "persistent") # type: ignore
        persistent = load(filename)

    if persistent is None:
        persistent = Persistent()

    # Create the backup of the persistent data.
    for k, v in persistent.__dict__.items():
        backup[k] = safe_deepcopy(v)

    return persistent


def init_debug_pickler():
    import io, pickle

    safe_types = set()

    for d in renpy.python.store_dicts.values():
        for v in d.values():
            if isinstance(v, type):
                safe_types.add(v)

    class DebugPickler(pickle.Pickler):
        def reducer_override(self, obj):
            t = obj if isinstance(obj, type) else type(obj)

            if t not in safe_types and t.__module__.startswith("store"):
                cls = (t.__module__ + '.' + t.__qualname__)[6:]
                raise TypeError("{} is not safe for use in persistent.".format(cls))

            return NotImplemented # lets normal reducing take place

    global dumps

    def dumps(o):
        b = io.BytesIO()
        DebugPickler(b, renpy.compat.pickle.PROTOCOL).dump(o)
        return b.getvalue()


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


register_persistent("_seen_ever", dictset_merge)
register_persistent("_seen_images", dictset_merge)
register_persistent("_seen_audio", dictset_merge)
register_persistent("_chosen", dictset_merge)


def merge(other):
    """
    Merges `other` (which must be a persistent object) into the
    current persistent object.
    """

    now = time.time()

    persistent = renpy.game.persistent

    pvars = persistent.__dict__
    ovars = other.__dict__

    fields = set(pvars.keys()) | set(ovars.keys())

    for f in fields:
        pval = pvars.get(f, None)
        oval = ovars.get(f, None)

        if pval == oval:
            continue

        ptime = persistent._changed.get(f, 0) # type: ignore

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
        persistent._changed[f] = t # type: ignore


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

    global old_persistent_data

    if not renpy.config.save_persistent:
        return

    if not should_save_persistent:
        return

    try:
        data = dumps(renpy.game.persistent)
        compressed = zlib.compress(data, 3)
        compressed += renpy.savetoken.sign_data(data).encode("utf-8")
        renpy.loadsave.location.save_persistent(compressed)
    except Exception:
        if renpy.config.developer:
            raise

    global persistent_mtime

    # Prevent updates just after save
    for mtime, _data in renpy.loadsave.location.load_persistent():
        persistent_mtime = max(persistent_mtime, mtime)



################################################################################
# MultiPersistent
################################################################################

# `_MultiPersistent` instances from `MultiPersistent` calls.
MP_instances = weakref.WeakSet()


def save_MP():
    """
    Called `save` for each `_MultiPersistent` instance.
    """
    for instance in MP_instances:
        instance.save()


def save_on_quit_MP():
    """
    Called `save` for each `_MultiPersistent` instance to be saved on exit.
    """
    for instance in MP_instances:
        if instance._save_on_quit:
            instance.save()


def get_MP(name):
    """
    Returns `_MultiPersistent` instance if exists.
    """
    for instance in MP_instances:
        if instance._name == name:
            return instance

class _MultiPersistent(object):

    _filename = ""
    _name = ""
    _save_on_quit = False

    def __getstate__(self):
        state = self.__dict__.copy()
        del state['_filename']
        del state['_name']
        del state['_save_on_quit']
        return state

    def __setstate__(self, state):
        self.__dict__.update(state)

    def __getattr__(self, name):
        if name.startswith("__") and name.endswith("__"):
            raise AttributeError()

        return None

    def save(self):
        try:
            fn = self._filename
            with open(fn + ".new", "wb") as f:
                dump(self, f)
        except OSError as e:
            if renpy.config.developer:
                raise e
        else:
            try:
                os.rename(fn + ".new", fn)
            except Exception:
                os.unlink(fn)
                os.rename(fn + ".new", fn)


def MultiPersistent(name, save_on_quit=False):
    """
    Returns `_MultiPersistent` object.
    """

    if not renpy.game.context().init_phase:
        raise Exception("MultiPersistent objects must be created during the init phase.")

    name = renpy.exports.fsdecode(name)
    rv = get_MP(name)
    if rv is not None:
        return rv

    if "RENPY_MULTIPERSISTENT" in os.environ:
        files = [ renpy.exports.fsdecode(os.environ["RENPY_MULTIPERSISTENT"]) ]

    elif renpy.android or renpy.ios:
        # Due to the security policy of mobile devices, we store MultiPersistent
        # in the same place as common persistent.
        # This is better than not working at all.
        files = [ renpy.config.savedir ]

    elif renpy.windows:
        files = [ os.path.expanduser("~/RenPy/Persistent") ]

        if 'APPDATA' in os.environ:
            files.append(
                os.path.join(
                    renpy.exports.fsdecode(os.environ['APPDATA']), "RenPy", "persistent"
                )
            )

    elif renpy.macintosh:
        files = [ os.path.expanduser("~/.renpy/persistent"),
                  os.path.expanduser("~/Library/RenPy/persistent") ]
    else:
        files = [ os.path.expanduser("~/.renpy/persistent") ]

    # Make the new persistent directory, why not?
    try:
        os.makedirs(files[-1]) # type: ignore
    except Exception:
        pass

    data = None

    # Find the first file that actually exists. Otherwise, use the last
    # file.
    for fn in files:
        fn = os.path.join(fn, name) # type: ignore
        if os.path.isfile(fn):
            try:
                with open(fn, "rb") as mpf:
                    data = mpf.read()
                break
            except Exception:
                pass

    rv = _MultiPersistent()

    if data is not None:
        try:
            rv = loads(data)
        except Exception:
            renpy.display.log.write("Loading MultiPersistent at %r:" % fn) # type: ignore
            renpy.display.log.exception()

    rv._filename = fn # type: ignore
    rv._name = name
    rv._save_on_quit = save_on_quit

    MP_instances.add(rv)

    return rv


renpy.loadsave._MultiPersistent = _MultiPersistent # type: ignore
renpy.loadsave.MultiPersistent = MultiPersistent # type: ignore
