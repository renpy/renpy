# Copyright 2004-2018 Tom Rothamel <pytom@bishoujo.us>
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

from __future__ import print_function

import os
import copy
import time

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
        f = file(filename, "rb")
        s = f.read().decode("zlib")
        f.close()
        persistent = loads(s)
    except:
        import renpy.display

        try:
            renpy.display.log.write("Loading persistent.")
            renpy.display.log.exception()
        except:
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

    filename = os.path.join(renpy.config.savedir, "persistent.new")
    persistent = load(filename)

    if persistent is None:
        filename = os.path.join(renpy.config.savedir, "persistent")
        persistent = load(filename)

    if persistent is None:
        persistent = Persistent()

    # Create the backup of the persistent data.
    v = vars(persistent)

    for k, v in vars(persistent).iteritems():
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
persistent_mtime = None


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
    pairs.sort()

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
        data = dumps(renpy.game.persistent).encode("zlib")
        renpy.loadsave.location.save_persistent(data)
    except:
        if renpy.config.developer:
            raise


################################################################################
# MultiPersistent
################################################################################


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

    name = renpy.exports.fsencode(name)

    if not renpy.game.context().init_phase:
        raise Exception("MultiPersistent objects must be created during the init phase.")

    if renpy.android:
        files = [ os.path.join(os.environ['ANDROID_OLD_PUBLIC'], '../RenPy/Persistent') ]

    elif renpy.ios:
        raise Exception("MultiPersistent is not supported on iOS.")

    elif renpy.windows:
        files = [ os.path.expanduser("~/RenPy/Persistent") ]

        if 'APPDATA' in os.environ:
            files.append(os.environ['APPDATA'] + "/RenPy/persistent")

    elif renpy.macintosh:
        files = [ os.path.expanduser("~/.renpy/persistent"),
                  os.path.expanduser("~/Library/RenPy/persistent") ]
    else:
        files = [ os.path.expanduser("~/.renpy/persistent") ]

    if "RENPY_MULTIPERSISTENT" in os.environ:
        files = [ os.environ["RENPY_MULTIPERSISTENT"] ]

    # Make the new persistent directory, why not?
    try:
        os.makedirs(files[-1])
    except:
        pass

    fn = ""  # prevent a warning from happening.

    # Find the first file that actually exists. Otherwise, use the last
    # file.
    for fn in files:
        fn = fn + "/" + name
        if os.path.exists(fn):
            break

    try:
        rv = loads(file(fn, "rb").read())
    except:
        rv = _MultiPersistent()

    rv._filename = fn  # W0201
    return rv


renpy.loadsave._MultiPersistent = _MultiPersistent
renpy.loadsave.MultiPersistent = MultiPersistent
