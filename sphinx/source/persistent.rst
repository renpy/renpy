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
have a None value, rather than causing an exception. If something other than
None is to be the default of a persistent value,
the :ref:`default <default-statement>` statement should be used::

    default persistent.main_background = "princess_not_saved"

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

Fields starting with two underscores (``__``) are supported, but will receive the
name-mangling effect described in :ref:`this section <elements-of-statements>`,
which means they will be specific to the file they're defined in. This implies that
if the file is renamed between two releases, access to the value that field had in
the previous release will be broken.

In addition to this, these fields are not affected by the :meth:`persistent._clear`
method.

As a reminder, fields starting with a single underscore ``_`` are reserved and
should not be used.

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

.. function:: persistent._hasattr(field_name)

    Tests whether the `field_name` persistent field has been set or not.
    This allows you to distinguish fields that have been explicitly set
    to None from fields that have never been set.

.. function:: persistent._clear(progress=False)

    Resets the persistent data, except for fields starting with ``__``.

    `progress`
        If true, also resets progress data that Ren'Py keeps.

    Note that this will re-apply defaults.

.. include:: inc/persistent

Multi-Game Persistence
----------------------

Multi-Game persistence is a feature that lets you share information between
Ren'Py games. This may be useful if you plan to make a series of games, and
want to have them share information.

To use multipersistent data, a MultiPersistent object must be created at init
time (preferably using ``define``).
The user can then update this object, and save it to disk by
calling its save method. Undefined fields default to None. To ensure the
object can be loaded again in a different game, we strongly advise against
storing instances of user-defined types in the object.

.. class:: MultiPersistent(key, save_on_quit=False)

    Creates a new ``MultiPersistent`` object. This should only be called at init time,
    and it returns a new ``MultiPersistent`` with the given key.

    `key`
        The key used to to access the multipersistent data. Games using the
        same key will access the same multipersistent data.

    `save_on_quit`
        If it is True, this object will be automatically saved when Ren'Py terminates.

    .. method:: save()

        Saves the multipersistent data to disk. This must be called after
        the data is modified.


As an example, take the first part of a two-part game::

    define mp = MultiPersistent("demo.renpy.org")

    label start:

        # ...

        # Record the fact that the user beat part 1.

        $ mp.beat_part_1 = True
        $ mp.save()

        e "You beat part 1. See you in part 2!"

And the second part::

    define mp = MultiPersistent("demo.renpy.org")

    label start:

        if mp.beat_part_1:
            e "I see you've beaten part 1, so welcome back!"
        else:
            e "Hmm, you haven't played part 1, why not try it first?"
