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

As persistent data is loaded before ``init python`` blocks are run, persistent data
should only contain types that are native to Python or Ren'Py. Alternatively,
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
            return current

        renpy.register_persistent('endings', merge_endings)

Persistent Functions
--------------------

.. include:: inc/persistent

Multi-Game Persistence
----------------------

Multi-Game persistence is a feature that lets you share information between
Ren'Py games. This may be useful if you plan to make a series of games, and
want to have them share information.

To use multipersistent data, a MultiPersistent object must be created inside
an ``init`` block. The user can then update this object, and save it to disk by
calling its save method. Undefined fields default to None. To ensure the
object can be loaded again, we suggest not assigning the object instances
of user-defined types.

.. class:: MultiPersistent(key)

    Creates a new ``MultiPersistent`` object. This should only be called inside an
    ``init`` block, and it returns a new ``MultiPersistent`` with the given key.

    `key`
        The key used to to access the multipersistent data. Games using the
        same key will access the same multipersistent data.


    .. method:: save()

        Saves the multipersistent data to disk. This must be called after
        the data is modified.


As an example, take the first part of a two-part game::

    init python:
        mp = MultiPersistent("demo.renpy.org")

    label start:

        # ...

        # Record the fact that the user beat part 1.

        $ mp.beat_part_1 = True
        $ mp.save()

        e "You beat part 1. See you in part 2!"

And the second part::

    init python:
        mp = MultiPersistent("demo.renpy.org")

    label start:

        if mp.beat_part_1:
             e "I see you've beaten part 1, so welcome back!"
        else:
             e "Hmm, you haven't played part 1, why not try it first?"
