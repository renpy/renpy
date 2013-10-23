Persistent Data
===============

Ren'Py supports persistent data, saved data that is not
associated with a particular point in a game. Persistent data is
accessed through fields of the persistent object, which is bound to the
variable ``persistent``.

All data reachable through fields on ``persistent`` is saved when
Ren'Py terminates, or when :func:`renpy.save_persistent` is called.
Persistent data is loaded when Ren'Py starts, and when Ren'Py detects
that the persistent data has been updated on disk.

The persistent object is special in that an access to an undefined field will
have a None value, rather than causing an exception.

An example use of persistent is the creation of an unlockable image gallery.
This is done by storing a flag in persistent that determines if the gallery has
been unlocked, as in ::

    label gallery:

        if not persistent.gallery_unlocked:
            show background
            centered "You haven't unlocked this gallery yet."
            $ renpy.full_restart()

        # Actually show the gallery here.

When the user gets an ending that causes the gallery to be unlocked, the flag
must be set to True. ::

    $ persistent.gallery_unlocked = True

As persistent data is loaded before the init code is run, persistent data
should only contain types that are native to python or Ren'Py. Alternatively,
classes that are defined in ``python early`` blocks can be used, provided
those classes can be pickled and implement equality.

Merging Persistent Data
-----------------------

There are cases where Ren'Py has to merge persistent data from two
sources. For example, Ren'Py may need to merge persistent data stored
on a USB drive with persistent data from the local machine.

Ren'Py does this merging on a field-by-field basis, taking the value
of the field that was updated more recently. In some cases, this is
not the desired behavior. In that case, the :func:`renpy.register_persistent`
function can be used.

For example, if we have a set of seen endings, we'd like to take the
union of that set when merging data. ::

    init python:
        if persistent.endings is None:
            persistent.endings = set()

        def merge_endings(old, new, current):
            current.update(old)
            current.update(new)

        renpy.register_persistent('endings', merge_endings)

Persistent Functions
--------------------

.. include:: inc/persistent
