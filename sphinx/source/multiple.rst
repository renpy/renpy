.. _multiple-dialogue:

Multiple Character Dialogue
===========================

Ren'Py supports displaying dialogue from multiple characters simultaneously.
Multiple dialogue is invoked by giving the lines of dialogue the multiple
argument. For example::

    e "Ren'Py supports displaying multiple lines of dialogue simultaneously." (multiple=2)
    l "About bloody time! I've been waiting for this for years." (multiple=2)

Multiple dialogue is invoked by passing a line of dialogue the `multiple` argument
with the number of lines of dialogue to combine together. (So if we had multiple=3,
three blocks of dialogue would be combined.)

Multiple dialogue works by showing the say screen more than once, with
different styles. Each say screen is responsible for showing dialogue from
a single character.

There are a few restrictions on multiple dialogue:

* When displaying multiple dialogue, text tags that cause the text to pause,
  like {p} and {w}, will not function properly. This is because each screen is
  only displayed once, and those tags require screens to be displayed multiple
  times to function.

* Auto-forward mode only works on the last block of text. While this should be
  fine in most cases, it can lead to problems if the last block of text is
  shorter than the rest, as auto-forward may engage early.

* Extend will not work. (It will only apply to the last block of text.)

Styles
------

Generally, the way multiple dialogue works is to display the say screen
multiple times, with the styles of various displayables systematically
renamed to reflect the block number and the number of blocks in total.

Specifically, multiple dialogue uses styles with names of the form
block`n`_multiple`m`_\`style`, where `n` is the one-based number of
the block, and `m` is the number of blocks of dialogue being
displayed at once.

In our example above, the window corresponding to each block of dialogue
are given the names:

* block1_multiple2_window
* block2_multiple2_window

This naming scheme is used for the dialogue, name, and namebox, as well
as the window. It's designed so style inheritance is useful here. For
the window styles we'll have:

window
    Used for the normal case of a single dialogue window, this can serve as
    a base for all dialogue windows.

multiple2_window
    This can be used for properties common to the two dialogue windows,
    like changing the background and reducing the margin and padding.

block1_multiple2_window
    This could be used to position the first of the two dialogue windows,
    such as using xalign 0.0 to put it on the left side.

block2_multiple2_window
    Similarly, this can be used to position the second window, with
    xalign 1.0 putting it on the right side.

The Multiple Say Screen
-----------------------

For more control, there is the multiple say screen. When it exists, the
multiple say screen is used in place of the normal say screen. It takes
a third argument, `multiple`, which is a tuple. The first component of
the tuple is the block number, and the second is the total number of
screens.


NVL-Mode
--------

By default, NVL-Mode displays multiple text blocks one on top of another.
This can be customized by changing the :ref:`nvl screen <nvl-screen>`, which is passed
a list of objects with the multiple argument that can be reorganized and presented.
