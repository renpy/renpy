Incompatible Changes
====================

This is a list of changes that may require intervention in the form of
changes to scripts or your development environment. Our intent is that
all other changes should not affect existing scripts.

Note that setting :var:`config.script_version` will cause many of
these changes to be reverted, at the cost of losing access to recent
features.

Incompatible changes to the GUI are documented at :ref:`gui-changes`, as
such changes only take effect when the GUI is regenerated.

Pending Deprecations
--------------------

These are changes that will take effect in a future version of Ren'Py.

Support for Python 2 and Ren'Py 7 will be dropped 1 year after Ren'Py 8.1 is
released, in May 2024.

The original OpenGL renderer will be removed 1 year after Ren'Py 8.1 is
released, in May 2024. If your game sets config.gl2 to False, you should
set it to True, and make sure your game runs well. If it doesn't, please
report any issues. When reporting issues, please determine the hardware
(device and GPU), os and driver versions, and year of manufacture.


.. _incompatible-8.2.0:
.. _incompatible-7.7.0:

8.2.0 / 7.7.0
--------------

**Text Changes** Ren'Py uses harfbuzz for shaping, which may produce
different glyphs than would have been produced differently, and may change
the spacing of text. The positioning of vertical text has also been
changed by harfbuzz rendering.

To revert this changes, include in your game::

    style default:
        shaper "freetype"

Ren'Py will automatically use an Emoji font when required. To disable this,
add::

    style default:
        emoji_font None


**Polar Coordinate Changes** Ren'Py now enforces that the angles given to
the :tpref:`angle` and :tpref:`anchorangle`
properties are in the range 0 to 360 degrees, inclusive of 0 but not of 360.
Previously, angles outside this range  gave undefined behavior, now the angles
will be clamped to this range. A 360 degree change will no longer cause motion,
but will instead be treated as a 0 degree change.

When animating :tpref:`angle` and :tpref:`anchorangle` with ATL, if a direction
is not supplied, the shortest arc will be used, even if it passes through 0.

There is not a compatibility define for these changes, as they are unlikely to
affect the visible behavior of games in practice.

**Empty ATL Blocks Forbidden** Previously, Ren'Py would allow an empty ATL block.
Now it will report that a block is required. You'll need to change::

    show eileen happy:
    "..."

to::

    show eileen happy
    "..."

In the unlikely case that you have an empty ATL block.

**Box Reverse** The :propref:`box_reverse` style property has changed its
behavior in two ways:

* Space is offered to displayables in the order the displayables are presented in
  the screen, where previously the space was offered in reverse order when
  :propref:`box_reverse` was enabled. This can change the sizes of some displayables.

* A hbox that has :propref:`box_wrap` set will wrap from top to
  bottom, rather than bottom to top. A vbox with :propref:`box_wrap`
  set will wrap from left to right, rather than right to left.

The goal of these changes is to make the behavior of box_reverse more useful
for laying out interfaces in right-to-left languages. To revert these changes,
add to your game::

    define config.simple_box_reverse = True


**build.itch_channels** That variable was always documented as a dict but was
mistakenly implemented as a list of tuples. It's now truly a dict. If you
were using list operations on it, you'll need to change your code::

    # formerly
    $ build.itch_channels.append(("pattern", "channel"))
    $ build.itch_channels.extend([("pattern", "channel")])
    define build.itch_channels += [("pattern", "channel")]

    # now
    $ build.itch_channels["pattern"] = "channel"
    $ build.itch_channels.update({"pattern": "channel"})
    define build.itch_channels["pattern"] = "channel"
    define build.itch_channels |= {"pattern": "channel"}


.. _incompatible-8.1.1:
.. _incompatible-7.6.1:

8.1.1 / 7.6.1
-------------


.. _android-key-migration:

**Android Key Migration** We've received reports of games uploaded to the Google Play as bundles
having their APKs rejected for having different keys. This was caused by
an old release of Ren'Py that used the APK key for bundles. In the Play Console,
this produced an error message like::


    You uploaded an APK that is not signed with the upload certificate. You must use
    the same certificate. The upload certificate has fingerprint:

        SHA1: ...

    and the certificate used to sign the APK you uploaded has fingerprint:

        SHA1: ...

While this can be cause by other problems (like simply using entirely incorrect
keys), one potential fix is:

