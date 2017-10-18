Incompatible Changes
====================

This is a list of changes that may require intervention in the form of
changes to scripts or your development environment. Our intent is that
all other changes should not affect existing scripts.

Note that setting :var:`config.script_version` will cause many of
these changes to be reverted, at the cost of losing access to recent
features.

Incompatible changes to the GUI are documented at :ref:`gui-changes`, as
such changes only take effect when the gui is regenerated.

.. _incompatible-6.99:

6.99.13
-------

The size of a hyperlink is now inherited from the size of the enclosing text.
To disable this, add::

    define config.hyperlink_inherit_size = False

The {nw} test tag now waits until voice and self-voicing are finished before
it continues.  To disable this behavior, add::

    define config.nw_voice = False

ATL Transforms now show at least one frame whenever a pause or interpolation
occurs. When a game doesn't expect this, it can show up as a series of
rapidly displayed singe fames. This can be disabled with::

    define config.atl_one_frame = False

The show layer at statement now persists the state of a transform like
any other ATL transform. This can lead to a behavior change in which,
for example, an offset persists between multiple show layer at
statements. To disable this, write::

    define config.keep_show_layer_state = False

While not an incompatible change, :func:`renpy.list_files` has been
changed to sort its output in a  standard order. The causes Ren'Py
to commit to behavior that had been ambiguous. For example, when
multiple files in the images directory had the same name, Ren'Py
would pick one at random. (The file picked could change from
system to system.) Now, the same file  is chosen wherever Ren'Py
is run.


6.99.12.3
---------

Ren'Py will no longer search for system-installed fonts when in developer
mode. If you game was using a system installed font, the font file should
be copied into the game/ directory. (But please make sure that this is
compatible with the font file's license.)


6.99.11
-------

The order of exection of ``style`` and ``translate`` statements has
changed, as documented in :ref:`the changelog <renpy-6.99.11>`. To
revent this change, add the code::

    define config.new_translate_order = False

Note that reverting this change may prevent the new GUI from working.


The :var:`config.quit_action` variable has changed it's default to one
that cause the quit prompt to be displayed of the in-game context. To
revert to the old behavior, add the code::

    define config.quit_action = ui.gamemenus("_quit_prompt")


Ren'Py now enforces maximum sizes given to buttons and windows. To disable
this behavior, add the code::

    define config.enforce_window_max_size = False



6.99.9
------

Ren'Py now plays interface sounds on a channel named "audio", that
supports multiple sound playback at once. This channel might not have
the same settings as a customized sound channel. The audio channel
settings can be changed by adjusting :var:`config.auto_channels`,
or the sound channel can be used by adding the code::

    define config.play_channel = "sound"


6.99.2
------

Ren'Py will now scan the an image directory (the directory named images
underneath the game directory) for images, and define them based on their
filename. To disable this behavior, use the code::

    init python:
        config.image_directory = None


.. _incompatible-6.18:

6.18
----

The ``show screen`` and ``call screen`` statements may now evaluate their
arguments as part of the screen prediction process. If evaluating the
arguments to a screen causes side effects to occur, the ``show screen``
or ``call screen`` statements should be given the new ``nopredict``
clause, which prevents prediction.

Screens now participate in transitions - transitions now go from the old
state of the screen to the new state. To disable this, set
:var:`config.transition_screens` to false.

Ren'Py no longer uses structural equality to transfer state (for example,
the state of a transform) when a screen replaces a screen with the same
tag. Instead, the :ref:`use statement <sl-use>` now supports an ``id``
property, which can be used to explicitly transfer state.

.. _incompatible-6.16:

6.16
----

The meaning of the `loop` parameter to :func:`MusicRoom` has changed. To
get the old behavior, set both `loop` and `single_track` to true.


.. _incompatible-6.15.7:

6.15.7
------

Ren'Py now expects auto-forward mode to be controlled by the "auto-forward" :func:`Preference`.
To have it controlled by the auto-forward mode slider, set :var:`config.default_afm_enable` to
None.

.. _incompatible-6.14:

6.14
----

Previously, Ren'Py moved archived files into the archived/
directory. It would search this directory automatically when running a
game or building archives. One-click builds make this unnecessary,
and files in archived/ should be moved back into the game directory.

:func:`MoveTransition` has changed its interface. The old version of
MoveTransition can be accessed as OldMoveTransition, if you don't want
to rewrite your code. (The changes only matter if you use factories with
MoveTransition.)

:func:`Transform` has changed its behavior with regards to
asymmetrically scaled and rotated images. It's unlikely the old
behavior was ever used.


.. _incompatible-6.13:

6.13.8
------

Old-style string interpolation has been re-enabled by default. If you
wrote code (between 6.13 and 6.13.7) that uses % in say or menu statements, you should either
write %% instead, or include the code::

    init python:
        config.old_substitutions = False

6.13
----

