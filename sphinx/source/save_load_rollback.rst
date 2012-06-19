=============================
Saving, Loading, and Rollback
=============================

Ren'Py has support for saving game state, loading game state, and rolling
back to a previous game state. Although implemented in a slightly different
fashion, rollback can be thought of as saving the game at the start of each
statement that interacts with the user, and loading saves when the user
rolls back.


.. note::

  While we usually attempt to keep save compatibility between releases, this
  compatibility is not guaranteed. We may decide to break save-compatibility
  if doing so provides a sufficiently large benefit.

What is Saved
=============

Ren'Py attempts to save the game state. This includes both internal state
and python state.

The internal state consists of all aspects of Ren'Py that are intented to
change once the game has started, and includes:

* The current statement, and all statements that can be returned to.
* The images and displayables that are being shown.
* The screens being shown, and the values of variables within those
  screens.
* The music that Ren'Py is playing.
* The list of nvl-mode text blocks.

The python state consists of the variables in the store that have changed since
the game began, and all objects reachable from those variables. Note that it's
the change to the variables that matters - changes to fields in objects will
not cause those objects to be saved.

In this example::

    define a = 1
    define o = object()
    
    label start:
         $ b = 1
         $ o.value = 42
         
only `b` will be saved. A will not be saved because it does not change once
the game begins. `O` is not saved because it does not change - the object it
refers to changes, but the variable itself does not.


What isn't Saved
================

Python variables that are not changed before the game begins will not be
saved. This can be a major problem if a variable that is saved and one that is
refer to the same object. (Alias the object.) In this example::

    init python:
        a = object()
        a.f = 1
        
    label start:
        $ b = a
        $ b.f = 2
        
        "a.f=[a.f] b.f=[b.f]"

`a` and `b` are aliased. Saving and loading may break this aliasing, causing
`a` and `b` to refer to different objects. Since this can be very confusing,
it's best to avoid aliasing saved and unsaved variables. (This is rare to
encounter directly, but might come up when an unsaved variable and saved field
alias.)

There are several other kinds of state that isn't saved:

control flow path
    Ren'Py only saves the current statement, and the statement it needs
    to return to. It doesn't remember how it got there. Importantly, if
    code (like variable assignments) is added to the game, it won't run.

mappings of image names to displayables
    Since this mapping is not saved, the image may change to a new image
    when the game loads again. This allows an image to change to a new
    file as the game evolves.

configuration variables, styles, and style properties
    Configuration variables and styles aren't saved as part of the game.
    Therefore, they should only be changed in init blocks, and left alone
    once the game has started.


Where Ren'Py Saves
==================

Saves occur at the start of a Ren'Py statement in the outermost interaction
context.

What's important here is to note that saving occurs at the **start** of a
statement. If a load or rollback occurs in the middle of a statement that
interacts multiple times, the state will be the state that was active
when the statement began.

This can be a problem in python-defined statements. In code like::

    python:
         i = 0
         while i < 10:
              i += 1
              narrator("The count is now [i].")

if the user saves and loads in the middle, the loop will begin anew. Using
similar code in Ren'Py - rather than Python - avoids this problem.::

   $ i = 0
   while i < 10:
        $ i += 1
        "The count is now [i]."


What Ren'Py can Save
====================

Ren'Py uses the python pickle system to save game state. This module can
save:

* Basic types, such as True, False, None, int, str, float, complex, str, and unicode objects.
* Compound types, like lists, tuples, sets, and dicts.
* Creator-defined objects, classes, functions, methods, and bound methods. For
  pickling these functions to succeed, they must remain available under their
  original names.
* Character, Displayable, Transform, and Transition objects.

There are certain types that cannot be pickled:

* Render objects.
* Iterator objects.
* File-like objects.
* Inner functions and lambdas.

By default, Ren'Py uses the cPickle module to save the game. Setting
:var:`config.use_cpickle` will make Ren'Py use the pickle module instead. This
makes the game slower, but is better at reporting save errors.


Save Functions and Variables
============================

There is one variable that is used by the high-level save system:

.. var:: save_name = ...

   This is a string that is stored with each save. It can be used to give 
   a name to the save, to help users tell them apart.
   
There are a number of high-level save actions and functions defined in the
:ref:`screen actions <screen-actions>`. In addition, there are the following
low-level save and load actions.


.. include:: inc/loadsave


Supporting Rollback and Roll Forward
====================================

Most Ren'Py statements automatically support rollback and roll forward. If
you call :func:`ui.interact` directly, you'll need to add support for rollback
and roll-forward yourself. This can be done using the following structure::


    # This is None if we're not rolling back, or else the value that was 
    # passed to checkpoint last time if we're rolling forward.
    roll_forward = renpy.roll_forward_info()

    # Set up the screen here...
    
    # Interact with the user.
    rv = ui.interact(roll_forward=roll_forward)

    # Store the result of the interaction.
    renpy.checkpoint(rv)
    
It's important that your game does not interact with the user after renpy.checkpoint
has been called. (If you do, the user may not be able to rollback.)

.. include:: inc/rollback

Blocking Rollback
=================

.. warning:: 

    Blocking rollback is a very user-unfriendly thing to do. If a user mistakenly
    clicks on an unintended choice, he or she will be unable to correct their
    mistake. Since rollback is equivalent to saving and loading, your users 
    will be forced to save more often, breaking game engagement.
    
    Blocking rollback to force users to view bad endings often reflects a
    mistake in game design. Instead, we recommend making bad endings engaging
    enough that users want to view them.

Rollback can be disabled on a global basis by setting :var:`config.rollback_enabled`
to false.

The following functions can be used to block or restrict rollback:

.. include:: inc/blockrollback