1. In your project's base directory, rename ``bundle.keystore`` to ``bundle.keystore.bak``.
2. In your project's base directory, copy ``android.keystore`` to ``bundle.keystore``.

Then rebuild and re-upload your bundle.


.. _incompatible-8.1.0:
.. _incompatible-7.6.0:

8.1.0 / 7.6.0
-------------

**Speech Bubbles** Adding bubble support to an existing game requires
adding files and script to the game. The :doc:`bubble` documentation
includes the required changes.


**Live2D** Ren'Py now requires Live2D Cubism 4 SDK for Native R6_2 or later.
It may refuse to run if an older version is used.


**Texture Memory** Ren'Py now accounts for texture memory more precisely.
In general, games can raise :var:`config.image_cache_size_mb` by 33%, and
use the same amount of memory.


**Audio Fadeout** When audio is stopped or changed using ``play``, there is now
a default fadeout of 0.016 seconds, to prevent pops. This is controlled by
the :var:`config.fadeout_audio` variable. To disable the fadeout::

    define config.fadeout_audio = 0.0

Fading is now logarithmic, which sounds smoother to the human ear as it matches
the way ears perceive sound. To revert to the old linear fades::

    define config.linear_fades = True


**Translate None** Ren'Py will now produce an error when encountering an explicit
``translate None`` statement that does not translate strings, styles, or python.
These should be rare, in practice. The recommended change is to replace::

    translate None start_abcd1234:
        e "This is a test"

with::

    e "This is a test" id start_abcd1234

This change can also be reverted with::

    define config.check_translate_none = False


**Keymap** The :doc:`keymap <keymap>` has changed substantially, which means that
if your game changes the default keymap - usually a bad idea - it
will need to be updated to reflect the new keysyms.


**File Search** Ren'Py will now only look for image files in game/images,
rather than all files. To look for all files in game/images, use::

    define config.search_prefixes += [ "images/" ]

The paths that are searched consider the purpose of the file, rather than the
type or extensions. So ``renpy.loadable("dlc.jpg")`` won't look for game/images/dlc.jpg.
If you'd like to find that file, write ``renpy.loadable("images/dlc.jpg")``. If you'd
like to search for a file that can be in either game/ or game/images, write
``renpy.loadable("dlc.jpg", "images")``.


**Android** Android has been changed so that the ``android.keystore`` file and
``bundle.keystore`` file are expected to be found in the project's base
directory, and not in the rapt directory. This allows projects to be
built with different keys, and helps ensure the same keys are used
with multiple Android versions.

If you'd like to use your own keys, configure your game, edit ``android.json``
to set update_keystores to false, and then edit ``local.properties`` and
``bundle.properties`` in ``rapt/project`` to point to your own keystore files.

The android configuration file has been renamed from ``.android.json`` to
``android.json``. Ren'Py will automatically create the new file if the old
exists.


**Dialogue history** Dialogue is now present in the history list
(and hence the history screen) during the statement in which the
dialogue is shown. Previously, it was only present at the end of the
statement. During the statement, the dialogue is shown with a kind of
"current".

In rare cases, your game might have relied on the old behavior. If so,
it can be disabled with::

    define config.history_current_dialogue = False


**Steam appid** When :var:`config.steam_appid` is not set, Ren'Py will delete
any existing ``steam_appid.txt`` file in the game directory. This is to prevent
the wrong app id from being used.


**Sticky layers** This release introduces the concept of sticky layers
which help automatically manage tags being placed on layers other than
their default. In the rare case that a game requires multiple of the
same tag, to be displayed at the same time, on different layers then
this may not be desirable.

To disable sticky layers entirely, add to your game::

    define config.sticky_layers = [ ]

Alternatively, to prevent only specific layers from being sticky, update
their definitions to include ``sticky=False``::

    init python:
        renpy.add_layer("ptfe", sticky=False)


**Lenticular bracket ruby text** This release of Ren'Py introduces
lenticular bracket ruby text, an easier way of writing ruby text. If
a game included a literal 【, it needs to be doubled, to "【【", to
quote it properly. (This is only strictly necessary when the text
is succeded by a full-width vertical bar, but works always.)

To disable lenticular bracket ruby text, add to your game::

    define config.lenticular_bracket_ruby = False

**Constant stores.** This release of Ren'Py introduces :ref:`constant stores <constant-stores>`, and
makes some of the built-in stores constant. Constant stores should not change
outside of the init phase. The following stores are constant:

    _errorhandling
    _gamepad
    _renpysteam
    _warper
    audio
    achievement
    build
    director
    iap
    layeredimage
    updater