The changes to text behavior can affect games in development in many
ways. The biggest change is the introduction of new-style
(square-bracket) text substitutions, and the elimination of old-style
(percent-based) substitutions. These changes can be reverted with the
code::

    init python:
        config.old_substitutions = True
        config.new_substitutions = False

New- and old-style substitutions can coexist in the same game, by
setting both variables to True.

Ren'Py has also changed the default line-wrapping behavior. While
the new behavior should never increase the number of lines in a
paragraph, it may change which words fall on each line. To restore
the old behavior, add the code::

    init python:
        style.default.layout = "greedy"
        style.default.language = "western"

A bug with negative line_spacing was fixed. This fix can cause blocks of
text to shrink in height. To revert to the old behavior, use::

    init python:
        config.broken_line_spacing = True

Finally, the new text code may lead to artifacts when displaying slow
text, especially in conjunction with a negative line spacing. Consider
adjusting :propref:`line_overlap_split` to fix this.

.. _incompatible-6.12.1:

6.12.1
------

Image names have changed from being static names to being
attribute-based. This can lead to image names that were previously
distinct becoming ambiguous. To disable attribute-based image names,
set :var:`config.image_attributes` to False.

Showing an image without providing a transform or ATL block will now
continue the previous transform that the image was using. This means
that a moving image may continue moving once it has changed. To revert
to the old behavior, set :var:`config.keep_running_transform` to False.

The `image` argument to :func:`Character` has changed meaning. While
the old meaning was unsupported in the screens-based environment, it
can be restored for compatibility purposes by setting
:var:`config.new_character_image_argument` to False.


.. _incompatible-6.12.0:

6.12.0
------

The definition of the `items` parameter of the :ref:`choice-screen` and
``nvl_choice`` screens has changed. The ``nvl_choice`` screen is
deprecated in favor of the :ref:`nvl-screen` screen.

Screens may be invoked at any time, in order to allow for image
prediction, unless they have a predict property of False. When the
predict property is not False, screens should not cause side effects
to occur upon their initial display.

For performance reason, Ren'Py now ignores the position properties of
ImageReferences. This means that the position properties of
style.image_placement are now ignored. To revert to the old behavior,
set :var:`config.imagereference_respects_position` to True.

.. _incompatible-6.11.1:

6.11.1
------

MoveTransition has been modified to respect the xoffset and yoffset
parameters of the displayables it is moving. The factory functions
that are used for movement now take `xoffset` and `yoffset`
parameters.  While the built-in movement factories take these
parameters without problem, user-defined factories may need to
be upgraded to use or ignore these additional parameters.


.. _incompatible-6.11.0:

6.11.0
------

* The transform specified by the :var:`config.default_transform`
  variable is used to initialize the transform properties of images
  shown using the show and hide statements. The default value of this
  transform sets :propref:`xpos` and :propref:`xanchor` to 0.5, and
  :propref:`ypos` and :propref:`yanchor` to 1.0.

  This represents a change in the default value of these style
  properties, which were previously uninitialized and hence defaulted
  to 0.

  By including the :var:`reset` transform in ATL transforms, these
  properties can be reset back to 0. Alternatively, one can stop using
  the default transform, and revert to the old behavior, using the
  code::

    init python:
        style.image_placement.xpos = 0.5
        style.image_placement.ypos = 1.0
        style.image_placement.xanchor = 0.5
        style.image_placement.yanchor = 1.0

        config.default_transform = None

* If a transform does not define one of the position properties
  :propref:`xpos`, :propref:`ypos`, :propref:`xanchor`, or
  :propref:`yanchor`, that property will be taken from the transform's
  child, if the defines that property.

  This makes it possible to have one transform control a displayable's
  vertical motion, and the other control the horizontal. But this is
  incompatible with previous behavior, and so can be disabled with the
  :var:`config.transform_uses_child_position` variable. ::

    init python:
        config.transform_uses_child_position = False

.. _incompatible-6.10.1:

6.10.0
------

* The default positions (left, right, center, truecenter,
  offscreenleft, and offscreenright) are now defined as ATL
  transforms. This means that showing an image at such a position will
  cause the position to be remembered. If you do not want this
  behavior, you need to redefine these positions, by adding the code::

    define left = Position(xalign=0.0)
    define center = Position(xalign=0.5)
    define truecenter = Position(xalign=0.5, yalign=0.5)
    define right = Position(xalign=1.0)
    define offscreenleft = Position(xpos=0.0, xanchor=1.0)
    define offscreenright = Position(xpos=1.0, xanchor=0.0)

.. _incompatible-6.9.2:

6.9.2
-----

* To migrate your game from Ren'Py 6.9.2 or later, copy the directory
  containing your game into your projects directory. You can choose a
  projects directory by clicking "Options", "Projects Directory" in the
  Launcher. Please see the
  `Ren'Py 6.9.2 release notes <http://www.renpy.org/wiki/renpy/releases/6.9.2>`_
  for information about migrating from older releases.