If your game changes a variable in one of these stores, outside of the init,
the store can be set to non-constant with (for example)::

    define audio._constant = False

**Mixer volumes** now must be specified using a new format, where 0.0 is -40 dB (power)
and 1.0 is 0 dB (power). To use the old format, where the samples were multiplied
by volume ** 2, use::

    define config.quadratic_volumes = True

Alternatively, you can determine new default volumes for :var:`config.default_music_volume`,
:var:`config.default_sfx_volume`, and :var:`config.default_voice_volume` variables. If any
of these is 0.0 or 1.0, it can be left unchanged.

**At Transform and Global Variables** An at transform block that uses a global variable
is not re-evaluated when the variable changes. This matches the behavior
for ATL that is not in screens.

The recommended fix is to capture the global variable into a local, by changing::

    screen test():
        test "Test":
            at transform:
                xpos global_xpos

to::

    screen test():
        $ local_xpos = global_xpos

        test "Test":
            at transform:
                xpos local_xpos

This change can be reverted with::

    define config.at_transform_compare_full_context = True


.. _incompatible-8.0.2:
.. _incompatible-7.5.2:

8.0.2 / 7.5.2
-------------

A modal screen now blocks the ``pause`` statement and :func:`renpy.pause``
function from timing out. This was the indended behavior, but didn't work
in some cases. This change can be reverted with::

    define config.modal_blocks_pause = False

The default games no longer filter Ruby/Furigana text tags from the history.
This requires the line in screens.rpy that sets :var:`gui.history_allow_tags`
to be changed to::

    define gui.history_allow_tags = { "alt", "noalt", "rt", "rb", "art" }

This change is only required if your game uses Ruby/Furigana text tags.


.. _incompatible-8.0.0:
.. _incompatible-7.5.0:

8.0.0 / 7.5.0
-------------

The "Windows, Mac, and Linux for Markets" distribution has been changed to
no longer prefix the contents of the zip file created with the directory
name and version number. If you'd like to retain the old behavior, add
to your game::

    init python:
        build.package("market", "zip", "windows linux mac renpy all", "Windows, Mac, Linux for Markets")

For the noalt text tag to work with history, you'll need to edit
screens.rpy to make sure that :var:`gui.history_allow_tags` contains
"noalt". The defaultfor this variable is::

    define gui.history_allow_tags = { "alt", "noalt" }

(This change was necessary in 7.4, but only documented now.)

The behavior of Ren'Py changed sometime in the 7.4 series, such that
rollback through a load behaved correctly, and reverted the changes
performed in the ``after_load`` label, and by :var:`config.after_load_callbacks`.
(The previous behavior was undefined, with some changes reverted and some not,
leaving the game in an inconsistent state.) If your game has to migrate
data after a load, it's now recommended to call :func:`renpy.block_rollback`
to prevent the changes from being rolled back.

The :var:`config.narrator_menu` variable now defaults to True. It's been
set to true in the default screens.rpy for some time. In the unlikely event
it was false in your game, restore the old behavior with::

    define config.narrator_menu = False

The sound and voice channels are now stopped when ending the main menu.
To revert to the prior behavior (only the movie channel was stopped), add
to your game::

    define config.main_menu_stop_channels = [ "movie" ]

Screens called by ``call screen`` no longer support roll forward by default.
See :ref:`the changelog <call-screen-roll-forward>` for the problems it can
cause. Roll forward can be enabled on a per screen basis with the `roll_forward` property,
or for all screens with::

    define config.call_screen_roll_forward = True

Key and timer statements no longer take up space inside a vbox or hbox, and
the showif statement does not take up space when its child is hidden. To revert
this change::

    define config.box_skip = False

The :propref:`focus_mask` style property now defaults to None for drag displayables.
This improves performance, but means that the displayable can be dragged by
transparent pixels. To revert this, the focus_mask property can be set to True
for individual drags, or globally with::

    style drag:
        focus_mask True

Both options reduce performance.

The :propref:`outline_scaling` style property now defaults to "linear". This means
the window scaling factor is applied to the outline size, and then rounded to an
integer. This can cause multiple outlines of similar sizes to disappear. To revert
this, the outline_scaling property can be set to "step" for individual text elements,
or globally with::

    style default:
        outline_scaling "step"

The :tpref:`crop_relative` transform property now defaults to True instead of False.
Absolute numbers of pixels to set the cropping should be expressed with ints or
``absolute`` numbers. To revert to the former default behavior, which casts floats to
an absolute number of pixels, use::

    define config.crop_relative_default = False

However, be warned that like most things documented only on this page, this will
conflict with - and cannot be used at the same time as - some other new features.
This setting applies to :tpref:`crop`, and also now to :tpref:`corner1` and
:tpref:`corner2`.

The platform-specific directories inside lib/ have had name changes. The
``lib/windows-x86_64`` directory is now ``lib/py2-windows-x86_64``. This
change helps support the development of the Python 3 powered Ren'Py 8.
These directories are not documented, and may change between Ren'Py
versions, but we do guarantee that ``sys.executable`` is set.

Vpgrids cannot be overfull anymore, and can only be underfull if the
``allow_underfull`` property is passed, or if :var:`config.allow_underfull_grids` is
set to True.

The way :doc:`layered images <layeredimage>` place their children, and how children
with variable size are sized, has changed. Instead of taking into account the available
area in the context the layeredimage is displayed, it now presumes the size of the
screen is available, unless an explicit size has been given with :tpref:`xsize`,
:tpref:`ysize` or :tpref:`xysize`. To revert to the old behavior, where a layeredimage
can display differently in different contexts, you can use::

    define config.layeredimage_offer_screen = False

Or you can also toggle it for specific layeredimages by passing them the
``offer_screen`` property.

The ``function`` statement in ATL will only block catch-up in cases where it
executes more than once. To revert to the old behavior, where ATL would block
at a function, use::

    define config.atl_function_always_blocks = True


.. _incompatible-7.4.11:

7.4.11
------

Ren'Py will now run a button's unhovered property even when focus is
changed by default, such as when a screen is shown or unshown. To
revert to the old behavior, use::

    define config.always_unfocus = False

.. _incompatible-7.4.9:

7.4.9
-----

Ren'Py will now interpret floating point numbers given to a Transform's
:tpref:`xsize` or :tpref:`ysize` properties as a size relative to the area
available to the Transform. To revert this change::

    define config.relative_transform_size = False

The order in which Ren'Py's self-voicing reads out layers, screens, and displayables
in screens has changed so that screens and displayables closest to the player
are read first. To revert to the old order::

    define config.tts_front_to_back = False


.. _incompatible-7.4.7:

7.4.7
-----

When :propref:`xminimum` and :propref:`xmaximum` are both floats, the
minimum is interpreted as being a fraction of the available area. This
means that :propref:`xsize` will have the expected result when being
given a float. This may cause some displayables to change size. To revert
this change::

    define config.adjust_minimums = False

An ATL displayable will now start its animation when it first
appears, rather than when the screen itself is shown. To revert this change::

    define config.atl_start_on_show = False

Input carets now blink by default. To change this::

    define config.input_caret_blink = False


.. _incompatible-7.4.6:

7.4.6
-----

The change regarding the layer at list in 7.4.5 was reverted. The new ``camera``
statement defaults to the new semantics, while leaving ``show layer`` alone.

.. _incompatible-7.4.5:


7.4.5
------

Games produced with this version use the model-based renderer by default.
To disable the model-based renderer, use::

    define config.gl2 = False

**Reverted in 7.4.6**
The ``scene`` statement no longer clears the layer at list. To clear the
layer at list, use::

    show layer master

Where "master" is the name of the layer. Alternatively, the old behavior
can be restored with::

    define config.scene_clears_layer_at_list = True


.. _incompatible-7.4.3:

7.4.3
-----

It is now possible to click to dismiss transitions introduced with
:func:`renpy.transition`, and places that use it like the ``with`` clause
of say or ``call screen`` statement. To prevent this, use::

    define config.dismiss_blocking_transitions = False


.. _incompatible-7.4.1:

7.4.1
-----

Pause with a delay now uses :func:`renpy.pause` rather than ``with Pause(...)``.
This means that the user will have to click to bypass multiple pauses in a row.
To revert to the old behavior, use::

    define config.pause_with_transition = True


.. _incompatible-7.4:

7.4
---

Mobile platforms now use hardware, rather than software, video playback.
To restore the old behavior, use::

    define config.hw_video = True

Ren'Py will now only show side images if with at least one attribute in
addition to the image tag. To disable this, use::

    define config.side_image_requires_attributes = False


While setting config variables, like :var:`config.mouse`, outside of the init
phase was never supported, it will not work in 7.4. Consider using the
:var:`default_mouse` variable to set a custom mouse cursor, instead.

.. _incompatible-7.3.3:

7.3.3
-----

Callbacks registered with :var:`config.start_callbacks` are now run
after ``default`` statements in all cases. To restore the old behavior
(where callbacks were run before ``default`` statements during game
but not replay start), use::

    define config.early_start_store = True

When given to a viewport or vpgrid with scrollbars, the minimum, xminimum,
and yminimum side properties now apply to the side containing the scrollbars
and viewport, and not solely the viewport.

To work around this, either use ``viewport_minimum``, ``viewport_xminimum``,
and ``viewport_yminimum``, or include::

    define config.compat_viewport_minimum = True

.. _incompatible-7.3.0:

7.3.0
-----

Screen language now produces the error "a non-constant keyword argument ...
is not allowed after a python block." when it encounters screens similar
to the following::

    screen test():

        default a = 0

        button:
            $ a = 1
            action Return(a)

            text "Test"

This is because the property `action` is run before the python assignment,
meaning this was returning 0 when clicked, not 1. To disable this check, add ::

    define config.keyword_after_python = True

to a file named 01compat.rpy in your game's game directory. However, your
game will have the old behavior.

The order in which children of the ``side`` layout are drawn is now
taken from the control string. To revert to the old fixed order, use::

    define config.keep_side_render_order = False

The interface of :var:`config.say_attribute_transition_callback` has
been changed in an incompatible way, to allow sets of old and new tags
to be given. To revert to the old interface, use::

    define config.say_attribute_transition_callback_attrs = False

It's mode parameter has also been slightly changed, and will now return
a value of ``both`` when both a ``permanent`` and ``temporary``
attribute transition is occuring.

.. _incompatible-7.2.2:

7.2.2
-----

:var:`config.say_attribute_transition_callback` has been changed to
accept a new argument, the image being displayed.


.. _incompatible-7.1.1:

7.1.1
-----

Ren'Py's window auto function will now determine if dialogue or a caption
is associated with a menu statement, and will attempt to hide or show the
dialogue window as appropriate. A "Force Recompile" is necessary to include
the information that enables this feature. While it should work with older
games, this can be disabled and the old behavior restored with::

    define config.menu_showed_window = True
    define config.window_auto_show = [ "say" ]
    define config.window_auto_hide = [ "scene", "call screen" ]

While not technically an incompatible change, there is a recommend change
to the history screen. Please see :ref:`the changelog entry <history-7.1.1>`
for details of how to update your game.


.. _incompatible-7.1:

7.1
---

When an image is not being show, say-with-attributes now resolves a side
image, rather than just using the attributes given. To disable this, add::


    define config.say_attributes_use_side_image = False


.. _incompatible-7.0:

7.0
---

Ren'Py now defines automatic images at init 0, rather than at a very late
init level. To revert to the prior behavior, add to your game::

    init -1:
        define config.late_images_scan = True

The :func:`Dissolve`, :func:`ImageDissolve`, and :func:`AlphaDissolve`
transitions now default to using the alpha channel of the source
displayables, as if ``alpha=True`` was given. To revert this change, add::

    define config.dissolve_force_alpha = False

Showing a movie sprite that is already showing will now replay the movie.
To revert to the previous behavior::

    define config.replay_movie_sprites = False



.. _incompatible-6.99:

6.99.13
-------

The size of a hyperlink is now inherited from the size of the enclosing text.
To disable this, add::

    define config.hyperlink_inherit_size = False

The {nw} text tag now waits until voice and self-voicing are finished before
it continues.  To disable this behavior, add::

    define config.nw_voice = False

ATL Transforms now show at least one frame whenever a pause or interpolation
occurs. When a game doesn't expect this, it can show up as a series of
rapidly displayed single frames. This can be disabled with::

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

The order of execution of ``style`` and ``translate`` statements has
changed, as documented in :ref:`the changelog <renpy-6.99.11>`. To
revent this change, add the code::

    define config.new_translate_order = False

Note that reverting this change may prevent the new GUI from working.


The :var:`config.quit_action` variable has changed its default to one
that causes the quit prompt to be displayed of the in-game context. To
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

Screens now participate in transitions – transitions now go from the old
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
